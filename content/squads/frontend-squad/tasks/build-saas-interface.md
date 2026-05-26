# Task: build-saas-interface

> Construir interface de produto / dashboard / app web com qualidade Linear-grade — polish, perf e densidade certa.

## Quando usar

- Dashboard de SaaS / produto interno
- App web autenticado (CRUD, listagens, formulários complexos)
- Painel admin
- Ferramenta de produtividade

## Quando NÃO usar

- LP de venda → use `*build-premium-landing-page`
- Site institucional → use `*build-institutional-site`

## Pré-requisitos

1. Design system com componentes de produto (não só de marketing) — Button, Input, Select, Modal, Toast, Drawer, Table, Card.
2. Especificação de telas (Figma ou descrição textual) — pelo menos 3 telas.
3. Modelo de dados / API (mesmo que mock).
4. Decisão de auth (Clerk, NextAuth, custom?).

## Workflow (4 etapas)

### Etapa 1 — Rauno Freiberg: Layout, densidade e hierarquia

**Input:** specs + design system.
**O que faz:**
- Define grid e spacing rhythm (compact? default? comfortable?)
- Hierarquia tipográfica para densidade alta (table, lista)
- Estados visuais: hover, focus, active, loading, empty, error
- Feedback loops: ações têm reação visual em < 100ms?
- Modo escuro pensado de saída (não retrofit)
**Saída:** `report-layout.md` + variáveis CSS / tokens secundários

### Etapa 2 — Sam Selikoff: Implementação React/Next.js

**Input:** etapa 1.
**O que faz:**
- Estrutura App Router com auth boundary
- Server components onde possível, client onde precisa interatividade
- Server actions para mutations
- TanStack Query / SWR para client cache
- Forms com server actions + optimistic update
- Suspense boundaries pensadas
- Streaming UI onde lista é grande
**Saída:** app rodando com mock data

### Etapa 3 — Emil Kowalski: Componentes interativos premium

**Input:** app rodando.
**O que faz:**
- Toast (Sonner) configurado e estilizado por design system
- Modal/Drawer (Vaul ou Radix) com animação de entrada/saída sem layout shift
- Command menu (cmdk) — busca rápida tipo Linear
- Tooltips com delay correto
- Dropdown / Select com animação refinada
- Loading skeletons que evitam saltos
**Saída:** components/ refinados

### Etapa 4 — Josh Comeau: CSS, a11y, dark mode

**Input:** app refinado.
**O que faz:**
- A11y profundo: ARIA roles, keyboard nav, focus trap em modais
- Dark mode com persistência (cookie no Next.js para evitar flash)
- Color contrast em todos os estados (loading, disabled, hover, focus)
- prefers-reduced-motion respeitado
- Screen reader friendly (anúncios em ARIA live para mudanças)
**Saída:** app final + `report-a11y.md`

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── app/
│   ├── (auth)/login/page.tsx
│   ├── (app)/dashboard/page.tsx
│   ├── (app)/{rota}/page.tsx
│   └── layout.tsx
├── components/
│   ├── ui/ (primitives: Button, Input, Modal...)
│   └── features/ (composições)
├── lib/ (utilities, server actions)
├── styles/
└── report.md
```

## Checkpoints

- **Após etapa 1** — usuário valida densidade e hierarquia
- **Após etapa 2** — usuário usa o app com mock data
- **Antes da entrega** — checklists passam

## Critérios de aceite

- Lighthouse ≥ 92 (SaaS pode ser mais que LP por menos imagens)
- INP < 100ms em interações típicas
- Tempo até interativo < 1.5s
- A11y: keyboard navegação completa, focus trap em modais, screen reader friendly
- Dark mode sem flash
- Empty/error states existem para todas as listas
- Mobile responsivo (mas SaaS pode priorizar desktop)

## Anti-padrões

- Spinner no lugar de skeleton (quebra densidade)
- Modal que reposiciona página atrás (CLS)
- Toast acumulando sem limite
- Form sem validação inline
- Tabela sem virtualization para listas grandes
- "Refresh página" depois de mutation (use optimistic + revalidate)
