# Cliente: Antigravity

Mesmo modelo do Codex: o InfinityOS é consumido via **prompts portáveis** dos clones
e squads, já que o Antigravity tem seu próprio modelo de extensões.

## Usar um clone

1. Abra `content/clones/<clone>/<clone>_02_SYSTEM_PROMPT_CLAUDE.md` (versão completa)
   ou a `*_CHATGPT.md` (compacta).
2. Cole como contexto/instrução de sistema no Antigravity.
3. Para um time, comece pelo `content/squads/<squad>/agents/<squad>-chief.md`.

## Roteamento

O `~/.infinity-os/route.py` continua útil para decidir o modelo por tarefa — o
resultado (Gemini/Qwen/Codex/Claude) orienta qual backend acionar no Antigravity.

> O conhecimento do vault (RAG) é nativo do Claude Code; no Antigravity, traga
> manualmente as notas relevantes do vault ao contexto quando precisar.
