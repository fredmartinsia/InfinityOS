#!/usr/bin/env bash
# ============================================================================
#  Passo 00 — Preflight: detecta o computador e os pré-requisitos.
#  Exporta: OS_KIND, RAM_GB, CPU_CORES, IS_APPLE_SILICON, HAS_NVIDIA, VRAM_GB
# ============================================================================
ui_header "1/11 · Analisando seu computador"

# --- Sistema operacional ----------------------------------------------------
case "$(uname -s)" in
  Darwin) OS_KIND="macos" ;;
  Linux)
    if grep -qi microsoft /proc/version 2>/dev/null; then OS_KIND="wsl"; else OS_KIND="linux"; fi ;;
  *) OS_KIND="desconhecido" ;;
esac

# --- RAM (GB) ---------------------------------------------------------------
RAM_GB=0
if [ "$OS_KIND" = "macos" ]; then
  RAM_GB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1024 / 1024 / 1024 ))
elif [ -r /proc/meminfo ]; then
  RAM_GB=$(( $(awk '/MemTotal/{print $2}' /proc/meminfo) / 1024 / 1024 ))
fi

# --- Núcleos ----------------------------------------------------------------
CPU_CORES="$(getconf _NPROCESSORS_ONLN 2>/dev/null || nproc 2>/dev/null || echo '?')"

# --- Apple Silicon / GPU ----------------------------------------------------
IS_APPLE_SILICON=0
HAS_NVIDIA=0
VRAM_GB=0
if [ "$OS_KIND" = "macos" ] && [ "$(uname -m)" = "arm64" ]; then
  IS_APPLE_SILICON=1
fi
if command -v nvidia-smi >/dev/null 2>&1; then
  HAS_NVIDIA=1
  VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9')
  [ -n "${VRAM_MB:-}" ] && VRAM_GB=$(( VRAM_MB / 1024 ))
fi

export OS_KIND RAM_GB CPU_CORES IS_APPLE_SILICON HAS_NVIDIA VRAM_GB

# --- Pré-requisitos ---------------------------------------------------------
have() { command -v "$1" >/dev/null 2>&1; }
PY_OK=0; GIT_OK=0; NODE_OK=0; CLAUDE_OK=0
have python3 && PY_OK=1
have git && GIT_OK=1
( have npx || have node ) && NODE_OK=1
have claude && CLAUDE_OK=1
export PY_OK GIT_OK NODE_OK CLAUDE_OK

# --- Resumo -----------------------------------------------------------------
gpu_desc="integrada/CPU"
[ "$IS_APPLE_SILICON" = "1" ] && gpu_desc="Apple Silicon (memória unificada)"
[ "$HAS_NVIDIA" = "1" ] && gpu_desc="NVIDIA (~${VRAM_GB} GB VRAM)"

ui_info "Sistema:   $OS_KIND"
ui_info "Memória:   ${RAM_GB} GB RAM  |  Núcleos: ${CPU_CORES}"
ui_info "Gráficos:  $gpu_desc"
echo
ui_info "Pré-requisitos:"
[ "$PY_OK" = 1 ]     && ui_ok "Python 3"          || ui_warn "Python 3 ausente (necessário p/ hooks de RAG)"
[ "$GIT_OK" = 1 ]    && ui_ok "git"               || ui_warn "git ausente"
[ "$NODE_OK" = 1 ]   && ui_ok "Node/npx"          || ui_warn "Node/npx ausente (necessário p/ AIOX e algumas CLIs)"
[ "$CLAUDE_OK" = 1 ] && ui_ok "Claude Code CLI"   || ui_warn "Claude Code CLI ausente (recomendado — instale em claude.com/code)"

log "preflight: os=$OS_KIND ram=${RAM_GB}GB cores=$CPU_CORES apple=$IS_APPLE_SILICON nvidia=$HAS_NVIDIA vram=${VRAM_GB}GB py=$PY_OK git=$GIT_OK node=$NODE_OK claude=$CLAUDE_OK"

if [ "$PY_OK" = 0 ]; then
  ui_error "Python 3 é obrigatório. Instale e rode de novo."
  ui_dim "macOS: brew install python   |   Linux: sudo apt install python3"
  exit 1
fi

# Resumo amigável da capacidade para modelos locais
if [ "$RAM_GB" -ge 32 ]; then
  ui_dim "Seu computador comporta modelos locais grandes (até ~30B)."
elif [ "$RAM_GB" -ge 16 ]; then
  ui_dim "Seu computador comporta modelos locais médios (~14B)."
elif [ "$RAM_GB" -ge 8 ]; then
  ui_dim "Seu computador comporta modelos locais pequenos (~7B)."
else
  ui_dim "Pouca RAM para modelos locais — vamos preferir modelos em nuvem."
fi
