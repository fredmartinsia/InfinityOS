---
id: manual-primeiro
title: Manual primeiro, automatize depois
layer: meta
domain: decisao
confidence: 0.7
deterministic: false
triggers: [automatizar, criar automacao, montar pipeline, escalar processo]
source: LightRAG
code_ref: null
---

> So automatize o que voce ja fez a mao e validou; nao construa automacao para um processo que ainda nao foi provado manualmente.

## Regra
Antes de automatizar um processo, confirme que ele ja foi executado manualmente e deu certo. Se ainda nao foi provado a mao, faca a versao manual primeiro (ou proponha isso) antes de investir em automacao.

## Quando aplicar
Pedidos de automacao, pipeline, escala de processo novo.

## Como aplicar
- Pergunte/verifique: esse fluxo ja rodou a mao com resultado?
- Se nao, proponha validar manual antes de codificar a automacao.

## Anti-padroes
- Automatizar um processo hipotetico que nunca foi testado na pratica.

## Evidencia
- LightRAG: 'Manual Primeiro. Principio: so automatiza o que ja fez a mao; regra pedagogica do usuário'.

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
