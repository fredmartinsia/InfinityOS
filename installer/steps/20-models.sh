#!/usr/bin/env bash
# ============================================================================
#  Passo 20 — Modelos locais: recomenda um modelo conforme o hardware e
#  oferece baixar via Ollama. Exporta CHOSEN_LOCAL_MODEL (usado no passo 30).
# ============================================================================
ui_header "3/8 — Modelo local (opcional)"

# Default mesmo sem download (o roteador referencia este nome)
CHOSEN_LOCAL_MODEL="qwen3-coder:30b"

if [ "${INFINITE_OS_SKIP_MODELS:-0}" = "1" ]; then
  ui_dim "Passo de modelos locais pulado (INFINITE_OS_SKIP_MODELS=1)."
  export CHOSEN_LOCAL_MODEL
  return 0 2>/dev/null || true
fi

if [ "${HAS_OLLAMA:-0}" != "1" ]; then
  ui_dim "Ollama não está instalado — pulando modelos locais. (O roteador usa nuvem.)"
  export CHOSEN_LOCAL_MODEL
  return 0 2>/dev/null || true
fi

# --- Escolhe o tier a partir da RAM, com bônus de GPU -----------------------
ram="${RAM_GB:-0}"
tier="minimal"; rec=""
if   [ "$ram" -ge 64 ]; then tier="workstation"; rec="qwen3-coder:30b"
elif [ "$ram" -ge 32 ]; then tier="power";       rec="qwen3-coder:30b"
elif [ "$ram" -ge 16 ]; then tier="standard";    rec="qwen2.5-coder:14b"
elif [ "$ram" -ge 8  ]; then tier="light";       rec="qwen2.5-coder:7b"
else                          tier="minimal";    rec=""
fi

# Bônus: Apple Silicon (memória unificada) ou GPU forte sobe um degrau
if [ "${IS_APPLE_SILICON:-0}" = "1" ] || [ "${VRAM_GB:-0}" -ge 16 ]; then
  case "$tier" in
    minimal)  tier="light";    rec="qwen2.5-coder:7b" ;;
    light)    tier="standard"; rec="qwen2.5-coder:14b" ;;
    standard) tier="power";    rec="qwen3-coder:30b" ;;
  esac
fi

if [ -z "$rec" ]; then
  ui_warn "RAM baixa (${ram} GB) para um modelo local confortável."
  if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Quer mesmo assim baixar um modelo pequeno (qwen2.5:3b)?" "N"; then
    rec="qwen2.5:3b"
  else
    ui_dim "Sem modelo local. Tudo bem — o roteador usa nuvem (Gemini/Claude)."
    export CHOSEN_LOCAL_MODEL
    return 0 2>/dev/null || true
  fi
fi

ui_info "Pelo seu hardware (tier: $tier), recomendo: ${C_BOLD}${rec}${C_RESET}"

# Pergunta (a não ser em modo -y)
do_pull=1
if [ "${ASSUME_YES:-0}" != "1" ]; then
  if ui_yesno "Posso baixar o modelo $rec agora?" "Y"; then do_pull=1; else do_pull=0; fi
fi

if [ "$do_pull" = "1" ]; then
  ui_dim "Baixando $rec (pode levar alguns minutos)..."
  if log_run ollama pull "$rec"; then
    ui_ok "Modelo $rec pronto."
    CHOSEN_LOCAL_MODEL="$rec"
  else
    ui_warn "Falha no download de $rec (veja o log). O roteador fará fallback."
  fi
else
  ui_dim "Pulado. O roteador usará nuvem até você baixar um modelo local."
fi

export CHOSEN_LOCAL_MODEL
log "models: tier=$tier rec=$rec chosen=$CHOSEN_LOCAL_MODEL"
