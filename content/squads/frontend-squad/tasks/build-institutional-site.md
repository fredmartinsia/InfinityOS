# Task: build-institutional-site

> Construir um site institucional multi-página com transições e narrativa. Estilo agência / marca premium / portfólio.

## Quando usar

- Site de empresa/marca com 3+ páginas (Home, Sobre, Serviços, Contato)
- Portfólio de profissional/estúdio
- Site de produto B2B com várias seções
- Press kit / brand showcase

## Quando NÃO usar

- LP única → use `*build-premium-landing-page`
- App / dashboard → use `*build-saas-interface`

## Pré-requisitos

1. Design system pronto (tokens, components, brand manual).
2. Sitemap definido (quais páginas, em que ordem, links entre elas).
3. Copy de cada página (mesmo que rascunho) — pelo menos hero + 2 seções por página.
4. Decisão de 3D no hero (sim / não / depois) — afeta budget de perf.

## Workflow (5 etapas)

### Etapa 1 — Olivier Larose: Page transitions e arquitetura de scroll

**Input:** sitemap + tokens + referências (Awwwards / Lusion).
**O que faz:**
- Arquitetura de page transitions (View Transitions API ou Framer Motion shared layout)
- Scroll choreography por página (cada página tem ritmo próprio)
- Loader/preloader entre rotas
- Lenis smooth scroll global
**Saída:** `app/template.tsx` com transitions + `animations/page-transitions.ts`

### Etapa 2 — Bruno Simon (opcional, se hero é 3D): WebGL hero

**Input:** especificação do hero 3D (cenário, interação, mobile fallback).
**O que faz:**
- Cena Three.js (R3F preferido para integrar com React)
- Modelo Blender otimizado (glTF, draco compression)
- Performance budget: <2MB asset, 60fps mobile mid-tier
- Mobile fallback (imagem estática ou versão simplificada)
**Saída:** `components/HeroScene.tsx` + assets em `public/3d/`

### Etapa 3 — Sam Selikoff: Implementação Next.js

**Input:** das etapas 1 e 2.
**O que faz:**
- Estrutura App Router multi-página
- Layouts compartilhados (header, footer, navigation)
- Static generation onde possível, ISR para conteúdo que muda
- MDX se houver páginas de conteúdo (blog, case studies)
- TypeScript + Tailwind
**Saída:** projeto Next.js completo

### Etapa 4 — Rauno Freiberg: Polish de navegação e densidade

**Input:** projeto rodando.
**O que faz:**
- Navigation com hover states ricos
- Active state em links da nav
- Spacing rhythm consistente entre páginas
- Hierarquia tipográfica calibrada
- Loading states não-quebrados (skeleton ou progressive)
**Saída:** projeto polido + diff de melhorias

### Etapa 5 — Josh Comeau: CSS final e a11y

**Input:** projeto polido.
**O que faz:**
- Auditoria a11y completa (skip links, landmarks, headings hierarchy)
- Dark mode entre páginas (estado persistido)
- Focus management entre rotas (foco volta ao topo? mantém?)
- prefers-reduced-motion respeitado em todas as transitions
**Saída:** projeto final + `report-a11y.md`

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── app/
│   ├── (root)/page.tsx
│   ├── sobre/page.tsx
│   ├── servicos/page.tsx
│   ├── contato/page.tsx
│   ├── template.tsx (page transitions)
│   ├── layout.tsx
│   └── loading.tsx
├── components/
│   ├── HeroScene.tsx (se 3D)
│   ├── Navigation.tsx
│   ├── Footer.tsx
│   └── ...
├── animations/
├── public/
└── report.md
```

## Checkpoints

- **Após etapa 1** — usuário valida transitions e ritmo geral
- **Após etapa 2 (se 3D)** — usuário valida cena 3D em desktop e mobile
- **Após etapa 3** — usuário navega por todas as páginas
- **Antes da entrega** — ambos checklists passam

## Critérios de aceite

- Lighthouse ≥ 88 em mobile (3D abaixa um pouco vs LP simples)
- Page transition < 600ms total
- Sitemap completamente navegável
- 0 broken links
- A11y audit passa
- Mobile + desktop polidos
- Dark mode persiste entre páginas

## Anti-padrões

- 3D no hero sem mobile fallback
- Page transition que esconde conteúdo por > 1s
- Navigation que se reposiciona entre páginas (CLS)
- Loader infinito sem progresso percebido
