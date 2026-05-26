# Task: review

> Revisão final de qualidade antes de entregar ao usuário. Roda os checklists e produz um veredito claro.

## Quando usar

- Antes de entregar qualquer output do squad
- Quando o usuário diz "tá pronto?" e o chief quer ter certeza
- Antes de deploy em produção
- Como sanity check após mudanças significativas

## Pré-requisitos

1. Output do squad existe e está rodando localmente
2. Checklists `output-quality.md` e `motion-quality.md` estão acessíveis

## Workflow (paralelo — 3 reviewers)

### Reviewer 1 — Rauno Freiberg: Output quality

**O que faz:**
- Roda o checklist `checklists/output-quality.md` item a item
- Para cada item: PASS / FAIL / NA com nota
- Identifica top 3 melhorias que mais elevam qualidade
**Saída:** `review-output-quality.md`

### Reviewer 2 — Emil Kowalski: Motion quality

**O que faz:**
- Roda o checklist `checklists/motion-quality.md` item a item
- Verifica cada animação: tem propósito? easing certo? interruptível?
- Sinaliza animações decorativas para remoção
**Saída:** `review-motion-quality.md`

### Reviewer 3 — Josh Comeau: A11y final

**O que faz:**
- Roda axe-core
- Testa com keyboard somente (sem mouse)
- Roda screen reader em pelo menos uma tela completa
- Confirma prefers-reduced-motion alternativa funciona
**Saída:** `review-a11y.md`

## Síntese — frontend-chief

Após os 3 reviewers, o chief consolida:

```
🎯 Review Final

Output Quality (Rauno):     {N pass / M fail}
Motion Quality (Emil):       {N pass / M fail}
A11y (Josh):                 {N violations}

Top 3 melhorias:
1. {melhoria}
2. {melhoria}
3. {melhoria}

Veredito: 
[A] Pronto para entrega — passa nos 3 checklists com folga
[B] Pronto após fixes críticos — corrigir os {N} críticos antes de entregar
[C] Não pronto — voltar pra etapa anterior do workflow original
```

## Critérios de aceite (do review)

- Os 3 reports existem e estão preenchidos
- Veredito é claro (A, B ou C — sem "talvez")
- Top 3 melhorias estão priorizadas

## Como usar fora de workflow

Se o usuário pediu o squad pra fazer X e quer só uma segunda opinião antes de deploy:
```
/frontend-chief
*review {caminho do output}
```

O chief roda esse workflow em paralelo nos 3 reviewers e devolve o veredito em ~5 minutos.
