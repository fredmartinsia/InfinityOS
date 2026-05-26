# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.1.0] — Não lançado

Primeira versão completa do InfiniteOS.

### Adicionado
- **Instalador "modo idiota"** (`install.sh` + 8 passos): preflight de hardware,
  detecção/instalação guiada de CLIs (Ollama, Gemini, Qwen, Codex, gh),
  model-advisor por hardware, núcleo Claude Code, AIOX via npx, conteúdo,
  setup Obsidian e smoke test. Defaults seguros, backup e `uninstall.sh`.
- **Núcleo Claude Code:** 7 scripts (RAG + proteção do vault), 9 skills,
  11 templates de memória, `settings.template.json` com hooks.
- **Conteúdo:** 56 clones de especialistas + 17 squads multi-agente (sanitizados).
- **Roteamento de modelos:** `route.py` + config (Claude/Gemini/Qwen/Codex) com
  fallback; tiers de hardware.
- **Setup Obsidian + RAG:** estrutura de pastas guiada por perfil, REGRAS/INDEX
  dinâmico e índice de RAG construído na instalação.
- **opensquad** (framework de pipelines) e **vault-template**.
- **Docs** (10) no padrão AIOX + **clients/** para VS Code, Codex, Antigravity, Gemini CLI.
- **Gate de zero vazamento:** `scripts/sanitize-check.sh`, git pre-push hook,
  GitHub Action (CI) e `.gitleaks.toml`. `install-manifest.yaml` com SHA256.
