#!/usr/bin/env bash
# ============================================================================
#  infinite-os — instalador (modo idiota)
#  git clone ... && cd infinite-os && ./install.sh
#
#  Guiado, com defaults seguros (Enter = sim). Detecta seu computador,
#  pergunta antes de instalar qualquer coisa, faz backup e valida no fim.
# ============================================================================
set -uo pipefail

# Raiz do repo = pasta deste script
INFINITE_OS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export INFINITE_OS_ROOT

# Carrega libs
. "$INFINITE_OS_ROOT/installer/lib/env.sh"
. "$INFINITE_OS_ROOT/installer/lib/ui.sh"
. "$INFINITE_OS_ROOT/installer/lib/log.sh"

log_init

# Flags
ASSUME_YES=0
ONLY_STEP=""
for arg in "$@"; do
  case "$arg" in
    -y|--yes) ASSUME_YES=1 ;;
    --step=*) ONLY_STEP="${arg#--step=}" ;;
    -h|--help)
      echo "Uso: ./install.sh [-y|--yes] [--step=NN]"
      echo "  -y        aceita os defaults sem perguntar (não-interativo)"
      echo "  --step=NN roda só um passo (ex.: --step=00)"
      exit 0 ;;
  esac
done
export ASSUME_YES

ui_banner "$PRODUCT_NAME v$PRODUCT_VERSION"
ui_info "Este instalador vai configurar seu ambiente de orquestração de agentes."
ui_info "Ele pergunta antes de instalar qualquer coisa. Em caso de dúvida, Enter = sim."
ui_dim  "Log completo em: $INSTALL_LOG"

# Lista ordenada de passos
STEPS=(
  "00-preflight"
  "10-clis"
  "20-models"
  "30-claude-core"
  "40-aiox"
  "50-content"
  "60-obsidian"
  "70-smoke-test"
)

run_step() {
  local name="$1"
  local file="$INFINITE_OS_ROOT/installer/steps/${name}.sh"
  if [ ! -f "$file" ]; then
    ui_warn "Passo ausente: $name (pulado)"
    log "MISSING STEP: $file"
    return 0
  fi
  log "STEP START: $name"
  # shellcheck disable=SC1090
  . "$file"
  log "STEP END: $name"
}

if [ -n "$ONLY_STEP" ]; then
  for s in "${STEPS[@]}"; do
    [[ "$s" == "$ONLY_STEP"* ]] && run_step "$s"
  done
else
  for s in "${STEPS[@]}"; do
    run_step "$s"
  done
fi

ui_header "Pronto!"
ui_ok "Instalação concluída."
ui_info "Abra o Claude Code e rode:  /onboarding"
ui_dim  "Para desfazer:  ./uninstall.sh   (backup em $BACKUP_DIR)"
