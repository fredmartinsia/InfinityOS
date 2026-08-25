# Cliente: Codex CLI

O Codex CLI hoje suporta prompts customizados (slash commands) via
`~/.codex/prompts/*.md` com frontmatter `description`, e ja le skills no
formato aberto `SKILL.md` em diretorios como `~/.agents/skills`. Ele nao tem
o sistema de hooks do Claude Code (nada equivalente a PreToolUse/Stop/etc
roda automaticamente), mas skills e prompts sim, entao boa parte do harness
Opensquad (agentes de squad, skills) chega ao Codex de forma nativa.

## Instalacao automatica

```bash
./clients/codex/install-codex.sh
```

O script:
1. Converte cada agente de `content/squads/<squad>/agents/<agente>.md` num
   prompt Codex em `~/.codex/prompts/<squad>-<agente>.md` (frontmatter
   `description` + o corpo original do agente).
2. Cria um symlink `~/.agents/skills` apontando para `claude/skills/` do
   repo, para o Codex ler as skills nativamente.
3. Escreve ou anexa `~/.codex/AGENTS.md` com as regras do harness
   (`claude/heuristics/AGENTS.md`), dentro de um bloco marcado para nao
   duplicar em execucoes futuras.

E idempotente: rodar de novo atualiza os prompts e o bloco de regras sem
duplicar nada, e qualquer arquivo/symlink que ja exista no caminho de
destino e salvo com backup (`.bak-AAAAMMDD-HHMMSS`) antes de ser sobrescrito.

## Usar um prompt de squad no Codex

Depois de instalar, dentro do Codex CLI:

```
/<squad>-<agente>
```

Exemplo: `/frontend-squad-olivier-larose` carrega o mesmo agente que no
Claude Code.

## Usar um clone (fora de squad)

1. Escolha o clone em `content/clones/<clone>/` (ou `<vault>/CLONES/<clone>/`).
2. Copie o conteudo de `*_02_SYSTEM_PROMPT_CHATGPT.md` (versao compacta,
   ate 8k) ideal para a janela do Codex.
3. Cole como instrucao de sistema/contexto inicial e converse.

## Roteamento

Use o roteador para decidir quando vale chamar o Codex (validacao cruzada,
raciocinio fino):

```bash
python3 ~/.infinity-os/route.py --type cross_validation
# resultado: codex  [codex/default]
```

## O que ainda nao existe no Codex

- Hooks automaticos (PreToolUse, Stop, SessionStart etc): sem equivalente.
  Regras deterministicas do harness (por exemplo, o bloqueio de travessao)
  nao rodam sozinhas no Codex, precisam ser reforcadas via AGENTS.md/prompt.
- Statusline customizada.

Para squads, comece pelo prompt `<squad>-<squad>-chief` (a logica de
orquestracao) e traga os agentes especialistas conforme a necessidade.
