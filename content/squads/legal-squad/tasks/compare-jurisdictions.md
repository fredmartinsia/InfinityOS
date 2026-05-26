---
task: compareJurisdictions()
responsavel: "@jurisdiction-navigator"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: medium
model_preference: sonnet

Entrada:
  - campo: topic
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: jurisdictions
    tipo: list
    origem: User Input
    obrigatorio: true

Saida:
  - campo: Comparison Table
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Cada jurisdição analisada via YAML"
  - "[ ] Tabela comparativa gerada"
  - "[ ] Recomendação de redação para cada"
---

# Task: Compare Jurisdictions

**Task ID:** LEGAL-NAV-002
**Version:** 1.0.0
**Command:** `*compare-jurisdictions`
**Agent:** Jurisdiction Navigator (@jurisdiction-navigator)
**Purpose:** Compara como um tema específico (cláusula, conceito legal, obrigação) funciona em N jurisdições — com tabela e redação sugerida para cada.

---

## Overview

```
Topic + Jurisdictions → Load N YAMLs → Analyze Each → Compare → Table + Clause Variants
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| topic | string | User Input | sim | cláusula ou conceito: "non-compete", "limitação de responsabilidade", "DPA", "governing law", "e-signature", "consumer law", etc. |
| jurisdictions | list | User Input | sim | Lista de jurisdiction_codes: ["br", "pt", "us"] |

## Preconditions

- Ao menos 2 jurisdições fornecidas para comparação
- Topic claramente definido (cláusula, conceito ou obrigação específica)
- YAMLs disponíveis para as jurisdições listadas

## Execution Phases

**Phase 1 — Load YAMLs:**
Para cada jurisdiction_code na lista, ler `data/jurisdictions/{code}.yaml` e extrair a seção relevante para o topic.

**Phase 2 — Analyze Each Jurisdiction:**
Para cada jurisdição:
- Base legal aplicável ao topic
- Enforceability: é válido? Com quais condições?
- Limitações: o que não pode ser feito?
- Red flags locais relacionados ao topic
- Redação típica ou recomendada

**Phase 3 — Comparative Table:**
Gerar tabela comparativa com colunas por jurisdição e linhas por aspecto:
- Sistema legal (civil / common)
- Base legal
- Validade (Sim / Não / Parcial)
- Condições de enforceability
- Limitações principais
- Red flags locais

**Phase 4 — Clause Variants:**
Para cada jurisdição, redigir versão da cláusula adaptada ao topic com referências legais corretas.

## Output Format

```markdown
## Comparativo Jurisdicional — [Topic]

### Tabela Comparativa

| Aspecto | [País 1] | [País 2] | [País 3] |
|---|---|---|---|
| Sistema legal | civil/common | ... | ... |
| Base legal | Lei X | Lei Y | Lei Z |
| Válido? | Sim/Não/Parcial | ... | ... |
| Condições | ... | ... | ... |
| Limitações | ... | ... | ... |
| Red flag | ... | ... | ... |

### Variantes de Cláusula

**[País 1] — [Nome da Lei]:**
[Texto da cláusula adaptada]

**[País 2] — [Nome da Lei]:**
[Texto da cláusula adaptada]

### Recomendação
[Para contrato multi-jurisdição: qual abordagem minimiza conflito entre as jurisdições?]
```

## Veto Conditions

- Apenas 1 jurisdição fornecida → solicitar ao menos 2 para comparação
- Topic genérico demais sem especificação → solicitar refinamento antes de executar

## Completion Criteria

- [ ] Cada jurisdição analisada via YAML
- [ ] Tabela comparativa gerada
- [ ] Recomendação de redação para cada
