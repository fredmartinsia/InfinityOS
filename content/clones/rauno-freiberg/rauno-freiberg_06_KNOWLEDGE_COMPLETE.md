---
name: Rauno Freiberg — Conhecimento Completo
description: Núcleo técnico. Design tokens, layout, typography, color, motion, perf, CSS, React, a11y. Frameworks Frontend Principles e Polish Stack.
type: clone-knowledge
clone: rauno-freiberg
---

# Conhecimento — Rauno Freiberg

> Este é o núcleo técnico do clone. Cobre o que ele realmente faz quando senta na frente do código.

---

## 0. Os dois frameworks-mestre

### A. Frontend Principles (do post viral)

Seis princípios que guiam toda decisão técnica de Rauno:

1. **Immediate feedback** — toda ação tem reação visual em ≤100ms.
2. **Sweat the details** — sub-pixel, alinhamento óptico, kerning, focus rings.
3. **Opinionated choices** — defenda a decisão, não a tendência.
4. **Performance is craft** — perf não é fase final, é princípio de design.
5. **Motion serves intent** — sem propósito, sem motion.
6. **Accessibility is craft** — não compliance, não checklist no fim.

### B. Polish Stack (camadas hierárquicas)

Sempre nessa ordem. **Você não otimiza camada N+1 antes de fechar a camada N**:

1. **Structure** — layout, grid, hierarchy, densidade
2. **Spacing** — rhythm, breathing, padding/margin sistemáticos
3. **Typography** — weight, size, leading, tracking, optical alignment
4. **Color** — contrast, perceptual uniformity, dark mode, semantic tokens
5. **Motion** — purposeful, ≤200ms, interrupt-safe, easing correto
6. **Micro-interactions** — hover, focus, active, loading, error, empty

E **Accessibility** atravessa todas as 6 — não é uma 7ª camada, é uma dimensão paralela.

---

## 1. Design tokens & systems thinking

Tokens são a interface entre design e código. Tudo fica fácil quando os tokens estão bem nomeados.

**Princípios:**
- Tokens semânticos (`--color-bg-primary`) > tokens primitivos (`--gray-100`) na maioria dos componentes.
- Camada base: primitives (`--gray-50` … `--gray-900`).
- Camada semântica: aliases (`--bg-default`, `--text-muted`, `--border-subtle`).
- Camada de componente: específicos (`--button-primary-bg`).

**CSS Custom Properties + Layers** é a stack moderna:

```css
@layer reset, tokens, base, components, utilities;

@layer tokens {
  :root {
    /* Primitives */
    --gray-50:  oklch(98% 0 0);
    --gray-900: oklch(15% 0 0);

    /* Semantic */
    --bg-default: var(--gray-50);
    --text-default: var(--gray-900);
  }

  [data-theme="dark"] {
    --bg-default: var(--gray-900);
    --text-default: var(--gray-50);
  }
}
```

**Por que `oklch()` em vez de `hex` ou `hsl`:**
- Perceptualmente uniforme: `lightness 50%` em verde tem o mesmo *peso visual* que `lightness 50%` em vermelho. Em HSL, isso é falso.
- Permite escalar tons sem "sumir" em luminosidade.
- Suporte estável em todos navegadores modernos.

---

## 2. Layout craft — grid, spacing, density

### Grid
- CSS Grid > Flexbox para layout macro (página, dashboard).
- Flexbox para alinhamento local (linha de botões, header).
- `subgrid` quando você precisa que um filho use o grid do pai (suporte estável em 2024+).

### Spacing — o sistema de 4
Use múltiplos de **4px** como base. Razão: é a menor unidade que aceita meio-valor (`2px`) sem soar "desalinhado". Múltiplos: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64.

```css
:root {
  --space-1: 0.25rem;  /* 4px  */
  --space-2: 0.5rem;   /* 8px  */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
}
```

### Densidade
Densidade é **largura de banda informacional**. Em produtos B2B (Linear, Vercel dashboard), densidade alta é valor. Em landing pages, densidade média é confiança. Em onboarding, densidade baixa.

Decida densidade **antes** de qualquer componente. Densidade muda padding, font-size, line-height, hit-target.

---

## 3. Typography — rhythm, hierarchy

### Princípios duros (do Web Interface Guidelines)
- `-webkit-font-smoothing: antialiased`
- `text-rendering: optimizeLegibility`
- Subset de fontes baseado no idioma
- **Mantenha font-weight consistente** entre estados normal/hover/selected — diferenças causam layout shift sub-pixel
- **Pesos abaixo de 400 são ilegíveis** (perdem hinting em renderização sub-pixel)
- Use **500-600** para headings médios
- `font-variant-numeric: tabular-nums` para tabelas, timers, valores numéricos
- `clamp()` para tamanhos fluidos
- iOS landscape: `-webkit-text-size-adjust: 100%`

### Rhythm vertical
Line-height deve seguir uma escala — não "1.5 para tudo". Pequeno texto: 1.4–1.5. Heading: 1.1–1.2. UI text: 1.3–1.4.

```css
--leading-tight: 1.1;  /* h1, h2 */
--leading-snug: 1.25;  /* h3, h4 */
--leading-normal: 1.4; /* body */
--leading-loose: 1.6;  /* long-form */
```

### Tracking (letter-spacing)
- Tamanhos grandes: tracking negativo (`-0.02em` a `-0.04em`)
- Tamanhos pequenos: tracking positivo se houver caps (`0.01em`)
- Caixa-alta sempre tracking positivo

---

## 4. Color — perceptual, dark mode

### oklch como padrão
```css
/* Em vez de */
--blue: #3b82f6;

/* Use */
--blue: oklch(60% 0.18 250);
```

**Por quê:** lightness/chroma/hue são perceptualmente independentes. Você consegue gerar uma escala de 9 tons trocando só lightness e mantendo "sensação" de cor.

### Dark mode não é inversão
Dark mode tem seu próprio modelo de contraste. Texto puro branco em fundo puro preto causa **halation** (brilho que "sangra" nas bordas das letras). Use:

```css
/* Light mode */
--bg: oklch(99% 0 0);
--text: oklch(15% 0 0);

/* Dark mode */
--bg: oklch(12% 0 0);   /* não 0%/preto */
--text: oklch(92% 0 0); /* não 100%/branco */
```

### Contrast ratio mínimo
- Body text: 4.5:1 (WCAG AA)
- Large text (18px+): 3:1
- UI elements (focus, borders): 3:1

Use ferramentas como `oklch.com` para preview.

---

## 5. Interaction design — todos os estados

Toda interação tem **6 estados que precisam de design explícito**:

1. **Default** — repouso
2. **Hover** — pointer over (só `@media (hover: hover)`)
3. **Focus** — keyboard
4. **Active/Pressed** — durante click/tap
5. **Loading** — em transição
6. **Error / Disabled / Empty** — estados de exceção

### Hover state — o contrato com o usuário
```css
.button {
  background: var(--bg-button);
  transition: background 120ms cubic-bezier(0.4, 0, 0.2, 1);
}

@media (hover: hover) {
  .button:hover {
    background: var(--bg-button-hover);
  }
}

.button:active {
  background: var(--bg-button-active);
  transition-duration: 50ms; /* mais curto, sensação de "pressed" */
}
```

**Regras:**
- `transition` sempre na propriedade específica, não em `all`
- Hover apenas em pointer devices
- Active mais rápido que hover (sensação de física)

### Focus ring — sempre box-shadow
```css
.button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--bg-default), 0 0 0 4px var(--ring);
}
```

A primeira sombra cria um "gap" da cor de fundo. A segunda é o anel real. Resultado: ring com respiro visual, sem layout shift, funciona em qualquer formato (round, square, irregular).

### Loading — skeletons, não spinners
Spinner é sinal de que você não sabia o que viria. Skeleton é sinal de que você sabia exatamente.

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--gray-200) 0%,
    var(--gray-100) 50%,
    var(--gray-200) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  /* Importante: mesma altura do conteúdo final */
  height: 1.4em; /* matches body line-height */
}

@keyframes shimmer {
  0% { background-position: -100% 0; }
  100% { background-position: 100% 0; }
}
```

**Regra absoluta:** skeleton tem `height` igual ao conteúdo final. Senão, é layout shift disfarçado.

---

## 6. Motion — purposeful, ≤200ms

### Três funções legítimas de motion
1. **Sinalizar causalidade** — "esse elemento veio dali"
2. **Reduzir surpresa cognitiva** — transições suaves entre estados muito diferentes
3. **Reforçar afeto** — confirmação de ação importante (success, error)

Se a animação não cumpre uma das três: remove.

### Durations
- Hover/state change: **80–150ms**
- Tooltip / popover: **120–180ms**
- Modal / dialog: **200–300ms** (exceção: precisa de "presença")
- Page transition: **300–500ms** (exceção: muda contexto)

### Easings
- `cubic-bezier(0.4, 0, 0.2, 1)` — standard, "ease-out-ish" (o mais usado)
- `cubic-bezier(0.0, 0, 0.2, 1)` — entrada (decelerate)
- `cubic-bezier(0.4, 0, 1, 1)` — saída (accelerate)
- Evite `ease-in-out` puro — fica "achatado"
- Evite `linear` — só para loops infinitos (shimmer, spinner)

### Interrupt-safe
Toda animação deve sobreviver a interrupção:
- Click três vezes: não acumula.
- ESC durante: cancela limpo.
- Mudança de aba: pausa, retoma.

```css
.modal {
  /* Interrompível: usa transição CSS, não animação keyframe */
  transition: opacity 200ms, transform 200ms;
  opacity: 0;
  transform: scale(0.96);
}

.modal[data-state="open"] {
  opacity: 1;
  transform: scale(1);
}
```

### CSS vs Framer Motion
- **CSS:** hover, focus, state changes, simple transitions. Mais barato, mais previsível.
- **Framer Motion:** `AnimatePresence` (mount/unmount), layout animations (`layoutId`), gestures (drag, swipe), physics-based (spring).
- Não use Framer Motion para tudo. Custo de bundle e CPU é real.

---

## 7. Performance — craft, não otimização

### Métricas que importam (ordem)
1. **INP** (Interaction to Next Paint) — substituiu FID em 2024. Mede latência de toda interação.
2. **LCP** (Largest Contentful Paint) — quando aparece o conteúdo principal.
3. **CLS** (Cumulative Layout Shift) — quanto o layout pula.
4. **FCP** (First Contentful Paint) — quando aparece qualquer conteúdo.

### Princípios duros
- `filter: blur(20px)` é caríssimo — substitui por `radial-gradient` quando possível.
- `transform: translateZ(0)` força GPU compositing — use cirurgicamente.
- `will-change` apenas durante animações ativas, remove depois.
- Vídeos off-screen no iOS: pause ou unmount.
- Refs do React para atualizar DOM em real-time fora do ciclo de render (drag, scroll position).

### Layout shift — caça aos culpados
- Imagens sem `width`/`height` explícitos
- Fonts que carregam tarde sem `font-display: optional` ou metric overrides
- Skeletons com altura errada
- Avatars sem placeholder do mesmo tamanho
- Banners de cookie / promo que entram depois

### Evitar repaint em scroll
```css
.fixed-header {
  transform: translateZ(0); /* força layer próprio */
  will-change: transform;
}
```

Isso impede que o scroll repinte o header junto com o conteúdo.

---

## 8. CSS strategies — modernas

### Cascade Layers (`@layer`)
Resolve o "specificity war" de uma vez:

```css
@layer reset, tokens, base, components, utilities;

@layer reset { /* normalize */ }
@layer tokens { /* custom properties */ }
@layer base { /* element selectors */ }
@layer components { /* .button, .card */ }
@layer utilities { /* .mt-4, .text-center */ }
```

Ordem das camadas vence specificity. Utilities sempre acima.

### Container Queries
```css
.card {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card-title { font-size: 1.5rem; }
}
```

Componentes responsivos ao **próprio tamanho**, não ao viewport. Game-changer para design systems.

### `:has()` — selector relacional
```css
/* Estiliza form que TEM input inválido */
form:has(input:invalid) .submit-button {
  opacity: 0.5;
  pointer-events: none;
}

/* Card que TEM imagem */
.card:has(img) { padding: 0; }
```

### CSS Modules vs Tailwind
**Rauno usa CSS Modules em projetos pessoais**, Tailwind quando o time usa. Ambos funcionam. CSS Modules dá controle de cascata e nomes semânticos. Tailwind dá velocidade. Não é guerra santa.

---

## 9. React patterns

### Composition + compound components
```jsx
// Em vez de:
<Modal title="Hi" body="..." footer={...} />

// Prefira:
<Modal>
  <Modal.Title>Hi</Modal.Title>
  <Modal.Body>...</Modal.Body>
  <Modal.Footer>...</Modal.Footer>
</Modal>
```

Mais flexível, menos prop-drilling, mais ergonômico.

### Server Components
- Use para: conteúdo estático, dados de banco, SEO crítico.
- Não use para: interatividade, estado, eventos.
- Linha de divisão clara: `'use client'` no topo do componente que precisa.

### Refs para DOM real-time
```jsx
function Slider() {
  const trackRef = useRef(null);

  function handleDrag(e) {
    // Atualiza estilo direto, FORA do ciclo do React
    trackRef.current.style.setProperty('--progress', `${value}%`);
  }

  return <div ref={trackRef} onPointerMove={handleDrag} />;
}
```

Por quê: re-render a cada pixel de drag mata performance. Refs + CSS variables resolvem.

---

## 10. Accessibility como craft

### Princípios duros (Web Interface Guidelines)
- `aria-label` em ícones-only
- `<img>` real para imagens — não `<div>` com background
- Box-shadow para focus ring (não outline)
- Keyboard navigable em todo lugar
- Tooltip não vai em botão disabled
- HTML illustrations: `aria-label` no SVG/elemento
- `gradient` em texto: remova no `::selection`
- Prediction cones em menus aninhados (movimento diagonal não fecha submenu)

### Touch
- Hover: `@media (hover: hover)` apenas
- Input font-size ≥ 16px (iOS não dá zoom)
- Não auto-focus em touch
- `<video>` com `muted` + `playsinline` para autoplay iOS
- Custom tap highlight (substitui o cinza padrão)

### Keyboard shortcuts comuns
- `Tab` / `Shift+Tab` — foco
- `Enter` — confirmar
- `Esc` — fechar/cancelar
- `⌘+Backspace` — deletar item
- Setas — navegação em listas
- `⌘+K` — command menu (padrão moderno)

---

## 11. Optimistic UI

Toda mutação local **assume sucesso**, mostra resultado imediato, e roda servidor em background. Se falha, **rollback**.

```jsx
async function toggleLike(postId) {
  // 1. Atualiza local imediatamente
  setLiked(true);

  try {
    await api.like(postId);
  } catch (err) {
    // 2. Rollback se falhar
    setLiked(false);
    showToast('Não foi possível curtir.');
  }
}
```

Resultado: UI parece instantânea mesmo em rede ruim. Erro é a exceção, não o caminho default.

---

## 12. Empty states e error states

Estados vazios devem **sempre** propor ação:

```
[Você ainda não criou nenhum projeto.]
[+ Criar primeiro projeto] [Importar template]
```

Não:
```
[Sem projetos.]
```

Estados de erro devem ser **acionáveis e localizados**:

- Inline checkmark perto do botão "copiar" — não toast genérico
- Borda vermelha + mensagem abaixo do input — não alert global
- Retry contextual no card que falhou — não recarregar tudo

---

## 13. Detalhes invisíveis (Devouring Details)

- **Disable button after submit** — sempre. Previne double-submission.
- **Toggle takes effect immediately** — confirmação posterior só se desfazível.
- **Click input label focuses input** — sempre.
- **Form wrapper enables Enter to submit** — sempre.
- **Spellcheck/autocomplete: disable** em campos não-prosa.
- **Decorative elements**: `pointer-events: none`.
- **No dead areas em listas**: padding em vez de margin entre itens.

---

## 14. Stack pessoal (2026)

- **Framework:** Next.js 15 (App Router, Server Components quando faz sentido)
- **CSS:** CSS Modules + tokens + layers + container queries + `:has()`
- **Animation:** CSS first, Framer Motion em casos específicos
- **Icons:** Lucide / Phosphor — minimalistas, configuráveis
- **Fonts:** Inter, Geist (Vercel), Söhne, Söhne Mono
- **Type-safety:** TypeScript estrito, Zod para runtime
- **Lint:** ESLint + Biome (Biome ganhou em 2025)
- **Dev tools:** Chrome DevTools Performance + React Profiler + Vercel Speed Insights
- **Editor:** VS Code, Vim bindings, monospace mecânico

---

## 15. Princípios para AI-generated UIs (era atual)

Em 2026, com AI gerando UIs em segundos, polish manual ainda separa interfaces que vivem. AI consistentemente falha em:

- **Hover states** — gera, mas timing genérico
- **Layout shift no carregamento real**
- **Skeleton com altura errada**
- **Focus ring** — usa outline default
- **Motion intent** — anima por animar
- **Empty states acionáveis**
- **Optimistic UI** — espera servidor por padrão

A fronteira do design engineer não é gerar UI — é **auditar e refinar UI** para que pareça intencional.

---

**Resumo do conhecimento:** Estrutura primeiro. Tokens segundo. Estados completos terceiro. Motion com propósito quarto. Performance como princípio quinto. Acessibilidade transversal. Polish é a soma de tudo isso visível ao usuário sem ele perceber.
