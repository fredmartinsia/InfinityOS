# Checklist: Motion Quality

> Critérios de qualidade para QUALQUER animação no output do squad. Animação que falha aqui é decoração descartável e deve ser removida ou refeita.

## Princípio fundamental

**Toda animação tem um propósito narrativo ou funcional. Se não consegue explicar em uma frase qual é o propósito, é decoração — remova.**

Propósitos válidos:
- **Storytelling** — guia o olhar pela narrativa do conteúdo
- **Feedback** — mostra que uma ação foi recebida (click, hover, drag)
- **Continuidade** — preserva o contexto entre estados (item da lista → tela de detalhe)
- **Affordance** — indica que algo é interativo (botão pulsa sutilmente, cursor magnético)
- **Progress** — comunica que algo está acontecendo (loader, skeleton)

Propósitos inválidos:
- "Para ficar bonito"
- "Porque o site de referência tinha"
- "Pra animar"
- "Pra parecer premium"

## Para cada animação

### 1. Propósito

- [ ] **Propósito claro** declarável em uma frase ("entrada do hero comunica início da narrativa")
- [ ] **Não-decorativa** — remover essa animação prejudicaria a experiência?
- [ ] **Não-redundante** — não há outra animação no mesmo elemento competindo

### 2. Timing

- [ ] **Duração apropriada:**
  - Micro-interaction (hover, focus, press): 100-200ms
  - Component transition (modal, drawer, dropdown): 200-300ms
  - Page transition: 400-600ms
  - Hero / scroll storytelling: depende do scroll, mas elementos individuais 600-1500ms max
- [ ] **Não muito rápida** (< 100ms vira "pisca")
- [ ] **Não muito lenta** (> 800ms para micro-interactions é tedioso)

### 3. Easing

- [ ] **Não-linear** — `linear` quase nunca é a resposta certa
- [ ] **Easing apropriado:**
  - Entrada: `ease-out` ou spring (chega devagar = parece chegar)
  - Saída: `ease-in` ou spring (sai rápido = some sem chamar atenção)
  - Looping: `ease-in-out`
  - Spring physics para movimento "natural" (Framer Motion / GSAP)
- [ ] **Curva customizada** para casos específicos (`cubic-bezier(0.34, 1.56, 0.64, 1)` para overshoot)

### 4. Performance

- [ ] **60fps** em desktop (sem dropped frames perceptíveis)
- [ ] **30fps+ aceitável em mobile mid-tier** (idealmente 60fps)
- [ ] **Anima apenas `transform` e `opacity`** — não `width`, `height`, `top`, `left`, `margin`
  - Exceção: animação de layout com FLIP technique ou `layoutId` do Framer Motion (medido)
- [ ] **GPU-accelerated** — usa `will-change` ou `translateZ(0)` apenas onde compensa (não global)
- [ ] **Sem re-layout** (paint OK, layout não)

### 5. Interrupção

- [ ] **Interruptível** — clicar / scrollar antes da animação acabar não trava nada
- [ ] **Estado consistente** ao interromper (Framer Motion faz isso de graça; CSS animation requer cuidado)
- [ ] **Sem flicker** ao mudar de estado A para B no meio da animação

### 6. Acessibilidade

- [ ] **prefers-reduced-motion** respeitado:
  - Animação removida OU
  - Animação substituída por fade simples e curto
  - Movimento espacial removido (parallax, scroll storytelling) — preferir fade
- [ ] **Não causa motion sickness** (parallax extremo, rotação rápida)
- [ ] **Sem flashes** acima de 3 por segundo (epilepsia)
- [ ] **Anúncios em ARIA live** quando animação carrega conteúdo importante

### 7. Mobile

- [ ] **Funciona em mobile** (testado em viewport pequena)
- [ ] **Não exige hover** para ser ativada (mobile não tem hover)
- [ ] **Não bloqueia scroll** (`touch-action: pan-y` se necessário)
- [ ] **Performance OK em mobile** (testado em throttle 4G + CPU 4x slow)

### 8. Layout shift

- [ ] **CLS = 0** durante e após animação
- [ ] **Reservou espaço** antes do elemento entrar (não deixa o pai "expandir" durante entrada)
- [ ] **Animação de width/height** usa transform scale ou layout animation framework

## Para scroll-driven animations especificamente

- [ ] **Lenis ou smooth scroll equivalente** ativo (sem ele, scrub fica engasgado)
- [ ] **scrub: true** em ScrollTrigger (não `false` se queremos sincronia com scroll)
- [ ] **start/end** definidos com viewport reference (não pixel hardcoded)
- [ ] **`pin: true`** apenas onde a seção precisa "ficar fixa" enquanto anima — não em tudo
- [ ] **`pinSpacing`** ajustado se precisar (default cria espaço extra)
- [ ] **`invalidateOnRefresh: true`** se layout pode mudar
- [ ] **Cleanup** ao desmontar (`ScrollTrigger.kill()`) — vaza memória se não fizer
- [ ] **Mobile alternative** definida (scroll storytelling pesado pode virar fade simples no mobile)

## Para 3D / WebGL animations

- [ ] **Cena pausa** quando off-screen (`useFrame` condicional)
- [ ] **Throttle** de updates onde frame-precise não importa
- [ ] **Pixel ratio** capado (`gl.setPixelRatio(Math.min(2, devicePixelRatio))`)
- [ ] **Frustum culling** ativo para cenas com muitos meshes
- [ ] **Mobile fallback** (imagem estática ou versão simplificada)

## Veredito por animação

Para cada animação no output, marcar:

- ✅ **APROVADA** — propósito claro, timing/easing certo, perf OK, interruptível, a11y OK
- ⚠️ **APROVADA COM AJUSTE** — problema pequeno: ajusta easing, duration, ou adiciona prefers-reduced-motion
- ❌ **REPROVADA** — propósito decorativo OU perf ruim OU não respeita reduced motion
  - Ação: remover OU refazer

## Veredito final

- ✅ **MOTION PRONTO** — todas animações aprovadas (com ou sem ajuste)
- ❌ **MOTION NÃO PRONTO** — pelo menos 1 animação reprovada que precisa ser refeita ou removida
