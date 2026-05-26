---
task: auditContract()
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
  - campo: jurisdiction_code
    tipo: string
    origem: Session State
    obrigatorio: false

Saida:
  - campo: Risk Report
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Todos os attack vectors verificados"
  - "[ ] Riscos classificados por severidade"
  - "[ ] Recomendações específicas para cada risco"
---

# Task: Audit Contract

**Task ID:** LEGAL-RISK-001
**Version:** 1.0.0
**Command:** `*audit-contract`
**Orchestrator:** Risk Auditor (risk-auditor)
**Purpose:** Auditoria adversarial completa de contrato existente — identifica todos os riscos por severidade e entrega relatório acionável.

---

## Overview

```
Contract → Parse Structure → Apply Attack Vectors → Classify Risks → Recommendations → Report
    │            │                  │                    │                │               │
    ▼            ▼                  ▼                    ▼                ▼               ▼
 Full text   Clauses +         6 attack vectors    CRITICAL/HIGH/    Per-risk fix    Risk report
             structure         per clause          MEDIUM/LOW        suggestions     with scores
```

---

## Inputs

| Field | Type | Source | Required | Description |
|-------|------|--------|----------|-------------|
| contract_file | string | User Input | Yes | Texto completo do contrato |
| party_role | string | User Input | Yes | "prestador" ou "cliente" — perspectiva de quem proteger |
| jurisdiction_code | string | Session State | No | Detectado pelo diagnose; se ausente, inferir do contrato |

---

## Preconditions

- Contrato completo disponível (não apenas trechos)
- Papel da parte a proteger definido (prestador vs cliente — muda radicalmente a análise)
- jurisdiction_code disponível (para aplicar lei correta nos testes de nulidade)

---

## Execution Phases

### Phase 1: Structure Parse

1. Mapear a estrutura do contrato: listar todas as cláusulas numeradas com título e assunto
2. Identificar o tipo de contrato (prestação de serviços / SaaS / NDA / sociedade / outro)
3. Identificar lacunas estruturais: quais seções padrão estão ausentes?
4. Verificar se todos os Anexos referenciados existem e estão preenchidos

### Phase 2: Adversarial Attack (6 vetores por cláusula)

Para cada cláusula substantiva, aplicar:
1. **Ambiguidade**: "Esta linguagem pode ser interpretada de mais de uma forma? A interpretação desfavorável é possível?"
2. **Lacuna**: "O que acontece se X ocorrer e não há cláusula cobrindo isso? Quem se beneficia do silêncio?"
3. **Assimetria**: "Esta cláusula cria obrigação desproporcional? É leonina ou abusiva?"
4. **Nulidade**: "Esta cláusula viola lei cogente da jurisdição? (ex: direitos morais inalienáveis, CDC, eIDAS, LGPD)"
5. **Inexequibilidade**: "Esta cláusula é válida em teoria mas impossível de executar na prática?"
6. **Scope creep**: "Esta linguagem permite que a contraparte exija mais do que o contratado?"

### Phase 3: Regulatory Compliance Check

1. DPA: há tratamento de dados pessoais? Existe cláusula de DPA? É adequada para a jurisdição?
2. Consumer law: a contraparte pode ser considerada consumidor? As leis imperativas estão respeitadas?
3. IP: titularidade dos entregáveis está clara durante E após a vigência? Metodologia da prestadora protegida?
4. Foro/Arbitragem: está preenchido? É válido na jurisdição?
5. Limitação de responsabilidade: existe? Cap definido? Carve-outs presentes?

### Phase 4: Severity Classification

Para cada risco identificado, classificar:
- CRITICAL: pode anular o contrato, gerar multa regulatória imediata, ou expor a responsabilidade ilimitada
- HIGH: provavelmente será usado contra a parte em caso de disputa
- MEDIUM: risco real mas gerenciável, probabilidade menor
- LOW: questão cosmética ou de best practice

### Phase 5: Recommendations

Para cada risco, formular recomendação específica de correção (não genérica).

---

## Output Format

```markdown
## Risk Auditor — Relatório de Auditoria

**Contrato:** [tipo]
**Jurisdição:** [code]
**Parte protegida:** [prestador | cliente]
**Nota geral:** [X/10]

### Riscos CRITICAL ([n] encontrados)
[Para cada risco:]
**[C-N] [Título do risco]**
- **Cláusula:** [número/título]
- **Problema:** [descrição específica]
- **Impacto:** [consequência real]
- **Recomendação:** [correção específica]

### Riscos HIGH ([n] encontrados)
[Mesma estrutura]

### Riscos MEDIUM ([n] encontrados)
[Mesma estrutura — versão resumida]

### Riscos LOW ([n] encontrados)
[Lista simples]

### Sumário Executivo
[3-4 parágrafos: principais vulnerabilidades, avaliação geral, recomendação de ação]
```

---

## Veto Conditions

- Contrato incompleto (seções faltando) → solicitar versão completa antes de auditar
- >7 riscos CRITICAL → recomendar ao Legal Chief considerar reescrita ao invés de correção pontual

---

## Completion Criteria

- [ ] Todos os 6 attack vectors aplicados às cláusulas substantivas
- [ ] Compliance regulatória verificada (DPA, consumer, IP, foro)
- [ ] Todos os riscos classificados por severidade com justificativa
- [ ] Recomendação específica para cada risco
- [ ] Sumário executivo com nota geral
