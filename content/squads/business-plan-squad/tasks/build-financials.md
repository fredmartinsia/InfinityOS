# Task: build-financials

> **Construção do plano financeiro completo: CAPEX + OPEX + Projeções 5 anos + DCF + Valuation.**

## Quando usar
- Standalone para gerar planilha financeira conceitual
- Parte final do workflow `create-business-plan`

## Pré-requisitos
- Modelo de receita definido (Osterwalder)
- TAM/SAM/SOM dimensionado (Aulet)
- Estratégia genérica escolhida (Porter)
- LTV/COCA preliminar (Aulet)

## Workflow

Acionar `/aswath-damodaran`. Ele vai construir em 6 etapas:

### Etapa 1 — CAPEX inicial
Decompor o investimento inicial em categorias:
- **Ativos tangíveis** (imóveis, equipamentos, móveis, máquinas)
- **Ativos intangíveis** (software proprietário, marca registrada, patentes, licenças)
- **Working capital inicial** (estoque inicial, garantias, depósitos)
- **Pré-operacionais** (consultoria, branding, marketing de lançamento, jurídico)

Separar **CAPEX único** de **CAPEX recorrente** (manutenção anual ≈ D&A).

### Etapa 2 — OPEX recorrente
Listar custos operacionais mensais:
- **Fixos:** aluguel, salários base, software, contabilidade
- **Variáveis:** custo dos produtos vendidos (COGS), comissões, marketing variável
- **Semi-variáveis:** energia, suporte ao cliente

### Etapa 3 — Projeções 5 anos
Construir:
- **DRE/P&L simplificado:** Receita → COGS → Gross Profit → OPEX → EBITDA → D&A → EBIT → Impostos → Net Income
- **Cash Flow:** EBIT × (1-T) + D&A - CAPEX - ΔWorking Capital = FCF
- **Premissas explícitas:** crescimento de receita ano-a-ano, margem bruta, ramp-up de OPEX

### Etapa 4 — WACC ajustado ao país
- **Risk-free rate:** treasury de 10 anos do país (ou US se moeda forte)
- **ERP (Equity Risk Premium):** usar dataset Damodaran do país específico
- **Beta:** unlevered de comparáveis, re-alavancado para estrutura de capital
- **Cost of Debt:** taxa de mercado para a empresa
- **WACC = E/V × Re + D/V × Rd × (1-T)**

### Etapa 5 — DCF e Terminal Value
- Descontar FCF de cada ano a WACC
- Terminal Value via Gordon: TV = FCFₙ₊₁ / (WACC - g), com **g ≤ GDP nominal de longo prazo** (~2-3%)
- Enterprise Value = soma dos FCFs descontados + TV descontado
- Equity Value = EV - Net Debt

### Etapa 6 — Sensibilidade + Payback
- **3 cenários:** Pessimista / Base / Otimista — variar receita, margem, WACC
- **Sensibilidade individual:** ±20% em premissas-chave (CAC, churn, ticket médio)
- **Payback simples:** quando FCF acumulado = CAPEX inicial
- **Payback descontado:** quando FCF descontado acumulado = CAPEX

## Outputs entregáveis
1. **Planilha CAPEX detalhada** (categorias e valores)
2. **Planilha OPEX mensal** (rampa de 12 meses + cruise)
3. **DRE 5 anos**
4. **Cash Flow 5 anos**
5. **DCF + Valuation indicativa**
6. **Tabela de sensibilidade**
7. **Payback estimado**

## Quality Gates
- [ ] CAPEX separa único de manutenção
- [ ] OPEX tem rampa realista (não constante desde mês 1)
- [ ] Crescimento de receita justificado por premissa (não "porque sim")
- [ ] WACC usa dataset Damodaran do país específico
- [ ] Terminal growth ≤ GDP nominal de longo prazo (NUNCA 5%+)
- [ ] 3 cenários explicitam premissas que mudam
- [ ] Sensibilidade identifica 2-3 variáveis mais críticas
