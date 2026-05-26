# Cliente: VS Code

O VS Code usa o InfinityOS através da **extensão do Claude Code**, que lê a mesma
configuração em `~/.claude/`. Ou seja: skills, squads, hooks e RAG funcionam
igual ao terminal.

## Setup

1. Instale a extensão **Claude Code** no VS Code.
2. Garanta que o `./install.sh` já rodou (popula `~/.claude/`).
3. Abra a paleta e use os comandos/skills normalmente.

## Workspace recomendado

Crie um `.vscode/settings.json` no seu projeto para apontar o vault, se quiser
sobrescrever o default por projeto:

```json
{
  "terminal.integrated.env.osx": {
    "CLAUDE_VAULT_PATH": "${env:HOME}/Documents/Obsidian Vault"
  }
}
```
