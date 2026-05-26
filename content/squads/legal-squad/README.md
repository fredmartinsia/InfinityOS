# Legal Squad

Arsenal jurídico multi-jurisdicional — contratos, compliance, IP e proteção de dados para operações globais.

## Quick Start

```
@legal-chief        # Activate the orchestrator
*diagnose            # Triage any legal request
*audit-contract      # Adversarial audit of an existing contract
*create-contract     # Create a new contract from briefing
```

## Squad Specialists

| Icone | Persona | ID | Tier | Especialidade |
|-------|---------|-----|------|---------------|
| ⚖️ | Legal Chief | legal-chief | 0 | Orquestração e roteamento multi-dimensional |
| 📜 | Contract Architect | contract-architect | 1 | Redação e estruturação de contratos |
| 🔴 | Risk Auditor | risk-auditor | 1 | Red team adversarial — ataque ao contrato |
| 🛡️ | Patricia Peck | patricia-peck | 1 | BR — LGPD, direito digital, empresarial |
| 🇪🇺 | Manuel Lopes Rocha | manuel-lopes-rocha | 1 | PT/EU — RGPD, CNPD, contratos tech |
| 🌍 | Jurisdiction Navigator | jurisdiction-navigator | 1 | Global — US, UAE, ID, UK, SG, MX e mais |

## Model Routing

| Complexity | Model | Tasks |
|------------|-------|-------|
| high | Claude Opus | diagnose, audit-contract, red-team-review, review |
| medium | Claude Sonnet | compliance-check, draft-ip-clause, compare-jurisdictions |
| low | Claude Haiku | create-contract, generate-dpa, adapt-to-jurisdiction, revise-contract |

## Jurisdiction Coverage

| Pais | Codigo | Sistema Legal | Data Protection | YAML |
|------|--------|---------------|-----------------|------|
| Brasil | br | Civil Law | LGPD / ANPD | br.yaml |
| Portugal | pt | Civil Law | RGPD / CNPD | pt.yaml |
| Estados Unidos | us | Common Law | CCPA / state patchwork | us.yaml |
| UAE / Dubai | ae | DIFC (Common) + Onshore (Civil) | UAE PDPL 2021 | ae.yaml |
| Indonesia | id | Civil Law | UU PDP 2022 | id.yaml |
| EU (generico) | eu | Civil Law | GDPR / EDPB | eu.yaml |
| Reino Unido | uk | Common Law | UK GDPR / ICO | uk.yaml |
| Singapura | sg | Common Law | PDPA 2012 | sg.yaml |
| Mexico | mx | Civil Law | LFPDPPP / INAI | mx.yaml |

## Quick Commands

- `*diagnose` — Triage + roteamento de qualquer pedido juridico
- `*audit-contract` — Auditoria adversarial de contrato existente
- `*create-contract` — Criar novo contrato de briefing
- `*red-team-review` — Ataque ao contrato pela otica da contraparte
- `*compliance-check` — Validar RGPD/LGPD/outra lei de dados
- `*generate-dpa` — Gerar DPA para qualquer jurisdicao
- `*adapt-to-jurisdiction` — Adaptar contrato para novo pais
- `*compare-jurisdictions` — Tabela comparativa entre jurisdicoes

## Adding a New Jurisdiction

1. Criar `data/jurisdictions/{code}.yaml` seguindo o schema de `us.yaml`.
2. Zero refatoracao de agentes necessaria.
3. Disponivel imediatamente via `@jurisdiction-navigator`.

## Requirements

- AIOS >= 4.0.0
