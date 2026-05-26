---
name: emil-kowalski_06_KNOWLEDGE_COMPLETE
description: Base de conhecimento tecnico completa de Emil Kowalski — Sonner, Vaul, Framer Motion, springs, FLIP, performance
type: clone-knowledge
clone: emil-kowalski
---

# Knowledge Completo — Emil Kowalski

## Indice

1. [Sonner — Toast Component](#sonner)
2. [Vaul — Drawer Component](#vaul)
3. [Framer Motion / Motion](#framer-motion)
4. [CSS Animations Modernas](#css-modern)
5. [Spring Physics](#springs)
6. [FLIP Technique](#flip)
7. [View Transitions API](#view-transitions)
8. [Acessibilidade em Animacao](#a11y)
9. [Performance](#performance)
10. [Frameworks Mentais](#frameworks)
11. [Opinioes Fortes](#opinioes)

---

<a name="sonner"></a>
## 1. Sonner — Toast Component

### Por que existe
Toast components do React em geral eram quebrados: empilhamento sem hierarquia visual, swipe to dismiss inexistente ou ruim, animacoes com keyframes nao interrompiveis, API verbosa.

### Arquitetura

**Stack visual:**
- Toast mais novo no topo (ou bottom, dependendo da posicao)
- Toasts atras ficam menores (`scale: 0.95`, depois `0.9`) e empurrados para tras (`translateY`)
- Opacidade decai (`1 → 0.7 → 0.4`)
- Limite de toasts visiveis (geralmente 3)

**API minima:**

```tsx
import { Toaster, toast } from 'sonner'

function App() {
  return (
    <>
      <Toaster richColors position="top-right" />
      <button onClick={() => toast.success('Saved!')}>Save</button>
    </>
  )
}

// Tipos:
toast('Mensagem')
toast.success('Sucesso')
toast.error('Erro')
toast.loading('Carregando')
toast.promise(fetchData(), {
  loading: 'Salvando...',
  success: 'Salvo',
  error: 'Erro ao salvar',
})
```

### Decisao tecnica chave: empilhamento

```tsx
// Pseudo-implementacao do empilhamento
toasts.map((toast, index) => {
  const offset = index * GAP // ex: 14px
  const scale = 1 - index * 0.05 // 1, 0.95, 0.9
  const opacity = 1 - index * 0.3 // 1, 0.7, 0.4

  return (
    <motion.li
      style={{
        transform: `translateY(${offset}px) scale(${scale})`,
        opacity,
      }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    />
  )
})
```

### Swipe to dismiss

```tsx
const x = useMotionValue(0)
const opacity = useTransform(x, [-150, 0, 150], [0, 1, 0])

<motion.li
  drag="x"
  style={{ x, opacity }}
  onDragEnd={(_, info) => {
    if (Math.abs(info.offset.x) > 100) {
      dismissToast()
    }
  }}
/>
```

### Acessibilidade
- `role="status"` para info/success
- `role="alert"` para erro
- `aria-live="polite"` ou `assertive` conforme severidade
- Foco nao pula automaticamente (toast e nao bloqueante)
- Keyboard: foco no toast pausa auto-dismiss

---

<a name="vaul"></a>
## 2. Vaul — Drawer Component

### Por que existe
Drawers/sheets em React eram tipicamente position fixed + transform translateY com keyframe. Quebrava em interrupcao. Sem snap point. Sem scroll lock condicional. Sem nested drawers. Sem easing iOS.

### Arquitetura

**Estados:**
- `closed` (translateY: 100%)
- `open` (translateY: 0)
- `dragging` (translateY segue gesto)
- `snapping` (animando para snap point mais proximo)

**Snap points:**
```tsx
<Drawer.Root snapPoints={[0.4, 0.75, 1]}>
  <Drawer.Trigger>Open</Drawer.Trigger>
  <Drawer.Portal>
    <Drawer.Overlay />
    <Drawer.Content>
      <div className="drag-handle" />
      {/* content */}
    </Drawer.Content>
  </Drawer.Portal>
</Drawer.Root>
```

### Easing iOS customizado

```tsx
const IOS_EASING = 'cubic-bezier(0.32, 0.72, 0, 1)'

// Para entrada/saida controlada
.drawer {
  transition: transform 500ms cubic-bezier(0.32, 0.72, 0, 1);
}

// Para gesto
const y = useMotionValue(0)
const springY = useSpring(y, { damping: 30, stiffness: 300 })
```

### Scroll lock condicional

```tsx
// So bloqueia scroll do body se drawer NAO esta no topo (snap mais alto)
useEffect(() => {
  if (isFullyOpen) {
    document.body.style.overflow = ''
  } else {
    document.body.style.overflow = 'hidden'
  }
}, [isFullyOpen])
```

### shouldScaleBackground
```tsx
<Drawer.Root shouldScaleBackground>
```

Quando ativo, o body por tras escala para `0.95` e arredonda cantos — efeito iOS classico de "drawer empurrando o conteudo de tras".

### Decisao critica: position-based vs translate-based

Vaul usa **transform: translateY** apenas. Nao mexe em `top` ou `bottom`. Razao:
- transform compositor-only → 60fps
- `top` dispara layout → caro
- transform e interrompivel cleanly via spring

---

<a name="framer-motion"></a>
## 3. Framer Motion / Motion

### Quando usar Framer Motion vs CSS

| Caso | Tool |
|------|------|
| Hover, focus, color transition | CSS `transition` |
| Mount/unmount com exit animation | Framer Motion `AnimatePresence` |
| Layout animation (mudanca de posicao/tamanho) | Framer Motion `layout` prop |
| Shared layout entre elementos | Framer Motion `layoutId` |
| Gesto (drag, swipe) | Framer Motion `useMotionValue` + `useTransform` |
| Scroll-driven animation | Framer Motion `useScroll` + `useTransform` (ou CSS Scroll Timeline) |
| Spring nativo | Framer Motion `useSpring` |
| Animacao simples sem JS | CSS keyframes |
| Bundle critico (<10kb) | CSS, ou Motion One |

### Padroes Essenciais

**Mount/Unmount com exit:**
```tsx
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.2, ease: [0.32, 0.72, 0, 1] }}
    />
  )}
</AnimatePresence>
```

**Layout animation:**
```tsx
<motion.div layout>
  {/* este div anima automaticamente quando suas dimensoes mudam */}
</motion.div>
```

**Shared layout:**
```tsx
{items.map(item => (
  <motion.div key={item.id} layoutId={item.id} />
))}
// Quando um elemento com mesmo layoutId aparece em outro lugar,
// Framer Motion anima a transicao entre eles
```

**Gesto:**
```tsx
const x = useMotionValue(0)
const rotate = useTransform(x, [-200, 200], [-30, 30])
const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])

<motion.div
  drag="x"
  style={{ x, rotate, opacity }}
  dragConstraints={{ left: -200, right: 200 }}
/>
```

**Spring amortecido:**
```tsx
const y = useMotionValue(0)
const smoothY = useSpring(y, { damping: 30, stiffness: 300 })
```

**Variants (coreografia):**
```tsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
    },
  },
}

const item = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
}

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map(i => <motion.li key={i} variants={item} />)}
</motion.ul>
```

**Imperative API (quando declarativo nao basta):**
```tsx
const [scope, animate] = useAnimate()

const handleClick = async () => {
  await animate(scope.current, { scale: 1.2 }, { duration: 0.1 })
  await animate(scope.current, { scale: 1 }, { duration: 0.2 })
}
```

**Reduced motion:**
```tsx
const reduce = useReducedMotion()
const transition = reduce ? { duration: 0 } : { type: 'spring' }
```

---

<a name="css-modern"></a>
## 4. CSS Animations Modernas

### @starting-style (entry animation declarativa)

```css
.dialog {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.2s, transform 0.2s;

  @starting-style {
    opacity: 0;
    transform: translateY(20px);
  }
}
```

Quando o elemento e adicionado ao DOM, ele inicia com os valores em `@starting-style` e transita para os valores normais.

### transition-behavior: allow-discrete

Permite animar propriedades discretas (como `display`):

```css
.popover {
  display: none;
  opacity: 0;
  transition: opacity 0.2s, display 0.2s allow-discrete;
}

.popover[open] {
  display: block;
  opacity: 1;
}
```

### linear() easing function

CSS agora suporta easing complexo via `linear()`:

```css
.element {
  transition: transform 0.4s linear(0, 0.5, 0.8, 1);
}
```

Permite simular spring em CSS sem JS. Voce pode gerar com tools como `linear-easing-generator`.

### View Transitions API

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

.thumbnail {
  view-transition-name: hero;
}
```

```js
document.startViewTransition(() => {
  // mudanca de DOM
})
```

### prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

Ou granular:

```css
.fancy {
  transition: transform 0.5s;
}

@media (prefers-reduced-motion: reduce) {
  .fancy {
    transition: opacity 0.2s;
    transform: none;
  }
}
```

---

<a name="springs"></a>
## 5. Spring Physics

### Por que springs?
- **Velocidade preservada na interrupcao.** Tween reseta. Spring continua.
- **Sensacao natural.** Objetos no mundo real desaceleram com massa, atrito, amortecimento.
- **Sem duracao fixa.** A duracao emerge do sistema (stiffness + damping + mass + initial velocity).

### Parametros

- **stiffness:** rigidez da mola. Maior = mais rapido, mais "puxao".
- **damping:** amortecimento. Maior = menos overshoot.
- **mass:** massa do objeto. Maior = inercia maior.
- **velocity:** velocidade inicial (importante em interrupcao).

### Spring configs favoritas (Emil)

```tsx
const SNAPPY = { type: 'spring', stiffness: 400, damping: 30 }
const SMOOTH = { type: 'spring', stiffness: 200, damping: 25 }
const IOS_FEEL = { type: 'spring', stiffness: 200, damping: 30, mass: 1.2 }
const DRAWER = { type: 'spring', stiffness: 300, damping: 30 }
const GENTLE = { type: 'spring', stiffness: 100, damping: 20 }
const BOUNCY = { type: 'spring', stiffness: 300, damping: 15 } // overshoot
```

### Quando NAO usar spring

- Animacao de mount/unmount sem gesto: tween com easing pode ser mais previsivel
- Animacao com duracao especifica desejada (ex: bater com som a 200ms): use tween
- Animacoes de loading sequencial: keyframes ou tween

---

<a name="flip"></a>
## 6. FLIP Technique

**F**irst — meca posicao inicial
**L**ast — meca posicao final
**I**nvert — aplique transform inverso (parece estar no inicio)
**P**lay — anime transform para 0 (parece "fluido")

### Implementacao manual

```tsx
function flipAnimate(element: HTMLElement, change: () => void) {
  const first = element.getBoundingClientRect()
  change() // muda DOM/style
  const last = element.getBoundingClientRect()

  const dx = first.left - last.left
  const dy = first.top - last.top
  const sx = first.width / last.width
  const sy = first.height / last.height

  element.animate([
    { transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy})` },
    { transform: 'translate(0, 0) scale(1, 1)' },
  ], {
    duration: 300,
    easing: 'cubic-bezier(0.32, 0.72, 0, 1)',
  })
}
```

### Em Framer Motion

```tsx
// Framer Motion faz FLIP automaticamente com layout prop
<motion.div layout>{children}</motion.div>
```

Quando algo muda o layout deste div (largura, posicao no flex/grid, etc.), Framer Motion calcula FLIP e anima.

### Quando usar FLIP

- Reordenacao de listas
- Mudanca de tamanho responsiva animada
- Elemento mudando entre containers diferentes
- Qualquer animacao que envolveria animar `width`, `height`, `top`, `left`

---

<a name="view-transitions"></a>
## 7. View Transitions API

### Por que importa
Antes da View Transitions API, fazer transicao entre paginas/estados envolvia FLIP manual ou shared layout do Framer Motion. Agora o navegador faz nativamente.

### Same-page transitions

```js
// Quando algo muda no DOM
document.startViewTransition(() => {
  // mudanca aqui
  setState(newState)
})
```

### Cross-document (Chrome 126+)

```html
<meta name="view-transition" content="same-origin">
```

Ou via CSS:

```css
@view-transition {
  navigation: auto;
}
```

### Customizando

```css
::view-transition-old(root) {
  animation: 0.3s ease-out fade-out;
}

::view-transition-new(root) {
  animation: 0.3s ease-out fade-in;
}

/* Elemento especifico */
.hero {
  view-transition-name: hero-image;
}
```

### Quando usar
- Route transitions
- Tab transitions
- Modal opening de elemento clicado (image transitions)

### Quando NAO usar
- Componente isolado interno (use Framer Motion `layoutId`)
- Suporte universal critico (View Transitions API ainda nao e universal)

---

<a name="a11y"></a>
## 8. Acessibilidade em Animacao

### prefers-reduced-motion

**Sempre respeitar.** Sem desculpa.

```tsx
const reduce = useReducedMotion()

<motion.div
  animate={reduce ? {} : { y: 0, opacity: 1 }}
  initial={reduce ? false : { y: 20, opacity: 0 }}
/>
```

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Foco e animacao

- Animacao nao deve atrasar foco. Se um modal abre, foco deve ir para ele imediatamente, mesmo durante a animacao.
- `inert` em conteudo de fundo durante modal aberto.
- Focus trap em drawer/dialog.

### Roles e aria-live

- Toast info: `role="status"` + `aria-live="polite"`
- Toast erro: `role="alert"` + `aria-live="assertive"`
- Loading: `aria-busy="true"`
- Animacao de progresso: `role="progressbar"` + `aria-valuenow`

### Vestibular issues

Animacoes que zoom, rotacao 3D, ou parallax intenso podem causar nausea/desorientacao. **Sempre** desabilitar com `prefers-reduced-motion`.

---

<a name="performance"></a>
## 9. Performance

### Composite-only animation

So animar:
- `transform` (translate, scale, rotate, skew)
- `opacity`
- `filter` (com cuidado, mais caro)

Estas propriedades vivem na **camada de composicao**. Nao disparam layout nem paint. GPU faz.

### Anti-padroes

- Animar `width` / `height` → layout
- Animar `top` / `left` / `right` / `bottom` → layout
- Animar `margin` / `padding` → layout
- Animar `box-shadow` muito grande → paint caro
- `transition: all` → anima tudo, inclusive coisas que disparam layout

### will-change

```css
.drawer {
  will-change: transform;
}
```

**Cuidado:** `will-change` cria layer de composicao permanente. Use **so durante** a animacao (toggle via JS) ou em elementos que sempre animam. Layer demais = memoria GPU exausta.

### Frame budget

60fps = 16.67ms por frame. 120fps (ProMotion) = 8.33ms.
Se sua animacao causa frame drop, voce esta gastando demais.

### Como medir

```
Chrome DevTools → Performance tab
Record → faca a animacao → stop
Procure: yellow bars (scripting), purple (layout), green (paint)
Frame rate na linha "Frames"
```

### Mobile lento

- Throttling 4x slowdown no DevTools
- Teste em hardware real (Moto G low-end)
- Animacao que voa em MacBook M3 pode quebrar em Android low-end

### Bundle size

- Framer Motion: ~50kb gzip (ele tem motion mini agora)
- Motion One: ~3kb gzip
- CSS pure: 0kb JS

Para pagina critica de performance, considere CSS ou Motion One.

---

<a name="frameworks"></a>
## 10. Frameworks Mentais

### Layered Animation
Toda animacao complexa tem 3 camadas:
1. **Entrada** (mount transition)
2. **Layout** (mudanca de tamanho/posicao durante uso)
3. **Saida** (exit transition)

Cada camada pode usar tecnologia diferente:
- Entrada: AnimatePresence + spring
- Layout: layout prop (FLIP automatico)
- Saida: AnimatePresence exit

### Component Animation Lifecycle
1. **Mount** — animacao de entrada
2. **Idle** — sem animacao, ou loop sutil
3. **Interaction** — hover, focus, click, drag
4. **Layout change** — mudou tamanho/posicao
5. **Exit** — animacao de saida

### Spring vs Tween Decision Tree

```
A animacao envolve gesto?
├── SIM → spring
└── NAO → e mount/unmount?
        ├── SIM → tween com easing custom (ou spring)
        └── NAO → e propriedade simples (color, opacity)?
                ├── SIM → CSS transition
                └── NAO → tween com easing
```

### Easing Hierarchy

```
linear         ← PROIBIDO em UI (so spinner, progress)
ease-in        ← raramente (saida acelerada)
ease           ← default ruim, evitar
ease-out       ← BOM default para entradas
ease-in-out    ← bom para back-and-forth
cubic-bezier   ← BOM para identidade
spring         ← MELHOR para gesto/interrupcao
```

---

<a name="opinioes"></a>
## 11. Opinioes Fortes

### Linear easing
**Proibido em UI.** Excecoes: spinner (loop infinito de rotacao), progress bar (linear faz sentido aqui).

### Ease-in para entradas
**Errado.** Ease-in acelera. Para entrada voce quer desaceleracao no fim — ease-out.

### `transition: all`
**Anti-pattern.** Especifique propriedades:
```css
/* ruim */
.btn { transition: all 0.2s; }

/* bom */
.btn { transition: background-color 0.2s, transform 0.15s; }
```

### Animacoes 400ms+
**Quase sempre lento.** Reduza. Excecao: animacao com travel grande (drawer subindo de baixo da tela), 400-500ms ok.

### CSS keyframes em UI dinamica
**Quebrado para interrupcao.** `@keyframes` reinicia do 0% quando interrompido. Use `transition` (interrompivel) ou Framer Motion.

### Animar width/height
**Anti-pattern.** Use FLIP technique ou `layout` prop do Framer Motion.

### Page transitions com fade
**Preguicoso.** Use shared layout (Framer Motion `layoutId`) ou View Transitions API.

### Hover sem easing
**Quebrado.** Toda transicao deve ter easing definido, nem que seja `ease-out 150ms`.

### prefers-reduced-motion ignorado
**Bug de acessibilidade.** Sem desculpa.

### Framer Motion vs Motion One
- Framer Motion: dominante em React, recursos avancados (layout, layoutId, AnimatePresence). Use para componentes complexos.
- Motion One: leve, performant, bom para casos onde bundle importa. Use em landing pages.
- Para 95% dos casos em React, Framer Motion vence pela DX.

### CSS vs JS animation
- CSS: hover/focus/transition simples. Bundle 0.
- JS (Framer/Motion): qualquer coisa que envolva estado React, gesto, interrupcao, layout animation, exit animation.

### useSpring vs animate transition spring
- `useSpring`: amortece um motion value continuo (gesto).
- `animate={{ x: 100 }} transition={{ type: 'spring' }}`: anima um valor target.

Use `useSpring` quando o input e continuo (gesto, scroll). Use spring transition quando o input e discreto (estado).
