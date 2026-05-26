#!/usr/bin/env bash
# Instala os git hooks do repo (pre-push → gate de sanitização).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
HOOK_DIR="$ROOT/.git/hooks"
if [ ! -d "$ROOT/.git" ]; then
  echo "Não é um repositório git ainda. Rode 'git init' primeiro."
  exit 1
fi
cp "$ROOT/scripts/hooks/pre-push" "$HOOK_DIR/pre-push"
chmod +x "$HOOK_DIR/pre-push"
echo "✓ pre-push instalado em .git/hooks/ — o push roda o gate de sanitização."
