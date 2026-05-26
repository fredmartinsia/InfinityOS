---
task: diagnose()
responsavel: "@legal-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: high
model_preference: opus

Entrada:
  - campo: request
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: context
    tipo: object
    origem: Session State
    obrigatorio: false

Saida:
  - campo: Diagnosis Report
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Jurisdição detectada"
  - "[ ] Domínio identificado"
  - "[ ] Complexidade avaliada"
  - "[ ] Rota definida com modelo Anthropic correto"
---

# Task: Diagnose

**Task ID:** LEGAL-CHIEF-001
**Version:** 1.0.0
**Command:** `*diagnose`
**Orchestrator:** Legal Chief (legal-chief)
**Purpose:** Triage qualquer pedido jurídico: detecta jurisdição, identifica domínio, avalia complexidade e roteia para o agente e modelo Anthropic corretos.

---

## Overview

```
User Request → Detect Jurisdiction → Identify Domain → Assess Complexity → Route
     │               │                    │                  │              │
     ▼               ▼                    ▼                  ▼              ▼
 Raw input    BR/PT/US/AE/etc    contract/data/IP/etc  high/med/low   agent+model
```

---

## Inputs

| Field | Type | Source | Required | Description |
|-------|------|--------|----------|-------------|
| request | string | User Input | Yes | Descrição do pedido jurídico |
| context | object | Session State | No | Tipo de negócio, partes envolvidas, contratos existentes |

---

## Preconditions

- Legal Squad ativo com Legal Chief como entry agent
- Arquivos data/jurisdictions/*.yaml disponíveis para o Jurisdiction Navigator
- Todos os 6 agentes especialistas registrados

---

## Execution Phases

### Phase 1: Detect Jurisdiction

1. Analisar o pedido por sinais de jurisdição: referências a leis específicas (LGPD, RGPD, CCPA), moeda mencionada (R$, €, $, AED), idioma do contrato, localização das partes
2. Mapear para jurisdiction_code: br | pt | us | ae | id | eu | uk | sg | mx | unknown
3. Se jurisdiction_code = unknown: perguntar explicitamente antes de continuar
4. Se múltiplas jurisdições: identificar a primária (governing law) e secundárias (partes residentes)

### Phase 2: Identify Domain

1. Extrair o domínio jurídico primário do pedido:
   - contract_audit: "auditar, revisar, analisar riscos, gaps, buracos"
   - contract_create: "criar, redigir, novo contrato, modelo, minuta"
   - data_protection: "LGPD, RGPD, DPA, dados pessoais, consentimento"
   - ip_rights: "IP, direitos autorais, cessão, criativos, software"
   - compliance: "compliance, conformidade, checklist regulatório"
   - jurisdiction_adapt: "adaptar para, outro país, governing law"
   - cross_border: "internacional, multi-jurisdição, exportar serviço"
2. Identificar se há tensão entre domínios (ex: criação de contrato + necessidade de DPA)

### Phase 3: Assess Complexity

1. Classificar o pedido:
   - HIGH (Opus): auditoria adversarial, triage inicial com múltiplas variáveis, quality gate, análise de risco não óbvia
   - MEDIUM (Sonnet): compliance check com base em YAML, tabela comparativa, cláusula template com adaptação
   - LOW (Haiku): preencher template de contrato com briefing completo, DPA schema fill, substituição de governing law
2. Justificar a classificação com 1-2 frases

### Phase 4: Route

1. Selecionar agente primário e secundário com base na matriz:
   - contract_audit → risk-auditor (opus) + advisor da jurisdição
   - contract_create → contract-architect (haiku) + advisor da jurisdição
   - data_protection_br → patricia-peck (opus)
   - data_protection_pt_eu → manuel-lopes-rocha (opus)
   - data_protection_other → jurisdiction-navigator (sonnet)
   - ip_rights → contract-architect (sonnet) + advisor
   - compliance → advisor da jurisdição (sonnet)
   - jurisdiction_adapt → jurisdiction-navigator (haiku)
   - cross_border → jurisdiction-navigator (sonnet) + contract-architect
2. Se multi-specialist scenario: definir sequência (ex: risk-auditor → compliance-check → contract-architect)

---

## Output Format

```markdown
## Legal Chief — Diagnóstico

**Jurisdição detectada:** [BR | PT | US | AE | etc.]
**Domínio:** [contract_audit | contract_create | data_protection | ip_rights | compliance | adapt | cross_border]
**Complexidade:** [HIGH | MEDIUM | LOW]
**Modelo recomendado:** [Opus | Sonnet | Haiku]

### Rota
**Agente primário:** @[agent-id]
**Agente secundário:** @[agent-id] (se aplicável)
**Sequência recomendada:** [se multi-specialist]

### Resposta rápida
[1-3 parágrafos com análise inicial antes de despachar para especialista]

### Próximo passo
Para prosseguir: `*[task-name]` com [@agent-id]
```

---

## Veto Conditions

- Jurisdição impossível de detectar após análise → pausar e perguntar antes de continuar
- Pedido envolve mais de 3 jurisdições → recomendar abordagem em fases, não um diagnóstico único
- Pedido requer licença profissional local (representação legal formal) → informar que o squad é consultivo, não substitui advogado licenciado

---

## Completion Criteria

- [ ] Jurisdição identificada ou explicitamente solicitada ao usuário
- [ ] Domínio jurídico primário identificado
- [ ] Complexidade avaliada com justificativa
- [ ] Agente primário e modelo definidos
- [ ] Resposta rápida fornecida antes de despachar para especialista
