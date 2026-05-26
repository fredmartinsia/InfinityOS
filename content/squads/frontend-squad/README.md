# Frontend Squad — Web design e animação premium

Squad de **execução frontend** com 7 especialistas reais (clones) + 1 chief orquestrador. Constrói sites institucionais, landing pages, formulários interativos, SaaS e sistemas com qualidade Awwwards: scroll storytelling, frame-by-frame video, 3D/WebGL, micro-interactions Linear-grade.

**Consome** o design system pronto entregue pelo `design-system-squad`. **Não redesenha** tokens nem brand strategy — só executa o build com a alma certa.

## Time

### Tier 0 — Orquestrador
- 🎯 **frontend-chief** — Diagnostica, roteia, valida. Lê o design system antes de tudo.

### Tier 1 — Animação & storytelling cinematográfico
- 🎬 **Olivier Larose** — Scroll storytelling com GSAP + Lenis. Sites Awwwards-grade.
- 🌌 **Bruno Simon** — Three.js, WebGL, hero 3D, frame-by-frame video. Three.js Journey.
- 🎞️ **Cassie Evans** — GSAP/ScrollTrigger e SVG animation. GreenSock advocate.

### Tier 2 — Engenharia de interface
- 🧩 **Emil Kowalski** — Animação a nível de componente (Sonner, Vaul). Detalhes que outros ignoram.
- ⚡ **Rauno Freiberg** — Design engineering Linear-grade. Polish, perf, "feel".
- 🛠️ **Sam Selikoff** — Implementação React/Next.js + Tailwind + Framer Motion (Build UI).

### Tier 3 — CSS moderno e acessibilidade
- 🎨 **Josh Comeau** — Mental models de CSS, dark mode, a11y, animação CSS-only.

## Como usar

### Modo workflow (entrada padrão pelo chief)

```
/frontend-chief
```

O chief apresenta menu com 8 workflows. Escolha um:

| Comando | Quando usar |
|---------|-------------|
| `*build-premium-landing-page` | LP de conversão com narrativa scroll |
| `*build-institutional-site` | Site multi-página para marca/empresa |
| `*build-saas-interface` | Dashboard / produto / app web |
| `*build-interactive-form` | Form multi-step, pesquisa, quiz |
| `*build-3d-hero-or-frame-video` | Hero WebGL ou estilo Apple iPhone page |
| `*build-scroll-section` | Seção isolada plugável em qualquer página |
| `*audit-and-polish-existing` | Diagnóstico + polish de site que já existe |
| `*extract-from-reference` | Decompõe site de referência e replica técnica |

### Modo direto (chamar especialista)

```
/olivier-larose       # scroll animations e GSAP
/bruno-simon          # Three.js / WebGL
/cassie-evans         # animação SVG e GSAP/ScrollTrigger
/emil-kowalski        # animação de componentes
/rauno-freiberg       # polish e design engineering
/sam-selikoff         # implementação React/Next.js
/josh-comeau          # CSS moderno e a11y
```

## Cross-squad

Este squad **consome** o output do `design-system-squad`. Antes de executar, o chief lê:

1. `o negócio do usuário-brand/v2/` — tokens, componentes, brand manual
2. `o negócio do usuário-brand/deploy/manutencaopcgamer/index.html` — referência canônica
3. Qualquer `design system/{brand}/DESIGN.md` em projetos custom

Se o design system não existir, o chief pede para rodar `/design-system-chief` primeiro.

## Não-negociáveis

- Toda animação tem propósito narrativo — sem decoração descartável.
- `prefers-reduced-motion` é respeitado por padrão.
- Performance budget definido ANTES da implementação (LCP < 2.5s, INP < 200ms, CLS < 0.1).
- Tokens do design system sempre consumidos — nunca hex inline.
- Mobile-first para LPs, desktop-first para SaaS.
- Nenhuma entrega sem checklists `output-quality.md` + `motion-quality.md`.

## Output

Cada workflow grava em:

```
squads/frontend-squad/output/{project-slug}/
├── index.html (ou pages/ do Next.js)
├── components/
├── animations/
└── report.md   ← decisões de stack, perf, a11y
```

Aprendizados são gravados em `_memory/memories.md` após cada sessão.
