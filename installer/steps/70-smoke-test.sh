#!/usr/bin/env bash
# ============================================================================
#  Passo 70 — Smoke test: valida que a instalação ficou de pé.
# ============================================================================
ui_header "8/8 — Verificação final"

pass=0; warn=0
check_ok()   { ui_ok "$1"; pass=$((pass+1)); }
check_warn() { ui_warn "$1"; warn=$((warn+1)); }

# settings.json válido
if python3 -c "import json,sys; json.load(open('$CLAUDE_HOME/settings.json'))" 2>/dev/null; then
  check_ok "settings.json é JSON válido"
else
  check_warn "settings.json inválido ou ausente"
fi

# RAG dry-run
if CLAUDE_VAULT_PATH="${VAULT_PATH:-$DEFAULT_VAULT_PATH}" python3 "$CLAUDE_HOME/scripts/vault_rag.py" --dry-run >/dev/null 2>&1; then
  check_ok "Hook de RAG (vault_rag.py) executa"
else
  check_warn "vault_rag.py --dry-run falhou (cheque o vault path)"
fi

# Roteador
if [ -f "$HOME/.infinite-os/route.py" ] && python3 "$HOME/.infinite-os/route.py" --task "teste" >/dev/null 2>&1; then
  check_ok "Roteador de modelos (route.py) responde"
else
  check_warn "route.py não respondeu"
fi
[ -f "$HOME/.infinite-os/router.config.yaml" ] && check_ok "Config do roteador presente" || check_warn "router.config.yaml ausente"

# Contagens
nsk=$(ls -1d "$CLAUDE_HOME"/skills/*/ 2>/dev/null | wc -l | tr -d ' ')
nsq=$(ls -1d "$CLAUDE_HOME"/commands/*/ 2>/dev/null | wc -l | tr -d ' ')
ncl=$(ls -1d "${VAULT_PATH:-$DEFAULT_VAULT_PATH}"/CLONES/*/ 2>/dev/null | wc -l | tr -d ' ')
[ "${nsk:-0}" -ge 8 ]  && check_ok "Skills instaladas: $nsk"        || check_warn "Poucas skills: $nsk"
[ "${nsq:-0}" -ge 15 ] && check_ok "Squads instalados: $nsq"       || check_warn "Poucos squads: $nsq"
[ "${ncl:-0}" -ge 50 ] && check_ok "Clones no vault: $ncl"         || check_warn "Poucos clones: $ncl"

echo
if [ "$warn" -eq 0 ]; then
  ui_ok "Tudo verde ($pass checks). 🎉"
else
  ui_warn "$pass OK, $warn aviso(s). Veja o log: $INSTALL_LOG"
fi
log "smoke: pass=$pass warn=$warn skills=$nsk squads=$nsq clones=$ncl"
