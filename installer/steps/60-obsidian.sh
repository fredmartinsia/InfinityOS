#!/usr/bin/env bash
# ============================================================================
#  Passo 60 — Obsidian + RAG (entregue 100% pronto)
#  - Detecta/instala o Obsidian
#  - Cria/seleciona o vault
#  - Estrutura de pastas GUIADA por perfil + módulos opcionais
#  - REGRAS + GUIA + README/INDEX dinâmico (reflete as pastas escolhidas)
#  - Constrói o índice RAG agora (não no 1º prompt)
# ============================================================================
ui_header "9/11 · Obsidian + RAG"

# Robustez: se rodado isolado (--step=60), o passo 00 não setou OS_KIND.
if [ -z "${OS_KIND:-}" ]; then
  case "$(uname -s)" in
    Darwin) OS_KIND=macos ;;
    Linux)  OS_KIND=linux ;;
    *)      OS_KIND=desconhecido ;;
  esac
fi

VP="${VAULT_PATH:-$DEFAULT_VAULT_PATH}"

# --- Descrição de cada pasta (para o README dinâmico) -----------------------
describe_folder() {
  case "$1" in
    SQUADS)     echo "Squads multi-agente (orquestração)";;
    CLONES)     echo "Clones de especialistas";;
    _META)      echo "Índices, dashboards e MOCs";;
    Templates)  echo "Modelos reutilizáveis de nota";;
    Projetos)   echo "Seus projetos";;
    Clientes)   echo "Seus clientes / contas";;
    Pessoal)    echo "Notas pessoais";;
    "Diário")   echo "Notas do dia a dia";;
    "Finanças") echo "Controle financeiro";;
    Estudos)    echo "Estudos e aprendizados";;
    "Conteúdo") echo "Pauta e produção de conteúdo";;
    "Calendário") echo "Planejamento temporal";;
    "Negócios") echo "Seus negócios / empresas";;
    "Código")   echo "Snippets e notas técnicas";;
    *)          echo "Pasta do vault";;
  esac
}

# --- 1) Detecta Obsidian ----------------------------------------------------
obsidian_installed=0
if [ "$OS_KIND" = "macos" ] && [ -d "/Applications/Obsidian.app" ]; then obsidian_installed=1; fi
command -v obsidian >/dev/null 2>&1 && obsidian_installed=1
flatpak list 2>/dev/null | grep -qi obsidian && obsidian_installed=1

if [ "$obsidian_installed" = "1" ]; then
  ui_ok "Obsidian encontrado."
else
  ui_step "Obsidian não encontrado."
  if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Posso instalar o Obsidian agora?" "Y"; then
    case "$OS_KIND" in
      macos) log_run brew install --cask obsidian && ui_ok "Obsidian instalado." || ui_warn "Instale manualmente: obsidian.md/download" ;;
      linux|wsl) log_run flatpak install -y flathub md.obsidian.Obsidian || ui_warn "Instale manualmente: obsidian.md/download" ;;
      *) ui_warn "Instale o Obsidian manualmente: obsidian.md/download" ;;
    esac
  else
    ui_dim "Seguindo sem instalar o app — vou preparar a pasta do vault mesmo assim."
  fi
fi

# --- 2) Pasta do vault ------------------------------------------------------
if [ -d "$VP/.obsidian" ]; then
  ui_ok "Vault existente reaproveitado: $VP (não destruo nada)."
elif [ -d "$VP" ]; then
  ui_info "Pasta existe mas sem .obsidian — será inicializada ao abrir o Obsidian."
else
  mkdir -p "$VP"
  ui_ok "Vault criado em: $VP"
fi
mkdir -p "$VP/.obsidian"
[ -f "$VP/.obsidian/app.json" ] || printf '{\n  "alwaysUpdateLinks": true\n}\n' > "$VP/.obsidian/app.json"

# --- 3) Estrutura de pastas GUIADA ------------------------------------------
FOLDERS=(SQUADS CLONES _META Templates Projetos)   # base sempre presente

add_folder() {  # evita duplicatas
  for x in "${FOLDERS[@]}"; do [ "$x" = "$1" ] && return 0; done
  FOLDERS+=("$1")
}

# Vault que já existe e já tem conteúdo: NÃO montar estrutura por cima.
# Criar pasta nova num vault já bagunçado só aumenta a bagunça. Quem já tem
# conteúdo é atendido pela skill de reorganização, que olha o que existe antes
# de propor qualquer mudança.
SKIP_STRUCTURE=0
if [ "${INSTALL_MODE:-fresh}" = "upgrade" ]; then
  notas_existentes=$(find "$VP" -name "*.md" -not -path "*/.obsidian/*" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${notas_existentes:-0}" -gt 10 ]; then
    SKIP_STRUCTURE=1
    echo
    ui_ok "Seu vault já tem $notas_existentes notas. Não vou criar pasta nenhuma por cima."
    ui_info "Mexer na estrutura de um vault que já está em uso é justamente o que"
    ui_info "costuma bagunçar tudo. Isso é trabalho para a próxima etapa."
    ui_dim "Depois da instalação, abra o Claude Code e rode:  /organizar-vault"
    ui_dim "Ela mostra o retrato do que está desorganizado, propõe a arrumação,"
    ui_dim "faz backup e só move depois que você confirmar. Nada é apagado."
    # garante apenas as pastas que o sistema precisa para funcionar
    for d in SQUADS CLONES; do
      [ -d "$VP/$d" ] || { mkdir -p "$VP/$d"; ui_dim "  criei só a pasta $d, que o sistema precisa"; }
    done
  fi
fi

if [ "$SKIP_STRUCTURE" = "0" ] && [ "${ASSUME_YES:-0}" != "1" ]; then
  ui_info "Vamos montar a estrutura do seu vault. Escolha um perfil de base:"
  preset="$(ui_choice "Qual perfil combina mais com você?" \
    "Prestador de serviço / Agência" \
    "Criador de conteúdo" \
    "Empreendedor / Holding" \
    "Uso pessoal" \
    "Desenvolvedor" \
    "Só o básico")"
  case "$preset" in
    1) add_folder "Clientes" ;;
    2) add_folder "Conteúdo"; add_folder "Calendário" ;;
    3) add_folder "Negócios" ;;
    4) add_folder "Pessoal"; add_folder "Diário" ;;
    5) add_folder "Código" ;;
    6) : ;;
  esac

  ui_info "Quer adicionar mais alguma pasta? (Enter pula)"
  for extra in Clientes Pessoal "Diário" "Finanças" Estudos; do
    already=0; for x in "${FOLDERS[@]}"; do [ "$x" = "$extra" ] && already=1; done
    [ "$already" = "1" ] && continue
    if ui_yesno "Adicionar pasta '$extra'?" "N"; then add_folder "$extra"; fi
  done

  if ui_yesno "Quer adicionar alguma pasta personalizada (nome livre)?" "N"; then
    custom="$(ui_ask "Nome da pasta (vazio p/ encerrar)" "")"
    while [ -n "$custom" ]; do
      add_folder "$custom"
      custom="$(ui_ask "Outra pasta? (vazio p/ encerrar)" "")"
    done
  fi
fi

# Cria as pastas escolhidas
if [ "$SKIP_STRUCTURE" = "0" ]; then
  for d in "${FOLDERS[@]}"; do mkdir -p "$VP/$d"; done
  ui_ok "Estrutura criada: ${FOLDERS[*]}"
  log "obsidian: folders=${FOLDERS[*]}"
else
  log "obsidian: estrutura preservada (vault em uso, upgrade)"
fi

# --- 4) REGRAS + GUIA -------------------------------------------------------
VPX="$VP" python3 - "$INFINITY_OS_ROOT/vault-template/📋 REGRAS DO VAULT.template.md" "$VP/📋 REGRAS DO VAULT.md" <<'PY'
import os, sys, io
src, dst = sys.argv[1], sys.argv[2]
if not os.path.exists(dst):
    s = io.open(src, encoding="utf-8").read().replace("{{VAULT_PATH}}", os.environ["VPX"])
    io.open(dst, "w", encoding="utf-8").write(s)
PY
ui_ok "REGRAS DO VAULT instaladas."

# --- 5) README/INDEX dinâmico (reflete as pastas escolhidas) ----------------
INDEX_FILE="$VP/📊 INDEX - VAULT PRINCIPAL.md"

if [ "$SKIP_STRUCTURE" = "1" ]; then
  # vault em uso: não temos perfil escolhido, e reescrever o índice apagaria
  # o que a pessoa organizou. Quem cuida disso é a skill de reorganização.
  ui_dim "Índice do vault não foi tocado (seu vault já está em uso)."
else
  # se já existe um índice editado, guarda a versão da pessoa em vez de perder
  if [ -f "$INDEX_FILE" ]; then
    cp "$INDEX_FILE" "$INDEX_FILE.seu" 2>/dev/null && \
      ui_info "Seu índice anterior foi guardado como 📊 INDEX - VAULT PRINCIPAL.md.seu"
  fi
  {
    echo "# 📊 INDEX · Vault Principal"
    echo
    echo "> Gerado pelo infinity-os em $(date '+%Y-%m-%d'). Estrutura sob medida para o seu perfil."
    echo
    echo "## Pastas"
    echo
    for d in "${FOLDERS[@]}"; do
      echo "- **$d/**: $(describe_folder "$d")"
    done
    echo
    echo "## Como usar"
    echo
    echo "- Squads: \`/<nome-do-squad>\` no Claude Code (ex.: \`/hormozi-squad\`)."
    echo "- Clones: estão em \`CLONES/\` e são carregados pelos squads/skills."
    echo "- O RAG injeta automaticamente o contexto relevante deste vault a cada prompt."
    echo
    echo "_Veja as regras em \`📋 REGRAS DO VAULT.md\`._"
  } > "$INDEX_FILE"
  ui_ok "README/INDEX dinâmico gerado (descreve exatamente as suas pastas)."
fi

# --- 6) Índice RAG construído AGORA -----------------------------------------
if [ -f "$CLAUDE_HOME/scripts/vault_rag.py" ]; then
  if CLAUDE_VAULT_PATH="$VP" python3 "$CLAUDE_HOME/scripts/vault_rag.py" --reindex; then
    ui_ok "Índice RAG construído — pronto já na 1ª sessão."
  else
    ui_warn "Não consegui pré-indexar agora; o RAG indexa no 1º prompt."
  fi
else
  ui_dim "vault_rag.py ainda não instalado neste ambiente (rode o passo 30 antes)."
fi

ui_dim "Pesos do RAG por pasta (Clientes>Projetos>...) só se aplicam às pastas que existem."
