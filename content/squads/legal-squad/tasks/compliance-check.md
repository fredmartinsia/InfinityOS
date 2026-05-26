---
task: complianceCheck()
responsavel: "@jurisdiction-navigator"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: medium
model_preference: sonnet

Entrada:
  - campo: contract_file
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: jurisdiction_code
    tipo: string
    origem: Session State
    obrigatorio: true
  - campo: business_context
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: Compliance Report
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Data protection verificada"
  - "[ ] Consumer law verificada"
  - "[ ] Fiscal verificado"
  - "[ ] Cláusulas obrigatórias auditadas"
---

# Task: Compliance Check

**Task ID:** LEGAL-NAV-001
**Version:** 1.0.0
**Command:** `*compliance-check`
**Agent:** Jurisdiction Navigator (@jurisdiction-navigator)
**Purpose:** Valida conformidade regulatória de contrato com a legislação da jurisdição: data protection, consumer law e fiscal.

---

## Overview

```
Contract + Jurisdiction → Load YAML → Check Data Protection → Check Consumer Law → Check Fiscal → Report
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| contract_file | string | User Input | sim | Texto do contrato |
| jurisdiction_code | string | Session State | sim | br / pt / us / ae / id / eu / uk / sg / mx |
| business_context | string | User Input | não | B2B ou B2C; setor da empresa |

## Preconditions

- Contrato disponível em texto (copiado ou colado)
- jurisdiction_code definido no Session State ou fornecido pelo usuário
- YAML da jurisdição em `data/jurisdictions/{jurisdiction_code}.yaml`

## Execution Phases

**Phase 1 — Load Jurisdiction Data:**
1. Ler `data/jurisdictions/{jurisdiction_code}.yaml`
2. Extrair: `data_protection.key_laws`, `consumer_law.framework`, `fiscal.value_added`, `formalities`

**Phase 2 — Data Protection Check:**
1. O contrato envolve tratamento de dados pessoais? (verificar menção a dados de clientes, leads, usuários)
2. Se sim: DPA ou cláusula equivalente existe? Está adequada à legislação da jurisdição?
3. Base legal do tratamento identificada? (execução de contrato, legítimo interesse, consentimento)
4. Transferências internacionais de dados: há mecanismo adequado? (SCCs, DPF, adequacy)
5. Autoridade regulatória da jurisdição: ANPD (BR), CNPD (PT), ICO (UK), PDPC (SG), etc.

**Phase 3 — Consumer Law Check:**
1. Uma das partes pode ser classificada como consumidor? (pessoa física comprando para uso pessoal)
2. Se B2C: as leis imperativas da jurisdição estão respeitadas? (CDC, DL 24/2014, FTC, Consumer Rights Act, etc.)
3. Há cláusulas potencialmente abusivas sob a lei de consumidor da jurisdição?
4. Direito de arrependimento/rescisão: aplicável? Mencionado corretamente?

**Phase 4 — Fiscal Check:**
1. Qual o regime de IVA/VAT/ISS/sales tax aplicável?
2. Se cross-border: há cláusula sobre responsabilidade pelo pagamento de impostos?
3. Se partes em jurisdições diferentes: withholding tax mencionada? Quem suporta?
4. Faturação/invoice: o contrato menciona requisitos de forma (CFDI para MX, NF-e para BR, etc.)?

**Phase 5 — Mandatory Formalities:**
1. Idioma: o contrato exige idioma específico na jurisdição? (Bahasa Indonesia para ID, espanhol para MX doméstico)
2. Assinatura eletrônica: válida na jurisdição? Qual nível de certificação é necessário?
3. Notarização: necessária para o tipo de ato?
4. Registro: o contrato precisa ser registrado em alguma entidade?

## Output Format

```markdown
## Compliance Check — [Jurisdição]

### Data Protection
**Status:** ✅ Conforme | ⚠️ Parcialmente | ❌ Não conforme
[Itens verificados com status individual]

### Consumer Law
**Aplicável:** Sim | Não
**Status:** ✅ | ⚠️ | ❌
[Itens verificados]

### Fiscal
**Regime:** [IVA 23% PT / ISS 5% BR / VAT 5% AE / etc.]
**Status:** ✅ | ⚠️ | ❌
[Itens verificados]

### Formalidades
[Idioma, assinatura, notarização, registro]

### Gaps identificados
[Lista de gaps com recomendação]
```

## Veto Conditions

- Jurisdiction YAML não encontrado e jurisdição desconhecida → usar jurisdiction-navigator para raciocinar de first principles, avisar o usuário

## Completion Criteria

- [ ] Data protection verificada
- [ ] Consumer law verificada
- [ ] Fiscal verificado
- [ ] Cláusulas obrigatórias auditadas
