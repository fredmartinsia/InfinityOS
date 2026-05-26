#!/usr/bin/env bash
# ============================================================================
#  Passo 50 — Conteúdo: squads → ~/.claude/commands/  e clones → vault/CLONES/
#  (Os clones só são copiados aqui se o vault já existir; senão o passo 60
#   cria o vault e copia. Idempotente: não sobrescreve o que já existe.)
# ============================================================================
ui_header "6/8 — Conteúdo (squads + clones)"

# --- Squads → comandos do Claude Code ---------------------------------------
mkdir -p "$CLAUDE_HOME/commands"
nsq=0
for d in "$INFINITY_OS_ROOT"/content/squads/*/; do
  name="$(basename "$d")"
  rm -rf "$CLAUDE_HOME/commands/$name"
  cp -R "$d" "$CLAUDE_HOME/commands/$name"
  nsq=$((nsq+1))
done
ui_ok "$nsq squads instalados em ~/.claude/commands/."

# --- Clones → vault/CLONES (com render do {{VAULT_PATH}}) --------------------
# O caminho do vault foi definido no passo 30. Se ainda não existir, o passo 60
# cria a estrutura; aqui copiamos os clones para lá de qualquer forma.
CLONES_DST="${VAULT_PATH:-$DEFAULT_VAULT_PATH}/CLONES"
mkdir -p "$CLONES_DST"
ncl=0
for d in "$INFINITY_OS_ROOT"/content/clones/*/; do
  name="$(basename "$d")"
  if [ ! -d "$CLONES_DST/$name" ]; then
    cp -R "$d" "$CLONES_DST/$name"
    ncl=$((ncl+1))
  fi
done

# Render do placeholder {{VAULT_PATH}} nos clones recém-copiados
VP="${VAULT_PATH:-$DEFAULT_VAULT_PATH}" python3 - "$CLONES_DST" <<'PY'
import os, sys, io, glob
dst = sys.argv[1]; vp = os.environ["VP"]
for f in glob.glob(os.path.join(dst, "**", "*.md"), recursive=True) + \
         glob.glob(os.path.join(dst, "**", "*.agent.md"), recursive=True):
    try: s = io.open(f, encoding="utf-8").read()
    except Exception: continue
    if "{{VAULT_PATH}}" in s:
        io.open(f, "w", encoding="utf-8").write(s.replace("{{VAULT_PATH}}", vp))
PY
ui_ok "$ncl clones copiados para $CLONES_DST (caminhos resolvidos)."
log "content: squads=$nsq clones=$ncl dst=$CLONES_DST"
