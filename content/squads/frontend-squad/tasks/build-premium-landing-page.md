# Task: build-premium-landing-page

> Construir uma landing page de conversão com narrativa scroll, micro-interactions e polish a11y. Estilo "padrão FIFA" / Awwwards.

## Quando usar

- LP de venda de produto físico ou digital
- LP de captação (lead gen, waitlist, beta)
- LP de evento / lançamento
- Página única com objetivo conversional claro

## Quando NÃO usar

- Site multi-página → use `*build-institutional-site`
- Dashboard / app → use `*build-saas-interface`
- Form-first (sem hero/scroll) → use `*build-interactive-form`

## Pré-requisitos

1. **Design system pronto** — tokens.json, brand manual, componentes base. Se não existir, parar e rodar `/design-system-chief`.
2. **Briefing de copy** — headline, subheadline, problema, solução, vantagens, CTA, FAQ. O chief pede ao usuário se faltar.
3. **Imagens/assets do hero** — opcional para v1; pode usar placeholder e o usuário substitui depois.

## Workflow (4 etapas + 1 polish)

### Etapa 1 — Olivier Larose: Scroll choreography

**Input:** copy + tokens + referências (se houver site Awwwards).
**O que ele faz:**
- Mapeia o documento em "movimentos" (introdução → problema → solução → prova → CTA)
- Define o ritmo de scroll: onde tem pin, onde tem scrub, onde tem parallax
- Escolhe stack: GSAP + Lenis + ScrollTrigger
- Entrega esqueleto HTML/JSX com data-attributes para animação + arquivo `animations/page.ts` com timelines
**Saída:** `page.tsx` (ou `index.html`) + `animations/scroll.ts`

### Etapa 2 — Emil Kowalski: Component-level micro-interactions

**Input:** HTML/JSX da etapa 1 + tokens.
**O que ele faz:**
- Adiciona micro-interactions nos botões (hover, focus, press)
- Anima entrada de cards (stagger via Framer Motion)
- Refina estados de loading e success (skeletons inteligentes, success animation)
- Garante interrupção (clicar antes da animação acabar não quebra)
**Saída:** componentes refinados com Framer Motion variants + estados visuais

### Etapa 3 — Sam Selikoff: Implementação React/Next.js

**Input:** os arquivos das etapas 1 e 2.
**O que ele faz:**
- Estrutura o Next.js App Router (page.tsx, layout.tsx, loading.tsx, components/)
- Server actions para form de captação (com optimistic update)
- Suspense boundaries para imagens lazy
- Otimização Next.js Image, font loading
- TypeScript strict
**Saída:** projeto Next.js rodável + `package.json`

### Etapa 4 — Josh Comeau: CSS polish + acessibilidade

**Input:** projeto rodável.
**O que ele faz:**
- Auditoria CSS (cascade, specificity, custom props consistentes)
- Dark mode setup (color-scheme, prefers-color-scheme, sem flash)
- prefers-reduced-motion respeitado em todas as animações
- Contraste WCAG AA mínimo
- Focus management visível e lógico
- Container queries onde fizer sentido
**Saída:** CSS final + `report-a11y.md`

### Etapa Polish — Rauno Freiberg (opcional, recomendado)

Se o budget permite, aciono Rauno para um pass final:
- Audit de "feel" — hover responde em < 100ms?
- Layout shift zero?
- Densidade tipográfica certa?
- Spacing rhythm coerente?
- Loading state evita salto?

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── package.json
├── next.config.js (se Next.js)
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── loading.tsx
├── components/
│   ├── Hero.tsx
│   ├── Problem.tsx
│   ├── Solution.tsx
│   ├── Proof.tsx
│   ├── CTA.tsx
│   └── FAQ.tsx
├── animations/
│   ├── scroll.ts
│   └── component-variants.ts
├── styles/
│   └── tokens.css (importado do design system)
├── public/ (assets)
└── report.md
```

`report.md` documenta:
- Decisões de stack (por que GSAP vs Framer Motion em cada lugar)
- Performance budget vs medido (Lighthouse / WebPageTest)
- A11y audit (axe results)
- Próximos passos (ex: substituir placeholder do hero)

## Checkpoints

- **Após etapa 1** — usuário valida o roteiro de scroll (faz sentido a narrativa?)
- **Após etapa 3** — usuário valida o projeto rodando localmente
- **Antes da entrega** — checklists `output-quality.md` + `motion-quality.md` passam

## Critérios de aceite

- Lighthouse Performance ≥ 90 em mobile
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1
- Sem erro no axe (WCAG AA)
- Scroll sequência funciona em desktop + mobile (sem travadas)
- Animações respeitam prefers-reduced-motion
- Dark mode sem flash, com persistência
- Mobile (375px) e desktop (1440px) ambos polidos

## Anti-padrões a evitar

- Animação só pra ficar bonito (sem propósito narrativo)
- ScrollTrigger sem `markers: false` em produção
- Lottie pesado sem lazy load
- Hero com vídeo autoplay >5s sem fallback
- CTA flutuante intrusivo no mobile
- Form com 7+ campos sem multi-step
