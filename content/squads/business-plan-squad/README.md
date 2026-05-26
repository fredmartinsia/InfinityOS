# Business Plan Squad 📋

> **Squad universal para construção de Business Plans rigorosos.**
> 7 especialistas mundiais reais + orquestrador. Funciona para qualquer tipo de negócio (físico, digital, e-commerce, hotelaria, indústria, serviço) em qualquer geografia (Portugal, Brasil, UE, EUA, Dubai, Ásia).
> Rotear para `capital-squad` quando aplicação a fundos públicos portugueses (PRR, PT 2030, BPF).

## 🎯 Objetivo

Levar uma ideia ou negócio existente da pergunta **"vale a pena?"** até um **Business Plan completo, defensável e investível**, combinando:

- 🔍 **Customer Development** (Steve Blank) — validação antes do plano
- ♻️ **Lean Startup** (Eric Ries) — MVP, Build-Measure-Learn, Pivot
- 🎨 **Business Model Canvas + VPC** (Alexander Osterwalder) — modelo visual
- 🧮 **TAM/SAM/SOM disciplinado MIT** (Bill Aulet) — sizing rigoroso
- ♟️ **5 Forças + Estratégia Genérica** (Michael Porter) — competição estrutural
- 💰 **DCF + CAPEX + Valuation NYU** (Aswath Damodaran) — finanças
- 🚀 **Monopólio + Defensibility** (Peter Thiel) — diferenciação radical

## 👥 Equipa

| # | Especialista | Especialidade | Comando |
|---|---|---|---|
| 🎯 | **Business Plan Chief** *(sintético)* | Orquestrador + Onboarding + Roteamento + Consolidação | `/business-plan-chief` |
| 1 | **Steve Blank** | Pai do Customer Development, Lean Startup pioneer | `/steve-blank` |
| 2 | **Eric Ries** | The Lean Startup, MVP, Build-Measure-Learn | `/eric-ries` |
| 3 | **Alexander Osterwalder** | Business Model Canvas + Value Proposition Canvas | `/alexander-osterwalder` |
| 4 | **Bill Aulet** | MIT — Disciplined Entrepreneurship 24 Steps | `/bill-aulet` |
| 5 | **Michael Porter** | Harvard — Competitive Strategy, 5 Forças, Cadeia de Valor | `/michael-porter` |
| 6 | **Aswath Damodaran** | NYU Stern — Dean of Valuation, DCF, CAPEX | `/aswath-damodaran` |
| 7 | **Peter Thiel** | Zero to One — Monopólios, Defensibility, Last Mover | `/peter-thiel` |

**Perfil agregado:** 3 dos maiores pensadores da estratégia de negócios da história (Porter, Thiel, Aulet) + 3 dos maiores autores de empreendedorismo moderno (Blank, Ries, Osterwalder) + a maior autoridade global em valuation (Damodaran).

## 🚀 Como usar

### Opção 1 — Acesso ao orquestrador (recomendado)

```
/business-plan-chief
```

O Business Plan Chief executa o protocolo completo:
1. Lê contexto do projeto ativo (CLAUDE.md, _memoria/, company.md)
2. Faz onboarding profundo (8 perguntas)
3. **Checkpoint crítico:** vai aplicar a fundo perdido em Portugal?
   - **SIM** → handoff documentado para `/capital-chief` (capital-squad)
   - **NÃO** → segue
4. Aciona os 7 especialistas em sequência otimizada
5. Consolida em Business Plan final (10 seções)

### Opção 2 — Acesso direto a especialista

Quando souber exatamente quem deve acionar:

```
/steve-blank          # validação de hipóteses, customer discovery
/eric-ries            # MVP, pivot, Build-Measure-Learn
/alexander-osterwalder # Business Model Canvas, Value Proposition
/bill-aulet           # TAM/SAM/SOM método MIT
/michael-porter       # análise competitiva, 5 Forças
/aswath-damodaran     # DCF, CAPEX, valuation
/peter-thiel          # diferenciação radical, monopólio
```

### Opção 3 — Roteamento para fundos portugueses

```
/capital-chief        # quando saber que vai aplicar a PRR/PT 2030/BPF
```

O `business-plan-chief` faz handoff automático quando detecta a intenção.

## 🗺️ Routing Matrix (referência rápida)

| Pergunta típica | Especialista primário |
|---|---|
| "Tenho uma ideia, vale a pena?" | Steve Blank |
| "Como sei se devo pivotar?" | Eric Ries |
| "Como desenho meu modelo de negócio?" | Alexander Osterwalder |
| "Qual o TAM do meu mercado?" | Bill Aulet |
| "Quem são meus 5 concorrentes mais perigosos?" | Michael Porter |
| "Qual CAPEX para abrir essa operação?" | Aswath Damodaran |
| "Por que esse negócio vai vencer e não ser imitado?" | Peter Thiel |
| "Vou aplicar ao PRR/PT 2030" | → **capital-chief** (capital-squad) |

## 🔄 Workflow do Chefe (resumido)

```
1. Leitura de contexto
   ├─ CLAUDE.md global
   ├─ CLAUDE.md do projeto (se existir)
   └─ Obsidian Vault _memoria/ (se existir)
        ↓
2. Onboarding profundo (8 perguntas)
   ├─ Tipo de negócio + setor
   ├─ Estágio (ideia, MVP, operacional, escalando)
   ├─ Localização e mercado-alvo
   ├─ Capital disponível
   ├─ Modelo de receita
   ├─ Time atual
   ├─ Prazo
   └─ Ambição (escala, foco, exit)
        ↓
3. ☑️ CHECKPOINT: vai aplicar a fundo perdido em Portugal?
   ├─ SIM → handoff /capital-chief
   └─ NÃO → continua
        ↓
4. Roteamento sequencial dos 7 especialistas
   ├─ 1º Steve Blank — validação cliente
   ├─ 2º Eric Ries — definição de MVP / hipóteses
   ├─ 3º Alexander Osterwalder — Business Model Canvas
   ├─ 4º Bill Aulet — TAM/SAM/SOM disciplinado
   ├─ 5º Michael Porter — análise competitiva
   ├─ 6º Peter Thiel — defensibility / vantagem sustentável
   └─ 7º Aswath Damodaran — CAPEX, projeções, DCF
        ↓
5. Consolidação em Business Plan (10 seções)
   ├─ 1.  Executive Summary
   ├─ 2.  Empresa / Promotor
   ├─ 3.  Análise de Mercado
   ├─ 4.  Modelo de Negócio
   ├─ 5.  Estratégia Competitiva
   ├─ 6.  Plano Operacional
   ├─ 7.  Time + Plano de Pessoas
   ├─ 8.  Plano Financeiro (CAPEX/OPEX/Projeções/DCF)
   ├─ 9.  Análise de Risco + Mitigações
   └─ 10. Apêndices
```

## 📦 Arquitetura

```
business-plan-squad/
├── README.md                          # este ficheiro
├── squad.yaml                         # configuração master + routing matrix
├── agents/
│   ├── business-plan-chief.md         # orquestrador sintético
│   ├── steve-blank.md                 # → /Obsidian Vault/CLONES/steve-blank/
│   ├── eric-ries.md                   # → /Obsidian Vault/CLONES/eric-ries/
│   ├── alexander-osterwalder.md       # → /Obsidian Vault/CLONES/alexander-osterwalder/
│   ├── bill-aulet.md                  # → /Obsidian Vault/CLONES/bill-aulet/
│   ├── michael-porter.md              # → /Obsidian Vault/CLONES/michael-porter/
│   ├── aswath-damodaran.md            # → /Obsidian Vault/CLONES/aswath-damodaran/
│   └── peter-thiel.md                 # → /Obsidian Vault/CLONES/peter-thiel/
├── tasks/
│   ├── create-business-plan.md        # workflow completo end-to-end
│   ├── analyze-market.md              # TAM/SAM/SOM + competidores
│   ├── build-financials.md            # CAPEX + projeções + valuation
│   ├── validate-hypothesis.md         # customer development
│   └── route-to-funding.md            # handoff para capital-squad
├── checklists/
│   └── output-quality.md              # gate de qualidade do BP final
└── data/
    └── routing-catalog.yaml           # routing matrix detalhado do chefe
```

## ⚠️ Regras Operacionais

- **Universal:** funciona em qualquer país, qualquer tipo de negócio. O chefe adapta o foco ao contexto (PT, BR, Dubai, EUA têm regulações diferentes).
- **Idioma padrão:** pt-BR (a critério do usuário; o chefe pode mudar para pt-PT se o foco for Portugal).
- **Onboarding obrigatório:** o chefe não pula as 8 perguntas iniciais — cada uma calibra o nível de profundidade dos especialistas.
- **Checkpoint de fundo perdido:** SEMPRE perguntar antes de avançar. Se SIM → handoff `/capital-chief`. Não duplicar trabalho.
- **Sem invenção:** especialistas não fabricam dados de mercado, números ou citações. Se não souber, marcar "PENDENTE — pesquisa secundária necessária".
- **Sem promessa:** o squad maximiza a qualidade do plano, nunca garante captação, sucesso de mercado ou aprovação de investidor.

## 🔗 Conexões com outros squads

- **`capital-squad`** — Captação de capital em Portugal (BPF, PT 2030, PRR, IFD, tax planning). Handoff documentado quando aplicável.
- **`copy-squad`** / **`copy-master`** — Para redação do Executive Summary, pitch e materiais de marketing após BP fechado.
- **`brand-squad`** — Para posicionamento de marca após estratégia competitiva definida.
- **`legal-squad`** — Para revisão de estruturas societárias propostas no BP.
- **`advisory-board`** — Para "second opinion" estratégico de Charlie Munger, Ray Dalio, etc.

## 📅 Versão

- **v1.0.0** — Criado 2026-05-19 via `/createclone` Squad Mode

## 🎓 Filosofia do squad

> "A business plan is a fundraising document. A business model is a strategic document. Validation comes first." — síntese da escola Blank/Ries/Osterwalder
>
> "Strategy is making trade-offs." — Michael Porter
>
> "Competition is for losers." — Peter Thiel
>
> "Discipline beats inspiration." — Bill Aulet
>
> "Valuation is a craft, not a science." — Aswath Damodaran

Sete vozes, uma metodologia integrada.
