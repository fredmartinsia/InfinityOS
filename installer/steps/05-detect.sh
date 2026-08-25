#!/usr/bin/env bash
# ============================================================================
#  Passo 05: detecta instalação anterior e decide o modo de instalação.
#
#  Este passo existe por um motivo específico: quem já instalou uma versão
#  antiga tem coisa própria misturada com coisa do pacote. Squad que a pessoa
#  criou, nota que ela escreveu, ajuste que ela fez no settings. Nada disso
#  pode ser apagado por uma atualização.
#
#  O que ele faz: olha o que já existe, separa o que veio do pacote do que é
#  da pessoa, e define o modo (instalação nova ou atualização). Os passos
#  seguintes leem esse modo e se comportam de acordo.
#
#  Exporta:
#    INSTALL_MODE       fresh | upgrade
#    PREV_VERSION       versão encontrada, ou "desconhecida"
#    UPGRADE_POLICY     preserve | additive | replace
#    EXISTING_VAULT     caminho do vault já existente, se houver
#    CUSTOM_SQUADS      lista de squads que a pessoa criou (não vieram do pacote)
#    HAS_LIGHTRAG       1 se já existe instalação de LightRAG
# ============================================================================

ui_header "2/11 · Procurando instalação anterior"

STATE_DIR="$HOME/.${PRODUCT_SLUG}"
VERSION_FILE="$STATE_DIR/VERSION"
MANIFEST_FILE="$STATE_DIR/installed-manifest.txt"

INSTALL_MODE="fresh"
PREV_VERSION="desconhecida"
UPGRADE_POLICY="preserve"
EXISTING_VAULT=""
CUSTOM_SQUADS=""
HAS_LIGHTRAG=0

# ---------------------------------------------------------------------------
# 1. sinais de que já existe alguma instalação
# ---------------------------------------------------------------------------
SIGNS=0

[ -d "$STATE_DIR" ] && SIGNS=$((SIGNS+1))
[ -d "$CLAUDE_HOME/commands" ] && [ -n "$(ls -A "$CLAUDE_HOME/commands" 2>/dev/null)" ] && SIGNS=$((SIGNS+1))
[ -d "$CLAUDE_HOME/skills" ] && [ -n "$(ls -A "$CLAUDE_HOME/skills" 2>/dev/null)" ] && SIGNS=$((SIGNS+1))
[ -f "$CLAUDE_HOME/settings.json" ] && SIGNS=$((SIGNS+1))

if [ -f "$VERSION_FILE" ]; then
  PREV_VERSION="$(tr -d '[:space:]' < "$VERSION_FILE" 2>/dev/null)"
  [ -z "$PREV_VERSION" ] && PREV_VERSION="desconhecida"
fi

# procura o vault em alguns lugares prováveis
for cand in "${VAULT_PATH:-}" "$DEFAULT_VAULT_PATH" "$HOME/Documents/Obsidian Vault" \
            "$HOME/Obsidian Vault" "$HOME/Documents/Obsidian" "$HOME/vault"; do
  [ -n "$cand" ] || continue
  if [ -d "$cand" ]; then
    EXISTING_VAULT="$cand"
    SIGNS=$((SIGNS+1))
    break
  fi
done

# LightRAG já instalado?
if [ -d "$HOME/lightrag-workspace" ] || [ -n "${LIGHTRAG_HOME:-}" ]; then
  HAS_LIGHTRAG=1
fi

# ---------------------------------------------------------------------------
# 2. instalação nova: sai daqui rápido
# ---------------------------------------------------------------------------
if [ "$SIGNS" -eq 0 ]; then
  ui_ok "Nenhuma instalação anterior encontrada. Vamos fazer a instalação completa."
  export INSTALL_MODE PREV_VERSION UPGRADE_POLICY EXISTING_VAULT CUSTOM_SQUADS HAS_LIGHTRAG
  log "INSTALL_MODE=fresh"
  return 0 2>/dev/null || true
fi

INSTALL_MODE="upgrade"

# ---------------------------------------------------------------------------
# 3. retrato do que já existe
# ---------------------------------------------------------------------------
ui_warn "Encontrei uma instalação anterior neste computador."
echo

n_squads=0; n_skills=0; n_scripts=0; n_clones=0; n_notas=0
[ -d "$CLAUDE_HOME/commands" ] && n_squads=$(find "$CLAUDE_HOME/commands" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
[ -d "$CLAUDE_HOME/skills" ]   && n_skills=$(find "$CLAUDE_HOME/skills" -maxdepth 1 -mindepth 1 2>/dev/null | wc -l | tr -d ' ')
[ -d "$CLAUDE_HOME/scripts" ]  && n_scripts=$(find "$CLAUDE_HOME/scripts" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
if [ -n "$EXISTING_VAULT" ]; then
  [ -d "$EXISTING_VAULT/CLONES" ] && n_clones=$(find "$EXISTING_VAULT/CLONES" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  n_notas=$(find "$EXISTING_VAULT" -name "*.md" -not -path "*/.obsidian/*" 2>/dev/null | wc -l | tr -d ' ')
fi

ui_info "Versão instalada:  $PREV_VERSION   (esta é a $PRODUCT_VERSION)"
ui_info "Squads:            $n_squads"
ui_info "Skills:            $n_skills"
ui_info "Scripts:           $n_scripts"
if [ -n "$EXISTING_VAULT" ]; then
  ui_info "Vault:             $EXISTING_VAULT"
  ui_info "  clones:          $n_clones"
  ui_info "  notas suas:      $n_notas"
else
  ui_info "Vault:             não encontrei, vou perguntar depois"
fi
[ "$HAS_LIGHTRAG" = 1 ] && ui_info "LightRAG:          já instalado" || ui_info "LightRAG:          ainda não instalado"

# ---------------------------------------------------------------------------
# 4. o que é seu e o que veio do pacote
#    Um squad que existe aqui mas não existe em content/squads foi criado pela
#    pessoa. Ele nunca pode ser tocado.
# ---------------------------------------------------------------------------
if [ -d "$CLAUDE_HOME/commands" ]; then
  for d in "$CLAUDE_HOME/commands"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    if [ ! -d "$INFINITY_OS_ROOT/content/squads/$name" ]; then
      CUSTOM_SQUADS="$CUSTOM_SQUADS $name"
    fi
  done
  CUSTOM_SQUADS="$(echo "$CUSTOM_SQUADS" | sed 's/^ *//')"
fi

if [ -n "$CUSTOM_SQUADS" ]; then
  echo
  ui_ok "Encontrei coisa que é sua, e que o pacote não conhece:"
  for s in $CUSTOM_SQUADS; do ui_dim "  $s"; done
  ui_info "Isso NÃO vai ser tocado em nenhuma hipótese."
fi

# ---------------------------------------------------------------------------
# 5. escolha do modo
# ---------------------------------------------------------------------------
echo
if [ "${ASSUME_YES:-0}" = "1" ]; then
  UPGRADE_POLICY="preserve"
  ui_dim "Modo não interativo: usando a política mais segura (preservar o que é seu)."
else
  ui_info "Como você quer que eu trate o que já está aí?"
  echo
  choice="$(ui_choice "Escolha o modo de atualização" \
    "Atualizar preservando o que é meu (recomendado)" \
    "Só adicionar o que falta, não mexer em nada existente" \
    "Reinstalar do zero, com backup completo antes")"
  case "$choice" in
    1) UPGRADE_POLICY="preserve" ;;
    2) UPGRADE_POLICY="additive" ;;
    3) UPGRADE_POLICY="replace" ;;
    *) UPGRADE_POLICY="preserve" ;;
  esac
fi

echo
case "$UPGRADE_POLICY" in
  preserve)
    ui_ok "Modo: atualizar preservando."
    ui_dim "Conteúdo do pacote (squads, clones, scripts) é atualizado para a versão nova."
    ui_dim "O que é seu (squads próprios, suas notas, seus ajustes) fica intocado."
    ui_dim "Se um arquivo do pacote foi editado por você, eu guardo a sua versão ao lado, com sufixo .seu, em vez de perder."
    ;;
  additive)
    ui_ok "Modo: só adicionar."
    ui_dim "Eu instalo apenas o que ainda não existe. Nada do que já está aí é alterado."
    ui_dim "Isso é o mais seguro, mas você não recebe as correções dos arquivos antigos."
    ;;
  replace)
    ui_warn "Modo: reinstalar do zero."
    ui_dim "Faço um backup completo antes de qualquer coisa, e te digo onde ele ficou."
    ui_dim "Suas notas do vault continuam intocadas: reinstalar mexe no sistema, não no seu conteúdo."
    if ! ui_yesno "Confirma reinstalar do zero?" "N"; then
      UPGRADE_POLICY="preserve"
      ui_ok "Voltei para o modo seguro: atualizar preservando."
    fi
    ;;
esac

# ---------------------------------------------------------------------------
# 6. backup, sempre, independente do modo
# ---------------------------------------------------------------------------
echo
ui_step "Backup de segurança"
mkdir -p "$BACKUP_DIR"
for item in settings.json commands skills scripts heuristics instincts; do
  if [ -e "$CLAUDE_HOME/$item" ]; then
    cp -R "$CLAUDE_HOME/$item" "$BACKUP_DIR/" 2>/dev/null && log "backup: $item"
  fi
done
[ -d "$STATE_DIR" ] && cp -R "$STATE_DIR" "$BACKUP_DIR/state" 2>/dev/null
ui_ok "Backup salvo em: $BACKUP_DIR"
ui_dim "Se algo der errado, é só copiar de volta de lá."

# ---------------------------------------------------------------------------
# 7. registra o que o pacote instalou, para a próxima atualização saber
# ---------------------------------------------------------------------------
mkdir -p "$STATE_DIR"

export INSTALL_MODE PREV_VERSION UPGRADE_POLICY EXISTING_VAULT CUSTOM_SQUADS HAS_LIGHTRAG
log "INSTALL_MODE=$INSTALL_MODE POLICY=$UPGRADE_POLICY PREV=$PREV_VERSION VAULT=$EXISTING_VAULT"
ui_ok "Pronto. Vou seguir só com o que faz sentido para o seu caso."
