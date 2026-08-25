---
id: qualidade-acima-de-economia
title: Qualidade acima de economia (mas economize por arquitetura)
layer: meta
domain: decisao
confidence: 0.75
deterministic: false
triggers: [economia de token, custo, modelo barato, otimizar custo]
source: work_style + claude-mem
code_ref: null
---

> Economizar token e bom, mas nunca a ponto de prejudicar a qualidade; use o modelo certo para a tarefa certa, e economize movendo trabalho para codigo e modelos baratos, nao cortando profundidade.

## Regra
Busque eficiencia de custo, mas jamais sacrificando profundidade, nuance ou precisao. A economia vem da arquitetura (codigo para o deterministico, modelo barato para o braçal, modelo caro para o julgamento), nao de entregar menos.

## Quando aplicar
Qualquer decisao de custo/modelo.

## Como aplicar
- Roteie: deterministico -> codigo; volumoso mecanico -> modelo barato/local; julgamento -> modelo top.
- Se o modelo top e essencial para a qualidade, use o modelo top.

## Anti-padroes
- Usar modelo fraco em tarefa critica so para economizar e entregar resultado raso.

## Evidencia
- 'e legal pensar na economia de token, mas eu nao quero focar na economia a ponto de prejudicar a qualidade' (verbatim, work_style).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
