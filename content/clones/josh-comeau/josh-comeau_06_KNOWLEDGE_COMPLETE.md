---
name: josh-comeau_06_KNOWLEDGE_COMPLETE
description: Corpo de conhecimento de Josh Comeau — CSS profundo, layout, animação, dark mode, acessibilidade, React
type: clone-knowledge
clone: josh-comeau
---

# Josh Comeau — Corpo de Conhecimento Completo

> "Mental model first, syntax second. Once you see the model, the rules click."

Este é o conhecimento operacional de Josh Comeau. Cada seção segue a estrutura **mental model → why → how → polish/a11y**.

---

## 1. CSS — A Cascata Real

### Mental model
A cascata CSS é um algoritmo que, para cada propriedade de cada elemento, decide qual valor declarado vence. Não é por "ordem que aparece" sozinha — é por uma sequência de critérios:

1. **Origin & importance** — user agent < user < author < user `!important` < author `!important`
2. **Cascade layers** (`@layer`) — camadas declaradas vencem por ordem
3. **Specificity** — selector mais específico vence (a, b, c)
4. **Order of appearance** — se tudo empata, o último declarado vence

### Why
Existe pra resolver conflitos quando múltiplas regras se aplicam ao mesmo elemento. Sem isso, o navegador não saberia qual `color` usar.

### Cascade Layers — o jeito moderno

```css
/* Declaramos a ordem das camadas primeiro */
@layer reset, base, components, utilities;

@layer reset {
  /* CSS reset entra aqui */
  *, *::before, *::after { box-sizing: border-box; }
}

@layer base {
  body { font-family: system-ui; }
}

@layer components {
  .button { padding: 12px 16px; }
}

@layer utilities {
  /* Vence components mesmo com specificity menor — porque a camada vem depois */
  .text-center { text-align: center; }
}
```

**Linha a linha:**
- `@layer reset, base, components, utilities;` — declara a ordem. Camadas posteriores vencem.
- Dentro de cada `@layer`, specificity ainda funciona normal — mas só **dentro daquela camada**.
- A camada como um todo vence a anterior, não importa specificity.

### Polish/a11y
Não impacta a11y diretamente, mas ajuda muito a manter um reset/base previsível, o que reduz bugs visuais que afetam usabilidade.

---

## 2. Layout — Os 5 Layout Modes

### Mental model
Todo elemento na página está usando **um** dos 5 layout modes:

1. **Flow** (default) — block + inline
2. **Flexbox** — `display: flex`
3. **Grid** — `display: grid`
4. **Positioned** — `position: absolute/fixed/sticky`
5. **Table** — `display: table`

A propriedade que você está tentando usar **só faz sentido dentro do layout mode certo**. `align-items` não faz nada em flow. `vertical-align` não faz nada em flex.

### Flexbox — mental model

> "Flexbox distribui espaço ao longo de **um eixo**. Tudo gira em torno disso."

- `flex-direction` define o **eixo principal**
- `justify-content` alinha **ao longo do eixo principal**
- `align-items` alinha **no eixo cruzado**
- `flex-grow` / `flex-shrink` / `flex-basis` controlam como o item ocupa espaço **no eixo principal**

```css
.parent {
  display: flex;
  flex-direction: row;       /* main axis = horizontal */
  justify-content: center;   /* ao longo do main axis */
  align-items: center;       /* no cross axis (vertical) */
  gap: 16px;                 /* substitui margin entre items */
}
```

### Grid — mental model

> "Grid trabalha em duas dimensões. Você define **trilhas**, e itens vão pra **células**."

```css
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;  /* sidebar fixa, conteúdo flex */
  grid-template-rows: auto 1fr auto; /* header, main, footer */
  grid-template-areas:
    "sidebar header"
    "sidebar main"
    "sidebar footer";
  min-height: 100vh;
}

.sidebar { grid-area: sidebar; }
.header  { grid-area: header; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

### Containing block — conceito subestimado

Cada elemento absoluto se posiciona em relação ao seu **containing block**. Para `position: absolute`, o containing block é o ancestral mais próximo com `position` diferente de `static`. Se você esquecer disso, seu absolute vai parar no `<html>`.

**Regra de bolso:** sempre que usar `position: absolute`, dá `position: relative` no pai imediato pra "ancorar" o filho.

### Intrinsic sizing

```css
.card {
  width: min-content;   /* o mínimo que o conteúdo permite (palavra mais longa) */
  width: max-content;   /* o tamanho natural sem quebrar */
  width: fit-content;   /* min(max-content, available-space) */
}
```

---

## 3. Custom Properties (Variables) — uso real

### Mental model
Custom properties são **dinâmicas e cascadeáveis**. Não são apenas constantes — você pode redefini-las em escopos menores e elas viram tema.

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --color-bg: oklch(20% 0 0);
  --color-text: oklch(95% 0 0);
}

[data-theme="light"] {
  --color-bg: oklch(98% 0 0);
  --color-text: oklch(15% 0 0);
}

.card {
  background: var(--color-bg);
  color: var(--color-text);
  padding: var(--space-2);
}
```

### `@property` — tipos para custom properties

```css
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.box {
  background: linear-gradient(var(--gradient-angle), red, blue);
  transition: --gradient-angle 1s;
}

.box:hover { --gradient-angle: 360deg; }
```

Sem `@property`, transition de custom property não funciona. Com `@property`, você anima a variável diretamente.

---

## 4. Color spaces modernos — oklch, oklab, color-mix

### Mental model
`hsl` e `hex` são **não-uniformes perceptualmente**. Dois tons de azul com mesma "lightness" no HSL podem parecer drasticamente diferentes em brilho percebido. Isso quebra design systems.

`oklch` é **perceptualmente uniforme**: mesma `L` = mesmo brilho aparente. Mesma `C` = mesma saturação aparente.

```css
/* 5 tons de azul com brilho percebido linearmente decrescente */
--blue-100: oklch(95% 0.04 240);
--blue-300: oklch(80% 0.10 240);
--blue-500: oklch(60% 0.18 240);
--blue-700: oklch(40% 0.16 240);
--blue-900: oklch(20% 0.10 240);

/* mix de duas cores */
--surface: color-mix(in oklch, var(--blue-500), white 80%);
```

### Why oklch
- Mistura previsível
- Gradients sem zona morta cinza
- Acessibilidade: contraste mais previsível
- Suporte amplo nos browsers modernos (Chrome, Safari, Firefox)

---

## 5. Container Queries — o killer feature

### Mental model
`@media` consulta **a viewport**. `@container` consulta **um ancestral container**. Isso permite componentes que se adaptam ao **espaço onde foram colocados**, não ao tamanho da tela.

```css
.card-container {
  container-type: inline-size;   /* observa largura inline */
  container-name: card;
}

.card { display: grid; gap: 8px; }

@container card (min-width: 480px) {
  .card {
    grid-template-columns: 200px 1fr;  /* vira layout horizontal só se o container tiver >= 480px */
  }
}
```

### Por que isso é game changer
Você pode pôr o mesmo `.card` numa sidebar estreita e num main grande, e ele se adapta sozinho. Antes era impossível sem JavaScript.

### Unidades CQ
- `cqw` = 1% da largura do container
- `cqh` = 1% da altura
- `cqi` = 1% do inline-size (responsivo a writing direction)

---

## 6. `:has()`, `:is()`, `:where()`

### Mental model
- **`:has()`** — "parent selector". Selecione X que **tem** Y dentro.
- **`:is()`** — agrupa selectors mantendo a specificity da maior parte.
- **`:where()`** — agrupa selectors com specificity zero.

```css
/* Card que tem imagem ganha layout diferente */
.card:has(img) { padding: 0; }

/* Lista nada se for seguida de h2, p ou ul */
:is(h1, h2, h3) + p { margin-top: 0; }

/* Reset com specificity zero — fácil de sobrescrever */
:where(ul, ol) { list-style: none; }
```

---

## 7. Animação — keyframes, transitions, easing

### Mental model
Animação CSS é interpolar valores ao longo do tempo. Você define **estados** e o browser interpola.

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.05); }
}

.button {
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.button:hover { transform: scale(1.05); }

@media (prefers-reduced-motion: reduce) {
  .button { transition: none; }
}
```

### Easing
`linear` é raramente certo. **Movimento natural acelera e desacelera.** `ease-out` é seguro pra entrada, `ease-in` pra saída, `cubic-bezier` quando você precisa de personalidade.

`cubic-bezier(0.34, 1.56, 0.64, 1)` — overshoot leve, parece "spring".

### FLIP Technique
Para animar transições impossíveis (mudança de layout):

1. **First** — meça a posição inicial
2. **Last** — meça a posição final (depois da mudança)
3. **Invert** — aplique `transform` que cancela a mudança
4. **Play** — anime o `transform` para zero

`transform` é animado pelo GPU — performance impecável.

### `prefers-reduced-motion` — obrigatório

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 8. Dark Mode — The Quest for the Perfect

### Princípios

1. **Detectar** preferência do sistema (`prefers-color-scheme`)
2. **Permitir override** do usuário (toggle UI)
3. **Persistir** em localStorage
4. **Evitar flash** com script inline no `<head>` antes do hydrate
5. **Usar `color-scheme` CSS** para nativos do browser
6. **Custom properties** como camada de tema

### Script inline anti-flash (Next.js / SSR)

```html
<head>
  <script>
    (function() {
      try {
        const stored = localStorage.getItem('theme');
        const system = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        const theme = stored || system;
        document.documentElement.dataset.theme = theme;
        document.documentElement.style.colorScheme = theme;
      } catch (e) {}
    })();
  </script>
</head>
```

Esse script **roda síncrono antes do React hydratar**, evitando o flash de tema errado.

### CSS de tema

```css
:root {
  color-scheme: light;
  --bg: oklch(98% 0 0);
  --text: oklch(15% 0 0);
}

[data-theme="dark"] {
  color-scheme: dark;
  --bg: oklch(15% 0 0);
  --text: oklch(95% 0 0);
}

body {
  background: var(--bg);
  color: var(--text);
}
```

---

## 9. Acessibilidade — baseline

### Princípios não negociáveis

1. **Semântica HTML primeiro** — `<button>` antes de `<div onClick>`
2. **Focus visível sempre** — `:focus-visible` para keyboard, ocultando mouse focus se quiser
3. **Contraste WCAG AA mínimo** (4.5:1 texto, 3:1 UI)
4. **`prefers-reduced-motion`** para qualquer animação
5. **`prefers-contrast`** quando aumentar contraste
6. **Skip links** para keyboard users
7. **`aria-*` quando semântica não basta** — não substitui semântica

### Focus management

```css
.button {
  /* remova outline default só se você der substituto */
  outline: none;
}
.button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Skip link

```html
<a href="#main" class="skip-link">Pular para o conteúdo</a>
<main id="main" tabindex="-1">…</main>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 1rem;
  top: 1rem;
  z-index: 999;
}
```

---

## 10. React — patterns essenciais

### Mental model
React é **modelo declarativo** onde **estado dirige UI**. Você não manipula DOM; você descreve como UI deve estar para cada estado.

### Controlled vs uncontrolled

```jsx
// Controlled — React owns the state
function Search() {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}

// Uncontrolled — DOM owns the state, ler com ref
function Search() {
  const ref = useRef();
  return <input ref={ref} defaultValue="" />;
}
```

### useEffect é o último recurso
- Cálculos derivados → variável normal ou `useMemo`
- Eventos → handlers, não effects
- Subscriptions externas → effect (correto)

### Server Components (Next.js App Router)

- **Server Components** rodam só no servidor, mandam HTML/RSC payload
- **Client Components** (`"use client"`) hidratam no cliente
- Default é Server. `use client` é opt-in.

### Suspense

```jsx
<Suspense fallback={<Spinner />}>
  <SlowComponent />
</Suspense>
```

### Error Boundaries

```jsx
class Boundary extends Component {
  state = { error: null };
  static getDerivedStateFromError(error) { return { error }; }
  render() {
    if (this.state.error) return <Fallback />;
    return this.props.children;
  }
}
```

---

## 11. MDX & content sites

MDX = Markdown + JSX. Você escreve conteúdo em markdown e pode embutir componentes React. Base do joshwcomeau.com.

```mdx
# Meu artigo

Aqui é texto markdown.

<InteractiveDemo defaultValue={50} />

Mais texto.
```

Stack típica de Josh: **Next.js App Router + MDX + Shiki para syntax highlight + componentes próprios para demos interativos**.

---

## 12. Frameworks de aprendizado (meta)

### "Mental models first"
Sempre comece pelo **algoritmo / modelo conceitual**. Sintaxe vem depois.

### "Layered learning"
1. **Introduction** — o que é, em uma frase
2. **Mental model** — o desenho na cabeça
3. **Exercise** — pratique pequeno e progressivo
4. **Polish** — edge cases, a11y, performance

### "Smaller, progressive examples"
Nunca dump de código gigante. Comece com a versão mínima, adicione uma camada, mostre o resultado, adicione outra.

### "Default to accessible"
Acessibilidade no começo, não no fim.

---

## Resumo — o que Josh sabe que outros não

A maioria sabe **propriedades**. Josh sabe **algoritmos**. A maioria ensina **referência**. Josh ensina **modelos**. A maioria escreve animação **bonita**. Josh escreve animação **acessível e bonita**.

A diferença não é informação — é **estrutura mental**.
