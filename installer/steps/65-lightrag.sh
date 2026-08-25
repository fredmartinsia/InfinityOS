#!/usr/bin/env bash
# ============================================================================
#  Passo 65: LightRAG, a camada de memória do sistema.
#
#  O LightRAG lê as notas do seu vault Obsidian e monta um índice de grafo
#  (entidades e relações entre elas) mais um índice vetorial (busca por
#  significado, não só por palavra exata). É essa memória que os agentes
#  consultam pra lembrar do seu negócio sem reler tudo a cada prompt.
#
#  Ordem: detecta o que já existe (não reinstala à toa), confere pré-requisito
#  por pré-requisito com explicação simples, instala só o que falta, e no fim
#  oferece rodar a primeira indexação. Se algo faltar ou falhar, o passo avisa
#  e devolve o controle: o resto do harness funciona sem o LightRAG.
# ============================================================================

ui_header "10/11 · Memória de longo prazo (LightRAG)"

if [ "${INFINITY_OS_SKIP_LIGHTRAG:-0}" = "1" ]; then
  ui_dim "Passo do LightRAG pulado (INFINITY_OS_SKIP_LIGHTRAG=1)."
  return 0 2>/dev/null || true
fi

# Robustez: se rodado isolado (--step=65), passos anteriores podem não ter rodado.
if [ -z "${OS_KIND:-}" ]; then
  case "$(uname -s)" in
    Darwin) OS_KIND=macos ;;
    Linux)  OS_KIND=linux ;;
    *)      OS_KIND=desconhecido ;;
  esac
fi

ui_info "O LightRAG é a memória de longo prazo do sistema: ele lê as notas do seu"
ui_info "vault e monta um grafo mais um índice vetorial (busca por significado)."

# Mesmo nome de variável que o passo 05 (detecção) já usa pra achar o LightRAG.
LR_HOME="${LIGHTRAG_HOME:-$HOME/lightrag-workspace}"
LR_VENV="$LR_HOME/.venv"
LR_HOST="127.0.0.1"
LR_PORT="9621"   # fixo: é a porta que claude/scripts/vault_rag.py e ingest_gate.py já esperam
LR_VAULT="${VAULT_PATH:-$DEFAULT_VAULT_PATH}"
CONFIG_ROOT="$HOME/.config"

# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------

# lê uma variável salva em ~/.config/<slug>/env (mesmo formato do passo 25)
read_config_key() {
  local slug="$1" var="$2" file="$CONFIG_ROOT/$slug/env"
  [ -f "$file" ] || { printf ''; return 0; }
  grep "^export ${var}=" "$file" 2>/dev/null | tail -1 | cut -d'"' -f2
}

# testa se o servidor responde de verdade (HTTP real, timeout curto)
lr_server_alive() {
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 \
         "http://${LR_HOST}:${LR_PORT}/health" 2>/dev/null)
  [ "$code" = "200" ]
}

# dispara a leitura do vault (endpoint oficial /documents/scan, processa em segundo plano)
lr_trigger_scan() {
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST --max-time 10 \
         "http://${LR_HOST}:${LR_PORT}/documents/scan" 2>/dev/null)
  case "$code" in 2??) return 0 ;; *) return 1 ;; esac
}

# ---------------------------------------------------------------------------
# 1) Detecção primeiro: já está tudo funcionando?
# ---------------------------------------------------------------------------
lr_workspace_ok=0; lr_pkg_ok=0; lr_server_ok=0
[ -d "$LR_HOME" ] && lr_workspace_ok=1
if [ -x "$LR_VENV/bin/python3" ] && "$LR_VENV/bin/python3" -c "import lightrag" >/dev/null 2>&1; then
  lr_pkg_ok=1
fi
lr_server_alive && lr_server_ok=1

if [ "$lr_workspace_ok" = 1 ] && [ "$lr_pkg_ok" = 1 ] && [ "$lr_server_ok" = 1 ]; then
  ui_ok "O LightRAG já está instalado e o servidor está no ar em http://${LR_HOST}:${LR_PORT}."
  ui_dim "Workspace: $LR_HOME"
  log "lightrag: ja instalado e rodando (workspace=$LR_HOME porta=$LR_PORT)"
  if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Quer reindexar o vault agora (relê tudo e atualiza a memória)?" "N"; then
    if lr_trigger_scan; then
      ui_ok "Reindexação disparada, roda em segundo plano no servidor."
      ui_dim "Acompanhe com: curl http://${LR_HOST}:${LR_PORT}/documents/pipeline_status"
    else
      ui_warn "Não consegui disparar a reindexação agora."
      ui_dim "Rode depois: curl -X POST http://${LR_HOST}:${LR_PORT}/documents/scan"
    fi
  else
    ui_dim "Sem reindexar agora. Pra rodar depois:"
    ui_dim "  curl -X POST http://${LR_HOST}:${LR_PORT}/documents/scan"
  fi
  ui_ok "Passo do LightRAG concluído."
  return 0 2>/dev/null || true
fi

ui_dim "Não achei uma instalação completa e funcionando. Vamos checar o que falta."

# ---------------------------------------------------------------------------
# 2) Pré-requisitos, um a um
# ---------------------------------------------------------------------------
ui_step "Pré-requisitos"

# a) Python 3.10+ com venv (venv = uma pasta isolada com o Python do projeto,
#    pra não bagunçar o Python do sistema)
LR_PY="$(command -v python3 || true)"
py_ok=0
if [ -n "$LR_PY" ] && "$LR_PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  py_ok=1
fi
if [ "$py_ok" = 1 ] && "$LR_PY" -c "import venv" >/dev/null 2>&1; then
  ui_ok "Python $("$LR_PY" --version 2>&1 | awk '{print $2}') encontrado, com venv."
else
  ui_warn "Preciso de Python 3.10 ou mais novo, com o módulo venv."
  ui_dim "macOS: brew install python@3.12"
  ui_dim "Linux (Debian/Ubuntu): sudo apt install python3.12 python3.12-venv"
  ui_warn "Pulando o LightRAG por enquanto. O resto do harness funciona sem ele."
  log "lightrag: abortado, python insuficiente"
  return 0 2>/dev/null || true
fi

# b) Ollama instalado, no ar, e com o modelo de embedding baixado
#    (embedding = o motor que transforma texto em vetores de significado,
#    pra achar notas parecidas mesmo sem a palavra exata)
if ! command -v ollama >/dev/null 2>&1; then
  ui_warn "Ollama não encontrado (é ele que roda o modelo de embedding, localmente)."
  if [ "$OS_KIND" = "macos" ]; then
    ui_dim "Instale com: brew install --cask ollama   (ou em https://ollama.com/download)"
  else
    ui_dim "Instale com: curl -fsSL https://ollama.com/install.sh | sh"
  fi
  ui_warn "Pulando o LightRAG por enquanto. Rode de novo depois de instalar o Ollama."
  log "lightrag: abortado, ollama ausente"
  return 0 2>/dev/null || true
fi
ui_ok "Ollama encontrado."

OLLAMA_URL="${OLLAMA_HOST:-http://localhost:11434}"
if ! curl -s --max-time 3 "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
  ui_warn "O Ollama está instalado, mas o servidor dele não está no ar."
  if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Posso tentar abrir o Ollama agora?" "Y"; then
    if [ "$OS_KIND" = "macos" ] && command -v open >/dev/null 2>&1; then
      open -a Ollama >/dev/null 2>&1 || nohup ollama serve >/dev/null 2>&1 &
    else
      nohup ollama serve >/dev/null 2>&1 &
    fi
    sleep 3
  fi
  if ! curl -s --max-time 3 "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
    ui_warn "Ainda não consegui falar com o Ollama."
    ui_dim "Abra-o manualmente e rode este passo de novo: ./install.sh --step=65"
    log "lightrag: abortado, ollama nao respondeu"
    return 0 2>/dev/null || true
  fi
fi
ui_ok "Ollama está no ar."

lr_has_bge=0
if curl -s --max-time 5 "$OLLAMA_URL/api/tags" 2>/dev/null | grep -q '"name":"bge-m3'; then
  lr_has_bge=1
fi
if [ "$lr_has_bge" = 0 ]; then
  ui_warn "O modelo de embedding 'bge-m3' ainda não está baixado (download de cerca de 1,2 GB)."
  do_pull=0
  if [ "${ASSUME_YES:-0}" = "1" ]; then
    do_pull=1
  elif ui_yesno "Baixar o bge-m3 agora (cerca de 1,2 GB)?" "Y"; then
    do_pull=1
  fi
  if [ "$do_pull" = 1 ]; then
    ui_dim "Baixando bge-m3, pode levar alguns minutos, depende da sua internet..."
    if log_run ollama pull bge-m3; then
      ui_ok "bge-m3 pronto."
      lr_has_bge=1
    else
      ui_warn "Falha ao baixar o bge-m3 (veja o log: $INSTALL_LOG)."
    fi
  fi
fi
if [ "$lr_has_bge" = 0 ]; then
  ui_warn "Sem o bge-m3, o LightRAG não consegue indexar. Pulando por enquanto."
  ui_dim "Rode depois: ollama pull bge-m3   e então ./install.sh --step=65"
  log "lightrag: abortado, bge-m3 ausente"
  return 0 2>/dev/null || true
fi

# c) chave de API pro LLM de indexação (o modelo que lê o texto e extrai
#    entidades/relações pro grafo; reaproveita o que o passo 25 já configurou)
lr_provider=""; lr_key=""
nvidia_key="${NVIDIA_API_KEY:-$(read_config_key nvidia NVIDIA_API_KEY)}"
openrouter_key="${OPENROUTER_API_KEY:-$(read_config_key openrouter OPENROUTER_API_KEY)}"

if [ -n "$nvidia_key" ]; then
  lr_provider="nvidia"; lr_key="$nvidia_key"
  ui_ok "Vou usar a chave da NVIDIA NIM (já configurada no passo de credenciais) pra indexar."
elif [ -n "$openrouter_key" ]; then
  lr_provider="openrouter"; lr_key="$openrouter_key"
  ui_ok "Vou usar a chave do OpenRouter (já configurada no passo de credenciais) pra indexar."
else
  ui_warn "Nenhuma chave de API pronta pra extrair entidades do texto (NVIDIA ou OpenRouter)."
  ui_dim "Rode primeiro o passo de credenciais: ./install.sh --step=25"
  ui_dim "As chaves ficam em ~/.config, nunca entram no repositório."
  if [ "${ASSUME_YES:-0}" = "1" ] || ui_yesno "Quer pular o LightRAG por agora e configurar a chave depois?" "Y"; then
    ui_dim "Sem problema. Depois: ./install.sh --step=25   e então ./install.sh --step=65"
    log "lightrag: abortado, sem chave de API"
    return 0 2>/dev/null || true
  fi
  ui_warn "Seguindo sem chave: o pacote instala, mas indexar vai falhar até você configurar uma."
fi

# d) Postgres é OPCIONAL. Sem ele, o LightRAG guarda tudo em arquivo no próprio
#    workspace, o que já funciona bem. Só usamos Postgres se já estiver rodando
#    e a pessoa topar.
lr_use_pg=0
if command -v pg_isready >/dev/null 2>&1 && pg_isready -q >/dev/null 2>&1; then
  ui_info "Encontrei um Postgres rodando neste computador (opcional, ajuda em vaults grandes)."
  if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Quer usar o Postgres pro armazenamento do LightRAG?" "N"; then
    pg_user="${USER:-$(id -un 2>/dev/null || echo postgres)}"
    if command -v createdb >/dev/null 2>&1 && createdb lightrag >/dev/null 2>&1; then
      ui_ok "Banco 'lightrag' pronto."
      lr_use_pg=1
    elif command -v psql >/dev/null 2>&1 && psql -lqt 2>/dev/null | cut -d'|' -f1 | tr -d ' ' | grep -qx lightrag; then
      ui_ok "Banco 'lightrag' já existia, vou usar ele."
      lr_use_pg=1
    else
      ui_warn "Não consegui preparar o banco Postgres. Seguindo com armazenamento em arquivo."
    fi
  fi
fi
[ "$lr_use_pg" = 0 ] && ui_dim "Armazenamento: em arquivo, dentro do workspace (mais simples, sem Postgres)."

# ---------------------------------------------------------------------------
# 3) Instalação, só do que falta, sempre idempotente
# ---------------------------------------------------------------------------
ui_step "Instalando"

mkdir -p "$LR_HOME"

if [ ! -x "$LR_VENV/bin/python3" ]; then
  ui_dim "Criando o venv (pasta isolada com o Python só deste projeto) em $LR_VENV..."
  if ! log_run "$LR_PY" -m venv "$LR_VENV"; then
    ui_error "Não consegui criar o venv. Veja o log: $INSTALL_LOG"
    ui_warn "Pulando o LightRAG. O resto do harness segue funcionando sem ele."
    log "lightrag: abortado, falha ao criar venv"
    return 0 2>/dev/null || true
  fi
fi
[ -x "$LR_VENV/bin/pip" ] || log_run "$LR_VENV/bin/python3" -m ensurepip --upgrade

ui_dim "Instalando o pacote lightrag-hku (biblioteca do LightRAG), pode levar um minuto..."
log_run "$LR_VENV/bin/pip" install --upgrade pip -q
if ! log_run "$LR_VENV/bin/pip" install -q "lightrag-hku[api,offline-llm,offline-storage]"; then
  ui_error "Falha ao instalar o lightrag-hku. Veja o log: $INSTALL_LOG"
  ui_warn "O restante do harness segue funcionando sem o LightRAG."
  log "lightrag: abortado, falha no pip install"
  return 0 2>/dev/null || true
fi
ui_ok "Pacote lightrag-hku instalado em $LR_VENV."

# requirements.txt (pra reinstalar depois sem precisar deste passo)
cat > "$LR_HOME/requirements.txt" <<'EOF'
# Gerado pelo instalador do InfinityOS (installer/steps/65-lightrag.sh).
# Reinstale com: .venv/bin/pip install -r requirements.txt
lightrag-hku[api,offline-llm,offline-storage]
EOF

# .env: variáveis de configuração. NUNCA entra no repositório, fica só aqui,
# com permissão 600 (só o seu usuário lê).
if [ "$lr_use_pg" = 1 ]; then
  kv_storage="PGKVStorage"; vec_storage="PGVectorStorage"; doc_storage="PGDocStatusStorage"
else
  kv_storage="JsonKVStorage"; vec_storage="NanoVectorDBStorage"; doc_storage="JsonDocStatusStorage"
fi

case "$lr_provider" in
  nvidia)
    llm_host="https://integrate.api.nvidia.com/v1"
    llm_model="meta/llama-3.3-70b-instruct"
    ;;
  openrouter)
    llm_host="https://openrouter.ai/api/v1"
    llm_model="meta-llama/llama-3.3-70b-instruct:free"
    ;;
  *)
    # sem chave configurada ainda: deixa o padrão NVIDIA pronto pra quando a
    # pessoa configurar uma chave (o passo 25 grava em ~/.config/nvidia/env)
    llm_host="https://integrate.api.nvidia.com/v1"
    llm_model="meta/llama-3.3-70b-instruct"
    ;;
esac

lr_env_file="$LR_HOME/.env"
{
  printf '# Gerado pelo instalador do InfinityOS em %s. Nunca commite este arquivo.\n' "$(date '+%Y-%m-%d %H:%M')"
  printf 'HOST=%s\n' "$LR_HOST"
  printf 'PORT=%s\n' "$LR_PORT"
  printf 'WORKING_DIR=./rag_storage\n'
  printf 'INPUT_DIR=%s\n' "$LR_VAULT"
  printf 'WORKSPACE=vault\n'
  printf '\n'
  printf 'LLM_BINDING=openai\n'
  printf 'LLM_MODEL=%s\n' "$llm_model"
  printf 'LLM_BINDING_HOST=%s\n' "$llm_host"
  printf 'LLM_BINDING_API_KEY=%s\n' "$lr_key"
  printf '\n'
  printf 'EMBEDDING_BINDING=ollama\n'
  printf 'EMBEDDING_MODEL=bge-m3\n'
  printf 'EMBEDDING_DIM=1024\n'
  printf 'EMBEDDING_BINDING_HOST=%s\n' "$OLLAMA_URL"
  printf '\n'
  printf 'LIGHTRAG_KV_STORAGE=%s\n' "$kv_storage"
  printf 'LIGHTRAG_VECTOR_STORAGE=%s\n' "$vec_storage"
  printf 'LIGHTRAG_GRAPH_STORAGE=NetworkXStorage\n'
  printf 'LIGHTRAG_DOC_STATUS_STORAGE=%s\n' "$doc_storage"
  if [ "$lr_use_pg" = 1 ]; then
    printf '\n'
    printf 'POSTGRES_HOST=localhost\n'
    printf 'POSTGRES_PORT=5432\n'
    printf 'POSTGRES_USER=%s\n' "${pg_user:-$USER}"
    printf 'POSTGRES_PASSWORD=\n'
    printf 'POSTGRES_DATABASE=lightrag\n'
  fi
} > "$lr_env_file"
chmod 600 "$lr_env_file"
ui_ok "Arquivo .env criado em $lr_env_file (permissão 600, nunca vai pro repositório)."

# scripts de subir/parar o servidor
cat > "$LR_HOME/start_server.sh" <<'EOF'
#!/usr/bin/env bash
# Sobe o servidor LightRAG (API REST em http://127.0.0.1:9621) lendo o .env
# deste diretório. Roda em segundo plano; pare com ./stop_server.sh.
cd "$(dirname "$0")" || exit 1
mkdir -p logs
nohup .venv/bin/lightrag-server >> logs/lightrag.log 2>&1 &
echo $! > .server.pid
echo "LightRAG subindo (PID $(cat .server.pid)). Log em logs/lightrag.log"
EOF
chmod +x "$LR_HOME/start_server.sh"

cat > "$LR_HOME/stop_server.sh" <<'EOF'
#!/usr/bin/env bash
# Para o servidor LightRAG iniciado por start_server.sh.
cd "$(dirname "$0")" || exit 1
if [ -f .server.pid ] && kill "$(cat .server.pid)" 2>/dev/null; then
  echo "LightRAG parado."
  rm -f .server.pid
else
  echo "Não achei um processo rodando (talvez já estivesse parado)."
fi
EOF
chmod +x "$LR_HOME/stop_server.sh"

# README explicando como usar
cat > "$LR_HOME/README.md" <<EOF
# LightRAG deste computador

Memória de longo prazo do InfinityOS: um índice de grafo mais vetor, montado
em cima das notas do seu vault Obsidian, pra qualquer agente achar contexto
relevante sem reler tudo.

## Subir o servidor

    ./start_server.sh

Sobe em segundo plano em http://127.0.0.1:${LR_PORT}. Log em logs/lightrag.log.

## Parar o servidor

    ./stop_server.sh

## Ver se está no ar

    curl http://127.0.0.1:${LR_PORT}/health

## Indexar (ou reindexar) o vault

Com o servidor no ar:

    curl -X POST http://127.0.0.1:${LR_PORT}/documents/scan

Isso lê a pasta configurada em INPUT_DIR (o seu vault) e processa em segundo
plano. Pra acompanhar o progresso:

    curl http://127.0.0.1:${LR_PORT}/documents/pipeline_status

## Onde fica cada coisa

- .env: configuração (chaves, modelos, portas). Nunca vai pro repositório.
- .venv/: o Python isolado deste projeto (não mexe no Python do sistema).
- rag_storage/: o índice em si (grafo mais vetores).
- requirements.txt: reinstale com .venv/bin/pip install -r requirements.txt

## Reinstalar do zero

Apague .venv/ e rag_storage/ e rode de novo:

    ./install.sh --step=65
EOF
ui_ok "README.md e scripts de subir/parar gerados em $LR_HOME."

log "lightrag: instalado workspace=$LR_HOME pg=$lr_use_pg provider=${lr_provider:-nenhum}"

# sobe o servidor (idempotente: se já está no ar, não faz nada)
if lr_server_alive; then
  ui_ok "Servidor já está no ar."
else
  ui_dim "Subindo o servidor..."
  ( bash "$LR_HOME/start_server.sh" >/dev/null 2>&1 )
  tries=0
  until lr_server_alive || [ "$tries" -ge 20 ]; do
    sleep 1
    tries=$((tries + 1))
  done
  if lr_server_alive; then
    ui_ok "Servidor no ar em http://${LR_HOST}:${LR_PORT}."
  else
    ui_warn "O servidor não respondeu a tempo. Veja $LR_HOME/logs/lightrag.log."
    ui_dim "Tente de novo com: $LR_HOME/start_server.sh"
  fi
fi

# ---------------------------------------------------------------------------
# 4) Primeira indexação (opcional, perguntada)
# ---------------------------------------------------------------------------
if lr_server_alive; then
  echo
  ui_step "Primeira indexação"
  ui_info "Isso lê as notas do seu vault e monta o índice. Pode demorar (de minutos"
  ui_info "a horas, dependendo do tamanho do vault) e consome cota da API de indexação."
  do_index=0
  if [ "${ASSUME_YES:-0}" = "1" ]; then
    ui_dim "Modo não interativo: a indexação não começa sozinha."
  elif ui_yesno "Quer indexar o vault agora?" "N"; then
    do_index=1
  fi
  if [ "$do_index" = 1 ]; then
    if lr_trigger_scan; then
      ui_ok "Indexação disparada, roda em segundo plano no servidor."
      ui_dim "Acompanhe com: curl http://${LR_HOST}:${LR_PORT}/documents/pipeline_status"
    else
      ui_warn "Não consegui disparar a indexação agora."
      ui_dim "Rode depois: curl -X POST http://${LR_HOST}:${LR_PORT}/documents/scan"
    fi
  else
    ui_dim "Sem indexar agora. Quando quiser:"
    ui_dim "  curl -X POST http://${LR_HOST}:${LR_PORT}/documents/scan"
  fi
fi

ui_ok "Passo do LightRAG concluído."
return 0 2>/dev/null || true
