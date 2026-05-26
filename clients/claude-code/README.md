# Cliente: Claude Code (primário)

O Claude Code é o motor do InfinityOS — tudo funciona nativamente após o
`./install.sh`. Nada extra a fazer aqui.

- **Skills:** `/createclone`, `/opensquad`, `/onboarding`, `/obsidian-*`, etc.
- **Squads:** `/<nome-do-squad>` (ex.: `/hormozi-squad`).
- **Hooks:** RAG (`vault_rag`), proteção (`vault_guard`) e persistência
  (`vault_writer`) já ligados em `~/.claude/settings.json`.
- **Roteador:** `~/.infinity-os/route.py`.

Disponível como CLI, app desktop, web (claude.ai/code) e extensões de IDE.
