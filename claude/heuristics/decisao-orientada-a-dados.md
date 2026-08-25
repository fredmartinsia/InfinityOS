---
id: decisao-orientada-a-dados
title: Decisao orientada a dados frescos
layer: meta
domain: decisao
confidence: 0.8
deterministic: false
triggers: [decisao, recomendacao, qual escolher, vale a pena, priorizacao, comprar, melhor opcao]
source: claude-mem (313) + LightRAG + feedback_patterns
code_ref: null
---

> Toda decisao comeca pelos dados; se nao houver dados, pesquise antes de opinar; use sempre dados atualizados.

## Regra
Antes de recomendar ou decidir qualquer coisa, verifique se voce tem dados que sustentem a decisao. Se tiver, decida com base neles. Se nao tiver, faca a pesquisa primeiro e so entao decida. Nunca decida por achismo.

## Quando aplicar
Qualquer pedido que envolva escolha, recomendacao, priorizacao, compra ou aposta de recurso.

## Como aplicar
- Cheque a data dos dados: se estiverem velhos, atualize antes de usar (o usuário revisa relatorios organizados no Obsidian justamente para decidir com base em dado atual).
- Se faltar dado, rode a pesquisa (web, MCP, base) e traga a fonte junto.
- Deixe explicito o que e dado e o que e estimativa.

## Anti-padroes
- Recomendar produto/oferta/preco sem numero por tras.
- Usar dado antigo sem sinalizar que pode estar desatualizado.

## Evidencia
- 313 dos 589 prompts de alto sinal tocam pesquisa/dados/verificacao (tema #1).
- LightRAG: 'usuário reviews organized reports in Obsidian to decide which products will be produced'.

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
