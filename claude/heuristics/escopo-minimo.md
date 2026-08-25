---
id: escopo-minimo
title: Escopo minimo, nao implemente o que nao foi pedido
layer: entrega
domain: entrega
confidence: 0.7
deterministic: false
triggers: [implementar, criar, adicionar, montar]
source: instinto existente (feedback_patterns)
code_ref: null
---

> Faca exatamente o que foi pedido; nao adicione features nao solicitadas; se algo parece faltar, pergunte antes de adicionar.

## Regra
Implemente estritamente o escopo pedido. Nao expanda por conta propria. Se identificar algo faltando, pergunte antes de adicionar. Prefira deixar um campo vazio mas preparado a implementar a mais.

## Quando aplicar
Toda implementacao ou criacao.

## Como aplicar
- Entregue o essencial pedido.
- Liste 'possiveis extensoes' em vez de ja implementa-las.

## Anti-padroes
- Adicionar features bonus que atrasam o essencial.
- Inferir escopo alem do pedido.

## Evidencia
- 'por enquanto pode deixar esse campo em branco' e 'nao precisa incluir a parte da participacao dos socios' (verbatim).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
