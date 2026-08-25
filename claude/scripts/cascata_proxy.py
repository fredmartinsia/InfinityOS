#!/usr/bin/env python3
"""
cascata_proxy.py

Proxy local que da ao Claude Code uma cascata de modelos gratuitos do OpenRouter.

Como funciona: o Claude Code fala Anthropic Messages API e manda um nome
simbolico de cadeia no campo "model" (ex: "cascata-pesado"). O proxy resolve
esse nome na lista real de modelos definida em ~/.claude/cascata_models.json,
manda o primeiro da lista como "model" e a lista inteira como "models", e o
proprio OpenRouter cai para o proximo em caso de 429, erro do provedor ou
estouro de janela de contexto. O proxy ainda faz um retry proprio para o que
o OpenRouter nao cobre (falha de rede, timeout, 5xx antes do primeiro byte).

Uso:
    python3 cascata_proxy.py            # roda em foreground
    python3 cascata_proxy.py --daemon   # sobe em background
    python3 cascata_proxy.py --check    # valida os slugs da config e sai
    python3 cascata_proxy.py --stop     # derruba a instancia que estiver na porta
"""

import hashlib
import http.client
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOME = os.path.expanduser("~")
CONFIG_PATH = os.environ.get("CASCATA_CONFIG", os.path.join(HOME, ".claude", "cascata_models.json"))
LOG_PATH = os.environ.get("CASCATA_LOG", os.path.join(HOME, ".claude", "logs", "cascata.log"))
ENV_PATH = os.path.join(HOME, ".config", "openrouter", "env")
PORT = int(os.environ.get("CASCATA_PORT", "47822"))

_log_lock = threading.Lock()
_stats_lock = threading.Lock()
_stats = {"iniciado_em": time.time(), "requisicoes": 0, "fallbacks": 0, "erros": 0, "ultimos": []}
_classificacao_cache = {}


# ----------------------------------------------------------------------------
# infra basica
# ----------------------------------------------------------------------------

def carregar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_chave():
    chave = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if chave:
        return chave
    # fallback: le o arquivo protegido, sem depender do shell
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for linha in f:
                m = re.match(r'\s*export\s+OPENROUTER_API_KEY\s*=\s*"?([^"\n]+)"?', linha)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return ""


def log(msg):
    carimbo = time.strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{carimbo}] {msg}\n"
    with _log_lock:
        try:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(linha)
        except OSError:
            pass
    if os.environ.get("CASCATA_VERBOSE") == "1":
        sys.stderr.write(linha)
        sys.stderr.flush()


def registrar(cadeia, modelo_servido, ms, tentativa, erro=None):
    with _stats_lock:
        _stats["requisicoes"] += 1
        if tentativa > 0 or (modelo_servido and cadeia and modelo_servido != cadeia[0]):
            _stats["fallbacks"] += 1
        if erro:
            _stats["erros"] += 1
        _stats["ultimos"].insert(0, {
            "quando": time.strftime("%H:%M:%S"),
            "pediu": cadeia[0] if cadeia else None,
            "serviu": modelo_servido,
            "ms": ms,
            "tentativa": tentativa,
            "erro": erro,
        })
        del _stats["ultimos"][20:]


# ----------------------------------------------------------------------------
# upstream
# ----------------------------------------------------------------------------

def abrir_upstream(payload, chave, timeout):
    """Abre a conexao com o OpenRouter e devolve (conexao, resposta) sem ler o corpo."""
    corpo = json.dumps(payload).encode("utf-8")
    conn = http.client.HTTPSConnection("openrouter.ai", timeout=timeout)
    conn.request("POST", "/api/v1/messages", body=corpo, headers={
        "x-api-key": chave,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
        "Accept-Encoding": "identity",
        "HTTP-Referer": "https://github.com/fredmartins/cascata-proxy",
        "X-Title": "claude-or cascata",
    })
    return conn, conn.getresponse()


def chamada_simples(payload, chave, timeout):
    """Chamada nao streaming, usada pelo classificador de complexidade."""
    conn = None
    try:
        conn, resp = abrir_upstream(payload, chave, timeout)
        dados = resp.read()
        if resp.status != 200:
            return None
        return json.loads(dados)
    except Exception:
        return None
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


# ----------------------------------------------------------------------------
# orquestrador de complexidade
# ----------------------------------------------------------------------------

def primeira_fala_do_usuario(payload):
    """A primeira mensagem do usuario na conversa.

    Serve para duas coisas: e o texto que descreve a tarefa (o que o
    classificador precisa ver) e e a identidade estavel da sessao, ja que
    continua sendo messages[0] em todos os turnos seguintes.
    """
    for msg in payload.get("messages") or []:
        if msg.get("role") != "user":
            continue
        conteudo = msg.get("content")
        if isinstance(conteudo, str):
            return conteudo
        if isinstance(conteudo, list):
            partes = [b.get("text", "") for b in conteudo if isinstance(b, dict) and b.get("type") == "text"]
            if partes:
                return "\n".join(partes)
    return ""


def eh_primeiro_turno(payload):
    msgs = payload.get("messages") or []
    if len(msgs) > 2:
        return False
    for msg in msgs:
        conteudo = msg.get("content")
        if isinstance(conteudo, list):
            for bloco in conteudo:
                if isinstance(bloco, dict) and bloco.get("type") in ("tool_result", "tool_use"):
                    return False
    return True


def nota_de_complexidade(texto, cfg, chave):
    """Devolve 1 a 10, ou None se nao conseguir classificar a tempo."""
    orq = cfg.get("orquestrador") or {}
    texto = (texto or "").strip()
    if not texto:
        return None

    prompt = (
        "Classifique a complexidade da tarefa abaixo numa escala de 1 a 10.\n"
        "1 a 3 = pergunta simples, resposta curta, sem varios passos.\n"
        "4 a 10 = codigo, analise, arquitetura, varios arquivos ou varios passos.\n"
        "Responda APENAS o numero, sem nenhuma outra palavra.\n\n"
        "TAREFA:\n" + texto[:2000]
    )
    # o orcamento precisa ser folgado: esses modelos gastam tokens em "thinking"
    # antes do texto, e com poucos tokens a resposta sai vazia.
    resposta = chamada_simples({
        "model": orq.get("modelo"),
        "max_tokens": int(orq.get("max_tokens", 500)),
        "messages": [{"role": "user", "content": prompt}],
    }, chave, float(orq.get("timeout_s", 12)))

    if not resposta:
        return None
    bruto = " ".join(
        b.get("text", "") for b in resposta.get("content", [])
        if isinstance(b, dict) and b.get("type") == "text"
    ).strip()
    if not bruto:
        return None
    achado = re.search(r"\b(10|[1-9])\b", bruto)
    if not achado:
        return None
    return int(achado.group(1))


def montar_cadeia(payload, cfg, chave):
    """Resolve o campo model numa cadeia real de modelos.

    A nota de complexidade e decidida uma vez por conversa, no primeiro turno,
    e vale para todos os turnos seguintes. A identidade da conversa e a
    primeira fala do usuario, que nao muda ao longo da sessao.
    """
    pedido = payload.get("model") or ""
    cadeias = cfg.get("cadeias") or {}

    if pedido not in cadeias:
        # nome nao simbolico: respeita o que veio, sem cascata
        return [pedido], None

    cadeia = list(cadeias[pedido])
    orq = cfg.get("orquestrador") or {}
    if pedido != "cascata-pesado":
        return cadeia, None
    if not orq.get("ligado") or os.environ.get("CASCATA_ORQUESTRADOR") == "0":
        return cadeia, None

    abertura = primeira_fala_do_usuario(payload)
    if not abertura:
        return cadeia, None

    id_sessao = hashlib.sha256(abertura[:600].encode("utf-8")).hexdigest()
    agora = time.time()
    nota = None

    with _stats_lock:
        em_cache = _classificacao_cache.get(id_sessao)
    if em_cache and agora - em_cache[1] < 21600:
        nota = em_cache[0]
    elif eh_primeiro_turno(payload):
        nota = nota_de_complexidade(abertura, cfg, chave)
        if nota is not None:
            with _stats_lock:
                _classificacao_cache[id_sessao] = (nota, agora)
                if len(_classificacao_cache) > 500:
                    mais_velha = min(_classificacao_cache, key=lambda k: _classificacao_cache[k][1])
                    del _classificacao_cache[mais_velha]

    limite = int(orq.get("nota_maxima_para_leve", 3))
    if nota is not None and nota <= limite:
        rapido = orq.get("modelo")
        if rapido in cadeia:
            cadeia.remove(rapido)
            cadeia.insert(0, rapido)
    return cadeia, nota


# ----------------------------------------------------------------------------
# handler HTTP
# ----------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "cascata-proxy/1.0"

    def log_message(self, *args):
        pass

    # -- utilidades de resposta -------------------------------------------

    def responder_json(self, status, obj):
        corpo = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def responder_bytes(self, status, ctype, corpo):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    # -- rotas -------------------------------------------------------------

    def do_GET(self):
        if self.path.startswith("/health"):
            with _stats_lock:
                snapshot = dict(_stats)
                snapshot["uptime_s"] = int(time.time() - _stats["iniciado_em"])
                snapshot["ultimos"] = list(_stats["ultimos"])
            try:
                cfg = carregar_config()
                snapshot["cadeias"] = {k: v for k, v in (cfg.get("cadeias") or {}).items()}
                orq = cfg.get("orquestrador") or {}
                snapshot["orquestrador"] = (
                    orq.get("ligado") and os.environ.get("CASCATA_ORQUESTRADOR") != "0"
                )
            except Exception as e:
                snapshot["config_erro"] = str(e)
            snapshot["ok"] = True
            self.responder_json(200, snapshot)
            return
        self.responder_json(404, {"error": {"message": "Not Found", "type": "not_found"}})

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        bruto = self.rfile.read(tamanho) if tamanho else b"{}"

        if "count_tokens" in self.path:
            self.contar_tokens(bruto)
            return
        if "/v1/messages" in self.path:
            self.encaminhar_mensagens(bruto)
            return
        self.responder_json(404, {"error": {"message": f"path nao suportado: {self.path}", "type": "not_found"}})

    # -- count_tokens ------------------------------------------------------

    def contar_tokens(self, bruto):
        """O OpenRouter devolve 404 nesse path, entao estimamos localmente."""
        try:
            payload = json.loads(bruto)
        except Exception:
            payload = {}
        texto = json.dumps(payload.get("messages", []), ensure_ascii=False)
        texto += json.dumps(payload.get("system", ""), ensure_ascii=False)
        texto += json.dumps(payload.get("tools", []), ensure_ascii=False)
        self.responder_json(200, {"input_tokens": max(1, int(len(texto) / 3.5))})

    # -- messages ----------------------------------------------------------

    def encaminhar_mensagens(self, bruto):
        inicio = time.time()
        try:
            payload = json.loads(bruto)
        except Exception as e:
            self.responder_json(400, {"error": {"message": f"JSON invalido: {e}", "type": "invalid_request_error"}})
            return

        try:
            cfg = carregar_config()
        except Exception as e:
            self.responder_json(500, {"error": {"message": f"config ilegivel: {e}", "type": "api_error"}})
            return

        chave = carregar_chave()
        if not chave:
            self.responder_json(401, {"error": {"message": "OPENROUTER_API_KEY ausente", "type": "authentication_error"}})
            return

        cadeia, nota = montar_cadeia(payload, cfg, chave)
        rede = cfg.get("rede") or {}
        timeout = float(rede.get("timeout_upstream_s", 900))
        max_tent = int(rede.get("max_tentativas", 3))
        backoff = float(rede.get("backoff_base_s", 2))
        por_request = int(rede.get("max_models_por_request", 3))
        streaming = bool(payload.get("stream"))

        # o OpenRouter recusa models[] com mais de 3 itens, entao a cadeia vira
        # blocos: cada tentativa manda um bloco e o servidor faz a cascata interna.
        blocos = [cadeia[i:i + por_request] for i in range(0, len(cadeia), por_request)]
        while len(blocos) < max_tent:
            blocos.append(blocos[-1])
        blocos = blocos[:max(max_tent, 1)]

        etiqueta = payload.get("model")
        ultimo_erro = None

        for tentativa, restante in enumerate(blocos):
            envio = dict(payload)
            envio["model"] = restante[0]
            if len(restante) > 1:
                envio["models"] = restante

            conn = None
            try:
                conn, resp = abrir_upstream(envio, chave, timeout)

                if resp.status != 200:
                    corpo = resp.read()
                    conn.close()
                    conn = None
                    texto_erro = corpo[:400].decode("utf-8", "replace")
                    # 400 de "modelo invalido" tambem e retentavel: acontece quando
                    # um modelo sai do catalogo do OpenRouter (os gratuitos somem sem
                    # aviso). Sem isso, um slug morto derrubaria a cadeia inteira.
                    modelo_sumiu = resp.status in (400, 404) and re.search(
                        r"not a valid model|No endpoints found|is not available",
                        texto_erro, re.IGNORECASE)
                    retentavel = resp.status == 429 or resp.status >= 500 or bool(modelo_sumiu)
                    ultimo_erro = f"HTTP {resp.status}: {texto_erro[:200]}"
                    if retentavel and tentativa + 1 < len(blocos):
                        espera = backoff * (2 ** tentativa)
                        cab = resp.getheader("Retry-After")
                        if cab and cab.isdigit():
                            espera = min(float(cab), 30.0)
                        log(f"bloco {tentativa} falhou ({ultimo_erro[:120]}), esperando {espera:.0f}s e caindo para {blocos[tentativa + 1][0]}")
                        time.sleep(espera)
                        continue
                    ms = int((time.time() - inicio) * 1000)
                    registrar(cadeia, None, ms, tentativa, ultimo_erro)
                    log(f"{etiqueta}: FALHA definitiva {ultimo_erro[:200]}")
                    self.responder_bytes(resp.status, "application/json", corpo)
                    return

                # 200: a partir daqui o cliente comeca a receber bytes
                if streaming:
                    self.repassar_stream(resp, cadeia, tentativa, inicio, etiqueta, nota)
                else:
                    corpo = resp.read()
                    servido = None
                    try:
                        servido = json.loads(corpo).get("model")
                    except Exception:
                        pass
                    ms = int((time.time() - inicio) * 1000)
                    registrar(cadeia, servido, ms, tentativa)
                    log(self.frase_log(etiqueta, cadeia, servido, ms, tentativa, nota))
                    self.responder_bytes(200, "application/json", corpo)
                return

            except Exception as e:
                ultimo_erro = f"{type(e).__name__}: {e}"
                if tentativa + 1 < len(blocos):
                    espera = backoff * (2 ** tentativa)
                    log(f"bloco {tentativa} caiu ({ultimo_erro[:120]}), esperando {espera:.0f}s e caindo para {blocos[tentativa + 1][0]}")
                    time.sleep(espera)
                    continue
            finally:
                if conn:
                    try:
                        conn.close()
                    except Exception:
                        pass

        ms = int((time.time() - inicio) * 1000)
        registrar(cadeia, None, ms, len(blocos), ultimo_erro)
        log(f"{etiqueta}: cadeia inteira falhou. ultimo erro: {ultimo_erro}")
        try:
            self.responder_json(502, {"error": {
                "message": f"cascata esgotada em {len(cadeia)} modelos. ultimo erro: {ultimo_erro}",
                "type": "api_error"}})
        except Exception:
            pass

    def repassar_stream(self, resp, cadeia, tentativa, inicio, etiqueta, nota):
        """Repassa SSE linha a linha usando chunked, sem bufferizar a resposta."""
        self.send_response(200)
        self.send_header("Content-Type", resp.getheader("Content-Type") or "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

        servido = None
        try:
            while True:
                linha = resp.readline()
                if not linha:
                    break
                if servido is None and b'"model"' in linha:
                    achado = re.search(rb'"model"\s*:\s*"([^"]+)"', linha)
                    if achado:
                        servido = achado.group(1).decode("utf-8", "replace")
                self.wfile.write(b"%X\r\n" % len(linha))
                self.wfile.write(linha)
                self.wfile.write(b"\r\n")
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            ms = int((time.time() - inicio) * 1000)
            registrar(cadeia, servido, ms, tentativa)
            log(self.frase_log(etiqueta, cadeia, servido, ms, tentativa, nota, stream=True))

    @staticmethod
    def frase_log(etiqueta, cadeia, servido, ms, tentativa, nota, stream=False):
        marca = ""
        if servido and cadeia and servido != cadeia[0]:
            marca = f" FALLBACK (pediu {cadeia[0]})"
        elif tentativa > 0:
            marca = f" RETRY {tentativa}"
        extra = f" nota={nota}" if nota is not None else ""
        tipo = "stream" if stream else "json"
        return f"{etiqueta} -> {servido or '?'} [{tipo}] {ms}ms{marca}{extra}"


# ----------------------------------------------------------------------------
# comandos de linha
# ----------------------------------------------------------------------------

def cmd_check():
    cfg = carregar_config()
    print(f"config: {CONFIG_PATH}")
    try:
        with urllib.request.urlopen(cfg.get("endpoint_modelos"), timeout=30) as r:
            catalogo = json.load(r)["data"]
    except Exception as e:
        print(f"ERRO ao buscar catalogo do OpenRouter: {e}")
        return 1

    validos = {}
    for m in catalogo:
        preco = m.get("pricing") or {}
        try:
            gratis = float(preco.get("prompt", 1)) == 0 and float(preco.get("completion", 1)) == 0
        except Exception:
            gratis = False
        validos[m["id"]] = (m.get("context_length") or 0, gratis)

    problemas = 0
    for nome, cadeia in (cfg.get("cadeias") or {}).items():
        print(f"\ncadeia {nome}:")
        for i, modelo in enumerate(cadeia, 1):
            if modelo not in validos:
                print(f"  {i}. {modelo}  ==> NAO EXISTE no OpenRouter")
                problemas += 1
                continue
            ctx, gratis = validos[modelo]
            aviso = "" if gratis else "  ==> ATENCAO: NAO e gratuito"
            if not gratis:
                problemas += 1
            print(f"  {i}. {modelo}  ctx={ctx:,}{aviso}")

    orq = (cfg.get("orquestrador") or {}).get("modelo")
    if orq:
        if orq not in validos:
            print(f"\norquestrador {orq} ==> NAO EXISTE")
            problemas += 1
        else:
            print(f"\norquestrador: {orq} ctx={validos[orq][0]:,} gratuito={validos[orq][1]}")

    chave = carregar_chave()
    print(f"\nchave OPENROUTER: {'ok (' + chave[:12] + '...)' if chave else 'AUSENTE'}")
    if not chave:
        problemas += 1

    print(f"\n{'TUDO OK' if problemas == 0 else str(problemas) + ' PROBLEMA(S) ENCONTRADO(S)'}")
    return 0 if problemas == 0 else 1


def porta_ocupada():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def cmd_daemon():
    if porta_ocupada():
        print(f"cascata_proxy ja esta no ar na porta {PORT}")
        return 0
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    saida = open(LOG_PATH, "a")
    subprocess.Popen(
        [sys.executable, os.path.abspath(__file__)],
        stdout=saida, stderr=saida, stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(40):
        time.sleep(0.25)
        if porta_ocupada():
            print(f"cascata_proxy no ar na porta {PORT}")
            return 0
    print("cascata_proxy nao subiu a tempo. veja " + LOG_PATH)
    return 1


def cmd_stop():
    saida = subprocess.run(["lsof", "-ti", f"tcp:{PORT}"], capture_output=True, text=True)
    pids = [p for p in saida.stdout.split() if p.strip()]
    if not pids:
        print("nada rodando na porta " + str(PORT))
        return 0
    for pid in pids:
        subprocess.run(["kill", pid])
    print("derrubado: " + ", ".join(pids))
    return 0


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--check":
        return cmd_check()
    if arg == "--daemon":
        return cmd_daemon()
    if arg == "--stop":
        return cmd_stop()

    cfg = carregar_config()
    servidor = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    servidor.daemon_threads = True
    cadeias = ", ".join(f"{k}({len(v)})" for k, v in (cfg.get("cadeias") or {}).items())
    log(f"cascata_proxy no ar em 127.0.0.1:{PORT} | cadeias: {cadeias}")
    print(f"cascata_proxy no ar em http://127.0.0.1:{PORT} | cadeias: {cadeias}", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        log("cascata_proxy encerrado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
