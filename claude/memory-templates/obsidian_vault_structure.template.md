---
name: Estrutura do Vault Obsidian
description: Localizacao, pastas top-level e convencoes do vault de {{USER_NAME}}
type: reference
---

## Localizacao

- Vault path: `{{VAULT_PATH}}`
- Total de notas aproximado: {{NOTES_COUNT}}

## Pastas Top-Level

{{TOP_LEVEL_FOLDERS}}

**Estrutura recomendada pelo InfinityOS:**
- `_META/` — INDEXes e MOCs centrais (dashboards)
- `Projetos/` — projetos ativos, um por subpasta
- `Clientes/` — pessoas e empresas recorrentes
- `CLONES/` — 36 clones AI (copiados pelo onboarding)
- `Templates/` — templates reutilizaveis
- `Diario/` — notas datadas
- `Reuniões/` — atas de reunioes

## Convencoes

- **INDEX:** `📊 INDEX - {Nome}.md` (hub de uma area)
- **MOC:** `📊 MOC - {Categoria}.md` (Map of Content agrupando notas)
- **DASHBOARD:** `📊 DASHBOARD - {Tipo}.md` (visao consolidada)
- **Datados:** `YYYY-MM-DD.md`
- **Templates:** `TEMPLATE - {Nome}.md`
- **Clones:** `{nome-slug}_{NN}_{MODULE}.md` (NN de 01 a 12)

## Plugins Obsidian Ativos

{{OBSIDIAN_PLUGINS}}

## Como Aplicar

Quando o usuario pedir pra gravar/ler algo "no Obsidian", assumir essas convencoes. Quando criar novos arquivos via skills, seguir o padrao de nomes acima.
