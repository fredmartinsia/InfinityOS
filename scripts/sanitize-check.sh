#!/usr/bin/env bash
# ============================================================================
#  infinite-os — gate de zero vazamento
#  Falha (exit 1) se achar segredos, PII ou dados de projeto no repositório.
#  Roda localmente, no git pre-push hook e no CI.
# ============================================================================
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
cd "$ROOT"

# Onde procurar: tudo, menos .git e o manifesto (cheio de hashes hex)
EXCLUDES=(--exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules
          --exclude=install-manifest.yaml --exclude=*.db
          --exclude=sanitize-check.sh)  # contém os próprios padrões

fail=0
report() { echo "  ✗ $1"; fail=1; }

echo "== Gate de sanitização =="

# --- 1) Segredos de alta confiança ------------------------------------------
# Formatos inequívocos de credencial (não dão falso-positivo em docs).
SECRET_RE='sk-[A-Za-z0-9]{20,}|sk-or-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
if grep -rInE "${EXCLUDES[@]}" "$SECRET_RE" . >/tmp/aos_secrets 2>/dev/null; then
  echo "[segredos] encontrados:"; cat /tmp/aos_secrets; report "segredos acima"
else
  echo "  ✓ sem segredos de alta confiança"
fi

# --- 2) PII / dados de projeto ----------------------------------------------
# Padrões do Fred/projetos. 'nobres' sozinho é palavra comum em PT → só pegamos
# as formas de MARCA (nobres 3d / nobrestech).
PII_RE='fredmartins|fmartins|3d\.nobresamz|nobres[ ._-]?3d|nobrestech|clube ?infinit|vv group|morrinhos|marciano martins|fred martins|infizap'
# Falsos-positivos conhecidos a ignorar:
ALLOW='Fred Hahn'
if grep -rInE "${EXCLUDES[@]}" -i "$PII_RE" . 2>/dev/null | grep -vE "$ALLOW" >/tmp/aos_pii 2>/dev/null; then
  if [ -s /tmp/aos_pii ]; then
    echo "[PII/projeto] encontrados:"; cat /tmp/aos_pii; report "PII/projeto acima"
  else
    echo "  ✓ sem PII/dados de projeto"
  fi
else
  echo "  ✓ sem PII/dados de projeto"
fi

# --- 2b) Nome próprio do autor ----------------------------------------------
# 'Fred' como nome próprio. Allowlist: 'Fred Hahn' (revisor real do livro do Caples).
if grep -rInE "${EXCLUDES[@]}" "\bFred\b" . 2>/dev/null | grep -vE "Fred Hahn" >/tmp/aos_name 2>/dev/null; then
  if [ -s /tmp/aos_name ]; then
    echo "[nome do autor] encontrados:"; cat /tmp/aos_name; report "nome do autor acima"
  else
    echo "  ✓ sem nome próprio do autor"
  fi
else
  echo "  ✓ sem nome próprio do autor"
fi

# --- 3) Caminhos pessoais absolutos -----------------------------------------
# /Users/<nome> real — placeholders /Users/me e /Users/you são permitidos.
if grep -rInE "${EXCLUDES[@]}" "/Users/[A-Za-z0-9._-]+" . 2>/dev/null \
   | grep -vE "/Users/(me|you|user|username|seu-usuario)\b" >/tmp/aos_paths 2>/dev/null; then
  if [ -s /tmp/aos_paths ]; then
    echo "[caminhos absolutos] encontrados:"; cat /tmp/aos_paths; report "caminhos absolutos acima"
  else
    echo "  ✓ sem caminhos absolutos pessoais"
  fi
else
  echo "  ✓ sem caminhos absolutos pessoais"
fi

# --- 4) Arquivos proibidos no tree ------------------------------------------
BAD_FILES=$(find . -path ./.git -prune -o \
  \( -name ".env" -o -name "settings.local.json" -o -name "*.sha256" \
     -o -name "vault_unlock.json" -o -name "*.db" -o -name "history.jsonl" \) -print 2>/dev/null)
if [ -n "$BAD_FILES" ]; then
  echo "[arquivos proibidos]:"; echo "$BAD_FILES"; report "arquivos proibidos acima"
else
  echo "  ✓ sem arquivos proibidos (.env/.db/settings.local/etc.)"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "✅ GATE OK — nada sensível encontrado."
else
  echo "🛑 GATE FALHOU — resolva os itens acima ANTES de qualquer push."
fi
rm -f /tmp/aos_secrets /tmp/aos_pii /tmp/aos_paths
exit "$fail"
