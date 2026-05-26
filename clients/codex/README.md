# Cliente: Codex CLI

O Codex não tem o sistema de hooks/skills do Claude Code, então o consumo é via
**prompts portáveis** (os system prompts dos clones) + o **roteador**.

## Usar um clone no Codex

1. Escolha o clone em `content/clones/<clone>/` (ou `<vault>/CLONES/<clone>/`).
2. Copie o conteúdo de `*_02_SYSTEM_PROMPT_CHATGPT.md` (versão compacta, ≤8k) —
   ideal para a janela do Codex.
3. Cole como instrução de sistema/contexto inicial e converse.

## Roteamento

Use o roteador para decidir quando vale chamar o Codex (validação cruzada,
raciocínio fino):

```bash
python3 ~/.infinity-os/route.py --type cross_validation
# → codex  [codex/default]
```

## Dica

Para squads, comece pelo `agents/<squad>-chief.md` (a lógica de orquestração) e
traga os agentes especialistas conforme a necessidade.
