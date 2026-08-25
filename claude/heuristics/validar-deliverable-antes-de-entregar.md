---
id: validar-deliverable-antes-de-entregar
title: Teste o deliverable antes de entregar
layer: entrega
domain: entrega
confidence: 0.7
deterministic: false
triggers: [entrega, esta pronto, html, pagina, site, relatorio]
source: claude-mem (relatorio-visual + placeholder-real)
code_ref: links-validos-http-200
---

> Antes de dizer que esta pronto, exercite o deliverable: link abre (HTTP 200), HTML e responsivo em mobile, o conteudo esta completo e sem truncamento.

## Regra
Nao entregue sem exercitar. Cheque: links respondem, layout funciona em mobile (o usuário cobra responsividade), nada esta truncado, todos os elementos prometidos estao presentes (mockup, botoes, tipografia).

## Quando aplicar
Entrega de paginas, sites, relatorios HTML, qualquer artefato navegavel.

## Como aplicar
- Rode o validador de links quando houver URLs.
- Confira o HTML em viewport mobile.
- Cheque completude contra o que foi prometido.

## Anti-padroes
- Dizer 'pronto' sem abrir o resultado.
- Entregar HTML que quebra no celular.

## Evidencia
- 'o HTML em mobile nao ta funcionando, preciso que corrija pra ficar responsivo' (verbatim, Qwen).
- 'nao trouxe o mockup, nao trouxe os botoes, nao trouxe a tipografia' (verbatim).

## Aplicacao deterministica
Aplicada/apoiada por codigo: `links-validos-http-200`. Onde possivel, o codigo executa a regra; o modelo nao precisa lembrar dela.
