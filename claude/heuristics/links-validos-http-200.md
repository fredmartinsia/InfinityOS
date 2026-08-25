---
id: links-validos-http-200
title: Links validos (HTTP 200) antes de entregar
layer: deterministico
domain: entrega
confidence: 0.6
deterministic: true
triggers: [relatorio com links, entrega, pagina, lista de produtos]
source: feedback_patterns + claude-mem
code_ref: check_links.py
---

> Todo link em deliverable deve responder antes da entrega; verificado por script (check_links.py), nao por confianca no LLM.

## Regra
Antes de entregar qualquer material com links, rode o validador que checa HTTP 200 em cada URL. Se algum falhar, corrija antes de dizer que esta pronto.

## Quando aplicar
Entregas com URLs (relatorios, listas de produtos, paginas).

## Como aplicar
- Rode check_links.py sobre o arquivo/relatorio.
- Corrija ou remova links quebrados.

## Anti-padroes
- Entregar confiando que o link funciona sem testar.

## Evidencia
- 'acessei o link que me informou mas nao esta funcional' (verbatim). Recorrente em multiplos projetos.

## Aplicacao deterministica
Aplicada/apoiada por codigo: `check_links.py`. Onde possivel, o codigo executa a regra; o modelo nao precisa lembrar dela.
