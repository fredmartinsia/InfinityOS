# Task: audit-and-polish-existing

> Diagnosticar um site/app já existente e propor + aplicar polish: perf, a11y, design polish, motion onde fizer sentido.

## Quando usar

- Site já em produção que precisa elevar de nível
- LP que converte mas "parece básica"
- App que funciona mas tem detalhes quebrados (layout shifts, animações ruins, hovers inconsistentes)
- Site herdado de outra equipe / agência

## Quando NÃO usar

- Construir do zero → use o workflow correspondente (LP, site, SaaS)
- Refazer 80% — se for esse o caso, é melhor reconstruir

## Pré-requisitos

1. Acesso ao projeto (URL pública ou repositório local)
2. Design system existente (mesmo que rudimentar — vamos consumir o que tem)
3. Permissão para mexer no que precisa

## Workflow (4 etapas — todas começam com diagnóstico)

### Etapa 1 — Rauno Freiberg: Audit de "feel" e polish

**Input:** projeto rodando.
**O que faz:**
- Audit de hover states (todos respondem em < 100ms?)
- Audit de focus states (visíveis e lógicos?)
- Audit de loading states (skeleton ou pula?)
- Audit de spacing rhythm (consistente entre seções?)
- Audit de typography hierarchy (peso e tamanhos coerentes?)
- Audit de density (compact, default, comfortable — apropriado pro contexto?)
- Audit de feedback loops (toda ação tem feedback visual?)
**Saída:** `report-feel.md` com lista priorizada de fixes

### Etapa 2 — Josh Comeau: Audit de CSS e a11y

**Input:** projeto + report da etapa 1.
**O que faz:**
- axe-core audit (WCAG AA mínimo)
- Lighthouse a11y
- Color contrast em todos os estados (incluindo hover/disabled)
- Keyboard nav completo (Tab, Enter, Esc funcionam onde devem?)
- Screen reader test (pelo menos VoiceOver ou NVDA)
- Dark mode existe? Funciona sem flash?
- prefers-reduced-motion respeitado?
- CSS arquitetura saudável? (cascade, specificity, custom props)
**Saída:** `report-a11y.md` com violations + fixes

### Etapa 3 — Emil Kowalski: Audit de animações e micro-interactions

**Input:** projeto + reports anteriores.
**O que faz:**
- Cada animação tem propósito? (ou é decoração?)
- Easing curves apropriadas? (linear é ruim em quase tudo)
- Layout shifts durante animação?
- Animações interruptíveis?
- Toast / modal / drawer com animação polida?
- Botões com micro-interactions de press?
**Saída:** `report-motion.md` com lista de animações ruins + sugestões

### Etapa 4 — Sam Selikoff: Aplicação dos fixes priorizados

**Input:** os 3 reports.
**O que faz:**
- Prioriza fixes em 3 baldes: **Crítico** (a11y violations, perf < 50), **Importante** (feel issues, motion ruim), **Polish** (densidade, micro-detalhes)
- Aplica fixes em commits separados e claros
- Testa cada fix antes de mergear
- Documenta decisões em `report-fixes.md`
**Saída:** PRs ou diff aplicado + report final

## Etapa Bônus — Olivier Larose (se diagnóstico apontar falta de movimento)

Se o site é "polido mas estático demais", aciono Olivier para:
- Adicionar 1-2 momentos de scroll storytelling em pontos chave
- Page transitions sutis se ainda não existirem
- Sem reformar tudo — adições cirúrgicas

## Entrega

```
squads/frontend-squad/output/{slug}-audit/
├── README.md
├── reports/
│   ├── report-feel.md (Rauno)
│   ├── report-a11y.md (Josh)
│   ├── report-motion.md (Emil)
│   └── report-fixes.md (Sam — o que foi aplicado)
└── diff/ (ou PRs no repositório)
```

## Checkpoints

- **Após etapas 1+2+3** — usuário decide o que entra no escopo do polish (não precisa fazer tudo)
- **Antes de aplicar** — usuário aprova prioridade
- **Após aplicar** — re-audit dos 3 mostra melhora mensurável

## Critérios de aceite

- Lighthouse: melhora de pelo menos +10 pontos em uma das categorias
- axe: zero violations críticas restantes
- Lista priorizada documentada (não "consertei tudo aleatório")
- Commits/PRs separados por categoria
- Re-audit comprova melhora

## Anti-padrões

- "Refatorar enquanto conserta" (vire um workflow novo)
- Aplicar 50 fixes sem decidir prioridade (caos no git)
- Trocar stack durante audit (foge do escopo)
- Ignorar a11y porque "ninguém usa screen reader" (ilegal e errado)
- Adicionar animações decorativas no audit (audit é tirar o ruim, não adicionar mais)
