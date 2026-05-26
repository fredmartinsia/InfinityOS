---
task: review()
responsavel: "@legal-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: false
complexity: high
model_preference: opus

Entrada:
  - campo: deliverable
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: original_request
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: risk_report
    tipo: object
    origem: Session State
    obrigatorio: false

Saida:
  - campo: Review Verdict
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Checklist output-quality.md aplicado"
  - "[ ] Todos os CRITICALs verificados"
  - "[ ] Verdict emitido com justificativa"
---

# Task: Review

**Task ID:** LEGAL-CHIEF-002
**Version:** 1.0.0
**Command:** `*review`
**Orchestrator:** Legal Chief (legal-chief)
**Purpose:** Quality gate final — aplica o output-quality.md checklist e emite verdict PASS/REVISE/FAIL.

---

## Overview

```
Deliverable → Apply Checklist → Verify CRITICALs → Count Non-Critical Fails → Verdict
     │               │                 │                      │                  │
     ▼               ▼                 ▼                      ▼                  ▼
 Contract/DPA   5 categories      Block if any            3+ = REVISE       PASS/REVISE
 /clause/report  25+ items         CRITICAL fails          <3 = PASS          /FAIL
```

---

## Inputs

| Field | Type | Source | Required | Description |
|-------|------|--------|----------|-------------|
| deliverable | string | Session State | Yes | Contrato, DPA, cláusula ou relatório a revisar |
| original_request | string | Session State | Yes | Pedido original para verificar alinhamento |
| risk_report | object | Session State | No | Relatório do risk-auditor (para verificar se CRITICALs foram endereçados) |

---

## Preconditions

- checklists/output-quality.md carregado
- risk-auditor red-team deve ter rodado antes desta task (recomendado, não obrigatório)
- Entregável completo disponível

---

## Execution Phases

### Phase 1: Checklist Application

1. Ler o entregável integralmente
2. Para cada categoria do output-quality.md (1. Conformidade Regulatória, 2. Proteção de Ambas as Partes, 3. Cláusulas Críticas Obrigatórias, 4. Clareza e Enforceability, 5. Riscos & Adversarial):
   - Verificar cada item: [x] PASS / [ ] FAIL / [N/A] Não aplicável
   - Marcar itens CRITICAL separadamente

### Phase 2: CRITICAL Verification

1. Listar todos os itens marcados como CRITICAL no checklist
2. Para cada CRITICAL: verificar se está presente/endereçado no entregável
3. Se qualquer CRITICAL estiver FAIL → verdict automático = FAIL (não verificar o restante)
4. Se risk_report disponível: verificar se todos os critical_risks do relatório foram resolvidos

### Phase 3: Non-Critical Count

1. Contar total de itens FAIL não-CRITICAL
2. Se ≥3 FAIL não-CRITICAL → verdict = REVISE
3. Se <3 FAIL não-CRITICAL → verdict = PASS

### Phase 4: Verdict Output

1. Emitir verdict com justificativa
2. Para FAIL: listar os CRITICALs que falharam e ação necessária
3. Para REVISE: listar os non-critical failures e sugestões
4. Para PASS: confirmar entregável aprovado para uso

---

## Output Format

```markdown
## Legal Chief — Quality Gate

**Verdict: [PASS | REVISE | FAIL]**

### Checklist Summary
| Categoria | Total | PASS | FAIL | N/A |
|---|---|---|---|---|
| 1. Conformidade Regulatória | X | X | X | X |
| 2. Proteção das Partes | X | X | X | X |
| 3. Cláusulas Críticas | X | X | X | X |
| 4. Clareza | X | X | X | X |
| 5. Riscos | X | X | X | X |

### Itens CRITICAL
[Lista de CRITICALs com status]

### [Se FAIL] Bloqueadores
[Lista dos CRITICALs que falharam + ação necessária]

### [Se REVISE] Recomendações
[Lista de non-critical failures + sugestões de melhoria]

### [Se PASS] Aprovação
Entregável aprovado para uso. [Observações finais se relevante]
```

---

## Veto Conditions

- Entregável incompleto (seções faltando) → retornar com pedido de completar antes de revisar
- Nenhum risk-report e contrato envolve dados pessoais → recomendar rodar compliance-check antes

---

## Completion Criteria

- [ ] Todos os 25+ itens do checklist verificados
- [ ] CRITICALs verificados individualmente
- [ ] Verdict emitido com justificativa clara
- [ ] Ações necessárias listadas se FAIL ou REVISE
