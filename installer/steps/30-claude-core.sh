#!/usr/bin/env bash
# ============================================================================
#  Passo 30 — Núcleo Claude Code: backup, scripts/skills, settings.json,
#  roteador e proteção do vault. Exporta VAULT_PATH e LANGUAGE.
# ============================================================================
ui_header "6/11 · Núcleo do Claude Code"

mkdir -p "$CLAUDE_HOME"

# --- Backup do que já existe ------------------------------------------------
mkdir -p "$BACKUP_DIR"
for item in settings.json scripts skills commands; do
  if [ -e "$CLAUDE_HOME/$item" ]; then
    cp -R "$CLAUDE_HOME/$item" "$BACKUP_DIR/" 2>/dev/null && log "backup: $item"
  fi
done
ui_ok "Backup do ~/.claude atual em: $BACKUP_DIR"

# --- Perguntas: vault e idioma ---------------------------------------------
if [ "${ASSUME_YES:-0}" = "1" ]; then
  VAULT_PATH="$DEFAULT_VAULT_PATH"; LANGUAGE="$DEFAULT_LANGUAGE"
else
  VAULT_PATH="$(ui_ask "Onde fica (ou ficará) seu vault Obsidian?" "$DEFAULT_VAULT_PATH")"
  LANGUAGE="$(ui_ask "Idioma preferido" "$DEFAULT_LANGUAGE")"
fi
VAULT_PATH="${VAULT_PATH/#\~/$HOME}"
export VAULT_PATH LANGUAGE
log "core: vault=$VAULT_PATH lang=$LANGUAGE"

# --- Scripts e skills -------------------------------------------------------
mkdir -p "$CLAUDE_HOME/scripts" "$CLAUDE_HOME/skills"
cp "$INFINITY_OS_ROOT"/claude/scripts/*.py "$CLAUDE_HOME/scripts/" && chmod +x "$CLAUDE_HOME"/scripts/*.py
ui_ok "Scripts de RAG/proteção instalados ($(ls "$INFINITY_OS_ROOT"/claude/scripts/*.py | wc -l | tr -d ' ') arquivos)."
for s in "$INFINITY_OS_ROOT"/claude/skills/*/; do
  name="$(basename "$s")"
  rm -rf "$CLAUDE_HOME/skills/$name"
  cp -R "$s" "$CLAUDE_HOME/skills/$name"
done
ui_ok "Skills instaladas ($(ls -1d "$INFINITY_OS_ROOT"/claude/skills/*/ | wc -l | tr -d ' '))."

# --- settings.json (render) -------------------------------------------------
VAULT_PATH="$VAULT_PATH" LANGUAGE="$LANGUAGE" python3 - "$INFINITY_OS_ROOT/claude/settings.template.json" "$CLAUDE_HOME/settings.json" <<'PY'
import os, sys, io
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()
s = s.replace("{{VAULT_PATH}}", os.environ["VAULT_PATH"]).replace("{{LANGUAGE}}", os.environ["LANGUAGE"])
io.open(dst, "w", encoding="utf-8").write(s)
PY
ui_ok "settings.json renderizado (hooks de RAG, proteção e idioma)."

# --- Roteador de modelos ----------------------------------------------------
# CHOSEN_LOCAL_MODEL vem do passo 20 (analise real de RAM/disco). Se a pessoa
# nao instalou modelo local, usamos o sentinela "none" em vez de um nome fixo
# de modelo que nunca foi baixado: route.py trata "none" como alvo local
# indisponivel e cai direto pro fallback em nuvem (gemini/claude).
mkdir -p "$HOME/.infinity-os"
cp "$INFINITY_OS_ROOT/routing/route.py" "$HOME/.infinity-os/route.py"
cp "$INFINITY_OS_ROOT/routing/hardware-tiers.yaml" "$HOME/.infinity-os/hardware-tiers.yaml"
LOCAL_MODEL="${CHOSEN_LOCAL_MODEL:-none}" python3 - "$INFINITY_OS_ROOT/routing/router.config.template.yaml" "$HOME/.infinity-os/router.config.yaml" <<'PY'
import os, sys, io
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read().replace("{{LOCAL_MODEL}}", os.environ["LOCAL_MODEL"])
io.open(dst, "w", encoding="utf-8").write(s)
PY
if [ -n "${CHOSEN_LOCAL_MODEL:-}" ]; then
  ui_ok "Roteador de modelos em ~/.infinity-os/ (modelo local: ${CHOSEN_LOCAL_MODEL})."
else
  ui_ok "Roteador de modelos em ~/.infinity-os/ (sem modelo local instalado, tarefas de codigo pesado usam nuvem)."
fi

# --- Memory templates -------------------------------------------------------
SLUG="$(printf '%s' "$HOME" | sed 's#/#-#g')"
MEMDIR="$CLAUDE_HOME/projects/$SLUG/memory"
mkdir -p "$MEMDIR"
for t in "$INFINITY_OS_ROOT"/claude/memory-templates/*; do
  base="$(basename "$t" | sed 's/\.template//')"
  if [ ! -e "$MEMDIR/$base" ]; then
    VAULT_PATH="$VAULT_PATH" LANGUAGE="$LANGUAGE" python3 - "$t" "$MEMDIR/$base" <<'PY'
import os, sys, io
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()
s = s.replace("{{VAULT_PATH}}", os.environ["VAULT_PATH"]).replace("{{LANGUAGE}}", os.environ["LANGUAGE"])
io.open(dst, "w", encoding="utf-8").write(s)
PY
  fi
done
ui_ok "Templates de memória em $MEMDIR (o /onboarding preenche depois)."

# --- Proteção do vault (opcional) -------------------------------------------
if [ "${ASSUME_YES:-0}" != "1" ] && ui_yesno "Ativar a proteção do vault (exige código p/ apagar arquivos)?" "Y"; then
  ui_dim "Defina seu código de proteção (fica só como hash local, nunca no repo):"
  python3 "$CLAUDE_HOME/scripts/vault_guard_setup.py" </dev/tty || ui_warn "Setup da proteção pulado/falhou."
else
  ui_dim "Proteção do vault não configurada agora (rode vault_guard_setup.py quando quiser)."
fi

# --- Plugins de marketplace -------------------------------------------------
if [ "${INFINITY_OS_SKIP_PLUGINS:-0}" = "1" ]; then
  ui_dim "Instalação de plugins pulada (INFINITY_OS_SKIP_PLUGINS=1)."
elif command -v claude >/dev/null 2>&1; then
  log_run claude plugin install claude-mem@thedotmack || ui_warn "Instale depois: claude plugin install claude-mem@thedotmack"
  log_run claude plugin install ui-ux-pro-max@nextlevelbuilder || true
  ui_ok "Plugins de marketplace solicitados."
else
  ui_dim "Claude CLI ausente — instale os plugins depois (claude-mem, ui-ux-pro-max)."
fi
