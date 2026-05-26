---
name: Ferramentas Instaladas pelo InfinityOS
description: CLIs, skills, hooks e plugins instalados pelo install.sh
type: reference
---

Inventario do que o `install.sh` do InfinityOS instala no ambiente.

## Scripts em `~/.claude/scripts/`

- `vault_rag.py` — hook `UserPromptSubmit` que injeta contexto do Obsidian em cada prompt. Usa SQLite FTS5 local. Limite 450 tokens. Pesos: Clientes (1.4) > Projetos (1.3) > Infra (1.2) > Diario (1.1). Ignora prompts git/npm/deploy e diarios > 30 dias.
- `vault_writer.py` — hook `Stop` que dispara worker em background pra gravar resumo da sessao no vault.
- `vault_writer_bg.py` — worker que chama Gemini CLI, classifica projeto e grava no Obsidian. Novos projetos viram `.draft.md`.

Todos respeitam `CLAUDE_VAULT_PATH` (env var) — default `~/Documents/Obsidian Vault`.

## Skills Customizadas em `~/.claude/skills/`

- `createclone` — Cria clones AI com estrutura modular de 12 arquivos. Invocado com `/createclone`.
- `opensquad` — Orquestrador de squads multi-agent. Invocado com `/opensquad`.
- `obsidian-markdown` — Wikilinks, embeds, callouts, properties.
- `obsidian-bases` — Arquivos `.base` com views database-like.
- `obsidian-cli` — CLI pra vault Obsidian rodando.
- `json-canvas` — Arquivos `.canvas` (JSON Canvas spec 1.0).
- `defuddle` — Extracao limpa de conteudo web.
- `prd` — Gerador de Product Requirements Documents.
- `onboarding` — Wizard de onboarding do InfinityOS (usado uma vez na instalacao).

## Plugins (Squads) Instalados via `claude plugin install`

- `hormozi-squad` — Ofertas, copy, launches
- `design-squad` — Design system + UX
- `copy-squad` e `copy-master` — Copywriting (40+ agentes)
- `brand-squad` — Branding e posicionamento
- `advisory-board` — Conselho estrategico
- `c-level-squad` — CxO orchestration
- `cybersecurity` — Pentest, auditoria
- `data-squad` — Analytics, growth
- `legal-squad` — Contratos, compliance
- `movement` — Movement building (PT-BR)
- `storytelling` — Narrativa e pitch decks
- `traffic-masters` — Paid ads
- `claude-code-mastery` — Configuracao de Claude Code
- `AIOX` — BMAD-like framework (po, architect, dev, qa, sm, devops, etc.)

Plugin gerenciador de memoria:
- `claude-mem@thedotmack` — Observacoes persistentes cross-session

Plugin de UI/UX:
- `ui-ux-pro-max@nextlevelbuilder`

## Opensquad Framework

- `~/_opensquad/core/` — engine, pipelines, best-practices
- `~/_opensquad/_memory/` — company.md + preferences.md (parametrizados no onboarding)

## Squad Custom

- `~/squads/amazon-es-3d-product-miner/` — squad reutilizavel para prospeccao de produtos 3D.

## Como Aplicar

Antes de afirmar que uma ferramenta esta disponivel, valide com `ls ~/.claude/skills/`, `claude plugin list`, ou teste invocacao direta.
