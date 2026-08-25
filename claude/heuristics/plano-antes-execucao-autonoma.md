---
id: plano-antes-execucao-autonoma
title: Plano antes, execucao autonoma depois
layer: meta
domain: workflow
confidence: 0.8
deterministic: false
triggers: [tarefa grande, projeto, monta um plano, pode seguir, executa ate o fim]
source: claude-mem (208+69) + work_style
code_ref: null
---

> Analise, apresente um plano para aprovar; depois de aprovado, execute ate o fim sem pedir confirmacao a cada passo, e entregue relatorio enxuto.

## Regra
Para trabalho nao trivial: primeiro analise e proponha um plano detalhado para o usuário aprovar. Depois do 'pode seguir', execute de ponta a ponta sem interromper para confirmacoes, agrupando eventuais perguntas. No fim, entregue resultado com relatorio curto, nao verboso.

## Quando aplicar
Tarefas multi-etapa, projetos, qualquer execucao longa.

## Como aplicar
- Fase 1: analise + plano para aprovacao.
- Fase 2 (pos-aprovacao): execucao silenciosa, sem pedir 1/2 a cada acao.
- Para decisoes reversiveis de baixo risco, execute e reporte. Para irreversiveis/destrutivas, confirme.

## Anti-padroes
- Pedir confirmacao a cada passo depois do plano aprovado.
- Entregar relatorio intermediario verboso quando ele pediu execucao silenciosa.

## Evidencia
- 'monte um plano de acao completo... apos eu aprovar, voce consiga ir ate o final executando todas as acoes sem precisar ficar me pedindo confirmacao' (verbatim).
- 208 prompts tocam planejamento; 69 tocam autonomia; 78 prompts triviais de 'pode seguir'.

## Aplicacao deterministica
N/A: requer julgamento do modelo (nao e mecanicamente verificavel).
