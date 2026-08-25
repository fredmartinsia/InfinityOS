---
id: link-direto-na-entrega
title: Traga o link direto na entrega
layer: entrega
domain: entrega
confidence: 0.7
deterministic: false
triggers: [pesquisa, buscar produto, comprar, passagem, encontrar, onde acho]
source: claude-mem (167) + memoria
code_ref: null
---

> Em qualquer pesquisa (voo, produto, ferramenta), entregue o link de compra/acesso ja na primeira resposta, para ser pratico.

## Regra
Quando o usuário pede para buscar/comprar algo, traga o link direto de compra ou acesso ja na primeira resposta, sem obrigar ele a pedir de novo.

## Quando aplicar
Pesquisas de voos, produtos, ferramentas, servicos.

## Como aplicar
- Inclua a URL clicavel do item, nao so o nome.
- Se houver varias opcoes, link em cada uma.

## Anti-padroes
- Descrever o produto sem dar o link.
- Deixar o usuário pedir o link depois.

## Evidencia
- 167 prompts tocam link/compra/acesso. Memoria dedicada 'feedback-entregar-link-em-pesquisas'.

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
