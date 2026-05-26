# Task: validate-hypothesis

> **Plano de Customer Discovery + MVP design para validar hipóteses críticas antes de escrever o BP.**

## Quando usar
- O usuário ainda está em fase de ideia ou MVP early-stage
- Cuidado: se já tem operação rodando, esta task é menos crítica (mas ainda útil para novos pivots)

## Workflow

### Etapa 1 — Mapear hipóteses (Steve Blank)
Acionar `/steve-blank`. Ele vai:
1. Listar TODAS as hipóteses críticas do negócio (não óbvias) em 4 categorias:
   - **Cliente:** quem é, onde está, quanto custa achar
   - **Problema:** intensidade, frequência, alternativas atuais
   - **Solução:** o produto/serviço resolve de verdade?
   - **Modelo:** o cliente paga? Quanto? Com que frequência?
2. Priorizar pelas mais arriscadas (se essa hipótese cair, o negócio cai)
3. Definir plano de **Customer Discovery**:
   - 10-15 entrevistas qualitativas
   - Quem entrevistar (perfil específico, não amigos)
   - Como achar essas pessoas (LinkedIn, comunidades, eventos)
   - Roteiro semiestruturado (10-12 perguntas abertas)

### Etapa 2 — Definir MVP (Eric Ries)
Acionar `/eric-ries`. Ele vai:
1. Identificar o **menor experimento** que testa a hipótese mais arriscada
2. Decidir tipo de MVP:
   - **Concierge MVP:** entregar manualmente o serviço para 1-5 clientes
   - **Wizard of Oz MVP:** UI parece automatizada mas backend é manual
   - **Landing page MVP:** medir interesse via opt-ins/pre-orders
   - **Smoke test:** anúncio + CTR para validar demanda
   - **Functional MVP:** versão técnica enxuta com 1 feature core
3. Definir métricas (Actionable, não Vanity)
4. Definir critério objetivo de sucesso/falha do experimento
5. Definir cohort para análise de aprendizado
6. Cronograma: ciclo Build-Measure-Learn de 2-4 semanas

## Outputs entregáveis

### A) Hypothesis Validation Plan (Blank)
- Lista priorizada de hipóteses (top 5)
- Plano de discovery (10-15 entrevistas)
- Roteiro de entrevista
- Lista de potenciais entrevistados
- Cronograma (3-4 semanas)

### B) MVP Specification (Ries)
- Hipótese mais arriscada (a ser testada primeiro)
- Tipo de MVP escolhido + justificativa
- Métricas (3-5 actionable metrics)
- Critérios objetivos: "Se X acontecer = perseverar; Se Y acontecer = pivot"
- Cohort design
- Cronograma do ciclo BML (2-4 semanas)

## Quality Gates
- [ ] Hipóteses são específicas (não "as pessoas vão adorar")
- [ ] Entrevistados NÃO são amigos do fundador
- [ ] Roteiro é semiestruturado (perguntas abertas, não fechadas)
- [ ] MVP tem 1 hipótese principal (não 5)
- [ ] Critério de sucesso é numérico (não "se for promissor")
- [ ] Cronograma é curto (2-4 semanas, não 6 meses)

## O que vem depois
Após o discovery (com dados em mãos), retornar ao `/business-plan-chief` para incorporar os aprendizados no BMC (Osterwalder), TAM (Aulet) e estratégia (Porter).

## Anti-pattern comum
"Vou construir o produto completo e depois validar." → NÃO. O ponto é validar ANTES de construir. Se o BP já está sendo escrito sem hipóteses testadas, ele está sendo escrito sobre areia.
