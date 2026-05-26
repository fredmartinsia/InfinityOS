---
name: olivier-larose_06_KNOWLEDGE_COMPLETE
description: Núcleo de expertise técnica de Olivier Larose — GSAP, Lenis, Framer Motion, Three.js, Next.js, técnicas-assinatura
type: clone-knowledge
clone: olivier-larose
---

# Conhecimento Completo — Olivier Larose

> Este é o **arquivo nuclear** do clone. Tudo que ele "sabe" tecnicamente está aqui em forma utilizável. Snippets são prontos para colar em projeto Next.js App Router + TypeScript.

---

## 1. GSAP (GreenSock Animation Platform)

### Por que GSAP é o pilar

GSAP é a biblioteca de animação web mais completa em 2026. Ela ganhou status de standard porque:
- API consistente (`gsap.to`, `gsap.from`, `gsap.fromTo`, `gsap.timeline`).
- Easings expressivos sem reinventar (`power3.out`, `back.out(1.7)`, `elastic.out(1, 0.4)`).
- Performance superior em casos complexos (timelines coordenadas).
- Plugin ecosystem (ScrollTrigger, Flip, SplitText, Observer, MotionPath).
- Compatibilidade com qualquer framework (vanilla, React, Vue, Svelte).

Em 2024 a GreenSock anunciou que **todos os plugins ficaram free**, o que removeu a última fricção comercial. Hoje não há razão técnica para não usar GSAP em sites premium.

### Setup em Next.js App Router

```ts
// hooks/useGsap.ts
'use client';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

export function useGsap(callback: (ctx: gsap.Context) => void, deps: unknown[] = []) {
  const scope = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => callback(ctx), scope);
    return () => ctx.revert();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return scope;
}
```

A função `gsap.context()` é chave em React: encapsula seletores e cleanup, evitando vazamento entre re-renders.

### Timeline coreografada (padrão hero)

```ts
const tl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.9 } });

tl.from('.hero__bg',       { scale: 1.08, autoAlpha: 0, duration: 1.4 })
  .from('.hero__word',     { yPercent: 110, stagger: 0.06 }, '-=1.0')
  .from('.hero__cta',      { y: 30, autoAlpha: 0, ease: 'back.out(1.7)' }, '-=0.4');
```

Pontos: `defaults` herda em todo o timeline; offsets negativos (`'-=1.0'`) sobrepõem cenas para criar densidade narrativa; `back.out(1.7)` no CTA dá overshoot sutil.

### ScrollTrigger — patterns canônicos

```ts
// Reveal on enter
gsap.from('.section-title', {
  yPercent: 100, autoAlpha: 0, duration: 1, ease: 'power3.out',
  scrollTrigger: { trigger: '.section-title', start: 'top 80%' },
});

// Pin + scrub (horizontal scroll)
gsap.to('.h-track', {
  x: () => -(track.scrollWidth - innerWidth),
  ease: 'none',
  scrollTrigger: {
    trigger: '.h-section', pin: true, scrub: 1,
    end: () => `+=${track.scrollWidth - innerWidth}`,
    invalidateOnRefresh: true,
  },
});

// Parallax background
gsap.to('.bg', {
  yPercent: -30,
  ease: 'none',
  scrollTrigger: { trigger: '.bg-wrap', start: 'top bottom', end: 'bottom top', scrub: true },
});
```

### SplitText — texto palavra por palavra

```ts
import SplitText from 'gsap/SplitText';
gsap.registerPlugin(SplitText);

const split = new SplitText('.headline', { type: 'words,chars' });
gsap.from(split.words, {
  yPercent: 110, opacity: 0, stagger: 0.06, duration: 0.9, ease: 'power3.out',
  onComplete: () => split.revert(), // libera DOM original
});
```

Sempre `revert()` no `onComplete` para evitar problemas de SEO/acessibilidade após a animação.

### Flip plugin — layout transitions

```ts
import { Flip } from 'gsap/Flip';
gsap.registerPlugin(Flip);

const state = Flip.getState('.card');
// muda layout (ex: classe que move o card)
card.classList.toggle('expanded');
Flip.from(state, { duration: 0.8, ease: 'power3.inOut', absolute: true });
```

A técnica FLIP grava o estado, deixa o browser recalcular o layout, e anima do estado capturado para o atual. Resultado: transições impossíveis com CSS puro.

---

## 2. Lenis (smooth scroll)

### Por que Lenis sobre Locomotive

Lenis é mais leve, tem API menor, e foi construído para conviver com ScrollTrigger sem hacks. Em 2026, Lenis substituiu Locomotive na maioria dos sites Awwwards-grade. Locomotive virou legado.

### Setup em App Router

```ts
// app/components/SmoothScroll.tsx
'use client';
import { useEffect } from 'react';
import Lenis from 'lenis';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import gsap from 'gsap';

export default function SmoothScroll() {
  useEffect(() => {
    const lenis = new Lenis({
      lerp: 0.1,
      wheelMultiplier: 1,
      smoothWheel: true,
      // smoothTouch: false (default) — mantenha assim. Smooth touch quebra UX em mobile.
    });

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(lenis.raf as unknown as (time: number) => void);
    };
  }, []);
  return null;
}
```

Esse component vai no `layout.tsx` raiz para Lenis ser global.

### Configurações que Olivier escolhe

- `lerp: 0.1` — suavização sutil. `0.05` fica pesado, `0.15+` quase desativa o smooth.
- `smoothWheel: true`, `smoothTouch: false` — touch nativo é melhor que qualquer simulação.
- `wheelMultiplier: 1` — não acelera artificialmente o scroll.
- Para hero pages com pinning: às vezes desliga o Lenis temporariamente para evitar conflitos.

---

## 3. Framer Motion

### Quando Framer Motion sobre GSAP

Componentes React isolados, mount/unmount controlado, gestos (drag, hover, tap), e shared element transitions — Framer Motion vence. Para coreografia complexa de página, GSAP vence.

### `AnimatePresence` (mount/unmount)

```tsx
import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence mode="wait">
  {open && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
    />
  )}
</AnimatePresence>
```

A curva `[0.22, 1, 0.36, 1]` é um Bezier custom equivalente a `power3.out` — Olivier mantém um pequeno catálogo dessas curvas para usar consistentemente.

### `useScroll` + `useTransform` (parallax controlado)

```tsx
'use client';
import { motion, useScroll, useTransform } from 'framer-motion';

export function ParallaxImage() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '-30%']);
  return <motion.img src="/hero.webp" style={{ y }} />;
}
```

### `layoutId` — shared element transitions

```tsx
// Card na grid
<motion.div layoutId={`card-${id}`} onClick={() => setOpen(true)}>{...}</motion.div>

// Modal expandido
<motion.div layoutId={`card-${id}`}>{...}</motion.div>
```

Framer Motion calcula a transição entre os dois automaticamente. É a técnica FLIP encapsulada.

---

## 4. Three.js (nível operacional)

Olivier não é especialista em shaders. Ele implementa cenas básicas com `@react-three/fiber` + `@react-three/drei` com fluência. Casos típicos: imagens distorcidas no hover (com displacement map), partículas leves, esfera com matcap material.

### Setup mínimo

```tsx
'use client';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';

export function Scene() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
      <Environment preset="studio" />
      <mesh>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial color="#C9A84C" roughness={0.2} metalness={0.8} />
      </mesh>
      <OrbitControls enableZoom={false} />
    </Canvas>
  );
}
```

Para cenas complexas (shaders, post-processing), Olivier delega ou aprende sob demanda — mas o foco do canal não é WebGL avançado.

---

## 5. Next.js App Router (plataforma de produção)

### `template.tsx` é a chave de page transitions

`layout.tsx` persiste entre rotas (não re-renderiza). `template.tsx` re-renderiza por rota — ideal para mount/unmount transitions.

```tsx
// app/template.tsx
'use client';
import { motion } from 'framer-motion';

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}
```

### Server vs Client Component

Animação requer browser APIs (DOM, requestAnimationFrame, scroll). Logo, qualquer componente que anima é Client Component (`'use client'`). O resto do site pode (e deve) ser Server Component para performance.

### `loading.tsx` — preloader narrativo nativo

Next.js renderiza `loading.tsx` durante suspense. Olivier usa isso para preloaders com narrativa:

```tsx
export default function Loading() {
  return (
    <div className="loader">
      <span className="loader__counter">00 — 99</span>
    </div>
  );
}
```

E anima o counter com GSAP no client.

---

## 6. Técnicas-assinatura

### 6.1. Magnetic button

```ts
'use client';
const btn = ref.current!;
const radius = 120;
const onMove = (e: PointerEvent) => {
  const rect = btn.getBoundingClientRect();
  const dx = e.clientX - (rect.left + rect.width / 2);
  const dy = e.clientY - (rect.top + rect.height / 2);
  const dist = Math.hypot(dx, dy);
  if (dist < radius) {
    gsap.to(btn, { x: dx * 0.4, y: dy * 0.4, duration: 0.4, ease: 'power3.out' });
  }
};
const onLeave = () => gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: 'elastic.out(1, 0.4)' });
btn.addEventListener('pointermove', onMove);
btn.addEventListener('pointerleave', onLeave);
```

Três variáveis: `radius` (100-150), `pull strength` (0.3-0.5), `return easing` (`elastic.out(1, 0.4)`).

### 6.2. Custom cursor com lerp

```ts
const cursor = ref.current!;
let mx = 0, my = 0, cx = 0, cy = 0;
window.addEventListener('pointermove', (e) => { mx = e.clientX; my = e.clientY; });
const tick = () => {
  cx += (mx - cx) * 0.15;
  cy += (my - cy) * 0.15;
  cursor.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
  requestAnimationFrame(tick);
};
tick();
```

Fator `0.15` no lerp dá smooth elegante. CSS no cursor: `mix-blend-mode: difference` para reagir ao fundo.

### 6.3. Scroll-driven typography reveal

Combine SplitText (palavras) + ScrollTrigger:

```ts
const split = new SplitText('.section-h2', { type: 'words' });
gsap.from(split.words, {
  yPercent: 110, opacity: 0, stagger: 0.06, duration: 0.9, ease: 'power3.out',
  scrollTrigger: { trigger: '.section-h2', start: 'top 75%' },
});
```

Pai com `overflow: hidden` para o efeito de "máscara".

### 6.4. Image preloader narrativo

Não barra de progresso. Counter de 00 a 99 + reveal de marca + transição em curtain (mask-clip-path):

```ts
const tl = gsap.timeline();
tl.to({ v: 0 }, {
  v: 99, duration: 3, ease: 'power2.inOut',
  onUpdate() { counter.textContent = String(Math.floor(this.targets()[0].v)).padStart(2, '0'); },
})
.to('.preloader', { yPercent: -100, duration: 1.2, ease: 'power3.inOut' });
```

### 6.5. Horizontal scroll com pinning

Ver snippet em §1 (ScrollTrigger). Detalhes finos: `invalidateOnRefresh` é obrigatório; o `end` deve ser função para responder a resize; o track precisa ter `display: flex` com `width: max-content`.

### 6.6. Page transitions coordenadas

A combinação completa: `template.tsx` com `AnimatePresence` ou GSAP + curtain element global + Lenis pause durante a transição:

```ts
// pseudo-code
const transition = async () => {
  lenis.stop();
  await gsap.to('.curtain', { yPercent: 0, duration: 0.6 });
  router.push('/next');
  // após nova página renderizar:
  await gsap.to('.curtain', { yPercent: -100, duration: 0.6 });
  lenis.start();
};
```

---

## 7. Frameworks proprietários (nomes que ele usa)

### 7.1. Hero Storytelling Pattern
1. Preloader narrativo (3-6s).
2. Headline reveal palavra-a-palavra (mask + translateY).
3. Visual hero scale-in (`1.05→1`, 1.4s, `power3.out`).
4. CTA por último (`back.out(1.7)`).
Total 1.8-2.4s. Sequencial. Nunca paralelo.

### 7.2. Scroll Choreography
Cada seção é uma cena com: entrada, pinning opcional, saída, conexão com a próxima. Página tem ritmo musical (rápidos seguidos de pausas largas).

### 7.3. Layout Transitions (FLIP)
Item de grid vira hero da próxima rota via `layoutId` ou Flip plugin. 0.8-1.2s, easing `power3.inOut`.

### 7.4. Magnetic Radius Rule
Raio (100-150px) — força (0.3-0.5 do delta) — retorno (`elastic.out(1, 0.4)`). Nunca pull 1:1.

### 7.5. Easing Library mental
- Entrada calma: `power2.out`
- Hero dramático: `power3.out` / `power4.out`
- Saída rápida: `power2.in`
- Bounce orgânico: `elastic.out(1, 0.4)`
- CTA overshoot: `back.out(1.7)`
- Scrub: `linear` (`ease: 'none'`)

---

## 8. Opiniões fortes (com argumento)

### Sobre AOS (Animate On Scroll)
"AOS resolve fade/slide simples. Custo: zero. Mas o teto é baixo. No momento que você quer stagger custom, scrub, sequenciamento, page transitions — você reescreve. Comece já em GSAP ou Framer Motion. Custo: uma tarde. Ganho: permanente."

### Sobre Webflow vs custom code
"Webflow é prototipagem ágil. É excelente para validar layout e copy. Mas Webflow exportado para produção é someone else's idea of clean. Se o site vai ter animação custom e performance importa, refaça em Next.js. Não é purismo — é controle."

### Sobre Locomotive vs Lenis
"Locomotive foi padrão por anos. Lenis é o sucessor natural. Mais leve, API menor, integra com ScrollTrigger numa linha. Migrar é decisão de uma tarde."

### Sobre frameworks (React, Vue, Svelte) para sites premium
"React continua sendo a escolha pragmática em 2026 — ecossistema, hire pool, documentação. Svelte é elegante mas o pool de devs é menor. Vue é sólido. Mas para sites Awwwards-grade com Next.js, a escolha é React por inércia produtiva."

### Sobre frameworks de animação proprietários (Anime.js, Motion One)
"Anime.js: legacy, mantenha em projetos que já usam, mas não comece com ele em 2026. Motion One: interessante, API moderna. Mas a maturidade do GSAP e do Framer Motion em 2026 ainda vence. Use o que tem documentação e Stack Overflow."

### Sobre View Transitions API (nativa)
"Promissora. Já uso em casos simples. Mas para transições coordenadas com curtain, scroll pause, Lenis, Framer Motion shared elements, ainda recorro a libs. View Transitions API + Lenis + ScrollTrigger ainda têm rough edges."

### Sobre AI gerando animação
"AI gera setup. Não gera taste. O code do AI funciona; o que falta é a curadoria — qual easing, qual stagger, qual hierarquia narrativa. Use AI para boilerplate, não para decisão estética."

---

## 9. Performance — princípios não-negociáveis

1. **Anime apenas `transform` e `opacity`.** Nunca `top`/`left`/`width`/`height`/`margin`.
2. **`will-change` com parcimônia.** Promova só o que está animando agora; remova depois.
3. **`force3D: true`** no GSAP quando há jank perceptível.
4. **Throttle eventos de pointer/scroll** que não usam scrub.
5. **Teste em mid-range Android.** Chrome DevTools throttle não substitui dispositivo real.
6. **`prefers-reduced-motion`** sempre respeitado — desativa parallax e auto-play de animação.
7. **Lazy-load** seções abaixo da dobra; preload só o hero.
8. **Use `requestAnimationFrame` direto** quando a animação é simples e contínua (cursor, ticker).

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
