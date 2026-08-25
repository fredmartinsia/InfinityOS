---
id: clones-completos
title: Acione clones completos, nao so o system prompt
layer: copy
domain: clones
confidence: 0.7
deterministic: false
triggers: [aciona o clone, usa o clone, clone do, persona]
source: instinto existente (feedback_patterns)
code_ref: null
---

> Quando pedir 'aciona o clone X', carregue e use TODOS os arquivos do clone (frameworks, heuristicas, exemplos), nao apenas o SYSTEM_PROMPT.

## Regra
Ao acionar um clone/persona, carregue todos os arquivos dele em ~/Documents/Obsidian Vault/CLONES/{nome}/ e aplique frameworks, heuristicas e exemplos reais, nao so o estilo de escrita.

## Quando aplicar
Qualquer acionamento de clone/persona.

## Como aplicar
- Leia a pasta inteira do clone.
- Aplique os frameworks dele ao problema.

## Anti-padroes
- Usar so o SYSTEM_PROMPT e ignorar os frameworks.

## Evidencia
- 'nao usa so o prompt do Alex; usa tudo la, os frameworks, as heuristicas' (verbatim).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
