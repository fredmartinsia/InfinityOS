#!/usr/bin/env bash
# ============================================================================
#  Passo 25: chaves de API dos provedores de modelo.
#
#  Para cada provedor: detecta se você já tem, e se não tiver, abre a página de
#  cadastro no seu navegador, espera você colar a chave, TESTA a chave contra a
#  API de verdade e só então grava.
#
#  As chaves NUNCA entram no repositório. Vão para ~/.config/<provedor>/env,
#  com permissão de leitura exclusiva do seu usuário (chmod 600), e o seu perfil
#  de shell passa a carregar esses arquivos.
#
#  Todos os provedores são opcionais. O harness funciona só com o Claude Code.
# ============================================================================

ui_header "5/11 · Chaves de API dos provedores"

if [ "${INFINITY_OS_SKIP_CREDS:-0}" = "1" ]; then
  ui_dim "Passo de chaves pulado (INFINITY_OS_SKIP_CREDS=1)."
  return 0 2>/dev/null || true
fi

CONFIG_ROOT="$HOME/.config"
CRED_SUMMARY=()

# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------

# abre uma URL no navegador padrão, sem quebrar se não houver navegador
open_url() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then
    open "$url" >/dev/null 2>&1 && return 0
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 && return 0
  fi
  return 1
}

# lê uma chave sem ecoar na tela
read_secret() {
  local prompt="$1" __out="$2" value=""
  printf "  %s" "$prompt"
  read -r -s value < /dev/tty
  printf "\n"
  printf -v "$__out" '%s' "$value"
}

# grava a chave em ~/.config/<slug>/env com permissão restrita
save_key() {
  local slug="$1" var="$2" value="$3"
  local dir="$CONFIG_ROOT/$slug" file="$CONFIG_ROOT/$slug/env"
  mkdir -p "$dir"
  chmod 700 "$dir"
  # preserva outras variáveis já presentes no arquivo
  if [ -f "$file" ] && grep -q "^export ${var}=" "$file" 2>/dev/null; then
    local tmp; tmp="$(mktemp)"
    grep -v "^export ${var}=" "$file" > "$tmp" 2>/dev/null || true
    mv "$tmp" "$file"
  fi
  printf 'export %s="%s"\n' "$var" "$value" >> "$file"
  chmod 600 "$file"
}

# garante que o perfil de shell carrega o arquivo de credencial
wire_profile() {
  local slug="$1"
  local line="[ -f \"\$HOME/.config/$slug/env\" ] && source \"\$HOME/.config/$slug/env\""
  local profile=""
  case "${SHELL##*/}" in
    zsh)  profile="$HOME/.zshrc" ;;
    bash) profile="$HOME/.bashrc" ;;
    *)    profile="$HOME/.profile" ;;
  esac
  touch "$profile"
  if ! grep -qF ".config/$slug/env" "$profile" 2>/dev/null; then
    {
      printf '\n# InfinityOS: credencial %s\n' "$slug"
      printf '%s\n' "$line"
    } >> "$profile"
  fi
}

# valida a chave contra a API real. Devolve 0 se a chave funciona.
validate_key() {
  local slug="$1" key="$2" code=""
  case "$slug" in
    openrouter)
      code=$(curl -s -o /dev/null -w "%{http_code}" https://openrouter.ai/api/v1/key \
             -H "Authorization: Bearer $key" --max-time 20) ;;
    nvidia)
      code=$(curl -s -o /dev/null -w "%{http_code}" https://integrate.api.nvidia.com/v1/models \
             -H "Authorization: Bearer $key" --max-time 25) ;;
    groq)
      code=$(curl -s -o /dev/null -w "%{http_code}" https://api.groq.com/openai/v1/models \
             -H "Authorization: Bearer $key" --max-time 20) ;;
    xai)
      code=$(curl -s -o /dev/null -w "%{http_code}" https://api.x.ai/v1/models \
             -H "Authorization: Bearer $key" --max-time 20) ;;
    zai)
      code=$(curl -s -o /dev/null -w "%{http_code}" https://api.z.ai/api/anthropic/v1/models \
             -H "x-api-key: $key" -H "anthropic-version: 2023-06-01" --max-time 20) ;;
    gemini)
      code=$(curl -s -o /dev/null -w "%{http_code}" \
             "https://generativelanguage.googleapis.com/v1beta/models?key=$key" --max-time 20) ;;
    *) return 0 ;;
  esac
  [ "$code" = "200" ]
}

# ---------------------------------------------------------------------------
# fluxo de um provedor
#   setup_provider <slug> <VAR> <nome> <url_cadastro> <para_que_serve>
# ---------------------------------------------------------------------------
setup_provider() {
  local slug="$1" var="$2" nome="$3" url="$4" desc="$5"
  local existing="${!var:-}"

  echo
  ui_step "$nome"
  ui_dim "$desc"

  if [ -z "$existing" ] && [ -f "$CONFIG_ROOT/$slug/env" ]; then
    existing=$(grep "^export ${var}=" "$CONFIG_ROOT/$slug/env" 2>/dev/null | tail -1 | cut -d'"' -f2)
  fi

  if [ -n "$existing" ]; then
    if validate_key "$slug" "$existing"; then
      ui_ok "Você já tem esta chave e ela está funcionando."
      wire_profile "$slug"
      CRED_SUMMARY+=("$nome: já configurada")
      return 0
    else
      ui_warn "Existe uma chave gravada, mas ela não respondeu. Vamos trocar."
    fi
  fi

  if ! ui_yesno "Quer configurar $nome agora?" "Y"; then
    ui_dim "Pulado. Dá para configurar depois com: ./install.sh --step=25"
    CRED_SUMMARY+=("$nome: pulado")
    return 0
  fi

  if ui_yesno "Você já tem a chave em mãos?" "N"; then
    ui_dim "Ótimo, é só colar abaixo."
  else
    ui_info "Vou abrir a página de cadastro no seu navegador."
    ui_dim "$url"
    if open_url "$url"; then
      ui_ok "Página aberta. Crie a conta, gere a chave e volte aqui."
    else
      ui_warn "Não consegui abrir o navegador. Acesse manualmente:"
      ui_info "$url"
    fi
  fi

  local attempt=1 key=""
  while [ $attempt -le 3 ]; do
    read_secret "Cole a chave (fica invisível ao digitar), ou Enter para pular: " key
    if [ -z "$key" ]; then
      ui_dim "Pulado."
      CRED_SUMMARY+=("$nome: pulado")
      return 0
    fi
    ui_dim "Testando a chave contra a API..."
    if validate_key "$slug" "$key"; then
      save_key "$slug" "$var" "$key"
      wire_profile "$slug"
      export "$var=$key"
      ui_ok "Chave validada e guardada em ~/.config/$slug/env (só o seu usuário lê)."
      CRED_SUMMARY+=("$nome: configurada e testada")
      unset key
      return 0
    fi
    ui_warn "A API recusou essa chave (tentativa $attempt de 3)."
    attempt=$((attempt+1))
  done

  ui_warn "Não deu para validar. Seguindo sem $nome."
  CRED_SUMMARY+=("$nome: falhou na validação")
  unset key
  return 0
}

# ---------------------------------------------------------------------------
# execução
# ---------------------------------------------------------------------------

ui_info "Agora vamos ligar os provedores de modelo. Todos são opcionais."
ui_dim "A chave é testada contra a API antes de ser guardada, e nunca aparece na tela."
ui_dim "Nada disso entra no repositório: fica em ~/.config, só no seu computador."

if [ "${ASSUME_YES:-0}" = "1" ]; then
  ui_dim "Modo não interativo: passo de chaves pulado. Rode ./install.sh --step=25 depois."
  return 0 2>/dev/null || true
fi

setup_provider "openrouter" "OPENROUTER_API_KEY" \
  "OpenRouter" \
  "https://openrouter.ai/settings/keys" \
  "Porta de entrada para centenas de modelos, incluindo uma boa lista de gratuitos. É o mais útil para começar."

setup_provider "nvidia" "NVIDIA_API_KEY" \
  "NVIDIA NIM" \
  "https://build.nvidia.com/explore/discover" \
  "Modelos abertos grandes com cota gratuita generosa. Usado pelo motor de indexação do RAG."

setup_provider "groq" "GROQ_API_KEY" \
  "Groq" \
  "https://console.groq.com/keys" \
  "Inferência muito rápida de modelos abertos. Boa para tarefa mecânica e barata."

setup_provider "zai" "ZAI_API_KEY" \
  "Z.AI (modelos GLM)" \
  "https://z.ai/manage-apikey/apikey-list" \
  "Endpoint compatível com a API da Anthropic, o que permite rodar uma segunda instância do Claude Code por assinatura."

setup_provider "xai" "XAI_API_KEY" \
  "xAI (Grok)" \
  "https://console.x.ai/" \
  "Modelos Grok. Opcional, use se você já tem conta."

setup_provider "gemini" "GEMINI_API_KEY" \
  "Google Gemini" \
  "https://aistudio.google.com/apikey" \
  "Janela de contexto muito grande e camada gratuita. Opcional."

echo
ui_header "Resumo das chaves"
for line in "${CRED_SUMMARY[@]}"; do ui_info "$line"; done
echo
ui_dim "Para valer nesta sessão do terminal, abra um terminal novo ou rode:"
ui_dim "  source ~/.config/openrouter/env   (e o equivalente dos outros)"
ui_ok "Passo de chaves concluído."
