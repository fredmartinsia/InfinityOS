---
name: RAG Hook Configuration
description: Configuracao atual do hook RAG que injeta contexto do vault Obsidian em cada prompt
type: reference
---

## Status

- Script: `~/.claude/scripts/vault_rag.py` — **instalado**
- Hook configurado em: `~/.claude/settings.json` (UserPromptSubmit)
- Vault path usado: `{{VAULT_PATH}}`

## Como Funciona

1. Cada prompt do usuario passa pelo `UserPromptSubmit` hook
2. `vault_rag.py` le o prompt, remove stopwords PT/EN, extrai palavras-chave
3. Faz query FTS5 no SQLite local (`~/.claude/cache/vault_rag.db`)
4. Pondera resultados por pasta (Clientes > Projetos > Infra > Diario)
5. Injeta top-6 chunks no `system_prompt` (limite 450 tokens)

## Configuracao Customizavel (env vars)

- `CLAUDE_VAULT_PATH` — path do vault (default `~/Documents/Obsidian Vault`)
- `CLAUDE_RAG_MAX_TOKENS` — orcamento de tokens (default 450)
- `CLAUDE_RAG_TOP_CHUNKS` — chunks por query (default 6)
- `CLAUDE_RAG_DIARY_MAX_DAYS` — cutoff de Diario (default 30)

## Troubleshooting

Teste rapido:
```bash
python3 ~/.claude/scripts/vault_rag.py --dry-run
```

Se nada vier do vault em conversas:
1. Validar vault path: `echo $CLAUDE_VAULT_PATH` ou testar o dry-run
2. Forcar rebuild do indice: `rm ~/.claude/cache/vault_rag.db`
3. Checar se settings.json tem o hook: `cat ~/.claude/settings.json | grep vault_rag`

## Como Aplicar

Se o usuario reclamar que "o Claude nao sabe do meu projeto X", checar o RAG antes de sugerir carregar contexto manualmente.
