# Task: extract-from-reference

> Receber URL ou vídeo de referência (ex: site Awwwards, tutorial YouTube), decompor a técnica e entregar plano de réplica adaptado ao design system do usuário.

## Quando usar

- Usuário viu um site impressionante e quer replicar a técnica (sem copiar visualmente)
- Tutorial YouTube de animação que precisa ser adaptado para o projeto
- Site Awwwards Site of the Day como inspiração de movimento
- Cliente mandou "quero igual a esse aqui"

## Quando NÃO usar

- Cópia visual literal (problema legal e estratégico) — adaptamos a técnica, não o visual
- Replicar logo/marca — fora de escopo

## Pré-requisitos

1. URL do site OU link do vídeo OU screenshots da animação a replicar
2. Design system pronto (vamos adaptar a técnica para os tokens do usuário)
3. Decisão sobre escopo: replicar página inteira, uma seção, uma única animação?

## Workflow (3 etapas)

### Etapa 1 — frontend-chief: Decomposição da referência

**Input:** URL ou vídeo.
**O que faz:**
- Abre a referência (DevTools, performance tab, source view)
- Identifica stack provável (GSAP? Three.js? Framer Motion? CSS only?)
- Mapeia as técnicas usadas em uma lista numerada:
  - "1. Hero com pinned scroll-section, transformações em CSS via GSAP"
  - "2. Texto com split-by-letter + stagger reveal"
  - "3. Cursor magnético customizado"
  - etc.
- Para cada técnica, identifica complexidade (baixa / média / alta) e tempo estimado
- Identifica quais técnicas valem a pena vs quais são "show-off" desnecessário
**Saída:** `decomposition.md` com lista de técnicas + análise

### Etapa 2 — Especialista do tipo dominante: Plano de réplica

**Input:** decomposition.md.
**Quem é acionado:** depende do tipo dominante:
- Scroll storytelling → **Olivier Larose**
- 3D / WebGL → **Bruno Simon**
- Animação SVG → **Cassie Evans**
- Component animation → **Emil Kowalski**

**O que o especialista faz:**
- Para cada técnica do decomposition, propõe implementação no contexto do design system do usuário
- Adapta para tokens do usuário (não copia hex/typography da referência)
- Avalia trade-offs: vale a pena cada técnica? Performance custo? Acessibilidade?
- Gera plano: "implemente A primeiro, depois B, deixe C como nice-to-have"
**Saída:** `replica-plan.md`

### Etapa 3 — Sam Selikoff: Implementação

**Input:** replica-plan.md.
**O que faz:**
- Implementa as técnicas priorizadas no projeto do usuário
- Substitui visuais da referência por assets/tokens do usuário
- Valida que cada técnica funciona no contexto novo
- Documenta o que foi pulado e por quê
**Saída:** projeto/seção implementada + report

## Entrega

```
squads/frontend-squad/output/{slug}-from-reference/
├── README.md
├── decomposition.md (etapa 1)
├── replica-plan.md (etapa 2)
├── components/ (ou app/)
├── animations/
└── report.md (o que foi feito, o que foi cortado, próximos passos)
```

## Checkpoints

- **Após etapa 1** — usuário valida a decomposição (faz sentido?)
- **Após etapa 2** — usuário aprova o plano de réplica (escopo, prioridades)
- **Antes da entrega** — checklists passam

## Critérios de aceite

- Decomposição lista pelo menos 5 técnicas distintas (referência boa tem várias)
- Plano de réplica é adaptado ao design system do usuário, não cópia
- Implementação respeita perf budget (não importa as técnicas a custo de performance)
- Report explica o que foi cortado e por quê (transparência)

## Anti-padrões

- Cópia visual direta (legal e estratégico)
- Implementar tudo que viu, sem priorizar
- Replicar técnica que não tem sentido no contexto do usuário
- Ignorar perf da referência (Awwwards às vezes ignora mobile)
- Hardcode de valores da referência em vez de usar tokens
- "Vou só adaptar depois" — adapta junto, não depois

## Exemplos de decomposição

### Exemplo 1: Site Awwwards SOTD com hero 3D + scroll storytelling

```
1. Hero scene 3D com Three.js + R3F (alta complexidade, alto custo perf)
2. Scroll-pinned section com camera movement (média complexidade)
3. Texto que aparece palavra por palavra com stagger (baixa complexidade)
4. Cursor magnético em CTAs (baixa, mas custom)
5. Page transition com mask reveal (média)
6. Footer com Lottie em loop (baixa, mas pode pesar)

Vale tudo? Não — Lottie em loop é decoração descartável. 
Mantém: 1, 2, 3, 4, 5. Corta: 6.
```

### Exemplo 2: Tutorial YouTube de Olivier Larose

```
1. Lenis smooth scroll setup
2. ScrollTrigger pin com horizontal scroll
3. Stagger reveal de cards com clip-path
4. Magnetic button com mousemove

Tudo aplicável. Adaptamos cores e typography para tokens do user.
Tempo estimado: 4-6 horas para implementar tudo.
```
