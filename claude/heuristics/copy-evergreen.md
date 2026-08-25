---
id: copy-evergreen
title: Copy evergreen, sem hardcode efemero
layer: copy
domain: copy
confidence: 0.6
deterministic: false
triggers: [copy, conteudo, numeros, quantidade, estatistica]
source: instinto existente (feedback_patterns)
code_ref: null
---

> Prefira formulacoes reutilizaveis que nao exijam atualizacao a cada uso; abstraia numeros especificos em variavel/placeholder claro.

## Regra
Ao criar copy/conteudo com numeros especificos, prefira formulacoes que funcionem independente do numero exato, para nao gerar retrabalho a cada atualizacao. Se precisar do dado concreto, deixe-o isolado e facil de trocar.

## Quando aplicar
Copy/conteudo com dados que mudam com o tempo.

## Como aplicar
- Use variavel/placeholder claro em vez de numero cravado no meio da frase.

## Anti-padroes
- 'X mil participantes' cravado que precisa reescrever toda vez.

## Evidencia
- 'muda pra nao ter que adicionar essa quantidade de x mil; coloca algo reutilizavel' (verbatim).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
