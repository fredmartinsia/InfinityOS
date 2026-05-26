---
name: cassie-evans_06_KNOWLEDGE_COMPLETE
description: Conhecimento tecnico completo da Cassie — GSAP, ScrollTrigger, plugins, SVG fundamentals, acessibilidade
type: clone-knowledge
clone: cassie-evans
---

# Cassie Evans — Conhecimento Tecnico Completo

## Sumario
1. GSAP Core
2. ScrollTrigger
3. Plugins essenciais (MorphSVG, DrawSVG, MotionPath, Flip, ScrollSmoother, SplitText, CustomEase)
4. SVG fundamentals
5. Eases (todas as familias)
6. CSS animation comparativo
7. Acessibilidade em animacao
8. Frameworks proprios (SVG Animation Decision Tree, Storytelling com Timelines Aninhadas)

---

## 1. GSAP Core

### O que e GSAP
GSAP (GreenSock Animation Platform) e uma biblioteca de JavaScript para animacao web criada por **Jack Doyle** (a partir do legado Flash). E a ferramenta padrao da industria para animacao de UI complexa, scroll-driven animation e SVG.

**Marco historico:** em **outubro de 2024**, a **Webflow** comprou a GreenSock e tornou **TODO o GSAP gratuito**, incluindo plugins antes pagos do Club GreenSock e uso comercial. A licenca padrao agora cobre qualquer aplicacao.

### Instalacao
```bash
npm install gsap
```

```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin";
import { DrawSVGPlugin } from "gsap/DrawSVGPlugin";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(ScrollTrigger, MorphSVGPlugin, DrawSVGPlugin, MotionPathPlugin, Flip);
```

### Os quatro metodos centrais

#### `gsap.to(target, vars)`
Anima do estado ATUAL ate os valores em `vars`.
```js
gsap.to(".box", { x: 200, opacity: 1, duration: 0.6, ease: "power2.out" });
```

#### `gsap.from(target, vars)`
Anima a partir dos valores em `vars` ATE o estado atual. Util para "reveal".
```js
gsap.from(".hero", { y: 60, opacity: 0, duration: 0.8 });
// O elemento comeca y=60, opacity=0 e termina onde estava no DOM.
```

#### `gsap.fromTo(target, fromVars, toVars)`
Controle total dos dois extremos.
```js
gsap.fromTo(".item",
  { y: 40, opacity: 0 },
  { y: 0, opacity: 1, duration: 0.5, stagger: 0.08 }
);
```

#### `gsap.set(target, vars)`
Define valor instantaneo, sem animar. Util para preparar estado inicial.
```js
gsap.set(".panel", { autoAlpha: 0, y: 20 });
```

### Timeline (`gsap.timeline()`)
Sequencia coreografada. O coracao de qualquer animacao seria.

```js
const tl = gsap.timeline({
  defaults: { duration: 0.6, ease: "power2.out" },
  paused: true,
  onComplete: () => console.log("done")
});

tl.from(".title", { y: 40, opacity: 0 })
  .from(".subtitle", { y: 20, opacity: 0 }, "-=0.3") // overlap 300ms com a anterior
  .from(".cta", { scale: 0.8, opacity: 0 }, "<")     // comeca junto com a anterior
  .from(".image", { x: 100, opacity: 0 }, ">")       // comeca quando a anterior acabar (default)
  .add(otherTimeline)                                  // aninha outra timeline
  .addLabel("midpoint")                                // marca posicao
  .from(".final", { y: 30 }, "midpoint+=0.5");        // posiciona em label

tl.play();   // .pause(), .reverse(), .restart(), .seek("midpoint"), .timeScale(2)
```

#### Sintaxe de posicao na timeline
- `"+=0.5"` — 0.5s depois do final da timeline
- `"-=0.3"` — 0.3s antes do final (overlap)
- `"<"` — comeca junto com a tween anterior
- `">"` — comeca quando a anterior acabar (default)
- `"<+=0.2"` — 0.2s depois do inicio da anterior
- `"label"` — em uma label
- `"label+=0.5"` — 0.5s depois da label
- `2` — em segundos absolutos a partir do inicio

### `gsap.context()`
Em frameworks (React, Vue, Svelte), use `gsap.context()` para limpar animacoes ao desmontar.

```js
useEffect(() => {
  const ctx = gsap.context(() => {
    gsap.from(".item", { y: 40, opacity: 0, stagger: 0.1 });
  }, scopeRef);
  return () => ctx.revert();
}, []);
```

### `gsap.matchMedia()`
Branch por media query. Substituiu o antigo `gsap.matchMedia` deprecated.

```js
const mm = gsap.matchMedia();

mm.add("(min-width: 800px)", () => {
  // animacoes desktop
});

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // animacoes completas
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // versao reduzida ou estatica
});
```

---

## 2. ScrollTrigger

Plugin oficial para animacao atrelada a scroll. Substitui IntersectionObserver na maioria dos casos, com infinitamente mais controle.

### Estrutura basica
```js
gsap.to(".box", {
  x: 400,
  scrollTrigger: {
    trigger: ".box",
    start: "top center",
    end: "bottom top",
    scrub: 1,
    markers: true, // remova em producao
  }
});
```

### `start` e `end`
String com duas partes: `"posicao_no_trigger posicao_na_viewport"`.
- `"top center"` — quando o topo do trigger encontrar o centro da viewport, comeca.
- `"bottom 80%"` — quando o fundo do trigger atingir 80% da viewport.
- `"top top"` — topo do trigger no topo da viewport.

Tambem aceita pixels relativos: `"+=500"` (500px depois do start).

### `scrub` — atrelar ao scroll
- `scrub: true` — animacao trava 1:1 ao scroll.
- `scrub: 1` — segue scroll com 1s de "preguica" (lerp). RECOMENDADO. Suaviza scrolls bruscos.
- `scrub: 0.5` — mais responsivo.
- Sem scrub: animacao toca uma vez no trigger.

### `toggleActions` (sem scrub)
String com 4 estados: `"onEnter onLeave onEnterBack onLeaveBack"`.
- `"play none none reverse"` — toca ao entrar, reverte ao sair de volta.
- `"play pause resume reset"` — controle completo.
- `"restart pause resume reset"` — sempre reinicia.

### `pin`
Trava o trigger na tela enquanto a animacao ocorre.
```js
ScrollTrigger.create({
  trigger: ".panel",
  start: "top top",
  end: "+=1000",
  pin: true,
  pinSpacing: true, // (default true) reserva espaco apos o pin
});
```

### `snap`
Prende o scroll em pontos.
```js
scrollTrigger: {
  snap: {
    snapTo: "labels",       // snap pra labels da timeline
    duration: 0.5,
    ease: "power2.inOut"
  }
}
```

### Callbacks
`onEnter`, `onLeave`, `onEnterBack`, `onLeaveBack`, `onUpdate(self)` (recebe o ScrollTrigger com `self.progress`).

### Refresh
`ScrollTrigger.refresh()` recalcula os triggers (apos mudanca de layout, fonte carregada, etc).

```js
window.addEventListener("load", () => ScrollTrigger.refresh());
```

---

## 3. Plugins Essenciais (todos gratuitos desde out/2024)

### MorphSVG
Morpha qualquer path para qualquer path. **Atencao: numero de pontos importa**. Paths muito diferentes podem morphar feio — use `MorphSVGPlugin.convertToPath()` para converter shapes (rect, circle, ellipse) em path.

```js
gsap.to("#shape", {
  duration: 1,
  morphSVG: { shape: "#target", shapeIndex: 0 },
  ease: "power2.inOut"
});
```

`shapeIndex` ajusta o ponto de partida (gira o path) — util quando o morph "vira do avesso".

### DrawSVG
Anima o stroke de um path como se uma caneta estivesse desenhando.

```js
gsap.from("#path", {
  drawSVG: "0% 0%",  // comeca invisivel
  duration: 1.5,
  ease: "power2.inOut"
});

// Aceita strings ricas:
// "0%" -> "0% 0%" (ponto inicial)
// "100%" -> "0% 100%" (desenho completo)
// "50% 100%" (meta a final)
// "0% 50%" (inicio a metade)
```

### MotionPath
Anima qualquer elemento ao longo de um path SVG.

```js
gsap.to("#fish", {
  duration: 4,
  ease: "power1.inOut",
  motionPath: {
    path: "#wavyPath",
    align: "#wavyPath",
    autoRotate: true,    // o elemento gira com a curva
    alignOrigin: [0.5, 0.5]
  }
});
```

### Flip (FLIP technique)
Anima mudancas de layout sem layout shift. FLIP = First, Last, Invert, Play.

```js
const state = Flip.getState(".items");
// muda DOM (reordena, troca classes, etc)
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  stagger: 0.05,
});
```

Casos: card que abre virando modal, item de grid que muda de posicao, layout responsivo animado.

### ScrollSmoother
Inercia no scroll, similar ao Lenis mas integrada com ScrollTrigger.

```js
ScrollSmoother.create({
  smooth: 1.5,
  effects: true,
});
```

### SplitText (reescrito 2024, 50% menor)
Quebra texto em linhas, palavras, caracteres animaveis.

```js
const split = new SplitText(".title", { type: "chars,words" });
gsap.from(split.chars, {
  y: 40,
  opacity: 0,
  stagger: 0.02,
  duration: 0.6,
  ease: "back.out(1.7)"
});
```

### CustomEase
Desenhe sua propria curva.

```js
import { CustomEase } from "gsap/CustomEase";
gsap.registerPlugin(CustomEase);

CustomEase.create("myEase", "M0,0 C0.25,0.46 0.45,0.94 1,1");
gsap.to(".x", { x: 100, ease: "myEase", duration: 1 });
```

### Physics2D / PhysicsProps
Fisica simples (gravidade, friccao, velocidade).

### Observer / Draggable
- `Observer` — captura gesto generico (touch, scroll, wheel) sem ficar dependente de um.
- `Draggable` — faz qualquer elemento arrastavel.

---

## 4. SVG Fundamentals

### viewBox
O sistema de coordenadas interno do SVG. *"E como uma janela: nao importa o tamanho real do SVG na tela, o codigo trabalha nas coordenadas do viewBox."*

```html
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- coordenadas vao de 0,0 a 800,600 -->
</svg>
```

### Paths e atributo `d`
- `M x y` — move (sem desenhar)
- `L x y` — line to
- `C x1 y1 x2 y2 x y` — bezier cubica
- `Q x1 y1 x y` — bezier quadratica
- `Z` — fecha o path

```html
<path d="M 10 80 C 40 10, 65 10, 95 80 S 150 150, 180 80" stroke="black" fill="transparent"/>
```

### Symbol + Use (reuso)
```html
<svg>
  <symbol id="icon-heart" viewBox="0 0 24 24">
    <path d="M..."/>
  </symbol>
</svg>
<svg><use href="#icon-heart" /></svg>
```

### Mask vs ClipPath
- **clipPath**: corta de forma binaria (dentro ou fora). Nao tem alpha.
- **mask**: usa luminancia/alfa. Pode ter degradacoes.

```html
<defs>
  <clipPath id="clip">
    <circle cx="50" cy="50" r="40" />
  </clipPath>
</defs>
<image clip-path="url(#clip)" .../>
```

### Filters (especialmente para criativo)
- `feGaussianBlur` — blur
- `feTurbulence` + `feDisplacementMap` — distorcao organica (efeito agua, fogo)
- `feColorMatrix` — manipulacao de cor

```html
<filter id="goo">
  <feGaussianBlur stdDeviation="10"/>
  <feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" />
</filter>
```

### transform-origin em SVG
Pegadinha classica. Em SVG, `transform-origin` por padrao e baseado no canto da tela, nao do elemento.

**Solucao 1 (CSS):**
```css
.shape { transform-box: fill-box; transform-origin: center; }
```

**Solucao 2 (GSAP):** ja resolve magicamente.
```js
gsap.to(".shape", { rotation: 360, transformOrigin: "50% 50%" });
```

---

## 5. Eases — Familias e Personalidade

| Ease | Personalidade | Quando usar |
|---|---|---|
| `none` (linear) | Mecanico, sem alma | Animacao constante (rotacao infinita, scroll-bound em casos raros) |
| `power1.out` | Sutil | Fades simples |
| `power2.out` | Default seguro, **favorita da Cassie** | UI geral |
| `power3.out` | Mais snappy | CTA, reveals dinamicos |
| `power4.out` | Muito snappy | Hover rapido |
| `back.out(1.7)` | Brincalhao, "passou e voltou" | Botoes, cards, microinteracoes |
| `back.in(1.7)` | Antecipacao | Saidas com personalidade |
| `elastic.out(1, 0.3)` | Cartoon, balanca | Squash and stretch |
| `bounce.out` | Pula | Personagens, brinquedos |
| `expo.out` | Explosivo no comeco, freia | Reveals dramaticos |
| `sine.inOut` | Suave, organico | Loop infinito, respiracao |
| `circ.out` | Curva pesada | Acelera de 0 com peso |
| `steps(n)` | Pixelado | Animacao frame-by-frame |

`back.out(1.7)` e a "Cassie ease": ela usa muito.

---

## 6. CSS Animation vs GSAP — Quando Usar Cada

| Cenario | Ferramenta |
|---|---|
| Hover simples (cor, escala) | `transition` CSS |
| Animacao de loading (spinner) | `@keyframes` CSS |
| Sequencia de 3+ etapas | GSAP `timeline` |
| Atrelado a scroll | GSAP `ScrollTrigger` |
| Interrompivel suavemente (ex: drag) | GSAP (CSS reinicia, GSAP retargeta) |
| Morph de SVG | `MorphSVG` |
| Path drawing | `DrawSVG` |
| Layout shift | `Flip` |
| Texto granular | `SplitText` |
| Animacao com fisica | `Physics2D` ou Spring (Framer Motion) |

Cassie respeita CSS. Para microinteracoes simples (hover de botao), CSS e perfeito. Para qualquer coisa com sequencia, scroll, ou interrupcao, GSAP vence.

---

## 7. Acessibilidade em Animacao

### `prefers-reduced-motion`
Media query do sistema operacional. Usuario com vestibular issues, enxaqueca, ou sensibilidade marca isso nas preferencias do OS.

```js
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // timeline rica
  gsap.from(".cards", { y: 60, stagger: 0.1, opacity: 0 });
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // versao calma: sem movimento, so opacidade
  gsap.from(".cards", { opacity: 0, duration: 0.3 });
});
```

### Outras boas praticas
- **`<title>` em SVG** — descricao acessivel.
- **`role="img"`** + **`aria-label`** em SVG decorativo.
- **`aria-hidden="true"`** em SVG puramente decorativo (nao adiciona ruido a screen reader).
- **Foco visivel** preservado durante animacao.
- **Sem flashes rapidos** (epilepsia: < 3 flashes/segundo).
- **Velocidade humana**: animacoes UI < 400ms quase sempre.

---

## 8. Frameworks Proprios

### SVG Animation Decision Tree (Cassie's tree)
Pergunte na ordem:
1. **Forma estatica que muda cor/posicao/escala?** -> CSS transition.
2. **Sequencia de eventos?** -> `gsap.timeline()`.
3. **Atrelado a scroll?** -> `ScrollTrigger` (com `scrub` para 1:1).
4. **Forma muda de geometria?** -> `MorphSVG`.
5. **Stroke "desenha"?** -> `DrawSVG`.
6. **Elemento segue caminho curvo?** -> `MotionPath`.
7. **Layout muda (item troca de container/grid)?** -> `Flip`.
8. **Texto granular (caractere por caractere)?** -> `SplitText`.
9. **Inercia no scroll?** -> `ScrollSmoother`.

### Storytelling com Timelines Aninhadas
*"Cenas dentro de cenas. Caixas dentro de caixas."*

```js
// Cada cena testavel isolada
const sceneOne = () => {
  const tl = gsap.timeline();
  tl.from(".s1-title", { y: 30, opacity: 0 })
    .from(".s1-image", { scale: 0.9, opacity: 0 }, "-=0.3");
  return tl;
};

const sceneTwo = () => {
  const tl = gsap.timeline();
  tl.from(".s2-card", { y: 40, opacity: 0, stagger: 0.1 });
  return tl;
};

// Master orquestra
const master = gsap.timeline();
master
  .add(sceneOne())
  .add(sceneTwo(), "-=0.4")  // cenas se sobrepoe
  .add(() => console.log("storyline complete"));
```

Beneficio: cada cena vira funcao testavel, reutilizavel, e o sequenciamento fica explicito no master.

### Estrutura primeiro, animacao depois
Antes de qualquer GSAP, a Cassie sempre passa pelo SVG:
1. **viewBox correto?**
2. **Grupos `<g>` nomeados via `id` ou class?**
3. **Cada elemento que vai ser animado tem identificador unico?**
4. **`<use>` reusado quando faz sentido?**
5. **Lixo limpo (atributos vazios, transforms inline desnecessarios)?**

*"Se voce tenta animar um SVG bagunçado, voce vai sofrer. Limpa primeiro."*

---

## Recursos canonicos

- **gsap.com/docs** — documentacao oficial.
- **gsap.com/community/forums** — forum (Carl Schooff e a alma).
- **codepen.io/GreenSock** — colecao oficial de demos.
- **codepen.io/cassie-codes** — demos da Cassie.
- **cassie.codes** — blog pessoal dela.
- **gsap.com/blog** — artigos tecnicos (varios da Cassie).
