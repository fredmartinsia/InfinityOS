#!/usr/bin/env bash
# ============================================================================
#  Passo 10 — CLIs externas: detecta o que falta e oferece instalar.
#  Uma confirmação por ferramenta. Nunca instala sem o "Sim".
#  Exporta: HAS_OLLAMA (para o passo de modelos locais).
# ============================================================================
ui_header "2/8 — Ferramentas de linha de comando (CLIs)"
if [ "${INFINITE_OS_SKIP_CLIS:-0}" = "1" ]; then
  ui_dim "Passo de CLIs pulado (INFINITE_OS_SKIP_CLIS=1)."
  return 0 2>/dev/null || true
fi
ui_info "Vou checar quais CLIs você já tem. Para cada que faltar, pergunto se posso instalar."
echo

have() { command -v "$1" >/dev/null 2>&1; }

# confirm "Pergunta?" -> 0/1 (respeita modo -y)
confirm() {
  if [ "${ASSUME_YES:-0}" = "1" ]; then return 0; fi
  ui_yesno "$1" "Y"
}

# offer_install <nome> <cli> <desc> <mac_cmd> <linux_cmd>
offer_install() {
  local nome="$1" cli="$2" desc="$3" mac="$4" linux="$5"
  if have "$cli"; then
    ui_ok "$nome já instalado"
    return 0
  fi
  ui_step "$nome — não encontrado. $desc"
  if ! confirm "Posso instalar o $nome agora?"; then
    ui_dim "Pulado. Você pode instalar depois; o roteador usa fallback."
    return 1
  fi
  local cmd=""
  case "$OS_KIND" in
    macos) cmd="$mac" ;;
    linux|wsl) cmd="$linux" ;;
    *) ui_warn "SO não suportado para instalação automática do $nome."; return 1 ;;
  esac
  ui_dim "Executando: $cmd"
  if log_run bash -c "$cmd"; then
    ui_ok "$nome instalado."
    return 0
  else
    ui_warn "Falha ao instalar $nome (veja o log). Siga sem ele por enquanto."
    return 1
  fi
}

# --- gh (GitHub CLI) --------------------------------------------------------
offer_install "GitHub CLI (gh)" "gh" "Para operações de repositório/PR." \
  "brew install gh" \
  "type apt >/dev/null 2>&1 && (sudo apt-get update && sudo apt-get install -y gh) || sudo snap install gh"

# --- Ollama (modelos locais) ------------------------------------------------
HAS_OLLAMA=0
if offer_install "Ollama (modelos locais)" "ollama" "Roda modelos open-source localmente (Qwen, Llama)." \
  "brew install ollama" \
  "curl -fsSL https://ollama.com/install.sh | sh"; then
  HAS_OLLAMA=1
fi
have ollama && HAS_OLLAMA=1
export HAS_OLLAMA

# --- Gemini CLI -------------------------------------------------------------
offer_install "Gemini CLI" "gemini" "Modelo do Google p/ contexto gigante e extração." \
  "npm install -g @google/gemini-cli" \
  "npm install -g @google/gemini-cli"

# --- Qwen-Code CLI ----------------------------------------------------------
offer_install "Qwen-Code CLI" "qwen" "CLI de código do Qwen (raciocínio de código barato)." \
  "npm install -g @qwen-code/qwen-code" \
  "npm install -g @qwen-code/qwen-code"

# --- Codex CLI --------------------------------------------------------------
offer_install "Codex CLI" "codex" "CLI da OpenAI p/ validação cruzada." \
  "npm install -g @openai/codex" \
  "npm install -g @openai/codex"

echo
ui_dim "CLIs ausentes não travam nada — o roteador (routing/route.py) usa fallback até o Claude."
