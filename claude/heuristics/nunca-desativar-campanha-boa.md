---
id: nunca-desativar-campanha-boa
title: Nunca desative uma campanha boa sem autorizacao
layer: dominio
domain: trafego
confidence: 0.85
deterministic: false
triggers: [campanha, ads, anuncio, pausar, desativar, trafego, meta ads, google ads]
source: claude-mem (Qwen)
code_ref: null
---

> Em trafego pago, nunca pause ou desative uma campanha com bom desempenho sem autorizacao explicita do usuÃ¡rio; ele pediu essa regra apos perder performance.

## Regra
Ao operar contas de trafego, nunca pause/desative uma campanha que esta performando bem sem confirmacao explicita do usuÃ¡rio. Antes de qualquer acao que reduza veiculacao de uma campanha vencedora, pare e pergunte.

## Quando aplicar
Gestao de campanhas de trafego (Meta, Google, etc).

## Como aplicar
- Antes de pausar/reduzir, cheque se a campanha esta performando; se sim, confirme com o usuÃ¡rio.
- Documente por que a acao foi tomada.

## Anti-padroes
- Desativar automaticamente uma campanha vencedora e ferrar o desempenho.

## Evidencia
- 'cria uma regra ai pra nunca mais desativar uma campanha boa igual aconteceu com essa da Alexa para nao ferrar o desempenho' (verbatim, Qwen).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
