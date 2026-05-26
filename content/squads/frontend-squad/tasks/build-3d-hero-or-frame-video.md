# Task: build-3d-hero-or-frame-video

> Construir hero WebGL ou frame-by-frame video estilo Apple iPhone product page. Experiência cinematográfica de alto impacto.

## Quando usar

- Hero principal de site institucional ou produto premium
- Showcase de produto físico (carro, hardware, gadget)
- Frame-by-frame scroll-driven video (estilo Apple iPhone, AirPods Pro page)
- Cena 3D interativa com mouse / scroll / touch

## Quando NÃO usar

- LP simples sem necessidade de wow factor 3D → use `*build-premium-landing-page`
- Mobile-first com budget apertado (3D pesa) — ou planeje fallback

## Pré-requisitos

1. **Decisão clara: 3D real (Three.js) ou frame-by-frame video (canvas/img sequence)?**
   - 3D real: interatividade total, mas mais peso, mais risco de mobile não aguentar
   - Frame-by-frame: zero interatividade, mas ultra-controlado, mobile aguenta com sequência otimizada
2. Asset 3D (modelo Blender) ou sequência de frames (200-600 imagens em WebP/AVIF)
3. Performance budget: bundle target, FPS target, mobile mid-tier OK?

## Decisão entre os dois caminhos

### Caminho A — 3D real (Three.js / R3F)
**Quando escolher:**
- Usuário precisa interagir com a cena (rotacionar, zoom, hover em partes)
- Cena tem múltiplas variações dinâmicas (cor do produto, etc.)
- Vai virar showcase configurável

### Caminho B — Frame-by-frame video
**Quando escolher:**
- Animação é linear e pré-determinada (scroll → frame N)
- Estilo "Apple iPhone product page"
- Usuário quer máximo controle visual sem custo de runtime
- Asset 3D já existe e é renderizado em offline

## Workflow Caminho A — 3D real (3 etapas)

### Etapa A1 — Bruno Simon: Cena Three.js / R3F

**Input:** modelo Blender (.glb otimizado), specs de interação.
**O que faz:**
- Setup R3F (Canvas, useFrame, drei helpers)
- Carrega modelo via gltf-jsx ou useGLTF
- Lighting (Environment map, key light, fill)
- Camera setup (perspective ou ortho, FOV ajustado)
- Otimizações: draco compression, instancing, frustum culling
- Mobile fallback (tier detection ou imagem estática)
**Saída:** `components/HeroScene.tsx` + `public/3d/{asset}.glb`

### Etapa A2 — Olivier Larose: Scroll-driven camera

**Input:** cena Bruno.
**O que faz:**
- ScrollTrigger sincronizando posição/rotação da câmera
- Curvas de easing para movimento de câmera (não linear)
- Triggers entre seções (hero → scrolled → next-section)
- Lenis para suavizar scroll
**Saída:** `animations/hero-camera.ts`

### Etapa A3 — Rauno Freiberg: Polish de carregamento

**Input:** etapas A1 + A2.
**O que faz:**
- Preloader com progresso real (não falso)
- Suspense boundary com skeleton 3D
- Feedback visual durante carregamento (não tela branca)
- Mobile detection + fallback graceful
**Saída:** UX de carregamento polido

## Workflow Caminho B — Frame-by-frame video (3 etapas)

### Etapa B1 — Bruno Simon: Pipeline de frames otimizados

**Input:** sequência de frames (renderizada em Blender ou similar).
**O que faz:**
- Otimização: WebP ou AVIF, dimensões corretas (1920x1080 desktop, 1080x1920 mobile)
- Preload strategy: primeiros N frames priority, restante lazy
- Image atlas (sprite sheet) para reduzir requests
- Mobile: sequência reduzida (60% dos frames)
**Saída:** `public/frames/{name}-{N}.webp` (200-600 frames) + `frames-manifest.json`

### Etapa B2 — Olivier Larose: Scroll-driven canvas painting

**Input:** frames otimizados.
**O que faz:**
- Canvas 2D que pinta o frame correto baseado em scroll progress
- ScrollTrigger com scrub: true para sincronia perfeita
- Pin da seção enquanto a animação roda
- Throttle de updates para 60fps
**Saída:** `components/FrameByFrameHero.tsx`

### Etapa B3 — Cassie Evans: Polish de overlays SVG/animação

**Input:** etapas B1 + B2.
**O que faz:**
- Texto que aparece em momentos específicos da sequência (sobre o canvas)
- Animação de letras/words em sync com o canvas
- SVG decorations animados em momentos chave
- Smooth handoff entre seção da animação e seção seguinte
**Saída:** overlays + sincronização

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── components/
│   ├── HeroScene.tsx (Caminho A) OU FrameByFrameHero.tsx (Caminho B)
│   └── HeroOverlay.tsx (texto/SVG sobreposto)
├── animations/
│   └── hero-{camera|frames}.ts
├── public/
│   ├── 3d/{asset}.glb (A) OU frames/*.webp (B)
│   └── frames-manifest.json (B)
└── report.md (decisão A vs B + perf budget medido)
```

## Checkpoints

- **Antes de começar** — usuário escolhe Caminho A ou B (com Bruno explicando trade-offs)
- **Após Etapa 1** — usuário valida cena/asset em desktop
- **Após Etapa 2** — usuário valida scroll behavior
- **Antes da entrega** — perf testada em mobile mid-tier

## Critérios de aceite

### Caminho A (3D)
- 60fps em desktop, 30fps+ em mobile mid-tier
- Bundle 3D < 2MB
- Modelo glTF com draco compression
- Mobile fallback presente e ativado em tier baixo
- Preloader com progresso real

### Caminho B (frames)
- 60fps no scroll (sem stuttering)
- Frames < 50KB cada (WebP otimizado)
- First frame visível em < 1s
- Sequência mobile separada (menor)
- Sem flash entre frames

## Anti-padrões

- 3D sem mobile fallback (deixa metade dos usuários ver tela preta)
- Frame-by-frame com PNG de 200KB cada (3GB de assets total)
- Modelo Blender de 50MB sem otimização
- ScrollTrigger sem `invalidateOnRefresh` em layout que muda
- Câmera com movimento linear (sem easing)
- Hero 3D que bloqueia LCP (use lazy/Suspense)
