# Task: route-to-funding

> **Handoff documentado para `/capital-chief` quando o usuário vai aplicar a fundos públicos portugueses.**

## Quando usar
- Resposta SIM ao checkpoint do `/business-plan-chief` sobre fundos em Portugal
- Usuário menciona explicitamente: PRR, Portugal 2030, BPF, IFD, RFAI, SIFIDE, fundo perdido em PT

## Pré-requisitos
- Onboarding de 8 perguntas do `/business-plan-chief` completado
- Confirmação do usuário de que de fato vai aplicar a fundos PT

## Workflow

### Etapa 1 — Pacote de contexto
O `/business-plan-chief` consolida um sumário do que já se sabe:

```markdown
# Contexto pré-handoff para capital-squad

**Tipo de negócio:** [resumo de 2-3 linhas]
**Setor:** [setor específico]
**Estágio:** [ideia / MVP / operacional / escalando]
**Localização:** [cidade + país]
**Mercado-alvo:** [geografia + B2B/B2C/B2B2C]
**Capital próprio do promotor:** [ordem de grandeza]
**Capital total estimado necessário (24 meses):** [valor + breakdown CAPEX/working]
**Modelo de receita:** [como cobra + ticket médio + margens preliminares]
**Time:** [N pessoas, especialidades, gaps]
**Prazo desejado para o BP:** [data ou marco]
**Ambição 5 anos:** [cenário de sucesso descrito]

**Sinalização para fundos:**
- Tipo de fundo de interesse: [PRR / PT 2030 / BPF / IFD / RFAI / SIFIDE / outro]
- Aviso ou janela específica em mente: [se houver]
- Já tem consultor especializado contratado? [SIM/NÃO]
- Já tem advogado contratado? [SIM/NÃO]

**Próximos passos recomendados:**
1. Acionar /capital-chief para discovery específico de captação (50 perguntas, 6 blocos)
2. /capital-chief vai mapear elegibilidade real, calcular majorações, sugerir estrutura societária
3. Após output do capital-squad, retornar ao /business-plan-chief para consolidar BP final
```

### Etapa 2 — Comunicação ao usuário
O `/business-plan-chief` apresenta:

```
🎯 HANDOFF PARA CAPITAL-SQUAD

Você sinalizou intenção de aplicar a fundos portugueses. Existe um squad
especialista nisso: o capital-squad, com 7 portugueses reais (3 ex-ministros,
1 sócio PLMJ, 1 catedrático Nova SBE, etc.) que conhecem cada aviso PT 2030,
cada linha BPF e cada majoração ativável.

Em vez de duplicarmos esse trabalho, vou:
1. Salvar o contexto que já levantamos (vou gerar um sumário)
2. Encerrar essa sessão de business-plan
3. Recomendar que você acione: /capital-chief

Quando o capital-squad finalizar o trabalho deles (vai produzir um dossiê
de captação específico), você pode me chamar de volta com /business-plan-chief
para integrar tudo num Business Plan completo final.

Confirma a transição? [SIM / NÃO / "Quero fazer os dois em paralelo"]
```

### Etapa 3 — Casos especiais

**Caso A: Usuário quer fazer os dois em paralelo**
- Possível, mas o `/business-plan-chief` avisa que pode haver retrabalho
- Recomenda começar pelo `/capital-chief` (output é mais específico)
- Depois consolida no `/business-plan-chief`

**Caso B: Usuário muda de ideia (não vai aplicar)**
- Retornar ao Passo 4 do workflow do `/business-plan-chief` (roteamento dos 7 especialistas)
- Continuar BP completo

**Caso C: Aplicação a fundos NÃO portugueses (BNDES, FINEP, EU não-PT, SBA US)**
- `/business-plan-chief` segue com BP completo
- Adapta o output para o formato/idioma do programa (BNDES exige formato específico, EU Horizon Europe outro, etc.)

## Outputs entregáveis
- Sumário de contexto pré-handoff (texto estruturado)
- Recomendação de comando: `/capital-chief`
- Reminder de retorno após capital-squad (`/business-plan-chief` para consolidar)

## Quality Gates
- [ ] Sumário pré-handoff tem TODOS os 8 campos preenchidos
- [ ] Usuário confirma explicitamente a transição (SIM)
- [ ] `/business-plan-chief` registra na memória do projeto que houve handoff
- [ ] Não há duplicação de trabalho

## Por que isso importa
O `capital-squad` foi projetado especificamente para o contexto português (regulação, programas, instituições). O `business-plan-squad` é universal — bom para qualquer país. Para Portugal-com-fundos, o capital-squad é mais profundo. Não duplicar.
