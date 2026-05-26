# Arquitetura

O InfinityOS é um "sistema operacional de orquestração de agentes" em camadas,
montado sobre o Claude Code como motor primário.

```
┌──────────────────────────────────────────────────────────────┐
│  VOCÊ (prompt no Claude Code / VS Code / Codex / ...)         │
├──────────────────────────────────────────────────────────────┤
│  HOOKS (~/.claude/settings.json)                              │
│   • PreToolUse  → vault_guard.py   (protege o vault)          │
│   • UserPromptSubmit → vault_rag.py (injeta contexto do vault)│
│   • Stop → vault_writer.py          (salva insights)          │
├──────────────────────────────────────────────────────────────┤
│  ROTEAMENTO (~/.infinity-os/route.py)                            │
│   complexidade/tipo → Claude | Gemini | Qwen/Ollama | Codex   │
├──────────────────────────────────────────────────────────────┤
│  CONTEÚDO                                                     │
│   • Squads (~/.claude/commands/) — orquestração multi-agente  │
│   • Clones (vault/CLONES/)       — personas de especialistas  │
│   • Skills (~/.claude/skills/)   — createclone, opensquad...  │
│   • AIOX (via npx)               — po/architect/dev/qa/...     │
├──────────────────────────────────────────────────────────────┤
│  CONHECIMENTO (Obsidian Vault)                                │
│   pastas sob medida + RAG FTS5 indexado (vault_rag.db)        │
└──────────────────────────────────────────────────────────────┘
```

## Camadas

- **Motor — Claude Code.** Hooks, skills e comandos são nativos do Claude Code.
  Outras IDEs consomem os mesmos ativos (ver [MULTI-IDE.md](MULTI-IDE.md)).
- **Hooks.** Três scripts Python conectados via `settings.json`:
  `vault_guard.py` (proteção contra deleção), `vault_rag.py` (RAG automático),
  `vault_writer.py` (persistência de insights).
- **Roteamento.** `route.py` decide qual modelo/CLI usar por tarefa, com fallback
  até o Claude. Ver [MODEL-ROUTING.md](MODEL-ROUTING.md).
- **Conteúdo.** Clones (personas) e squads (times) reutilizáveis. Skills
  automatizam clonagem/orquestração. AIOX é instalado à parte via `npx`.
- **Conhecimento.** O vault Obsidian, com estrutura escolhida na instalação e
  índice de RAG construído na hora.

## Separação de dados

- **Repositório** = só estrutura, templates e ativos públicos. Zero dado pessoal.
- **`~/.claude/`** = sua instalação (settings, scripts, skills, comandos).
- **Vault Obsidian** = seu conhecimento e projetos (fica na sua máquina).
