---
task: redTeamReview()
responsavel: "@risk-auditor"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: high
model_preference: opus

Entrada:
  - campo: contract_file
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: party_role
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: Adversarial Report
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Contrato atacado como contraparte adversarial"
  - "[ ] Brechas de saída testadas"
  - "[ ] Ambiguidades mapeadas"
  - "[ ] Nulidades verificadas"
---

# Task: Red Team Review

**Task ID:** LEGAL-RISK-002
**Version:** 1.0.0
**Command:** `*red-team-review`
**Orchestrator:** Risk Auditor (risk-auditor)
**Purpose:** Ataque adversarial focado e agressivo — lê o contrato exclusivamente como a contraparte mais difícil possível. Mais rápido e focado que audit-contract.

---

## Overview

```
Contract → Assume Adversarial Position → Attack Every Clause → Find Exit Routes → Report
    │               │                         │                      │              │
    ▼               ▼                         ▼                      ▼              ▼
 Full text    "I am the            How do I use this      How do I exit      Adversarial
              counterparty"        clause against you?    without penalty?   findings
```

---

## Inputs

| Field | Type | Source | Required | Description |
|-------|------|--------|----------|-------------|
| contract_file | string | User Input | Yes | Texto completo do contrato |
| party_role | string | User Input | Yes | Parte a atacar (ex: "atacar as proteções do prestador") |

---

## Preconditions

- Contrato completo disponível
- Papel a atacar definido claramente

---

## Execution Phases

### Phase 1: Adversarial Positioning

1. Assumir completamente a posição da contraparte mais sofisticada possível
2. Objetivo: encontrar todas as formas de tirar vantagem, sair sem penalidade, ou exigir mais do que foi contratado
3. Listar os 5 objetivos adversariais prioritários (ex: não pagar, sair sem multa, exigir retrabalho ilimitado)

### Phase 2: Clause-by-Clause Attack

Para cada cláusula, atacar com 3 perguntas:
1. "Como uso esta linguagem para me beneficiar?"
2. "Qual ambiguidade posso explorar?"
3. "Como saio deste compromisso sem pagar penalidade?"

### Phase 3: Exit Route Mapping

1. Identificar todas as brechas que permitem rescisão sem ônus
2. Testar: "Se eu não pagar, o que acontece? Quanto tempo até a rescisão? Qual é o custo real?"
3. Testar: "Se eu quiser sair no mês 3, qual é minha saída mais barata?"

### Phase 4: Nullity Test

1. Buscar cláusulas que violam lei cogente → nulas → potencialmente contamina outras cláusulas
2. Verificar cláusulas abusivas pelo prisma de CDC/Consumer Protection — são anuláveis?

---

## Output Format

```markdown
## Risk Auditor — Red Team Report

**Atacando:** [proteções do prestador | proteções do cliente]
**Posição:** Contraparte adversarial máxima

### Objetivos adversariais identificados
1. [Objetivo 1]
2. [Objetivo 2]
[...]

### Brechas encontradas (por severidade)

**CRITICAL — Bloqueadores imediatos**
[Brechas que permitem dano imediato sem defesa]

**HIGH — Alavancas de pressão**
[Cláusulas que a contraparte pode usar para pressionar renegociação]

**MEDIUM — Oportunidades táticas**
[Ambiguidades que podem ser exploradas em contexto de disputa]

### Rotas de saída sem penalidade
[Mapeamento das brechas de rescisão]

### Nulidades potenciais
[Cláusulas que podem ser contestadas judicialmente]

### Veredicto adversarial
[Avaliação geral: quão fácil é para a contraparte "ganhar" com este contrato?]
```

---

## Veto Conditions

- Contrato incompleto → solicitar versão completa
- Pedido de usar para fins reais de litígio → lembrar que output é consultivo, não substitui advogado

---

## Completion Criteria

- [ ] Posição adversarial assumida completamente
- [ ] Todas as cláusulas substantivas atacadas
- [ ] Rotas de saída mapeadas
- [ ] Nulidades testadas
- [ ] Veredicto adversarial emitido
