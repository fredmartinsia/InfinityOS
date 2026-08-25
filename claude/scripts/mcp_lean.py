#!/usr/bin/env python3
"""
mcp_lean.py - liga/desliga MCP servers, plugins e ferramentas nativas pesadas sob
demanda pra manter o contexto inicial enxuto. Determinismo puro em codigo (token zero).

Alvos controlados:
  - meta-ads    (mcpServers em ~/.claude.json, http)    <- manual (Graph API no squad)
  - kairogen    (mcpServers em ~/.claude.json, http)    <- manual (/kairogen-on)
  - playwright  (mcpServers em ~/.mcp.json, stdio)       <- manual (/playwright-on)
  - workflow    (nativa, via permissions.deny)           <- manual (/workflow-on)
  - travel      (plugin travel-hacker@borski)            <- manual (/travel-on)
  - design      (plugin ui-ux-pro-max@nextlevelbuilder)  <- gatilho: squad de design

Subcomandos:
  clean              -> estado limpo: todos os alvos geridos OFF
  on <alvo>          -> liga
  off <alvo>         -> desliga
  status             -> mostra on/off
  autodetect         -> hook UserPromptSubmit: avisos por gatilho. Nunca bloqueia.

Nota: MCP recarrega com /mcp; nativa (deny) e plugin recarregam so com nova sessao.
"""
import json
import os
import re
import subprocess
import sys
import time
import glob

HOME = os.path.expanduser("~")
CLAUDE_JSON = os.path.join(HOME, ".claude.json")
MCP_JSON = os.path.join(HOME, ".mcp.json")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
REGISTRY = os.path.join(HOME, ".claude", "scripts", "mcp_lean_registry.json")

# MCP servers geridos: nome -> arquivo onde a entrada mcpServers mora.
# Ficam OFF por padrao (fora do autoload); a config completa mora no registry.
HTTP_MCPS = {
    "meta-ads": CLAUDE_JSON,
    "kairogen": CLAUDE_JSON,
    "playwright": MCP_JSON,
}

# ferramentas nativas geridas via permissions.deny (nome puro = fora do contexto).
# OFF = presente no deny; ON = ausente do deny. Recarrega so com nova sessao.
NATIVE_ONDEMAND = ("Workflow",)

# plugins geridos: chave curta -> id no enabledPlugins
PLUGINS = {
    "travel": "travel-hacker@borski",
    "design": "ui-ux-pro-max@nextlevelbuilder",
}
BACKUPS_KEEP = 5

# alvos que o usuário quer sempre ligados (usa muito): o clean do SessionEnd os pula,
# entao sobrevivem entre sessoes. Ainda da pra desligar manual com off <alvo>.
PERSIST_ON = {"playwright"}


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _prune_backups(path):
    for old in sorted(glob.glob(path + ".bak-*"))[:-BACKUPS_KEEP]:
        try:
            os.remove(old)
        except OSError:
            pass


def _save(path, data):
    ts = time.strftime("%Y%m%d-%H%M%S")
    try:
        with open(path, "r", encoding="utf-8") as src, \
                open(path + ".bak-" + ts, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    except OSError:
        pass
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)
    _prune_backups(path)


def _registry():
    return _load(REGISTRY)


# --- MCP servers (mcpServers em ~/.claude.json ou ~/.mcp.json) ---
def http_mcp_on(name):
    path = HTTP_MCPS[name]
    try:
        d = _load(path)
    except FileNotFoundError:
        d = {}
    ms = d.setdefault("mcpServers", {})
    if name in ms:
        return False
    ms[name] = _registry()[name]
    _save(path, d)
    return True


def http_mcp_off(name):
    path = HTTP_MCPS[name]
    try:
        d = _load(path)
    except FileNotFoundError:
        return False
    ms = d.get("mcpServers", {})
    if name not in ms:
        return False
    del ms[name]
    _save(path, d)
    return True


def is_http_mcp_on(name):
    path = HTTP_MCPS[name]
    try:
        return name in _load(path).get("mcpServers", {})
    except FileNotFoundError:
        return False


# --- ferramentas nativas via permissions.deny (settings.json) ---
def native_on(name):
    # remove do deny -> a ferramenta volta ao contexto (vale na proxima sessao)
    s = _load(SETTINGS)
    deny = s.get("permissions", {}).get("deny", [])
    if name not in deny:
        return False
    while name in deny:
        deny.remove(name)
    _save(SETTINGS, s)
    return True


def native_off(name):
    # adiciona ao deny -> some do contexto (vale na proxima sessao)
    s = _load(SETTINGS)
    deny = s.setdefault("permissions", {}).setdefault("deny", [])
    if name in deny:
        return False
    deny.append(name)
    _save(SETTINGS, s)
    return True


def is_native_on(name):
    # ON = NAO esta no deny
    s = _load(SETTINGS)
    return name not in s.get("permissions", {}).get("deny", [])


# --- plugins (enabledPlugins em settings.json) ---
def plugin_set(key, enabled):
    pid = PLUGINS[key]
    s = _load(SETTINGS)
    ep = s.setdefault("enabledPlugins", {})
    if ep.get(pid) == enabled:
        return False
    ep[pid] = enabled
    _save(SETTINGS, s)
    return True


def is_plugin_on(key):
    pid = PLUGINS[key]
    return bool(_load(SETTINGS).get("enabledPlugins", {}).get(pid, False))


# --- comandos ---
def cmd_clean():
    parts = []
    for name in HTTP_MCPS:
        if name in PERSIST_ON:
            parts.append(name + " mantido (persistente)")
            continue
        parts.append(name + " " + ("removido" if http_mcp_off(name) else "ja off"))
    for name in NATIVE_ONDEMAND:
        parts.append(name + " " + ("negado" if native_off(name) else "ja off"))
    for key in PLUGINS:
        parts.append(key + " " + ("desligado" if plugin_set(key, False) else "ja off"))
    print("[mcp_lean] clean: " + ", ".join(parts))


def _resolve(target):
    t = target.lower()
    if t in ("meta-ads", "metaads", "meta"):
        return "meta-ads"
    if t in ("kairogen", "kairo", "kairogen-ai"):
        return "kairogen"
    if t in ("playwright", "pw", "browser"):
        return "playwright"
    if t in ("workflow", "workflows", "wf"):
        return "Workflow"
    if t in ("travel", "travel-hacker", "viagem"):
        return "travel"
    if t in ("design", "ui-ux", "ui-ux-pro-max", "ux"):
        return "design"
    return None


_ALVOS = "meta-ads | kairogen | playwright | workflow | travel | design"


def cmd_on(target):
    key = _resolve(target)
    if key in HTTP_MCPS:
        ch = http_mcp_on(key)
        print("[mcp_lean] %s %s. Rode /mcp (reconnect) pra carregar as tools."
              % (key, "ligado" if ch else "ja on"))
    elif key in NATIVE_ONDEMAND:
        ch = native_on(key)
        print("[mcp_lean] %s %s. Reinicie a sessao pra a ferramenta voltar ao contexto."
              % (key, "liberado" if ch else "ja on"))
    elif key in PLUGINS:
        ch = plugin_set(key, True)
        print("[mcp_lean] plugin %s %s. Reinicie a sessao pra carregar as skills."
              % (key, "ligado" if ch else "ja on"))
    else:
        print("[mcp_lean] alvo desconhecido: %s (%s)" % (target, _ALVOS), file=sys.stderr)
        sys.exit(2)


def cmd_off(target):
    key = _resolve(target)
    if key in HTTP_MCPS:
        print("[mcp_lean] %s %s." % (key, "desligado" if http_mcp_off(key) else "ja off"))
    elif key in NATIVE_ONDEMAND:
        print("[mcp_lean] %s %s (no deny)." % (key, "negado" if native_off(key) else "ja off"))
    elif key in PLUGINS:
        print("[mcp_lean] plugin %s %s." % (key, "desligado" if plugin_set(key, False) else "ja off"))
    else:
        print("[mcp_lean] alvo desconhecido: %s (%s)" % (target, _ALVOS), file=sys.stderr)
        sys.exit(2)


def cmd_status():
    for name in HTTP_MCPS:
        print("%-12s %s (mcp)" % (name + ":", "ON" if is_http_mcp_on(name) else "off"))
    for name in NATIVE_ONDEMAND:
        print("%-12s %s (nativa)" % (name + ":", "ON" if is_native_on(name) else "off"))
    for key in PLUGINS:
        print("%-12s %s (%s)" % (key + ":", "ON" if is_plugin_on(key) else "off", PLUGINS[key]))


# gatilhos por squad
TRAFFIC_RE = re.compile(
    r"traffic[-_ ]?masters|traffic[-_ ]?chief|squad de tr[aá]fego|/traffic",
    re.IGNORECASE)
DESIGN_RE = re.compile(
    r"design[-_ ]?system|design[-_ ]?squad|design[-_ ]?chief|squad de design|/design",
    re.IGNORECASE)


def cmd_autodetect():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except (ValueError, OSError):
        payload = {}
    prompt = str(payload.get("prompt", ""))
    if not prompt:
        return
    msgs = []
    # meta-ads NAO liga mais no squad de trafego (decisao usuário 2026-07-14): dados da Meta
    # vao via Graph API (curl / sync_meta.py), nunca por MCP (estoura o contexto).
    # Ver ~/.claude/commands/traffic-masters/POLICY-DADOS-META.md
    # Religar pontualmente: python3 ~/.claude/scripts/mcp_lean.py on meta-ads
    if TRAFFIC_RE.search(prompt):
        msgs.append("squad de trafego: dados da Meta via GRAPH API (nao MCP). "
                    "Ver POLICY-DADOS-META.md do squad.")
    if DESIGN_RE.search(prompt):
        try:
            if plugin_set("design", True):
                msgs.append("plugin ui-ux-pro-max HABILITADO (squad de design). "
                            "Reinicie a sessao pra carregar as skills de design.")
        except (OSError, ValueError, KeyError):
            pass
    if msgs:
        print("[mcp_lean] " + " | ".join(msgs)
              + " Ao encerrar a sessao tudo desliga automaticamente.")


def main():
    args = sys.argv[1:]
    if not args:
        cmd_status()
        return
    cmd = args[0]
    if cmd == "clean":
        cmd_clean()
    elif cmd == "on" and len(args) >= 2:
        cmd_on(args[1])
    elif cmd == "off" and len(args) >= 2:
        cmd_off(args[1])
    elif cmd == "status":
        cmd_status()
    elif cmd == "autodetect":
        cmd_autodetect()
    else:
        print("uso: mcp_lean.py [clean | on <alvo> | off <alvo> | status | autodetect]",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
