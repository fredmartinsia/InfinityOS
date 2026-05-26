# Task: create-business-plan

> **Workflow completo end-to-end para criar um Business Plan rigoroso de qualquer negócio em qualquer país.**

## Quando usar
- O usuário tem ideia, MVP, operação inicial ou negócio existente e quer um BP estruturado para investidor, banco, sócio ou aplicação.
- Use sempre via `/business-plan-chief` (orquestrador) — ele coordena o workflow.

## Pré-requisitos
- Onboarding de 8 perguntas completado
- Checkpoint de fundo perdido em Portugal já respondido (se SIM, parar e rotear para `/capital-chief`)

## Workflow (executado pelo `/business-plan-chief`)

### Fase 1 — Validação (1-2 sessões)
1. **`/steve-blank`** — Mapeia hipóteses críticas. Define plano de Customer Discovery (10-15 entrevistas qualitativas com clientes potenciais reais). Lista perguntas das entrevistas.
2. **`/eric-ries`** — Define o MVP mínimo para validar a hipótese mais arriscada. Define métricas (Innovation Accounting) e critérios objetivos de pivot vs perseverar.

**Entregável da Fase 1:** documento "Hypothesis Validation Plan" com: hipóteses listadas, plano de discovery, MVP especificado, critérios de decisão.

### Fase 2 — Modelo (1 sessão)
3. **`/alexander-osterwalder`** — Preenche Business Model Canvas (9 blocos) + Value Proposition Canvas (Customer Profile + Value Map).

**Entregável:** BMC + VPC em formato visual (texto estruturado em blocos).

### Fase 3 — Mercado (1-2 sessões)
4. **`/bill-aulet`** — Identifica beachhead market. Calcula TAM (top-down + bottom-up). Define End User Profile, persona, DMU. Lista próximos 10 clientes-alvo.
5. **`/michael-porter`** — Aplica 5 Forças ao setor. Mapeia cadeia de valor. Escolhe estratégia genérica (Cost Leadership / Differentiation / Focus). Lista e analisa 5-10 concorrentes diretos.

**Entregável:** "Market Analysis Dossier" com TAM/SAM/SOM, beachhead identificado, 5 Forças do setor, concorrentes mapeados, estratégia escolhida.

### Fase 4 — Defensibilidade (1 sessão)
6. **`/peter-thiel`** — Responde 7 Perguntas de Zero to One. Identifica o "secret" do negócio. Mapeia características de monopólio futuro (Proprietary Tech / Network Effects / Economies of Scale / Branding). Avalia se a posição será defensável em 10 anos.

**Entregável:** "Defensibility Analysis" com 7 perguntas respondidas + plano para construir moat.

### Fase 5 — Financeiro (2 sessões)
7. **`/aswath-damodaran`** — CAPEX detalhado por categoria. OPEX recorrente. Projeções 5 anos (P&L + Cash Flow simplificado). DCF com WACC ajustado ao país. Sensibilidade (3 cenários: pessimista, base, otimista). Payback estimado. Valuation indicativa.

**Entregável:** "Financial Plan" com planilha conceitual de CAPEX, projeções 5 anos, DCF, sensibilidade.

### Fase 6 — Consolidação (1 sessão)
8. **`/business-plan-chief`** — Consolida todos os outputs em Business Plan de 10 seções:
   1. Executive Summary (2 páginas)
   2. Empresa / Promotor
   3. Análise de Mercado (Aulet + Porter)
   4. Modelo de Negócio (Osterwalder)
   5. Estratégia Competitiva (Porter + Thiel)
   6. Plano Operacional (CAPEX/infraestrutura/processos)
   7. Time + Plano de Pessoas
   8. Plano Financeiro (Damodaran)
   9. Análise de Risco + Mitigações
   10. Apêndices (pesquisas primárias, currículos, cartas de intenção)

**Entregável final:** Business Plan completo em pt-BR ou pt-PT (escolha do usuário), em formato Markdown estruturado pronto para conversão a PDF.

## Quality Gates
- [ ] Onboarding completo (8 perguntas)
- [ ] Checkpoint de fundo perdido respondido
- [ ] Cada fase validada pelo chefe antes da próxima
- [ ] Sem placeholders / TODO no BP final
- [ ] Citações e dados marcados com fonte ou "PESQUISA SECUNDÁRIA NECESSÁRIA"
- [ ] BP final passa pelo `checklists/output-quality.md`

## Adaptações por contexto
- **Negócio físico** (loja, restaurante, hotel): CAPEX inclui imóvel, reforma, equipamento. Operacional inclui staff e horários.
- **Negócio digital** (SaaS, app): CAPEX inclui desenvolvimento, infra cloud. Operacional inclui CAC/LTV detalhado.
- **E-commerce:** mix de físico (estoque, logística) + digital (plataforma, ads). Take-rate e contribution margin críticos.
- **Indústria:** CAPEX dominante. Importância de cadeia de suprimentos, regulações ambientais.

## Tempo estimado
- Negócio simples / single product: 6-10 horas distribuídas em 6-8 sessões.
- Negócio complexo / multi-vertical: 15-25 horas, 10-15 sessões.

## Output esperado
Business Plan final pronto para:
- Pitch a investidor (VC, anjo)
- Apresentação a banco para crédito
- Submissão a aceleradora
- Estruturação societária + alinhamento de sócios
- Aplicação a fundo de financiamento (se NÃO for em Portugal — caso seja, usar `/capital-chief`)
