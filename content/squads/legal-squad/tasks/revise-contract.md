---
task: reviseContract()
responsavel: "@contract-architect"
responsavel_type: Agent
atomic_layer: Task
elicit: false
complexity: low
model_preference: haiku

Entrada:
  - campo: contract_file
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: audit_report
    tipo: object
    origem: Session State
    obrigatorio: true

Saida:
  - campo: Revised Contract
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Todos os riscos CRITICAL corrigidos"
  - "[ ] Todos os riscos HIGH corrigidos"
  - "[ ] Change log produzido"
  - "[ ] Contrato limpo + tracked changes entregues"
---

# Task: Revise Contract

**Task ID:** LEGAL-ARCH-003
**Version:** 1.0.0
**Command:** `*revise-contract`
**Agent:** Contract Architect (@contract-architect)
**Purpose:** Aplica as correções identificadas no audit_report ao contrato original — produz versão limpa e versão com rastreamento de alterações.

---

## Overview

```
Contract + Audit Report → For Each Risk → Apply Fix → Produce Clean + Tracked → Change Log
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| contract_file | string | Session State | sim | Contrato original completo |
| audit_report | object | Session State | sim | Output do audit-contract ou red-team-review com lista de riscos e recomendações |

## Preconditions

- audit_report disponível com recomendações específicas (não genéricas)
- Contrato completo disponível no Session State
- Se há riscos CRITICAL: esses são obrigatórios de corrigir
- Se há riscos HIGH: fortemente recomendados de corrigir

## Execution Phases

**Phase 1 — Prioritize Corrections:**
1. Listar todos os riscos do audit_report por severidade: CRITICAL primeiro, depois HIGH, MEDIUM, LOW
2. Para cada risco: identificar a cláusula afetada e a correção específica recomendada

**Phase 2 — Apply CRITICAL Fixes:**
Para cada risco CRITICAL: aplicar a correção recomendada. Se a recomendação requer criação de nova cláusula (ex: DPA ausente), inserir `[REQUER: *generate-dpa]` em vez de criar do zero.

**Phase 3 — Apply HIGH and MEDIUM Fixes:**
Aplicar as correções HIGH e MEDIUM seguindo as recomendações do audit_report.

**Phase 4 — Produce Outputs:**
1. **Contrato limpo**: versão final com todas as correções aplicadas, sem marcações
2. **Contrato tracked**: mesma versão mas com cada alteração marcada `[INSERIDO]`, `[REMOVIDO]`, `[MODIFICADO]`
3. **Change log**: lista de cada alteração com: cláusula → problema → correção aplicada → justificativa

## Output Format

**Primeiro: Change Log**

```markdown
## Change Log

| # | Cláusula | Severidade | Problema | Correção Aplicada |
|---|---|---|---|---|
| 1 | Cláusula X | CRITICAL | Foro em branco | Foro de [cidade] inserido |
| 2 | Cláusula Y | HIGH | IP ambígua | Cláusula IP reescrita |
[...]
```

**Depois:** contrato limpo completo.

**Depois:** contrato tracked completo com marcações `[INSERIDO: ...]`, `[REMOVIDO: ...]`, `[MODIFICADO: foi "..." agora "..."]`.

## Veto Conditions

- Audit report sem recomendações específicas → retornar pedindo recomendações concretas
- Riscos CRITICAL sem solução clara no audit_report → escalar para contract-architect + advisor de jurisdição antes de aplicar

## Completion Criteria

- [ ] Todos os riscos CRITICAL do audit_report endereçados
- [ ] Todos os riscos HIGH endereçados
- [ ] Change log completo
- [ ] Contrato limpo produzido
- [ ] Contrato tracked produzido
