#!/usr/bin/env python3
"""
nvidia_proxy.py

Gerencia o daemon do claude-code-proxy (fuergaosi233/claude-code-proxy,
vendorizado em ~/.claude/vendor/claude-code-proxy, venv isolada) usado pelo
comando claude-n (.zshrc) para rodar o Claude Code em cima dos modelos
gratuitos da NVIDIA.

Por que existe: o Claude Code fala Anthropic Messages API (POST /v1/messages)
mas a API hospedada da NVIDIA (integrate.api.nvidia.com) so fala formato
OpenAI. Tentativa anterior usou o litellm, mas o /v1/messages dele so faz
passthrough literal pra Anthropic de verdade (confirmado lendo
litellm/llms/anthropic/experimental_pass_through/messages/handler.py), sem
traduzir formato pra outros providers. O claude-code-proxy foi feito
especificamente pra isso: traduz Anthropic Messages <-> OpenAI de verdade,
com tool calling e streaming.

Uso:
    python3 nvidia_proxy.py --daemon   # sobe o proxy em background
    python3 nvidia_proxy.py --stop     # derruba a instancia na porta
    python3 nvidia_proxy.py --check    # testa a chave e os modelos direto na NVIDIA
"""

import http.client
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

HOME = os.path.expanduser("~")
PROXY_DIR = os.path.join(HOME, ".claude", "vendor", "claude-code-proxy")
VENV_PYTHON = os.path.join(PROXY_DIR, ".venv", "bin", "python3")
START_SCRIPT = os.path.join(PROXY_DIR, "start_proxy.py")
LOG_PATH = os.environ.get(
    "NVIDIA_PROXY_LOG", os.path.join(HOME, ".claude", "logs", "nvidia_proxy.log")
)
KEY_PATH = os.path.join(HOME, ".claude", "scripts", ".nvidia_key")
PORT = int(os.environ.get("NVIDIA_PROXY_PORT", "47823"))

# Unico destino permitido. Nao vem de env de proposito: nada de fora pode
# apontar este proxy pra um provider pago (OpenRouter, Z.AI, OpenAI...).
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Modelos validados de verdade contra a API em 27/jul/2026 (testados direto,
# sem passar pelo proxy, COM tool calling - nao so completude simples).
# openai/gpt-oss-120b trava (timeout, nunca responde) quando a requisicao
# inclui "tools"; meta/llama-4-maverick-17b-128e-instruct morreu (HTTP 410,
# EOL em 27/jul/2026). nemotron-3-super-120b-a12b confirmado com tool_calls
# corretos e usado como "forte".
MODELO_RAPIDO = "meta/llama-3.3-70b-instruct"  # SMALL_MODEL (haiku)
MODELO_FORTE = "nvidia/nemotron-3-super-120b-a12b"  # BIG/MIDDLE_MODEL (opus/sonnet)
MODELOS = [
    MODELO_RAPIDO,
    MODELO_FORTE,
    "nvidia/llama-3.3-nemotron-super-49b-v1",
]


def carregar_chave():
    chave = os.environ.get("NVIDIA_API_KEY", "").strip()
    if chave:
        return chave
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def porta_ocupada(porta=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", porta)) == 0


def cmd_daemon():
    if porta_ocupada():
        print(f"nvidia_proxy ja esta no ar na porta {PORT}")
        return 0

    chave = carregar_chave()
    if not chave:
        print(f"NVIDIA_API_KEY ausente (nem env, nem {KEY_PATH})")
        return 1

    if not os.path.isfile(VENV_PYTHON):
        print(f"venv do claude-code-proxy nao encontrada: {VENV_PYTHON}")
        return 1
    if not os.path.isfile(START_SCRIPT):
        print(f"start_proxy.py nao encontrado: {START_SCRIPT}")
        return 1

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    saida = open(LOG_PATH, "a")
    ambiente = dict(os.environ)

    # Trava de custo: o proxy nao pode nem enxergar chave de provider pago.
    # Ele so le OPENAI_API_KEY/OPENAI_BASE_URL, mas herdar as outras do shell
    # deixava a porta aberta pra engano. Removidas explicitamente.
    for chave_proibida in (
        "OPENROUTER_API_KEY", "ZAI_API_KEY", "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "GROQ_API_KEY",
        "GEMINI_API_KEY", "GOOGLE_API_KEY", "TOGETHER_API_KEY",
        "AZURE_API_KEY", "AZURE_API_VERSION", "DEEPSEEK_API_KEY",
    ):
        ambiente.pop(chave_proibida, None)

    ambiente.update({
        "OPENAI_API_KEY": chave,
        "OPENAI_BASE_URL": NVIDIA_BASE_URL,
        "BIG_MODEL": MODELO_FORTE,
        "MIDDLE_MODEL": MODELO_FORTE,
        "SMALL_MODEL": MODELO_RAPIDO,
        "HOST": "127.0.0.1",
        "PORT": str(PORT),
        "LOG_LEVEL": "INFO",
        "REQUEST_TIMEOUT": "120",
        "MAX_TOKENS_LIMIT": "8192",
    })

    subprocess.Popen(
        [VENV_PYTHON, START_SCRIPT],
        stdout=saida, stderr=saida, stdin=subprocess.DEVNULL,
        start_new_session=True, env=ambiente, cwd=PROXY_DIR,
    )

    for _ in range(60):
        time.sleep(0.5)
        if porta_ocupada() and _health_ok():
            print(f"nvidia_proxy no ar em http://127.0.0.1:{PORT}")
            return 0
    print(f"nvidia_proxy nao subiu a tempo. veja {LOG_PATH}")
    return 1


def _health_ok():
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{PORT}/health", timeout=2
        ) as r:
            return r.status == 200
    except Exception:
        return False


def cmd_stop():
    saida = subprocess.run(["lsof", "-ti", f"tcp:{PORT}"], capture_output=True, text=True)
    pids = [p for p in saida.stdout.split() if p.strip()]
    if not pids:
        print(f"nada rodando na porta {PORT}")
        return 0
    for pid in pids:
        subprocess.run(["kill", pid])
    print("derrubado: " + ", ".join(pids))
    return 0


def _testar_modelo_direto(modelo, chave):
    """Chamada minima direto na NVIDIA (sem passar pelo proxy), so pra diagnostico."""
    corpo = json.dumps({
        "model": modelo,
        "messages": [{"role": "user", "content": "diga apenas: ok"}],
        "max_tokens": 10,
    }).encode("utf-8")
    conn = http.client.HTTPSConnection("integrate.api.nvidia.com", timeout=35)
    try:
        conn.request("POST", "/v1/chat/completions", body=corpo, headers={
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
        })
        resp = conn.getresponse()
        status = resp.status
        dados = resp.read()
        if status == 200:
            return True, "ok"
        return False, f"HTTP {status}: {dados[:200].decode('utf-8', 'replace')}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    finally:
        conn.close()


def cmd_check():
    chave = carregar_chave()
    print(f"chave NVIDIA: {'ok (' + chave[:10] + '...)' if chave else 'AUSENTE'}")
    if not chave:
        return 1

    print(f"venv claude-code-proxy: {VENV_PYTHON} ({'existe' if os.path.isfile(VENV_PYTHON) else 'AUSENTE'})")
    print(f"start_proxy.py: {START_SCRIPT} ({'existe' if os.path.isfile(START_SCRIPT) else 'AUSENTE'})")

    problemas = 0
    print("\ntestando os modelos direto na NVIDIA (sem proxy):")
    for modelo in MODELOS:
        ok, motivo = _testar_modelo_direto(modelo, chave)
        marca = "ok" if ok else "FALHOU"
        print(f"  {modelo}: {marca} ({motivo})")
        if not ok:
            problemas += 1

    print(f"\n{'TUDO OK' if problemas == 0 else str(problemas) + ' PROBLEMA(S) ENCONTRADO(S)'}")
    return 0 if problemas == 0 else 1


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--daemon":
        return cmd_daemon()
    if arg == "--stop":
        return cmd_stop()
    if arg == "--check":
        return cmd_check()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
