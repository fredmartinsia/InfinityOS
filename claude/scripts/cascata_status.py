#!/usr/bin/env python3
"""Diagnostico do claude-or: proxy, cadeias, ultimas chamadas e cota do dia."""

import json
import os
import re
import sys
import urllib.request

HOME = os.path.expanduser("~")
PORT = os.environ.get("CASCATA_PORT", "47822")
LOG = os.path.join(HOME, ".claude", "logs", "cascata.log")
ENV = os.path.join(HOME, ".config", "openrouter", "env")


def chave():
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if k:
        return k
    try:
        with open(ENV, "r", encoding="utf-8") as f:
            for linha in f:
                m = re.match(r'\s*export\s+OPENROUTER_API_KEY\s*=\s*"?([^"\n]+)"?', linha)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return ""


def busca(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    print("=" * 66)
    print("  claude-or  |  cascata de modelos gratuitos")
    print("=" * 66)

    try:
        h = busca(f"http://127.0.0.1:{PORT}/health", timeout=5)
    except Exception as e:
        print(f"\n  PROXY: FORA DO AR na porta {PORT}  ({type(e).__name__})")
        print("  suba com: python3 ~/.claude/scripts/cascata_proxy.py --daemon")
        print("  ou use o plano B: claude-or-direto")
        return 1

    m, s = divmod(int(h.get("uptime_s", 0)), 60)
    hh, m = divmod(m, 60)
    print(f"\n  PROXY: no ar na porta {PORT}  (uptime {hh}h{m:02d}m{s:02d}s)")
    print(f"  orquestrador de complexidade: {'ligado' if h.get('orquestrador') else 'desligado'}")
    print(f"  requisicoes: {h.get('requisicoes', 0)}  |  fallbacks acionados: "
          f"{h.get('fallbacks', 0)}  |  erros: {h.get('erros', 0)}")

    print("\n  CADEIAS")
    for nome, cadeia in (h.get("cadeias") or {}).items():
        print(f"    {nome}")
        for i, mod in enumerate(cadeia, 1):
            print(f"       {i}. {mod}")

    ultimos = h.get("ultimos") or []
    if ultimos:
        print("\n  ULTIMAS CHAMADAS")
        for u in ultimos[:8]:
            serviu = u.get("serviu") or "FALHOU"
            marca = ""
            if u.get("erro"):
                marca = "  <== ERRO"
            elif u.get("pediu") and serviu != u.get("pediu"):
                marca = f"  <== FALLBACK (pediu {u['pediu'].split('/')[-1]})"
            print(f"    {u.get('quando')}  {serviu:<45} {u.get('ms')}ms{marca}")

    k = chave()
    if k:
        cab = {"Authorization": f"Bearer {k}"}
        try:
            d = busca("https://openrouter.ai/api/v1/key", cab)["data"]
            print("\n  COTA OPENROUTER")
            print(f"    gasto hoje: ${d.get('usage_daily', 0):.4f}  |  no mes: ${d.get('usage_monthly', 0):.2f}")
            print(f"    conta free tier: {d.get('is_free_tier')}  "
                  f"(false = teto de 1000 requests/dia nos modelos :free)")
        except Exception as e:
            print(f"\n  COTA OPENROUTER: nao consegui consultar ({type(e).__name__})")
        try:
            c = busca("https://openrouter.ai/api/v1/credits", cab)["data"]
            resta = c.get("total_credits", 0) - c.get("total_usage", 0)
            print(f"    saldo restante: ${resta:.2f}  (so os comandos pagos consomem: "
                  f"claude-d, claude-q, claude-m)")
        except Exception:
            pass

    print("\n  COMANDOS")
    print("    claude-or          cascata gratuita, compacta em 240k (uso normal)")
    print("    claude-or-1m       cascata gratuita com janela de 900k, sem rede abaixo do ultra")
    print("    claude-or-direto   modelo unico gratuito, sem proxy (plano B)")
    print("    claude-d           deepseek-v4-pro   1M ctx   PAGO")
    print("    claude-q           qwen3.7-plus      1M ctx   PAGO")
    print("    claude-m           minimax-m3        1M ctx   PAGO")
    print("    claude-z           GLM 5.2 pela Z.ai (plano flat, fora do saldo acima)")

    if os.path.exists(LOG):
        tam = os.path.getsize(LOG) / 1024
        print(f"\n  log completo: {LOG}  ({tam:.0f} KB)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
