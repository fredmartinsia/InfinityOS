#!/usr/bin/env bash
# ============================================================================
#  install-codex.sh: leva o harness Opensquad para o Codex CLI
#
#  O Codex CLI le prompts customizados em ~/.codex/prompts/*.md (invocados
#  como slash command pelo nome do arquivo, com frontmatter "description")
#  e skills no padrao aberto ~/.agents/skills (agents.md / skill.md).
#  Este script:
#    1. Converte cada agente de content/squads/*/agents/*.md num prompt
#       Codex em ~/.codex/prompts/<squad>-<agente>.md
#    2. Aponta ~/.agents/skills para as skills do repo (symlink)
#    3. Escreve/anexa ~/.codex/AGENTS.md com as regras do harness
#  E idempotente: roda de novo sem duplicar, e faz backup com timestamp
#  antes de sobrescrever qualquer coisa que ja exista.
# ============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
INFINITY_OS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SQUADS_DIR="$INFINITY_OS_ROOT/content/squads"
SKILLS_DIR="$INFINITY_OS_ROOT/claude/skills"
HEURISTICS_AGENTS="$INFINITY_OS_ROOT/claude/heuristics/AGENTS.md"

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PROMPTS_DIR="$CODEX_HOME/prompts"
AGENTS_SKILLS_DIR="$HOME/.agents/skills"
AGENTS_MD="$CODEX_HOME/AGENTS.md"
STAMP="$(date +%Y%m%d-%H%M%S)"

log()  { printf '%s\n' "$*"; }
warn() { printf 'AVISO: %s\n' "$*" >&2; }

backup_if_exists() {
  # backup_if_exists <path>
  local target="$1"
  if [ -e "$target" ] || [ -L "$target" ]; then
    mv "$target" "${target}.bak-${STAMP}"
    log "  backup: ${target} para ${target}.bak-${STAMP}"
  fi
}

# ---------------------------------------------------------------------------
# 1) content/squads/*/agents/*.md vira ~/.codex/prompts/<squad>-<agente>.md
# ---------------------------------------------------------------------------
install_prompts() {
  if [ ! -d "$SQUADS_DIR" ]; then
    warn "content/squads nao encontrado em $SQUADS_DIR, pulando prompts."
    return 0
  fi
  mkdir -p "$PROMPTS_DIR"

  local count=0
  local agent_file squad_name agent_name dest title desc body
  while IFS= read -r agent_file; do
    squad_name="$(basename "$(dirname "$(dirname "$agent_file")")")"
    agent_name="$(basename "$agent_file" .md)"
    dest="$PROMPTS_DIR/${squad_name}-${agent_name}.md"

    # Descricao curta: primeira linha "# Titulo" do arquivo, sem markdown.
    title="$(grep -m1 '^# ' "$agent_file" | sed -E 's/^# +//; s/[*_`]//g')"
    if [ -z "$title" ]; then
      title="Agente ${agent_name} do squad ${squad_name}"
    fi
    desc="$(printf '%s' "$title" | sed 's/"/\\"/g')"

    body="$(cat "$agent_file")"

    {
      printf -- '---\n'
      printf 'description: "%s"\n' "$desc"
      printf -- '---\n\n'
      printf '%s\n' "$body"
    } > "$dest.tmp"
    mv "$dest.tmp" "$dest"
    count=$((count + 1))
  done < <(find "$SQUADS_DIR" -type f -path '*/agents/*.md' | sort)

  log "Prompts do Codex gerados: $count (em $PROMPTS_DIR)"
}

# ---------------------------------------------------------------------------
# 2) ~/.agents/skills: symlink para claude/skills do repo
# ---------------------------------------------------------------------------
install_skills_link() {
  if [ ! -d "$SKILLS_DIR" ]; then
    warn "claude/skills nao encontrado em $SKILLS_DIR, pulando skills."
    return 0
  fi
  mkdir -p "$(dirname "$AGENTS_SKILLS_DIR")"

  if [ -L "$AGENTS_SKILLS_DIR" ] && [ "$(readlink "$AGENTS_SKILLS_DIR")" = "$SKILLS_DIR" ]; then
    log "Skills ja apontam para $SKILLS_DIR, nada a fazer."
    return 0
  fi

  backup_if_exists "$AGENTS_SKILLS_DIR"
  ln -s "$SKILLS_DIR" "$AGENTS_SKILLS_DIR"
  log "Skills: $AGENTS_SKILLS_DIR aponta para $SKILLS_DIR"
}

# ---------------------------------------------------------------------------
# 3) ~/.codex/AGENTS.md com as regras do harness (escreve ou anexa)
# ---------------------------------------------------------------------------
install_agents_md() {
  mkdir -p "$CODEX_HOME"

  local marker="<!-- opensquad-harness-rules -->"
  local rules
  if [ -f "$HEURISTICS_AGENTS" ]; then
    rules="$(cat "$HEURISTICS_AGENTS")"
  else
    rules="# Regras do harness Opensquad (fallback: heuristicas nao encontradas em $HEURISTICS_AGENTS)"
  fi

  if [ -f "$AGENTS_MD" ] && grep -qF "$marker" "$AGENTS_MD"; then
    log "AGENTS.md ja tem o bloco do harness: substituindo o bloco (idempotente)."
    backup_if_exists "$AGENTS_MD"
    {
      printf '%s\n\n' "$marker"
      printf '%s\n' "$rules"
      printf '\n%s\n' "$marker"
    } > "$AGENTS_MD"
  elif [ -f "$AGENTS_MD" ]; then
    log "AGENTS.md existe sem o bloco do harness: anexando no fim (com backup)."
    backup_if_exists "$AGENTS_MD"
    {
      cat "${AGENTS_MD}.bak-${STAMP}"
      printf '\n\n%s\n\n' "$marker"
      printf '%s\n' "$rules"
      printf '\n%s\n' "$marker"
    } > "$AGENTS_MD"
  else
    {
      printf '%s\n\n' "$marker"
      printf '%s\n' "$rules"
      printf '\n%s\n' "$marker"
    } > "$AGENTS_MD"
  fi
  log "AGENTS.md do Codex atualizado: $AGENTS_MD"
}

main() {
  log "Instalando harness Opensquad no Codex CLI (CODEX_HOME=$CODEX_HOME)..."
  install_prompts
  install_skills_link
  install_agents_md
  log "Pronto. Prompts: $PROMPTS_DIR | Skills: $AGENTS_SKILLS_DIR | Regras: $AGENTS_MD"
}

main "$@"
