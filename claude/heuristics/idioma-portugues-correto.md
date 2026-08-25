---
id: idioma-portugues-correto
title: Portugues correto por padrao
layer: deterministico
domain: estilo
confidence: 0.8
deterministic: true
triggers: [*]
source: config + claude-mem (36)
code_ref: null
---

> Responda em portugues com ortografia e acentuacao corretas; pt-BR por padrao, pt-PT quando o publico for de Portugal. Ja aplicado via config language.

## Regra
Comunique em portugues correto, com acentos e diacriticos. Use pt-BR por padrao; use pt-PT quando o deliverable for para publico de Portugal (o usuÃ¡rio sinaliza). Nunca troque acento por ASCII.

## Quando aplicar
Toda comunicacao e deliverable.

## Como aplicar
- Config settings.json language=Portugues ja garante o idioma base.
- Ajuste pt-BR vs pt-PT conforme o publico do deliverable.

## Anti-padroes
- Escrever 'nao' por 'nao' sem acento em deliverable final.
- Misturar pt-PT em copy que devia ser pt-BR.

## Evidencia
- 36 prompts tocam idioma. 'a copy precisa ser em portugues de Portugal, falando em euro' vs 'muda a copy para portugues Brasil' (verbatim).

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
