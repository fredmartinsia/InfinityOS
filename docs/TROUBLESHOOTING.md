# Troubleshooting

## Instalação

**`python3: command not found`** — instale o Python 3.9+ (`brew install python` /
`sudo apt install python3`) e rode de novo.

**`claude: command not found`** — instale o Claude Code CLI (claude.com/code). O
instalador segue sem ele, mas os plugins de marketplace não serão instalados.

**Uma CLI não instalou** — sem problema: o roteador usa fallback até o Claude.
Instale depois e o `route.py` passa a usá-la automaticamente.

**Quero refazer um passo** — `./install.sh --step=NN` (ex.: `--step=60`).

## RAG

**O contexto do vault não aparece** — confira `CLAUDE_VAULT_PATH` no
`~/.claude/settings.json` e rode:
`CLAUDE_VAULT_PATH="<seu vault>" python3 ~/.claude/scripts/vault_rag.py --dry-run`.

**Reindexar do zero** — `python3 ~/.claude/scripts/vault_rag.py --reindex`.

**`ModuleNotFoundError`** — os scripts usam só a stdlib do Python; confirme que
está rodando com `python3` (não `python` 2.x).

## Proteção do vault

**Não consigo apagar algo no vault** — é o `vault_guard.py` protegendo. Confirme a
operação e siga o fluxo: responder "Sim" → `python3 ~/.claude/scripts/vault_grant.py`
→ repetir o comando. Para definir/trocar o código: `vault_guard_setup.py`.

**Quero desligar a proteção** — remova o hook `PreToolUse` do `~/.claude/settings.json`.

## Roteador

**`route.py` escolhe sempre o Claude** — os outros CLIs não estão instalados
(`which gemini`, `which ollama`...). Instale-os ou ajuste
`~/.infinite-os/router.config.yaml`.

## Multi-IDE

**Como uso um clone no Codex/Gemini?** — copie o `*_02_SYSTEM_PROMPT_*.md` do clone
e cole no cliente. Ver [MULTI-IDE.md](MULTI-IDE.md) e `clients/`.

## Desinstalar / reverter

`./uninstall.sh` restaura o backup mais recente do `~/.claude`
(`~/.infinite-os-backup-<data>`).
