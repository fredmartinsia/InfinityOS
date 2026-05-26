#!/usr/bin/env bash
# ============================================================================
#  infinity-os — desinstalador
#  Restaura o backup do ~/.claude feito antes da última instalação.
# ============================================================================
set -uo pipefail
INFINITY_OS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
. "$INFINITY_OS_ROOT/installer/lib/env.sh"
. "$INFINITY_OS_ROOT/installer/lib/ui.sh"

ui_banner "$PRODUCT_NAME — desinstalar"

# Acha o backup mais recente
latest="$(ls -1dt "$HOME"/.${PRODUCT_SLUG}-backup-* 2>/dev/null | head -1)"
if [ -z "$latest" ]; then
  ui_error "Nenhum backup encontrado (~/.${PRODUCT_SLUG}-backup-*)."
  ui_dim "Nada a restaurar. Você pode remover manualmente o que foi instalado em ~/.claude."
  exit 1
fi

ui_info "Backup encontrado: $latest"
ui_warn "Isto vai RESTAURAR o ~/.claude (settings/scripts/skills/commands) ao estado anterior."
if ! ui_yesno "Confirmar restauração?" "N"; then
  ui_dim "Cancelado."
  exit 0
fi

for item in settings.json scripts skills commands; do
  if [ -e "$latest/$item" ]; then
    rm -rf "$CLAUDE_HOME/$item"
    cp -R "$latest/$item" "$CLAUDE_HOME/$item"
    ui_ok "restaurado: $item"
  fi
done

# Remove a config do roteador (não estava no ~/.claude)
[ -d "$HOME/.infinity-os" ] && ui_dim "Mantida a pasta ~/.infinity-os/ (roteador). Remova manualmente se quiser."

ui_ok "Restauração concluída."
ui_dim "Plugins de marketplace e conteúdo do vault NÃO são removidos automaticamente."
