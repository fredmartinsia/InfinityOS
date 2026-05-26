---
task: generateDpa()
responsavel: "@jurisdiction-navigator"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: low
model_preference: haiku

Entrada:
  - campo: controller
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: processor
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: data_categories
    tipo: list
    origem: User Input
    obrigatorio: true
  - campo: purposes
    tipo: list
    origem: User Input
    obrigatorio: true
  - campo: jurisdiction_code
    tipo: string
    origem: Session State
    obrigatorio: true

Saida:
  - campo: DPA Document
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Controlador e processador identificados"
  - "[ ] Categorias de dados listadas"
  - "[ ] Finalidades declaradas"
  - "[ ] Medidas de segurança incluídas"
  - "[ ] Incidentes regulados"
---

# Task: Generate DPA

**Task ID:** LEGAL-NAV-003
**Version:** 1.0.0
**Command:** `*generate-dpa`
**Agent:** Jurisdiction Navigator (@jurisdiction-navigator)
**Purpose:** Gera DPA (Data Processing Agreement) completo para qualquer jurisdição a partir de parâmetros estruturados.

---

## Overview

```
Controller + Processor + Data + Purposes + Jurisdiction → Load YAML → Fill DPA Schema → Output
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| controller | string | User Input | sim | Nome e identificação do controlador (quem determina as finalidades) |
| processor | string | User Input | sim | Nome e identificação do processador (quem executa o tratamento) |
| data_categories | list | User Input | sim | Ex: ["dados de contato", "dados de comportamento online", "dados de leads"] |
| purposes | list | User Input | sim | Ex: ["gestão de campanhas publicitárias", "análise de performance"] |
| jurisdiction_code | string | Session State | sim | Determina a lei aplicável ao DPA |

## Preconditions

- Controlador e processador claramente distintos (quem instrui vs. quem executa)
- Categorias de dados não incluem dados sensíveis sem sinalização explícita
- jurisdiction_code definido no Session State

## Execution Phases

**Phase 1 — Identify Legal Framework:**
Ler `data/jurisdictions/{code}.yaml` → data_protection section → base legal padrão para B2B:
- **BR:** LGPD art. 7, V (execução de contrato) + art. 39 (operador)
- **PT/EU:** RGPD art. 6(1)(b) + art. 28 (subcontratante)
- **US:** sem lei federal omnibus — usar termos contratuais padrão (IAPP template)
- **UK:** UK GDPR art. 28
- **Outros:** aplicar framework via YAML

**Phase 2 — Fill DPA Schema (determinístico — substituição de variáveis):**
Preencher template DPA com:
- Partes (controlador + processador)
- Objeto do tratamento
- Natureza e finalidades do tratamento
- Tipo de dados pessoais e categorias de titulares
- Duração do tratamento
- Obrigações e direitos do controlador
- Obrigações do processador:
  - Tratar apenas conforme instruções
  - Confidencialidade
  - Medidas técnicas e organizativas (ISO 27001, SOC 2, ou mínimo contratual)
  - Subprocessadores (lista ou aprovação prévia)
  - Assistência ao controlador (exercício de direitos dos titulares)
  - Notificação de incidentes (prazo: 72h RGPD / prazo razoável LGPD)
  - Devolução ou eliminação ao final
  - Auditoria
- Transferências internacionais (se aplicável): mecanismo + referência legal
- Assinaturas

## Output Format

DPA completo pronto para inserir como Anexo II do contrato principal. Incluir header:

```
ANEXO II — ACORDO DE TRATAMENTO DE DADOS / DATA PROCESSING AGREEMENT
```

Seguido de todas as cláusulas numeradas, prontas para assinatura.

## Veto Conditions

- Dados sensíveis (saúde, biometria, religião, política) identificados nas categorias → sinalizar ao usuário e solicitar confirmação antes de prosseguir
- Controlador e processador parecem ser a mesma entidade → solicitar esclarecimento

## Completion Criteria

- [ ] Controlador e processador identificados
- [ ] Categorias de dados listadas
- [ ] Finalidades declaradas
- [ ] Medidas de segurança incluídas
- [ ] Incidentes regulados
