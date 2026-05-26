---
task: createContract()
responsavel: "@contract-architect"
responsavel_type: Agent
atomic_layer: Task
elicit: true
complexity: low
model_preference: haiku

Entrada:
  - campo: briefing
    tipo: object
    origem: User Input
    obrigatorio: true

Saida:
  - campo: Contract Draft
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Todas as partes identificadas"
  - "[ ] Escopo específico"
  - "[ ] Valores e prazos preenchidos"
  - "[ ] Jurisdição e foro declarados"
---

# Task: Create Contract

**Task ID:** LEGAL-ARCH-002
**Version:** 1.0.0
**Command:** `*create-contract`
**Agent:** Contract Architect (@contract-architect)
**Purpose:** Gera contrato completo de prestação de serviços a partir de briefing estruturado.

---

## Overview

```
Briefing → Select Template → Fill Sections → Add Standard Clauses → Mark Placeholders → Output
```

## Inputs

| Campo | Tipo | Origem | Obrigatório | Descrição |
|---|---|---|---|---|
| briefing | object | User Input | sim | {parte_prestadora, parte_cliente, tipo_servico, jurisdicao, valor, duracao, escopo, entregaveis} |

## Preconditions

Todos os campos do briefing obrigatórios antes de gerar o draft:

| Campo | Descrição |
|---|---|
| parte_prestadora | Nome, registro (CNPJ/NIF/EIN/NIPC), endereço, representante |
| parte_cliente | idem |
| tipo_servico | tráfego pago / gestão de redes / criação de site / e-commerce / landing page / criação de conteúdo / consultoria / outro |
| jurisdicao | br / pt / us / ae / id / eu / uk / sg / mx |
| valor | numérico + moeda + periodicidade (mensal / one-off / milestone) |
| duracao | X meses ou one-off com prazo de entrega |
| escopo | lista de serviços incluídos |
| entregaveis | lista de o que será produzido e entregue |

## Execution Phases

**Phase 1 — Validate Briefing:**
1. Verificar que todos os campos obrigatórios estão preenchidos
2. Se algum campo estiver faltando: pausar e solicitar antes de prosseguir
3. Inferir o template base pelo tipo_servico e jurisdicao

**Phase 2 — Select Template:**
Selecionar estrutura de seções pelo tipo:
- **Serviços recorrentes** (tráfego, redes, conteúdo): prazo mínimo + renovação automática + reajuste + penalidade por interferência
- **One-off** (site, landing, e-commerce): milestone pagamento (50%+50%) + prazo em dias úteis + nº de revisões + suporte pós-entrega

**Phase 3 — Generate Draft:**
Gerar contrato completo com todas as seções padrão:
1. PREÂMBULO
2. DEFINIÇÕES
3. OBJETO
4. ESCOPO
5. PREÇO E PAGAMENTO
6. PRAZO
7. OBRIGAÇÕES DA PRESTADORA
8. OBRIGAÇÕES DO CLIENTE
9. PROPRIEDADE INTELECTUAL `[PLACEHOLDER: usar *draft-ip-clause]`
10. CONFIDENCIALIDADE
11. PROTEÇÃO DE DADOS `[PLACEHOLDER: usar *generate-dpa se necessário]`
12. LIMITAÇÃO DE RESPONSABILIDADE
13. RESCISÃO
14. DISPOSIÇÕES GERAIS (cessão, força maior, foro, lei aplicável)
15. ASSINATURAS
16. ANEXO I — Escopo Detalhado

**Phase 4 — Insert Jurisdiction-Specific Elements:**
- Referências legais corretas para a jurisdição (Lei X.XXX/ano vs DL XX/ano vs Law No. X/year)
- Moeda correta (R$, €, $, AED)
- Foro correto (Comarca X / Tribunal Arbitral / Court of [cidade])
- Lei aplicável correta
- Termos fiscais corretos (IVA vs ISS vs VAT vs sales tax)

## Output Format

Contrato completo em texto, formatado para copiar/adaptar. Marcar com `[PLACEHOLDER: usar *draft-ip-clause]` e `[PLACEHOLDER: usar *generate-dpa]` onde especialização adicional é necessária.

## Veto Conditions

- Briefing incompleto sem campos obrigatórios → solicitar dados faltantes antes de gerar qualquer draft
- Jurisdição desconhecida sem YAML → raciocinar de first principles, sinalizar ao usuário

## Completion Criteria

- [ ] Todas as partes identificadas
- [ ] Escopo específico
- [ ] Valores e prazos preenchidos
- [ ] Jurisdição e foro declarados
