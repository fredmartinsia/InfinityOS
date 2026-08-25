---
id: deterministico-vira-codigo
title: O que e deterministico vira codigo, nao LLM
layer: meta
domain: arquitetura
confidence: 0.8
deterministic: false
triggers: [regra, sempre que, toda vez, valida, checa, automatiza, hook, script]
source: claude-mem (137) + workflow_automation_philosophy
code_ref: null
---

> Regra fixa ou verificavel deve ser executada por hook/script (custo zero de token, sempre roda); reserve o LLM e o modelo caro para o que exige julgamento.

## Regra
Ao identificar uma licao que e sempre a mesma e pode ser checada mecanicamente (proibir um caractere, validar link, checar idioma, aplicar formato), proponha e implemente um hook/script em vez de depender do LLM lembrar. Use o modelo caro (Opus/Fable) para planejar e julgar; deixe modelos baratos/locais e codigo fazerem o trabalho braçal.

## Quando aplicar
Sempre que uma orientacao se repete de forma identica e verificavel.

## Como aplicar
- Se a regra e binaria/verificavel: hook em ~/.claude/scripts + entrada no settings.json.
- Se e trabalho volumoso mas mecanico: modelo barato local (qwen via ollama) ou Codex/Gemini CLI.
- So use o modelo caro no que precisa de nuance e qualidade.

## Anti-padroes
- Repetir a mesma instrucao em todo prompt em vez de codificar uma vez.
- Gastar modelo caro em tarefa mecanica.

## Evidencia
- 'pense no que da pra gente fazer em situacoes deterministicas sem perder a qualidade, pro Codex e pro Gemini CLI' (verbatim).
- 137 prompts tocam custo/modelo/determinismo. Regra permanente 'Fable planeja, baratos executam'.

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
