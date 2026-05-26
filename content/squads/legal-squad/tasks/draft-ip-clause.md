---
task: draftIpClause()
responsavel: "@contract-architect"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: medium
model_preference: sonnet

Entrada:
  - campo: deliverables_type
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: jurisdiction_code
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: business_model
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: IP Clause
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Titularidade durante vigência definida"
  - "[ ] Titularidade após rescisão definida"
  - "[ ] Metodologia da prestadora protegida"
  - "[ ] Portfolio rights mencionado"
---

# Task: Draft IP Clause

**Task ID:** LEGAL-ARCH-001
**Version:** 1.0.0
**Command:** `*draft-ip-clause`
**Agent:** Contract Architect (@contract-architect)
**Purpose:** Gera cláusula completa de propriedade intelectual adaptada ao tipo de entregável e jurisdição.

---

## Overview

```
Deliverables Type + Jurisdiction → Select IP Framework → Draft Clause → Validate → Output
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| deliverables_type | string | User Input | sim | site, criativos, conteúdo, código-fonte, landing page, campanha, consultoria, combinação |
| jurisdiction_code | string | Session State | sim | Determina a lei de direitos autorais aplicável |
| business_model | string | User Input | não | B2B agência-cliente, SaaS, consultoria, etc. |

## Preconditions

- jurisdiction_code definido no Session State ou fornecido pelo usuário
- Tipo de entregável claramente especificado

## Execution Phases

**Phase 1 — Select IP Framework by Jurisdiction:**
- **BR:** Lei 9.610/98 (LDA) + Lei 9.609/98 (software) — obras encomendadas, cessão restrita (art. 4), direitos morais inalienáveis (art. 27)
- **PT/EU:** CDADC (Decreto-Lei 63/85) + Diretiva 2009/24/CE (software) — cessão exige forma escrita (art. 41 CDADC)
- **US:** Work-for-hire doctrine (17 USC §101) — obras por encomenda de empresa exigem instrumento escrito OU são work-for-hire se em lista de categorias
- **UK:** CDPA 1988 — works made in the course of employment; commissioned works: direitos pertencem ao criador salvo contrato em contrário
- **Outros:** raciocinar do sistema legal (civil law tende a proteger criador; common law tende a favorecer contratante)

**Phase 2 — Classify Deliverables:**
- Criativos (anúncios, posts, vídeos): obras intelectuais — cessão necessária para o cliente ter titularidade
- Código-fonte: software — regime especial em BR (Lei 9.609) e US (work-for-hire mais amplo)
- Conteúdo textual: direitos autorais plenos — cessão restrita em BR, precisa ser expressa
- Landing pages/sites: obra multimídia — componentes diferentes (código + design + texto) com regimes diferentes
- Metodologia/framework da prestadora: NUNCA ceder — proteger explicitamente

**Phase 3 — Draft IP Clause:**
Gerar cláusula completa com sub-cláusulas:
1. **Titularidade durante vigência**: quem é dono dos entregáveis enquanto o contrato está ativo
2. **Titularidade após pagamento integral**: o cliente adquire os direitos patrimoniais após quitação completa
3. **Titularidade após rescisão por inadimplemento**: a prestadora retém os entregáveis não pagos
4. **Metodologia e know-how**: permanece sempre da prestadora
5. **Portfólio**: prestadora pode mencionar o trabalho (exceto se cliente se opuser em X dias)
6. **Direitos morais** (se jurisdição relevante): mencionar inalienabilidade (BR/PT) ou waiver (UK/US)

## Output Format

```markdown
## Cláusula X — Propriedade Intelectual

### X.1 Obras Produzidas sob Este Contrato
[Texto da cláusula]

### X.2 Cessão de Direitos Patrimoniais
[Texto da cláusula]

### X.3 Rescisão e Inadimplemento
[Texto da cláusula]

### X.4 Metodologia e Know-How
[Texto da cláusula]

### X.5 Portfólio e Referências
[Texto da cláusula]

### X.6 Direitos Morais [se aplicável]
[Texto da cláusula]

---
**Notas de adaptação:**
[Explicação de como a cláusula foi adaptada para a jurisdição e tipo de entregável]
```

## Veto Conditions

- Tipo de entregável ambíguo sem esclarecimento → solicitar detalhamento antes de redigir
- Jurisdição desconhecida sem YAML → raciocinar de first principles e sinalizar ao usuário

## Completion Criteria

- [ ] Titularidade durante vigência definida
- [ ] Titularidade após rescisão definida
- [ ] Metodologia da prestadora protegida
- [ ] Portfolio rights mencionado
