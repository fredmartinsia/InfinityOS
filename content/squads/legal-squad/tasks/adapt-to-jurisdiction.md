---
task: adaptToJurisdiction()
responsavel: "@jurisdiction-navigator"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: low
model_preference: haiku

Entrada:
  - campo: contract_file
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: origin_jurisdiction
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: target_jurisdiction
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: Adapted Contract
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Governing law substituída"
  - "[ ] Foro/arbitragem substituído"
  - "[ ] Referências legais atualizadas"
  - "[ ] Moeda/fiscal ajustado"
  - "[ ] Idioma verificado"
---

# Task: Adapt to Jurisdiction

**Task ID:** LEGAL-NAV-004
**Version:** 1.0.0
**Command:** `*adapt-to-jurisdiction`
**Agent:** Jurisdiction Navigator (@jurisdiction-navigator)
**Purpose:** Adapta contrato existente de uma jurisdição origem para uma jurisdição destino: substitui governing law, foro, referências legais, moeda e requisitos formais.

---

## Overview

```
Contract (Origin) + Target Jurisdiction → Load Target YAML → Map Changes → Substitute → Adapted Contract
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| contract_file | string | User Input | sim | Texto do contrato original |
| origin_jurisdiction | string | Session State | sim | Jurisdição atual do contrato |
| target_jurisdiction | string | User Input | sim | Jurisdição destino |

## Preconditions

- Contrato completo disponível em texto
- origin_jurisdiction identificada (pode ser inferida do texto do contrato se não estiver no Session State)
- target_jurisdiction claramente especificada pelo usuário
- YAML da jurisdição destino disponível em `data/jurisdictions/{target}.yaml`

## Execution Phases

**Phase 1 — Load Target YAML:**
Ler `data/jurisdictions/{target}.yaml` — extrair: governing law típico, foro/arbitragem padrão, referências legais, moeda, fiscal, formalities.idioma, formalities.signature.

**Phase 2 — Map Substitutions (determinístico):**
Criar mapeamento de substituições:

| Elemento | Valor origem | Valor destino |
|---|---|---|
| Lei aplicável | Lei X do país Y | Lei A do país B |
| Foro | Comarca X | Tribunal/Câmara Y |
| Arbitragem (se houver) | Câmara X | Câmara Y |
| Moeda | R$/€/$ | [moeda destino] |
| IVA/VAT/ISS | X% | Y% |
| Base legal LGPD/RGPD | art. X LGPD | art. X RGPD |
| Referências de consumer law | CDC art. X | Lei Consumer destino |
| Forma de assinatura | ICP-Brasil/eIDAS | [equivalente] |

**Phase 3 — Execute Substitutions:**
Aplicar todas as substituições sistematicamente ao texto do contrato.

**Phase 4 — Add Missing Mandatory Elements:**
Verificar se a jurisdição destino exige elementos que não existem no contrato origem:
- Idioma obrigatório (Bahasa Indonesia para contratos domésticos ID)
- CFDI/NF-e ou equivalente fiscal mencionado
- Cláusula específica de consumer rights se B2C na destino
- DPA adequado à jurisdição destino (se já há DPA no contrato)

**Phase 5 — Flag Structural Incompatibilities:**
Identificar cláusulas que precisam de revisão por um especialista (não apenas substituição):
- Non-compete (enforceability varia radicalmente por jurisdição)
- Limitation of liability (gross negligence carve-out em common law é diferente)
- IP assignment (work-for-hire em US vs cessão expressa em BR/PT)

## Output Format

```markdown
## Contrato Adaptado — [Origem] → [Destino]

### Substituições Realizadas
[Tabela de todas as substituições aplicadas]

### Elementos Adicionados
[Lista de cláusulas/elementos obrigatórios na jurisdição destino que foram inseridos]

### Flags para Revisão Especializada
[Cláusulas que requerem revisão por especialista além da substituição mecânica]

---

[TEXTO DO CONTRATO ADAPTADO COMPLETO]
```

## Veto Conditions

- Target jurisdiction YAML não encontrado → raciocinar de first principles, sinalizar ao usuário
- Contrato original sem identificação de jurisdição origem → solicitar antes de prosseguir

## Completion Criteria

- [ ] Governing law substituída
- [ ] Foro/arbitragem substituído
- [ ] Referências legais atualizadas
- [ ] Moeda/fiscal ajustado
- [ ] Idioma verificado
