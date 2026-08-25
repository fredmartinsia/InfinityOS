---
id: dados-reais-sem-placeholder
title: Dados reais, nunca placeholder ou link quebrado
layer: entrega
domain: entrega
confidence: 0.7
deterministic: false
triggers: [relatorio, entrega, pagina, copy, links, imagens]
source: instinto existente (feedback_patterns)
code_ref: links-validos-http-200
---

> Todo link e imagem do deliverable tem que funcionar de verdade; nunca use placeholder, dado ou URL ficticio; se algo e estimativa, marque como tal.

## Regra
Antes de entregar qualquer relatorio, pagina ou copy, valide que todos os links abrem e todas as imagens referenciam arquivos reais. Nunca gere dado/URL ficticio para 'completar'. Estimativas devem ser marcadas explicitamente.

## Quando aplicar
Toda entrega com links, imagens ou numeros.

## Como aplicar
- Valide links (rode o script check_links quando houver muitos).
- Copie imagens para as pastas corretas e referencie com path validado.

## Anti-padroes
- Entregar com link que nao abre.
- Inventar dado so para preencher.

## Evidencia
- 'estou clicando e nao esta abrindo' e 'as imagens nao estao sendo referenciadas' (verbatim, multiplos projetos).

## Aplicacao deterministica
Aplicada/apoiada por codigo: `links-validos-http-200`. Onde possivel, o codigo executa a regra; o modelo nao precisa lembrar dela.
