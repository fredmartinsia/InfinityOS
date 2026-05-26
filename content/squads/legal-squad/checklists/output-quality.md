# Legal Output Quality Checklist

**Checklist ID:** LEGAL-CL-001
**Referenced by:** tasks/review.md
**Purpose:** Validate legal deliverables (contracts, DPAs, clauses, compliance reports) for quality before delivery.

[[LLM: INITIALIZATION INSTRUCTIONS

This checklist validates legal output specifically.

EXECUTION APPROACH:
1. For each category, verify every item against the deliverable
2. Mark items as [x] Pass, [ ] Fail, [N/A] Not Applicable
3. CRITICAL items block delivery — do NOT deliver with any CRITICAL unchecked
4. Run this checklist AFTER risk-auditor red-team review
5. If any CRITICAL fails: return to contract-architect or relevant specialist for correction

CRITICAL items are marked with (CRITICAL) suffix.]]

---

## 1. Conformidade Regulatória

- [ ] DPA ou cláusulas equivalentes de proteção de dados presentes se há tratamento de dados pessoais (GDPR/LGPD/CCPA/UAE PDPL/UU PDP/equivalente) (CRITICAL)
- [ ] Base legal do tratamento de dados identificada explicitamente na jurisdição aplicável (CRITICAL)
- [ ] Governing law e foro/arbitragem declarados e preenchidos — nunca em branco (CRITICAL)
- [ ] Consumer law local respeitada quando há parte consumidora (CDC/DL 24-2014 PT/FTC+UDAP/UAE Consumer Protection/etc.)
- [ ] Obrigações fiscais compatíveis com a jurisdição (IVA/VAT/ISS/sales tax/withholding) mencionadas ou consideradas

## 2. Proteção de Ambas as Partes

- [ ] Limitação de responsabilidade com cap numérico definido e carve-outs razoáveis (CRITICAL)
- [ ] Propriedade intelectual dos entregáveis explicitada durante a vigência E após rescisão (CRITICAL)
- [ ] Todos os anexos referenciados no corpo do contrato existem e estão preenchidos — nenhum em branco (CRITICAL)
- [ ] Cláusula de indenização presente e simétrica (sem assimetria abusiva)
- [ ] Confidencialidade com escopo, duração e exceções definidos
- [ ] Non-solicitation presente se o modelo de negócio justifica (pessoal + deliverables)

## 3. Cláusulas Críticas Obrigatórias

- [ ] Rescisão com prazo de notificação prévia E direito de cura antes de penalidade (CRITICAL)
- [ ] Escopo de serviços específico com entregáveis mensuráveis — sem "prazo razoável" isolado (CRITICAL)
- [ ] Red-team (risk-auditor) passou sem flags CRITICAL pendentes (CRITICAL)
- [ ] Força maior com clarificação explícita de outages de plataformas de terceiros
- [ ] Cláusula de cessão do contrato (com ou sem consentimento da outra parte)
- [ ] Reajuste atrelado a índice objetivo (IPCA/IPC-PT/CPI/equivalente) — não discricionário
- [ ] Modificações ao contrato exigem forma escrita

## 4. Clareza e Enforceability

- [ ] Terminologia consistente ao longo do documento (mesmo termo para o mesmo conceito) (CRITICAL)
- [ ] SLA ou prazos quantificados por severidade quando o serviço tem componente operacional
- [ ] Ausência de cláusulas contraditórias entre si
- [ ] Preâmbulo identifica as partes com dados completos (pessoa jurídica: número de registro, endereço, representante)
- [ ] Valores numéricos (prazo de aviso prévio, multas, caps, prazos de cura) são razoáveis e defensáveis
- [ ] Fluxo de rescisão é claro: gatilho → notificação → prazo → consequências

## 5. Riscos & Adversarial

- [ ] Contrato resiste ao teste "como a contraparte rompe isso sem penalidade?" (CRITICAL)
- [ ] Ausência de cláusulas potencialmente abusivas (CDC/Consumer Protection/Unfair Terms Directive)
- [ ] Nenhuma cláusula nula de pleno direito que possa contaminar o contrato
- [ ] Assimetrias entre prestador e cliente são justificadas pelo contexto negocial
- [ ] Contrato resiste ao teste "como um juiz da jurisdição aplicável interpretaria a cláusula mais ambígua?"
- [ ] Escopo não permite que o cliente exija mais do que foi contratado sem aprovação e custo adicional

---

## PASS/FAIL Criteria

**PASS:** All CRITICAL items [x] and fewer than 3 non-critical failures.
**REVISE:** All CRITICAL items [x] but 3+ non-critical failures — return to specialist.
**FAIL:** Any CRITICAL item unchecked — DO NOT DELIVER. Return to contract-architect or risk-auditor.

---

## Usage Notes

- Run AFTER risk-auditor `*red-team-review` — não substitui, complementa
- Para contratos multi-jurisdição: verificar itens regulatórios para CADA jurisdição envolvida
- DPA em branco = FAIL imediato se há tratamento de dados pessoais
- Foro em branco = FAIL imediato — sempre
