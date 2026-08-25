#!/usr/bin/env python3
"""Claude Code statusline — limites 5h/7d, contexto e custo da sessão."""
from __future__ import annotations
import json, os, sys, time
import urllib.request
from typing import Any

RESET="\033[0m"; DIM="\033[2m"; BOLD="\033[1m"
CYAN="\033[36m"; GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; WHITE="\033[37m"

# --- Cotas do GLM Coding Plan (Z.ai) ---
# O Claude Code so injeta rate_limits quando roda na Anthropic. No GLM (claude-z)
# esses campos chegam vazios; aqui perguntamos direto a API da Z.ai com a mesma chave.
ZAI_QUOTA_URL = "https://api.z.ai/api/monitor/usage/quota/limit"
ZAI_CACHE = os.path.expanduser("~/.claude/.cache/zai_quota.json")
ZAI_CACHE_TTL = 60  # segundos (statusline roda a cada 30s; cache evita 1 chamada/refresh)

def color_for(pct: float) -> str:
    if pct >= 90: return RED
    if pct >= 70: return YELLOW
    return GREEN

def bar(pct: float, width: int = 10) -> str:
    pct = max(0.0, min(100.0, float(pct)))
    filled = max(0, min(width, int(round(pct * width / 100.0))))
    return "█" * filled + "░" * (width - filled)

def fmt_pct(pct):
    return "—" if pct is None else f"{pct:.0f}%"

def fmt_reset(ts):
    if ts is None:
        return ""
    try:
        remaining = int(float(ts) - time.time())
    except (TypeError, ValueError):
        return ""
    if remaining <= 0:
        return "agora"
    h, rem = divmod(remaining, 3600)
    m = rem // 60
    if h > 0:
        return f"{h}h{m:02d}m"
    if m > 0:
        return f"{m}m"
    return f"{remaining}s"

def fmt_cost(cost):
    try:
        return f"${float(cost):.2f}" if cost is not None else ""
    except (TypeError, ValueError):
        return ""

def fmt_duration(ms):
    try:
        total = int(float(ms) // 1000)
    except (TypeError, ValueError):
        return ""
    if total <= 0:
        return ""
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"

def get(data, *keys, default=None):
    cur = data
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
        if cur is None:
            return default
    return cur

def to_float(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None

def seg_limit(label, pct, reset_ts):
    if pct is None:
        return f"{DIM}{label}:{RESET} {DIM}—{RESET}"
    c = color_for(pct)
    r = fmt_reset(reset_ts)
    return f"{c}{label}:{bar(pct)} {fmt_pct(pct)}{RESET}" + (f" {DIM}↻{r}{RESET}" if r else "")

def seg_ctx(pct):
    if pct is None:
        return f"{DIM}ctx:{RESET} {DIM}—{RESET}"
    c = color_for(pct)
    return f"{c}ctx:{bar(pct, 8)} {fmt_pct(pct)}{RESET}"

def zai_api_key():
    """Chave ZAI do ambiente (claude-z exporta ZAI_API_KEY) ou do arquivo de config."""
    k = os.environ.get("ZAI_API_KEY", "").strip()
    if k:
        return k
    try:
        with open(os.path.expanduser("~/.config/zai/env")) as f:
            for line in f:
                if "ZAI_API_KEY" in line and "=" in line:
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v:
                        return v
    except OSError:
        pass
    return None

def _parse_zai(payload):
    """Token TOKENS_LIMIT unit=3 = janela 5h, unit=6 = cota semanal (7d).
    nextResetTime vem em ms; fmt_reset espera segundos, logo dividimos por 1000."""
    five = week = (None, None)
    try:
        for lim in payload["data"]["limits"]:
            if lim.get("type") != "TOKENS_LIMIT":
                continue
            pct = lim.get("percentage")
            rst = (lim.get("nextResetTime") or 0) / 1000.0
            if lim.get("unit") == 3:
                five = (pct, rst)
            elif lim.get("unit") == 6:
                week = (pct, rst)
    except (KeyError, TypeError):
        pass
    return five[0], five[1], week[0], week[1]

def fetch_zai_quota():
    """(five_pct, five_reset, week_pct, week_reset) da Z.ai, com cache de 60s. None se falhar."""
    now = time.time()
    try:
        with open(ZAI_CACHE) as f:
            cache = json.load(f)
        if now - cache.get("ts", 0) < ZAI_CACHE_TTL:
            return _parse_zai(cache["data"])
    except (OSError, json.JSONDecodeError, KeyError, ValueError):
        pass
    key = zai_api_key()
    if not key:
        return (None, None, None, None)
    req = urllib.request.Request(ZAI_QUOTA_URL, headers={
        "Authorization": key,
        "Accept-Language": "en-US,en",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            payload = json.loads(resp.read())
    except Exception:
        return (None, None, None, None)  # statusline nunca pode quebrar
    try:
        os.makedirs(os.path.dirname(ZAI_CACHE), exist_ok=True)
        with open(ZAI_CACHE, "w") as f:
            json.dump({"ts": now, "data": payload}, f)
    except OSError:
        pass
    return _parse_zai(payload)

def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print(f"{DIM}statusline: json inválido{RESET}")
        return 0

    model = get(data, "model", "display_name", default="Claude")
    cwd = get(data, "workspace", "current_dir") or data.get("cwd") or ""
    folder = os.path.basename(cwd.rstrip("/")) if cwd else "?"
    cost_s = fmt_cost(get(data, "cost", "total_cost_usd"))
    dur_s = fmt_duration(get(data, "cost", "total_duration_ms"))
    ctx = to_float(get(data, "context_window", "used_percentage"))
    five = to_float(get(data, "rate_limits", "five_hour", "used_percentage"))
    week = to_float(get(data, "rate_limits", "seven_day", "used_percentage"))
    five_r = get(data, "rate_limits", "five_hour", "resets_at")
    week_r = get(data, "rate_limits", "seven_day", "resets_at")

    # Anthropic nao envia rate_limits no GLM: pergunta direto a Z.ai.
    if five is None and week is None:
        zf, zfr, zw, zwr = fetch_zai_quota()
        five = zf if five is None else five
        five_r = zfr if five_r is None else five_r
        week = zw if week is None else week
        week_r = zwr if week_r is None else week_r

    line1 = [f"{BOLD}{CYAN}[{model}]{RESET}", f"{WHITE}📁 {folder}{RESET}"]
    if cost_s:
        line1.append(f"{YELLOW}{cost_s}{RESET}")
    if dur_s:
        line1.append(f"{DIM}⏱ {dur_s}{RESET}")

    line2 = [seg_limit("5h", five, five_r), seg_limit("7d", week, week_r), seg_ctx(ctx)]
    if five is None and week is None:
        line2.append(f"{DIM}(limites após 1ª resposta){RESET}")

    print("  ".join(line1))
    print("  ".join(line2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
