#!/usr/bin/env bash
# ============================================================================
#  infinite-os — biblioteca de UX "modo idiota"
#  Prompts simples, defaults seguros (Enter = sim), cores e linguagem clara.
#  Filosofia: qualquer pessoa, sem jargão, consegue ir até o fim.
# ============================================================================

# --- Cores (desativadas se não for terminal ou se NO_COLOR setado) ----------
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  C_RESET=$'\033[0m'; C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'
  C_RED=$'\033[31m'; C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'
  C_BLUE=$'\033[34m'; C_CYAN=$'\033[36m'
else
  C_RESET=""; C_BOLD=""; C_DIM=""; C_RED=""; C_GREEN=""; C_YELLOW=""; C_BLUE=""; C_CYAN=""
fi

# --- Saída básica -----------------------------------------------------------
ui_header()  { printf "\n%s%s== %s ==%s\n" "$C_BOLD" "$C_CYAN" "$1" "$C_RESET"; }
ui_step()    { printf "%s▸%s %s\n" "$C_BLUE" "$C_RESET" "$1"; }
ui_info()    { printf "  %s\n" "$1"; }
ui_dim()     { printf "%s  %s%s\n" "$C_DIM" "$1" "$C_RESET"; }
ui_ok()      { printf "%s✓%s %s\n" "$C_GREEN" "$C_RESET" "$1"; }
ui_warn()    { printf "%s!%s %s\n" "$C_YELLOW" "$C_RESET" "$1"; }
ui_error()   { printf "%s✗ %s%s\n" "$C_RED" "$1" "$C_RESET" >&2; }

# Banner de boas-vindas
ui_banner() {
  printf "\n%s%s" "$C_BOLD" "$C_CYAN"
  printf "  ╔══════════════════════════════════════════╗\n"
  printf "  ║          %-32s║\n" "${1:-InfiniteOS}"
  printf "  ║   Seu sistema de agentes, replicável     ║\n"
  printf "  ╚══════════════════════════════════════════╝%s\n\n" "$C_RESET"
}

# --- Perguntas --------------------------------------------------------------
# ui_yesno "Pergunta?" [default: Y|N]  -> retorna 0 (sim) ou 1 (não)
# Enter sozinho usa o default. Aceita s/sim/y/yes e n/nao/no.
ui_yesno() {
  local prompt="$1" default="${2:-Y}" hint reply
  if [ "$default" = "Y" ]; then hint="[S/n]"; else hint="[s/N]"; fi
  while true; do
    printf "%s? %s%s %s " "$C_BOLD" "$prompt" "$C_RESET" "$hint"
    read -r reply </dev/tty || reply=""
    reply="$(printf '%s' "$reply" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
    [ -z "$reply" ] && { [ "$default" = "Y" ] && return 0 || return 1; }
    case "$reply" in
      s|sim|y|yes) return 0 ;;
      n|nao|não|no) return 1 ;;
      *) ui_warn "Responda 's' (sim) ou 'n' (não)." ;;
    esac
  done
}

# ui_ask "Pergunta?" "valor_default"  -> ecoa a resposta (ou o default)
ui_ask() {
  local prompt="$1" default="${2:-}" reply
  if [ -n "$default" ]; then
    printf "%s? %s%s [%s]: " "$C_BOLD" "$prompt" "$C_RESET" "$default" >&2
  else
    printf "%s? %s%s: " "$C_BOLD" "$prompt" "$C_RESET" >&2
  fi
  read -r reply </dev/tty || reply=""
  [ -z "$reply" ] && reply="$default"
  printf '%s' "$reply"
}

# ui_choice "Pergunta?" "opt1" "opt2" ...  -> ecoa o índice escolhido (1-based)
ui_choice() {
  local prompt="$1"; shift
  local opts=("$@") i reply
  printf "%s? %s%s\n" "$C_BOLD" "$prompt" "$C_RESET" >&2
  for i in "${!opts[@]}"; do
    printf "    %s%d)%s %s\n" "$C_CYAN" "$((i+1))" "$C_RESET" "${opts[$i]}" >&2
  done
  while true; do
    printf "  Escolha [1-%d]: " "${#opts[@]}" >&2
    read -r reply </dev/tty || reply=""
    if printf '%s' "$reply" | grep -Eq '^[0-9]+$' && [ "$reply" -ge 1 ] && [ "$reply" -le "${#opts[@]}" ]; then
      printf '%s' "$reply"; return 0
    fi
    ui_warn "Digite um número entre 1 e ${#opts[@]}."
  done
}
