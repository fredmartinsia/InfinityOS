#!/usr/bin/env python3
"""
router_orchestrator.py: orquestrador central de LLM do ecossistema o usuÃ¡rio.

Single source of truth para roteamento de inferencia. Substitui as cadeias
hardcoded de llm_contingency.py, cascata_proxy.py e lr_prod.FREE_MODELS por
uma unica configuracao em ~/.claude/router/providers.json.

Principios (regra de ouro do usuÃ¡rio, 2026-07-14, status ativo no vault):
  - Camadas free primeiro (OpenRouter :free, NVIDIA, Groq, Gemini).
  - Assinaturas flat (Claude Max, GLM Z.AI $50) depois, em cadeias de julgamento/codigo.
  - NUNCA API paga por token. assert_policy() aborta se violada.
  - Deterministico (regex, validacao de link, schema) => script Python, zero token.
  - Telemetria persistida em ~/.claude/router/telemetry.jsonl.

Uso:
  from router_orchestrator import complete, classify, qa_json

  # Classifica o tipo de tarefa
  tipo = classify("extraia as entidades deste texto")
  # -> "volume_short"

  # Executa com cadeia apropriada (fallback encadeado com QA)
  texto, info = complete("extraia entidades do texto: ...",
                         task_type="volume_short", qa=qa_json)

Compatibilidade (modulos legados podem importar e ganhar a cadeia nova):
  import router_orchestrator as ro
  ro.complete(...)         # API novo
  ro.qa_base, ro.qa_json   # validators compartilhados
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude/router/providers.json"
TELEMETRY_PATH = Path.home() / ".claude/router/telemetry.jsonl"

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)

# Recusa detectada em respostas de LLM (sinal de que cai pra proxima camada)
_RECUSA = ("i cannot", "i can't", "i am unable", "i'm unable", "as an ai",
           "nao posso ajudar", "desculpe, mas", "i apologize", "i'm just an ai")


# ---------------------------------------------------------------------------
# Carregamento de config
# ---------------------------------------------------------------------------

_CONFIG_CACHE = None
_CONFIG_MTIME = None


def _load_config(force=False):
    """Carrega providers.json com cache por mtime (relê se mudar)."""
    global _CONFIG_CACHE, _CONFIG_MTIME
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"config ausente: {CONFIG_PATH}")
    mtime = CONFIG_PATH.stat().st_mtime
    if force or _CONFIG_CACHE is None or mtime != _CONFIG_MTIME:
        _CONFIG_CACHE = json.loads(CONFIG_PATH.read_text())
        _CONFIG_MTIME = mtime
    return _CONFIG_CACHE


# ---------------------------------------------------------------------------
# Resolucao de chaves
# ---------------------------------------------------------------------------

def _source_env_file(path):
    """Le arquivo no formato `export VAR=val` e retorna dict."""
    out = {}
    try:
        for line in Path(path).read_text().splitlines():
            m = re.match(r"\s*export\s+([A-Z_]+)\s*=\s*(.+?)\s*$", line)
            if m:
                val = m.group(2).strip().strip('"').strip("'")
                out[m.group(1)] = val
    except Exception:
        pass
    return out


def _resolve_key(provider_cfg):
    """Resolve a chave do provider: env var > env file > key file > vazio."""
    env_key = provider_cfg.get("env_key")
    if env_key and os.environ.get(env_key):
        return os.environ[env_key]
    env_file = provider_cfg.get("env_file")
    if env_file:
        env_file = os.path.expanduser(env_file)
        if os.path.exists(env_file):
            vals = _source_env_file(env_file)
            if env_key and vals.get(env_key):
                return vals[env_key]
    key_file = provider_cfg.get("key_file")
    if key_file:
        key_file = os.path.expanduser(key_file)
        if os.path.exists(key_file):
            return Path(key_file).read_text().strip()
    return ""


def provider_status():
    """Retorna dict {provider_name: {has_key: bool, status: str}} pra healthcheck."""
    cfg = _load_config()
    out = {}
    for name, p in cfg.get("providers", {}).items():
        if p.get("kind") == "claude_local":
            out[name] = {"has_key": True, "status": "subscription"}
            continue
        k = _resolve_key(p)
        if k:
            out[name] = {"has_key": True, "status": "ready"}
        elif p.get("_status") == "pending_key":
            out[name] = {"has_key": False, "status": "pending_key"}
        else:
            out[name] = {"has_key": False, "status": "missing_key"}
    return out


# ---------------------------------------------------------------------------
# Chamadas de LLM
# ---------------------------------------------------------------------------

def _strip_think(t):
    t = re.sub(r"<think>.*?</think>", "", t or "", flags=re.DOTALL | re.IGNORECASE)
    if "</think>" in t:
        t = t.split("</think>")[-1]
    return re.sub(r"</?think>", "", t, flags=re.IGNORECASE).strip()


def _no_dash(t):
    """Troca em dash por virgula e en dash por hifen comum."""
    return (t or "").replace(EM_DASH, ", ").replace(EN_DASH, "-")


def _post_openai(url, key, model, prompt, system, timeout, max_tokens, extra_headers=None):
    """POST OpenAI-compatible chat completion."""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    elif "nemotron" in model.lower():
        msgs.append({"role": "system", "content": "detailed thinking off"})
    msgs.append({"role": "user", "content": prompt})
    body = json.dumps({
        "model": model,
        "messages": msgs,
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        # User-Agent custom: Groq bloqueia Python-urllib/3.x (HTTP 403).
        # Mascaramos como curl/8.0 que e aceito universalmente pelos provedores.
        "User-Agent": "curl/8.0",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    # Trata retorno sem content (Gemini as vezes responde vazio em safety filter,
    # ou provider retorna finish_reason != stop sem texto). Considera erro e cai
    # pro proximo da cadeia em vez de crashar com KeyError.
    try:
        choices = d.get("choices") or [{}]
        msg = choices[0].get("message") or {}
        content = msg.get("content")
        if not content and msg.get("reasoning_content"):
            content = msg["reasoning_content"]
        if not content:
            finish = choices[0].get("finish_reason", "?")
            raise RuntimeError(f"resposta sem content (finish_reason={finish})")
        return content
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"resposta malformada do provider: {str(e)[:80]}")


def _call_claude_cli(model, prompt, system, timeout):
    """Claude Code via assinatura Max (sem API key).

    O prompt vai por STDIN, nunca como valor de -p. O prompt do LightRAG comeca
    com "---Role---" e, passado em argv, o parser da CLI le o texto como flag e
    devolve "unknown option '---Role---'". Era por isso que estas camadas
    falhavam em 100% das chamadas de extracao. Stdin tambem evita estourar o
    limite de tamanho de argumento em prompt grande.
    """
    claude_bin = shutil.which("claude") or os.path.expanduser("~/.npm-global/bin/claude")
    p = (system + "\n\n" + prompt) if system else prompt
    cmd = [claude_bin, "-p", "--model", model, "--dangerously-skip-permissions"]
    r = subprocess.run(
        cmd, input=p, capture_output=True, text=True, timeout=timeout
    )
    if r.returncode != 0 or not (r.stdout or "").strip():
        raise RuntimeError(f"claude cli rc={r.returncode}: {(r.stderr or '')[:150]}")
    return r.stdout


def _call_provider(provider_name, provider_cfg, model, prompt, system, timeout, max_tokens):
    kind = provider_cfg.get("kind")
    if kind == "claude_local":
        return _call_claude_cli(model, prompt, system, timeout)

    key = _resolve_key(provider_cfg)
    if not key:
        raise RuntimeError(f"chave ausente para {provider_name}")

    endpoint = provider_cfg.get("endpoint")
    if not endpoint:
        raise RuntimeError(f"endpoint ausente para {provider_name}")

    extra_headers = provider_cfg.get("extra_headers")
    if provider_name == "openrouter_free" and not extra_headers:
        extra_headers = {
            "HTTP-Referer": "https://claude.or/local",
            "X-Title": "router_orchestrator",
        }
    return _post_openai(endpoint, key, model, prompt, system, timeout, max_tokens, extra_headers)


# ---------------------------------------------------------------------------
# QA validators (mesmo padrao do llm_contingency, preservado pra compat)
# ---------------------------------------------------------------------------

def qa_base(resp):
    """Fluidez minima: nao vazio, sem recusa, sem <think> residual.
    Aceita respostas curtas (>= 1 char) porque perguntas legitimas podem ter
    resposta de 1 palavra (ex: '8', 'sim', nome proprio). A validacao de
    conteudo fica nos QAs especificos (qa_json, qa_extract)."""
    if not resp or not resp.strip():
        return False
    low = resp.lower()
    if any(r in low for r in _RECUSA):
        return False
    if "<think>" in low:
        return False
    return True


def _extract_json(resp):
    raw = resp
    if "```json" in raw:
        raw = raw.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in raw:
        raw = raw.split("```", 1)[1].split("```", 1)[0]
    m = re.search(r"[\{\[].*[\}\]]", raw, re.DOTALL)
    return m.group(0) if m else raw.strip()


def qa_json(resp):
    if not qa_base(resp):
        return False
    try:
        json.loads(_extract_json(resp))
        return True
    except Exception:
        return False


def qa_json_or_text(resp):
    if not qa_base(resp):
        return False
    s = resp.strip()
    if s.startswith("{") or s.startswith("[") or "```json" in resp:
        return qa_json(resp)
    return len(s) >= 30


def qa_extract(resp):
    if not qa_base(resp):
        return False
    low = resp.lower()
    if "entity" in low or "relationship" in low or "<|>" in resp or "##" in resp:
        return True
    return len(resp.strip()) >= 40


# ---------------------------------------------------------------------------
# Classificacao de tarefa
# ---------------------------------------------------------------------------

def _pick_classifier(cfg):
    """Retorna (provider_name, model) do classificador, com fallback se sem chave."""
    orch = cfg.get("orchestrator", {})
    if not orch.get("enabled", True):
        return None, None
    classifier = orch.get("classifier", "groq_free:llama-3.1-8b-instant")
    if ":" not in classifier:
        return None, None
    provider_name, model = classifier.split(":", 1)
    p = cfg["providers"].get(provider_name)
    if not p:
        return None, None
    if p.get("kind") != "claude_local" and not _resolve_key(p):
        # fallback pra openrouter_free:ling-3.0-flash
        fb_name = "openrouter_free"
        fb = cfg["providers"].get(fb_name)
        if fb and _resolve_key(fb):
            return fb_name, "inclusionai/ling-3.0-flash:free"
        return None, None
    return provider_name, model


def classify(prompt, system=None):
    """Classifica o prompt em um dos 6 task_types. Retorna 'volume_long' se falhar."""
    cfg = _load_config()
    provider_name, model = _pick_classifier(cfg)
    if not provider_name:
        return "volume_long"

    tipos = list(cfg.get("task_types", {}).keys())
    sys_prompt = (
        "Classifique a tarefa em UM destes tipos, respondendo SOMENTE a palavra-chave: "
        + ", ".join(tipos) + ". "
        "Regras: judgment=estrategia/decisao/analise critica; "
        "code=implementar codigo/PR/refatorar; "
        "volume_short=resumir paragrafo, classificar, extrair entidade, rotear; "
        "volume_long=ingerir documento longo, resumir transcricao, extracao massiva; "
        "vision=analisar imagem/print/screenshot; "
        "deterministic=validar link, regex, schema, formato."
    )
    orch = cfg.get("orchestrator", {})
    try:
        resp = _call_provider(provider_name, cfg["providers"][provider_name], model,
                              prompt[:500], sys_prompt,
                              orch.get("timeout_s", 12), orch.get("max_tokens", 50))
        resp_clean = _strip_think(resp).strip().lower()
        for t in tipos:
            if t in resp_clean:
                return t
    except Exception:
        pass
    return "volume_long"


# ---------------------------------------------------------------------------
# Telemetria
# ---------------------------------------------------------------------------

def _log_telemetry(entry):
    try:
        TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY_PATH, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_telemetry(limit=100, provider=None, success=None):
    """Le as N ultimas entradas de telemetria, opcionalmente filtradas."""
    if not TELEMETRY_PATH.exists():
        return []
    out = []
    with open(TELEMETRY_PATH) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if provider and e.get("provider") != provider:
                continue
            if success is not None and e.get("success") != success:
                continue
            out.append(e)
    return out[-limit:]


# ---------------------------------------------------------------------------
# Policy guard (regra de ouro)
# ---------------------------------------------------------------------------

def assert_policy(chain, cfg=None):
    """Regra de ouro do usuÃ¡rio: nunca provider com cost=paid_token na cadeia."""
    cfg = cfg or _load_config()
    policy = cfg.get("policy", {})
    if not policy.get("paid_by_token_forbidden", True):
        return True

    providers = cfg["providers"]
    for step in chain:
        provider_name, _ = step.split(":", 1)
        p = providers.get(provider_name, {})
        if p.get("cost") == "paid_token":
            raise RuntimeError(
                f"POLITICA: provider {provider_name} custa por token, proibido pela regra de ouro"
            )
    return True


# ---------------------------------------------------------------------------
# Entrada principal
# ---------------------------------------------------------------------------

def complete(prompt, system=None, task_type=None, qa=None,
             timeout=180, max_tokens=4000, log=None):
    """Roteia a chamada pela cadeia do tipo de tarefa.

    - Fallback encadeado: erro tecnico OU QA reprovado => proximo da cadeia.
    - Deterministico retorna texto vazio com executor='python_script'.
    - Telemetria gravada em ~/.claude/router/telemetry.jsonl.

    Retorna (texto, info_dict).
    """
    cfg = _load_config()
    if task_type is None:
        task_type = classify(prompt, system)

    tt = cfg.get("task_types", {}).get(task_type)
    if not tt:
        raise RuntimeError(f"tipo de tarefa desconhecido: {task_type}")

    if tt.get("policy") == "zero_token":
        return "", {
            "task_type": task_type,
            "executor": "python_script",
            "provider": None,
            "model": None,
        }

    chain = tt["chain"]
    qa_fn = qa or qa_base
    assert_policy(chain, cfg)

    ultimo = None
    for step in chain:
        if ":" not in step:
            continue
        provider_name, model = step.split(":", 1)
        provider_cfg = cfg["providers"].get(provider_name)
        if not provider_cfg:
            continue

        # Pula provider sem chave (ex: groq_free pendente)
        if provider_cfg.get("kind") != "claude_local" and not _resolve_key(provider_cfg):
            if log:
                log(f"[router] {provider_name} sem chave, pulando")
            continue

        t0 = time.time()
        try:
            resp = _call_provider(provider_name, provider_cfg, model, prompt,
                                  system, timeout, max_tokens)
            resp = _no_dash(_strip_think(resp))
            latency_ms = int((time.time() - t0) * 1000)
            ok = qa_fn(resp)
            _log_telemetry({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "task_type": task_type,
                "provider": provider_name,
                "model": model,
                "latency_ms": latency_ms,
                "success": True,
                "qa_passed": ok,
                "error": None,
            })
            if ok:
                if log:
                    log(f"[router] {provider_name}:{model} OK em {latency_ms}ms")
                return resp, {
                    "task_type": task_type,
                    "provider": provider_name,
                    "model": model,
                    "latency_ms": latency_ms,
                }
            ultimo = f"{provider_name}:{model} reprovado no QA"
            if log:
                log(f"[router] {ultimo}; proximo")
        except Exception as e:
            latency_ms = int((time.time() - t0) * 1000)
            _log_telemetry({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "task_type": task_type,
                "provider": provider_name,
                "model": model,
                "latency_ms": latency_ms,
                "success": False,
                "qa_passed": False,
                "error": str(e)[:140],
            })
            ultimo = f"{provider_name}:{model} erro: {str(e)[:90]}"
            if log:
                log(f"[router] {ultimo}; proximo")

    raise RuntimeError(
        f"router: todas as camadas falharam. task_type={task_type}. ultimo: {ultimo}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main():
    import argparse
    ap = argparse.ArgumentParser(description="Router orchestrator de LLM")
    ap.add_argument("prompt", nargs="?", help="prompt pra testar")
    ap.add_argument("--type", default=None,
                    help="forca tipo: judgment|code|volume_short|volume_long|vision|deterministic")
    ap.add_argument("--classify-only", action="store_true",
                    help="so classifica, nao chama LLM")
    ap.add_argument("--json-output", action="store_true",
                    help="exige JSON valido (usa qa_json)")
    ap.add_argument("--status", action="store_true",
                    help="mostra status dos providers e sai")
    args = ap.parse_args()

    if args.status:
        print(json.dumps(provider_status(), indent=2, ensure_ascii=False))
        return

    if not args.prompt:
        ap.print_help()
        sys.exit(1)

    if args.classify_only:
        print(classify(args.prompt))
        return

    qa = qa_json if args.json_output else None

    def log(m):
        print(m, file=sys.stderr)

    txt, info = complete(args.prompt, task_type=args.type, qa=qa, log=log)
    print(f"\n>>> {info}", file=sys.stderr)
    print(txt)


if __name__ == "__main__":
    _main()
