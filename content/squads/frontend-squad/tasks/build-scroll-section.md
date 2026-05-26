# Task: build-scroll-section

> Construir uma seção isolada de scroll storytelling — plugável em qualquer página existente. Uma única "cena" de animação scroll-driven.

## Quando usar

- Você já tem uma página e quer adicionar UMA seção animada (não refazer tudo)
- Showcase de feature dentro de site maior
- Componente reutilizável de scroll storytelling
- Estudo / experimento isolado antes de aplicar em página completa

## Quando NÃO usar

- Site inteiro com scroll → use `*build-premium-landing-page` ou `*build-institutional-site`
- Hero principal → use `*build-3d-hero-or-frame-video`

## Pré-requisitos

1. Design system com tokens.
2. Especificação clara da seção: o que entra, o que sai, qual é o "movimento" central?
3. Assets necessários (imagens, SVG, vídeo, modelo 3D leve).

## Workflow (3 etapas)

### Etapa 1 — Olivier Larose: Choreography da seção

**Input:** spec da seção + tokens.
**O que faz:**
- Mapeia o "movimento": entrada → ápice → saída
- Decide stack: GSAP + ScrollTrigger (recomendado) ou Framer Motion useScroll/useTransform
- Define triggers: start em qual ponto do viewport, end onde, scrub ou stagger
- Decide se a seção tem `pin: true` (fica fixa enquanto anima)
- Estrutura HTML/JSX com data-attributes
**Saída:** `components/ScrollSection.tsx` + `animations/scroll-section.ts`

### Etapa 2 — Cassie Evans: Animação dos elementos internos

**Input:** estrutura da etapa 1.
**O que faz:**
- Animação de SVG (paths, masks, morphing) se houver
- Stagger refinado (delay sequencial em cards/letras/items)
- Easing curves específicas (não default linear)
- prefers-reduced-motion alternativa: simplifica em vez de remover
**Saída:** timelines GSAP + transformações

### Etapa 3 — Sam Selikoff: Empacotamento como componente plugável

**Input:** etapas 1 e 2.
**O que faz:**
- Empacota como componente React isolado e reutilizável
- Props mínimas e claras (`<ScrollSection variant="A" />`)
- Cleanup correto (ScrollTrigger.kill on unmount)
- TypeScript types exportados
- Storybook ou demo standalone
**Saída:** componente exportável + demo

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── components/
│   ├── ScrollSection.tsx (componente principal)
│   └── scroll-section/
│       ├── elements/ (sub-componentes internos)
│       └── styles.module.css
├── animations/
│   └── scroll-section.ts
├── demo/
│   └── page.tsx (página standalone para testar)
└── report.md
```

## Checkpoints

- **Após etapa 1** — usuário valida o movimento central
- **Antes da entrega** — testa em diferentes contextos (top da página, meio, dentro de seção menor)

## Critérios de aceite

- 60fps no scroll
- Funciona em qualquer página onde for plugado (sem dependências de layout pai)
- Cleanup correto (ScrollTrigger não vaza memória)
- prefers-reduced-motion respeitado
- Mobile: animação simplificada se necessário, mas presente
- Documentação clara de como usar o componente

## Anti-padrões

- ScrollTrigger global sem cleanup
- Hardcoded de classes que dependem de layout pai
- Animação que quebra se a seção é colocada num `overflow: hidden`
- Pin sem `pinSpacing: false` quando o pai já gerencia
- Múltiplos ScrollTriggers em loop sem `id` (não dá pra debugar)
