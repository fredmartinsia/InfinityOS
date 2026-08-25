#!/usr/bin/env bash
# ============================================================================
#  Passo 70 — Smoke test: valida que a instalação ficou de pé.
# ============================================================================
ui_header "11/11 · Verificação final"

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
if [ -f "$HOME/.infinity-os/route.py" ] && python3 "$HOME/.infinity-os/route.py" --task "teste" >/dev/null 2>&1; then
  check_ok "Roteador de modelos (route.py) responde"
else
  check_warn "route.py não respondeu"
fi
[ -f "$HOME/.infinity-os/router.config.yaml" ] && check_ok "Config do roteador presente" || check_warn "router.config.yaml ausente"

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

# ---------------------------------------------------------------------------
# Marcador de versão: é o que permite a próxima atualização saber o que já
# existe aqui, e não sobrescrever o que é seu.
# ---------------------------------------------------------------------------
STATE_DIR="$HOME/.${PRODUCT_SLUG}"
mkdir -p "$STATE_DIR"
printf '%s\n' "$PRODUCT_VERSION" > "$STATE_DIR/VERSION"
{
  printf '# Instalado pelo %s %s em %s\n' "$PRODUCT_NAME" "$PRODUCT_VERSION" "$(date '+%Y-%m-%d %H:%M')"
  printf '# Este arquivo diz o que veio do pacote. O que não está aqui é seu.\n'
  for d in "$INFINITY_OS_ROOT"/content/squads/*/; do
    [ -d "$d" ] && printf 'squad %s\n' "$(basename "$d")"
  done
  for d in "$INFINITY_OS_ROOT"/content/clones/*/; do
    [ -d "$d" ] && printf 'clone %s\n' "$(basename "$d")"
  done
} > "$STATE_DIR/installed-manifest.txt"
ui_dim "Versão registrada em $STATE_DIR/VERSION (usada na próxima atualização)."

# ---------------------------------------------------------------------------
# Próximos passos, na ordem certa
# ---------------------------------------------------------------------------
echo
ui_header "Seus próximos passos"

STEP_N=1
if [ "${INSTALL_MODE:-fresh}" = "upgrade" ]; then
  ui_step "$STEP_N. Arrumar a estrutura do vault"
  ui_dim "   Abra o Claude Code e rode:  /organizar-vault"
  ui_dim "   Ele mostra um retrato do que está bagunçado, propõe a arrumação e"
  ui_dim "   só move depois que você confirmar. Nada é apagado, e tem backup."
  STEP_N=$((STEP_N+1))
else
  ui_step "$STEP_N. Personalizar o sistema para você"
  ui_dim "   Abra o Claude Code e rode:  /onboarding"
  ui_dim "   É a entrevista que monta o vault do jeito do seu trabalho."
  STEP_N=$((STEP_N+1))
fi

missing_keys=0
for v in OPENROUTER_API_KEY NVIDIA_API_KEY GROQ_API_KEY ZAI_API_KEY; do
  [ -z "${!v:-}" ] && [ ! -f "$HOME/.config/$(echo "$v" | cut -d_ -f1 | tr '[:upper:]' '[:lower:]')/env" ] && missing_keys=$((missing_keys+1))
done
if [ "$missing_keys" -gt 0 ]; then
  ui_step "$STEP_N. Ligar os provedores de modelo que faltam"
  ui_dim "   Rode:  ./install.sh --step=25"
  ui_dim "   Ele abre a página de cadastro no seu navegador para cada um que faltar."
  STEP_N=$((STEP_N+1))
fi

if [ "${HAS_LIGHTRAG:-0}" != "1" ] && [ ! -d "$HOME/lightrag-workspace" ]; then
  ui_step "$STEP_N. Instalar a memória de longo prazo (LightRAG)"
  ui_dim "   Rode:  ./install.sh --step=65"
  ui_dim "   É ela que faz o sistema lembrar do seu contexto entre conversas."
  STEP_N=$((STEP_N+1))
fi

ui_step "$STEP_N. Usar"
ui_dim "   Digite / no Claude Code para ver os squads e clones disponíveis."
echo
