# RAG automático (Obsidian → Claude)

O InfiniteOS injeta automaticamente o contexto relevante do seu vault Obsidian em
cada prompt, via o hook `vault_rag.py` (evento `UserPromptSubmit`).

## Como funciona

1. A cada prompt, `vault_rag.py` recebe seu texto.
2. Indexa o vault num banco SQLite FTS5 (`~/.claude/cache/vault_rag.db`).
3. Busca os trechos mais relevantes (com pesos por pasta) e injeta os top N
   no contexto do Claude.
4. Filtra prompts triviais (comandos git/npm, prompts curtos) — não gasta contexto.

> O índice é construído **na instalação** (`vault_rag.py --reindex`), então o RAG
> já funciona na 1ª sessão. Depois ele se mantém automaticamente.

## Comandos úteis

```bash
# Diagnóstico (quantas notas o vault tem)
CLAUDE_VAULT_PATH="$HOME/Documents/Obsidian Vault" python3 ~/.claude/scripts/vault_rag.py --dry-run

# Reconstruir o índice manualmente
CLAUDE_VAULT_PATH="$HOME/Documents/Obsidian Vault" python3 ~/.claude/scripts/vault_rag.py --reindex
```

## Configuração (variáveis de ambiente)

| Variável | Default | O que faz |
|---|---|---|
| `CLAUDE_VAULT_PATH` | `~/Documents/Obsidian Vault` | Caminho do vault |
| `CLAUDE_RAG_MAX_TOKENS` | `450` | Orçamento de contexto injetado |
| `CLAUDE_RAG_TOP_CHUNKS` | `6` | Nº de trechos retornados |
| `CLAUDE_RAG_DIARY_MAX_DAYS` | `30` | Ignora notas de diário mais antigas |
| `CLAUDE_RAG_CACHE_DIR` | `$CLAUDE_HOME/cache` | Onde fica o `vault_rag.db` |

## Pesos por pasta

Os pesos (ex.: `Clientes` > `Projetos` > `Infra` > `Diário`) só se aplicam às
pastas que **existem** no seu vault — a estrutura que você escolheu na instalação
determina o que é priorizado.

## Persistência reversa

O hook `vault_writer.py` (evento `Stop`) salva, em background, insights da sessão
de volta na sua memória/vault — para continuidade entre sessões.
