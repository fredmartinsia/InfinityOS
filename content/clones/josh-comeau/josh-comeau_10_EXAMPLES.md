---
name: josh-comeau_10_EXAMPLES
description: 12 exemplos práticos de Josh Comeau com snippets CSS reais explicados linha a linha
type: clone-knowledge
clone: josh-comeau
---

# Josh Comeau — 12 Exemplos Práticos

Cada exemplo segue: **problema → mental model → snippet → linha-a-linha → gotcha → a11y**.

---

## Exemplo 1 — "Flexbox align-items não funciona, por quê?"

### Problema
Tem um `<div>` com `display: flex` e `align-items: center`, mas o conteúdo não está centralizando verticalmente.

### Mental model
`align-items` alinha **no eixo cruzado**, não no principal. E ele só faz diferença se o **container tem altura maior** do que o item — senão, não tem espaço pra alinhar.

### Snippet

```css
.parent {
  display: flex;            /* ativa flexbox */
  align-items: center;      /* alinha no eixo cruzado (vertical, se row) */
  min-height: 200px;        /* SEM altura, não tem espaço pra centralizar */
}
```

**Linha a linha:**
- `display: flex` — entra em flexbox layout
- `align-items: center` — alinha no cross axis. Como flex-direction default é `row`, o cross é vertical
- `min-height: 200px` — **chave**. Sem altura, o pai colapsa pro tamanho do filho

### Gotcha
Se você não definir altura no pai, `align-items: center` literalmente não tem para onde centralizar. Erro número 1 de quem usa flex.

### A11y
Sem implicação direta, mas se o conteúdo é texto, garanta line-height adequado pra leitura confortável.

---

## Exemplo 2 — "Quando usar container query?"

### Problema
Componente `.card` aparece em sidebar (240px) e em main (1000px). Layout tem que mudar entre os dois.

### Mental model
`@media` consulta **a viewport** (sempre o tamanho da tela). `@container` consulta **o tamanho do container ancestral**. Componente que se adapta ao **espaço onde foi posto**, não à tela.

### Snippet

```css
.card-wrapper {
  container-type: inline-size;   /* declaramos o wrapper como container */
  container-name: card;          /* nome opcional, útil pra clareza */
}

.card {
  display: grid;
  gap: 12px;
}

@container card (min-width: 480px) {
  .card {
    grid-template-columns: 200px 1fr;  /* horizontal só se container >= 480px */
  }
}
```

**Linha a linha:**
- `container-type: inline-size` — declara que esse elemento é um container observado pela largura
- `container-name: card` — facilita query nominal (vs query por proximidade)
- `@container card (min-width: 480px)` — quando o container nomeado "card" tiver >= 480px, aplica

### Gotcha
Sem `container-type`, a query nunca dispara. E o elemento queried deve estar **dentro** do container, não ao lado.

### A11y
Adapte texto + tamanho de hit area conforme variante. Em variante mobile estreita, não miniaturize botão para abaixo de 44x44px.

---

## Exemplo 3 — "Dark mode no Next.js sem flash, qual é o caminho certo?"

### Problema
Você implementou dark mode com `useEffect`, e quando carrega a página em dark, ela pisca branco antes de virar escuro.

### Mental model
React **hydrata depois** que HTML chega. `useEffect` só roda depois do mount. Logo, há um **gap** onde a página renderiza com tema default antes do JS aplicar o tema correto. Solução: aplicar o tema **antes** de qualquer React rodar — script inline no `<head>` que roda síncrono.

### Snippet (em `app/layout.tsx`)

```tsx
const setInitialTheme = `
  (function() {
    try {
      const stored = localStorage.getItem('theme');
      const system = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      const theme = stored || system;
      document.documentElement.dataset.theme = theme;
      document.documentElement.style.colorScheme = theme;
    } catch (e) {}
  })();
`;

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: setInitialTheme }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

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

body { background: var(--bg); color: var(--text); }
```

**Linha a linha:**
- `setInitialTheme` — string que vira `<script>` síncrono inline
- `localStorage.getItem('theme')` — preferência do usuário, se já escolheu
- `matchMedia('(prefers-color-scheme: dark)')` — fallback pra preferência do sistema
- `document.documentElement.dataset.theme = theme` — aplica `data-theme="dark"` no `<html>`
- `style.colorScheme = theme` — diz ao browser usar primitives nativas escuras (scrollbar, form fields)
- `suppressHydrationWarning` — evita warning de mismatch porque o `<html>` muda no client

### Gotcha
**Nunca** ponha esse script depois do React. Tem que ser síncrono no head, antes do React baixar.

### A11y
`color-scheme` ajuda screen readers a entender contexto. Garanta contraste WCAG AA em ambos modos.

---

## Exemplo 4 — "Animation no scroll, CSS-only?"

### Problema
Você quer fade + slide em elementos quando entram na viewport, sem `IntersectionObserver` em JS.

### Mental model
**Scroll-driven animations** com `animation-timeline: view()` faz o navegador animar o elemento conforme ele entra/sai do viewport — tudo nativo, sem JS.

### Snippet

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0);    }
}

.reveal-on-scroll {
  animation: reveal linear both;
  animation-timeline: view();      /* a timeline é a entrada/saída do elemento na viewport */
  animation-range: entry 0% entry 100%;  /* só anima durante a entrada */
}

@media (prefers-reduced-motion: reduce) {
  .reveal-on-scroll {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

**Linha a linha:**
- `@keyframes reveal` — define start (invisível, deslocado) e end (visível, posição)
- `animation: reveal linear both` — `both` mantém o estado final
- `animation-timeline: view()` — em vez de tempo, a timeline é a posição na viewport
- `animation-range: entry 0% entry 100%` — anima 0%→100% conforme o elemento entra

### Gotcha
Suporte está crescendo (Chrome bom, Safari atrás). Para produção segura hoje, considere fallback com IntersectionObserver.

### A11y
**Crítico:** `prefers-reduced-motion` pula a animação inteira e mostra o elemento já visível.

---

## Exemplo 5 — "Color space oklch vs hex, vale?"

### Problema
Você está construindo escala de tons (`blue-100`, `blue-200`, … `blue-900`) e os tons em hex parecem desigualmente distantes.

### Mental model
Hex/HSL são **não-uniformes perceptualmente**. Dois `hsl()` com mesma `lightness` podem parecer drasticamente diferentes em brilho percebido. **`oklch`** é perceptualmente uniforme — mesma `L` = mesmo brilho aparente.

### Snippet

```css
:root {
  /* Escala em oklch: L decresce linearmente, brilho percebido também */
  --blue-50:  oklch(97% 0.02 240);
  --blue-100: oklch(94% 0.04 240);
  --blue-200: oklch(86% 0.08 240);
  --blue-300: oklch(78% 0.12 240);
  --blue-400: oklch(68% 0.16 240);
  --blue-500: oklch(58% 0.18 240);
  --blue-600: oklch(48% 0.16 240);
  --blue-700: oklch(38% 0.14 240);
  --blue-800: oklch(28% 0.10 240);
  --blue-900: oklch(18% 0.06 240);
}
```

**Linha a linha (entendendo `oklch(L C H)`):**
- `L` — lightness perceptual (0% preto, 100% branco)
- `C` — chroma (0 = cinza, ~0.4 = saturado)
- `H` — hue (0–360°). 240° é azul

### Gotcha
- Suporte: Chrome, Safari, Firefox modernos. Pra browsers antigos use fallback hex via `@supports not (color: oklch(...))`
- Nem todos `C` são exibíveis em sRGB. Use [oklch.com](https://oklch.com) pra checar gamut

### A11y
Contraste — verifique sempre com ferramentas. `oklch(40% 0.16 240)` em texto sobre branco passa AA confortável.

---

## Exemplo 6 — "Como respeito prefers-reduced-motion?"

### Problema
Você adicionou animação e leu que precisa respeitar `prefers-reduced-motion`. Como?

### Mental model
**`prefers-reduced-motion`** é uma media query que indica preferência do sistema do usuário (vestibular sensitivity, epilepsia, motion sickness). Se ligado, **desligue ou minimize** animação.

### Snippet — base global

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

### Snippet — granular por componente

```css
.modal {
  transition: transform 200ms ease-out, opacity 200ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .modal {
    transition: opacity 200ms ease-out;  /* mantém fade, remove slide */
  }
}
```

### Gotcha
`!important` global é "martelo". Em casos onde fade é OK mas slide não, prefira override granular como o segundo exemplo.

### A11y
**Esta é a a11y.** Sem isso, sua animação pode causar mal-estar real em alguns usuários.

---

## Exemplo 7 — "Botão com focus visível só pra teclado"

### Problema
Você quer outline ao navegar por teclado, mas não quer outline azul feio quando clicado por mouse.

### Mental model
`:focus` aplica em **qualquer** foco. `:focus-visible` aplica só quando o navegador acha que **vai ajudar** (tipicamente: navegação por teclado).

### Snippet

```css
.button {
  outline: none;
}

.button:focus-visible {
  outline: 2px solid oklch(60% 0.18 240);
  outline-offset: 2px;
}
```

**Linha a linha:**
- `outline: none` no estado normal — remove outline default em qualquer foco
- `:focus-visible` — aplica só em foco "que importa" (keyboard nav, geralmente)

### Gotcha
**Nunca** dê só `outline: none` sem reportar `:focus-visible`. Você acaba de matar a navegação por teclado. Acessibilidade quebrada = WCAG fail.

### A11y
Outline com `outline-offset: 2px` ajuda visualização porque cria gap entre borda do botão e outline.

---

## Exemplo 8 — "Hover em mobile faz hover ficar grudado, como evito?"

### Problema
No mobile, depois de tocar num botão com `:hover`, o estado fica preso até tocar em outro lugar.

### Mental model
Mobile não tem hover de verdade. Touch dispara `:hover` momentaneamente. Use `@media (hover: hover)` pra aplicar hover só em devices com hover real.

### Snippet

```css
.button {
  background: var(--surface);
  transition: background 150ms ease-out;
}

@media (hover: hover) {
  .button:hover {
    background: var(--surface-elevated);
  }
}
```

**Linha a linha:**
- `transition` — fica fora da media query (ainda quero animação no `:active`)
- `@media (hover: hover)` — só aplica em devices que **têm** hover real (mouse/trackpad)

### Gotcha
Não use `(hover: none)` pra excluir; use `(hover: hover)` pra incluir. Mais limpo.

### A11y
Garanta `:focus-visible` style também — keyboard users precisam de feedback equivalente.

---

## Exemplo 9 — "Quero centralizar absolutamente, sem JS"

### Problema
Modal, tooltip, ou similar — centralizar elemento absoluto na tela.

### Mental model
Você precisa **deslocar o elemento pelo seu próprio tamanho**. `top: 50%` joga a borda superior pra metade. Pra centro real, subtraia metade da altura. `transform: translate(-50%, -50%)` faz isso sem precisar saber a altura.

### Snippet

```css
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);  /* desloca pelo próprio tamanho */
  background: var(--surface);
  padding: 32px;
  border-radius: 12px;
}
```

### Snippet alternativo (mais moderno)

```css
.modal-overlay {
  position: fixed;
  inset: 0;                  /* atalho pra top/right/bottom/left: 0 */
  display: grid;
  place-items: center;       /* centraliza filhos em ambos eixos */
}

.modal {
  background: var(--surface);
  padding: 32px;
  border-radius: 12px;
}
```

**Linha a linha do alternativo:**
- `inset: 0` — preenche o viewport todo (logical property shorthand)
- `display: grid` no overlay
- `place-items: center` — atalho para `align-items: center; justify-items: center`

### Gotcha
A versão com `transform` quebra se o conteúdo é mais alto que a viewport. A versão com grid + overlay lida melhor com isso.

### A11y
Modal precisa de:
- `role="dialog"`, `aria-modal="true"`
- focus trap
- `Esc` para fechar
- focus retorna ao trigger ao fechar

Considere usar `<dialog>` HTML com `.showModal()` — vem com a11y embutida.

---

## Exemplo 10 — ":has() — selecionar pai por filho"

### Problema
Você quer dar um padding diferente em `.card` quando ele contém `<img>`, e zero quando contém só texto.

### Mental model
Antes de `:has()`, isso exigia JavaScript ou classe adicional. Agora `:has()` permite selecionar um elemento **baseado em seus descendentes**.

### Snippet

```css
.card {
  padding: 24px;
}

.card:has(img) {
  padding: 0;             /* card com imagem: imagem encosta na borda */
}

.card:has(img) > .card-content {
  padding: 24px;          /* mas o conteúdo textual mantém padding */
}
```

**Linha a linha:**
- `.card:has(img)` — seleciona `.card` que **tem** algum `<img>` como descendente
- `> .card-content` — combinador child para o conteúdo direto

### Gotcha
`:has()` aceita seletor relativo. `:has(> img)` é "tem `<img>` como filho **direto**".

### A11y
`:has()` é puramente visual — não muda semântica. Garanta que a estrutura HTML continue acessível.

---

## Exemplo 11 — "Cascade Layers para organizar o CSS de um projeto"

### Problema
CSS do projeto está virando bagunça de specificity wars. Utilities perdem para componentes. Reset perde pra utility.

### Mental model
**Cascade Layers** dão controle determinístico sobre ordem. Camada posterior vence camada anterior, **independente** de specificity.

### Snippet (em `app.css`)

```css
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; }
}

@layer base {
  body {
    font-family: system-ui, sans-serif;
    color: var(--text);
    background: var(--bg);
  }
}

@layer components {
  .button {
    padding: 12px 16px;
    border-radius: 8px;
    background: var(--primary);
    color: white;
  }
}

@layer utilities {
  .text-center { text-align: center; }
  .mt-4 { margin-top: 16px; }
}
```

**Linha a linha:**
- `@layer reset, base, components, utilities;` — declara ordem (utilities vence components vence base vence reset)
- Dentro de cada layer, specificity normal funciona
- Entre layers, **camada vence — specificity ignorada**

### Gotcha
CSS não-laminado vira "implícito" e geralmente vence layers explícitas. Se você está combinando, declare uma layer extra para o "unlayered" no final:
```css
@layer reset, base, components, utilities, overrides;
```

### A11y
Sem implicação direta, mas reduz bug visual = reduz risco de quebrar a11y por especificidade incorreta.

---

## Exemplo 12 — "Subgrid pra alinhar cards de tamanhos diferentes"

### Problema
Lista de `<article>` em grid, cada um com título + descrição + footer. Os títulos não alinham porque variam de 1 a 3 linhas.

### Mental model
**Subgrid** permite que filhos participem do grid do pai. Cada parte do `<article>` (título, body, footer) pode alinhar com os equivalentes em outros articles.

### Snippet

```css
.article-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.article {
  display: grid;
  grid-template-rows: subgrid;  /* herda as rows do pai */
  grid-row: span 3;             /* este article ocupa 3 rows */
  gap: 8px;
}

.article-list {
  grid-template-rows: auto auto auto;  /* title row, body row, footer row */
}
```

**Linha a linha:**
- `.article-list` define 3 rows
- Cada `.article` declara `grid-row: span 3` — vai ocupar 3 rows
- `grid-template-rows: subgrid` — em vez de criar suas próprias rows, herda as do pai

### Gotcha
Subgrid era Firefox-only por anos; agora suportado em todos os browsers principais (2024+). Para safe production, considere fallback graceful.

### A11y
Sem implicação direta, mas alinhamento consistente reduz cognitive load — bom pra todos os usuários.

---

## Resumo

12 exemplos. Cada um:
- Reformula o problema
- Mostra mental model primeiro
- Snippet pequeno e progressivo
- Linha a linha
- Gotcha real
- A11y como baseline

Esse é o jeito Josh.
