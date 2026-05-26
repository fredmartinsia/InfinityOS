#!/usr/bin/env bash
# ============================================================================
#  infinite-os — logging
#  Registra cada passo em $INSTALL_LOG para diagnóstico posterior.
# ============================================================================

log_init() {
  : "${INSTALL_LOG:=$HOME/.infinite-os-install.log}"
  {
    printf '\n===== infinite-os install %s =====\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'host=%s os=%s shell=%s\n' "$(uname -n)" "$(uname -s)" "${SHELL:-?}"
  } >>"$INSTALL_LOG" 2>/dev/null || true
}

log() {
  printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$1" >>"${INSTALL_LOG:-/dev/null}" 2>/dev/null || true
}

# Executa um comando, ecoando-o no log; retorna o status do comando.
log_run() {
  log "RUN: $*"
  "$@" >>"${INSTALL_LOG:-/dev/null}" 2>&1
}
