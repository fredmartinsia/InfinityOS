#!/usr/bin/env bash
# ============================================================================
#  Passo 50 — Conteúdo: squads → ~/.claude/commands/  e clones → vault/CLONES/
#  (Os clones só são copiados aqui se o vault já existir; senão o passo 60
#   cria o vault e copia. Idempotente: não sobrescreve o que já existe.)
# ============================================================================
ui_header "8/11 · Conteúdo (squads + clones)"

# --- Squads: comandos do Claude Code ----------------------------------------
#
#  Regra de ouro: nada que a pessoa escreveu pode ser apagado.
#
#  Um squad que existe aqui mas não existe no pacote foi criado por ela. O laço
#  abaixo percorre o pacote, então esses nunca são alcançados: ficam intocados
#  por construção.
#
#  Para os squads que VÊM do pacote, o comportamento segue a política escolhida
#  no passo 05. Se a pessoa editou um arquivo do pacote, a versão dela é
#  preservada com o sufixo .seu em vez de ser perdida.
# ---------------------------------------------------------------------------
mkdir -p "$CLAUDE_HOME/commands"
POLICY="${UPGRADE_POLICY:-preserve}"
nsq=0; nskip=0; nkept=0

for d in "$INFINITY_OS_ROOT"/content/squads/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  dst="$CLAUDE_HOME/commands/$name"

  # ainda não existe: instala, sem drama
  if [ ! -d "$dst" ]; then
    cp -R "$d" "$dst"
    nsq=$((nsq+1))
    continue
  fi

  # já existe: a política decide
  case "$POLICY" in
    additive)
      nskip=$((nskip+1))
      continue
      ;;
    preserve)
      # guarda ao lado qualquer arquivo que a pessoa tenha alterado
      while IFS= read -r rel; do
        [ -n "$rel" ] || continue
        origem="$d$rel"
        atual="$dst/$rel"
        [ -f "$origem" ] && [ -f "$atual" ] || continue
        if ! cmp -s "$origem" "$atual"; then
          cp "$atual" "$atual.seu" 2>/dev/null && nkept=$((nkept+1))
        fi
      done < <(cd "$d" && find . -type f 2>/dev/null | sed 's|^\./||')
      # copia por cima, sem remover: arquivo que só existe no destino sobrevive
      cp -R "$d." "$dst/" 2>/dev/null || cp -R "$d"* "$dst/" 2>/dev/null
      nsq=$((nsq+1))
      ;;
    replace)
      # o backup completo já foi feito no passo 05
      rm -rf "$dst"
      cp -R "$d" "$dst"
      nsq=$((nsq+1))
      ;;
  esac
done

ui_ok "$nsq squads instalados ou atualizados em ~/.claude/commands/."
[ "$nskip" -gt 0 ] && ui_dim "$nskip squads já existentes foram deixados como estavam (modo só adicionar)."
[ "$nkept" -gt 0 ] && ui_info "$nkept arquivos que você tinha editado foram guardados com o sufixo .seu, ao lado do novo."
if [ -n "${CUSTOM_SQUADS:-}" ]; then
  ui_ok "Seus squads próprios seguem intactos: $CUSTOM_SQUADS"
fi

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
