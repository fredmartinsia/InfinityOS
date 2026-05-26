#!/usr/bin/env bash
# ============================================================================
#  infinity-os — configuração central
#  Único lugar onde o nome do produto e caminhos-base são definidos.
#  Para renomear o produto, mude PRODUCT_SLUG aqui e nada mais quebra.
# ============================================================================

# Nome do produto (usado em banners, backups, logs)
PRODUCT_NAME="InfinityOS"
PRODUCT_SLUG="infinity-os"
PRODUCT_VERSION="0.1.0"

# Raiz do repositório (resolvida a partir da localização deste arquivo)
if [ -z "${INFINITY_OS_ROOT:-}" ]; then
  _env_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
  INFINITY_OS_ROOT="$(cd "${_env_dir}/../.." && pwd)"
fi

# Destinos da instalação
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.${PRODUCT_SLUG}-backup-$(date +%Y%m%d-%H%M%S)}"
INSTALL_LOG="${INSTALL_LOG:-$HOME/.${PRODUCT_SLUG}-install.log}"

# Defaults do vault Obsidian
DEFAULT_VAULT_PATH="${DEFAULT_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
DEFAULT_LANGUAGE="${DEFAULT_LANGUAGE:-Portugues}"

export PRODUCT_NAME PRODUCT_SLUG PRODUCT_VERSION INFINITY_OS_ROOT \
       CLAUDE_HOME BACKUP_DIR INSTALL_LOG DEFAULT_VAULT_PATH DEFAULT_LANGUAGE
