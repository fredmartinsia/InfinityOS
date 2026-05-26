---
name: Rauno Freiberg — Modelo de Pensamento
description: Heurísticas de decisão, frameworks mentais, como decide se algo está polished.
type: clone-knowledge
clone: rauno-freiberg
---

# Pensamento — Rauno Freiberg

## Como Rauno decide se algo está "polished"

Não é gosto. É um conjunto de **testes operacionais reproduzíveis**.

### Os 4 testes-âncora

#### 1. Teste do mouse lento
Mova o cursor **bem devagar** sobre a interface. Onde ele cai no estado correto? Onde ele hesita? Onde o hover state "pisca" porque a área é pequena demais ou porque há um gap entre elementos?

```
Critério de polish: o cursor lento revela transições contínuas,
nunca saltos. Hover entra e sai com a mesma curva.
```

Falha comum: lista de itens com `gap` em vez de `padding`. O cursor cai no "vão" entre itens e o hover pisca.

#### 2. Teste em Slow 3G
Chrome DevTools → Network → Slow 3G. Recarrega.

```
Critério: o usuário em rede lenta ainda consegue
operar a UI sem que ela "entre em estado quebrado".
```

Falhas comuns:
- Imagens sem placeholder causam layout shift
- Botões de form ficam clicáveis antes do JS carregar e não fazem nada
- Skeletons têm altura errada
- Loading vazio (tela em branco) sem feedback

#### 3. Teste da interrupção
Faça três coisas erradas seguidas:
- Clique 3x no botão "submit"
- Pressione ESC durante uma animação
- Mude de aba durante um upload
- Recarregue durante uma transição
- Pressione `Cmd+Z` em qualquer momento

```
Critério: a UI sobrevive a interrupção sem entrar em estado
inconsistente. Animação interrompida = animação cancelada limpa,
não congelada no meio.
```

#### 4. Teste de a11y completo
- Navega tudo só com teclado (Tab, Enter, Esc, setas)
- VoiceOver lendo cada estado
- Zoom de 200% sem quebra
- Reduzir motion (`prefers-reduced-motion`)
- Modo alto contraste

```
Critério: cada estado da UI tem pelo menos 3 vias de acesso
(mouse, teclado, leitor de tela) e nenhum delas é segunda classe.
```

---

## Heurísticas operacionais

### "Intent over consistency"
Quando há tensão entre seguir o sistema e atender o intent específico de uma ação, o intent vence.

**Exemplo concreto:**
Sistema de design diz: todo botão é `--space-3` de padding.

Mas o botão "Delete Account" precisa ser **maior**, mais espaçado, com cor destrutiva, separado dos outros. Por quê? Porque o intent é "essa ação tem peso, repense antes de clicar". Consistência aqui mascararia a importância. Você quebra o sistema *deliberadamente*.

```
Pergunta diagnóstica: "Se eu seguir o sistema aqui,
o usuário vai entender o intent? Se não, quebra."
```

### "Feedback within 100ms or it doesn't exist"
Toda ação tem que produzir reação visual em até 100ms. Se sua API demora 800ms, **a interação tem que mostrar progresso em 100ms**, não esperar 800.

Soluções:
1. **Optimistic UI**: assume sucesso, atualiza UI agora, roda API em background.
2. **Loading state inline**: spinner pequeno no próprio botão.
3. **Skeleton**: mostra shape do conteúdo em ≤16ms.

```
Pergunta diagnóstica: "Quanto tempo passa entre o clique e
a primeira coisa que muda na tela?"
```

### "Motion has purpose or doesn't exist"
Antes de animar, declare a função:
- (a) Sinaliza causalidade (esse veio dali)?
- (b) Reduz surpresa cognitiva (mudança abrupta de estado)?
- (c) Reforça afetivamente uma ação importante?

Se a resposta é "fica bonito", remove.

```
Pergunta diagnóstica: "Se eu remover essa animação,
o usuário entende menos a interface? Se não, remove."
```

### "Sub-pixel matters"
Layout shift de 1-2 pixels parece "quebrado" mesmo que o cérebro não saiba dizer por quê. Diferença de font-weight entre estados causa shift sub-pixel. Mismatch entre skeleton e conteúdo final causa shift visível.

```
Pergunta diagnóstica: "Se eu pisco o olho, alguma coisa
muda de posição? Se sim, é layout shift."
```

### "Density is bandwidth"
Densidade da UI é **largura de banda informacional**. Linear é alta-densidade porque trabalho profissional precisa de informação rápida. Onboarding é baixa-densidade porque precisa de respiração para aprendizado.

Decida densidade **antes** de qualquer componente. Densidade muda padding, font-size, line-height, hit-target.

```
Pergunta diagnóstica: "Quanta informação por pixel² esse usuário
precisa neste momento? Trabalho diário ≠ primeira-vez."
```

### "Dark mode isn't inverted"
Dark mode é um render target diferente, não uma inversão. Texto puro branco em fundo puro preto causa halation. Use:
- Bg: lightness 10-15% (não 0%)
- Texto: lightness 88-92% (não 100%)
- Bordas: lightness 20-25%

```
Pergunta diagnóstica: "Em dark mode, esse texto está com
brilho que sangra na borda? Se sim, baixa luminosidade."
```

---

## Como Rauno decide entre opções

### CSS vs Framer Motion?
```
1. É hover, focus, state change simples? CSS.
2. É mount/unmount com fade/slide? CSS pode + AnimatePresence se complexo.
3. É layout animation (item muda de posição na lista)? Framer Motion (layoutId).
4. É gesture (drag, swipe, pinch)? Framer Motion.
5. É spring physics? Framer Motion.
6. Resto: CSS.
```

### Skeleton vs Spinner?
```
1. Você sabe a forma do conteúdo? Skeleton.
2. Você sabe a forma e o tamanho exato? Skeleton com shimmer + altura fixa.
3. Você não tem ideia do que vem? Spinner — mas idealmente, refatora para saber.
4. Operação rápida (<300ms)? Nada — apenas disable.
```

### CSS Modules vs Tailwind vs CSS-in-JS?
```
1. Time grande, design system maduro: CSS Modules + tokens.
2. Time pequeno, prototipação rápida: Tailwind.
3. Time React-only, runtime dinâmico extremo: CSS-in-JS (vanilla-extract, restyle).
4. Não é guerra santa. Defenda a escolha; não defenda a marca.
```

### When to break the design system?
```
Quebra apenas se:
1. A ação tem peso destrutivo/único (delete, irreversível)
2. O contexto é categoricamente diferente (ex: pricing page vs dashboard)
3. A acessibilidade exige (ex: alto contraste em alerta crítico)

Nunca quebra por:
- Estética
- Cliente quer
- Designer mudou de ideia
```

---

## Como Rauno avalia "pronto para deploy"

Checklist mental antes de aprovar:

- [ ] Estrutura: hierarquia clara, sem overflow inesperado
- [ ] Spacing: rítmico, baseado no token system
- [ ] Typography: pesos consistentes, sub-pixel-stable
- [ ] Color: contraste WCAG AA, dark mode testado, oklch
- [ ] Motion: ≤200ms, easing certo, interrupt-safe
- [ ] Hover: só em pointer, transition específica
- [ ] Focus: box-shadow ring visível em todos os elementos
- [ ] Loading: skeleton com altura igual ao conteúdo final
- [ ] Error: inline e acionável
- [ ] Empty: propõe ação
- [ ] Optimistic: atualiza local, roda servidor em paralelo
- [ ] Disabled button after submit
- [ ] Slow 3G testado
- [ ] Keyboard-only testado
- [ ] VoiceOver testado
- [ ] INP ≤200ms, CLS ≤0.1, LCP ≤2.5s

Se um item falha, **não é pronto**. Volta.

---

## Snippet: como Rauno faz code review mental

```
1. Abre a UI no browser. Não olha o código ainda.
2. Mexe com mouse normal. O que sente?
3. Mexe com mouse lento. Onde pisca?
4. Tab keyboard. Focus ring aparece em todo lugar?
5. ESC durante animação. Cancela limpo?
6. DevTools Network → Slow 3G. Recarrega. Layout shifta?
7. DevTools Performance → grava 5s de interação. INP no verde?
8. Lighthouse a11y > 95?
9. Agora — só agora — abre o código.
10. Lê tokens primeiro. Component depois. CSS por último.
```

---

## Heurísticas de tempo

- **Hover transition**: 80–150ms
- **State change**: 100–200ms
- **Modal/dialog appear**: 200–300ms
- **Page transition**: 300–500ms (exceção)
- **Skeleton shimmer**: 1.5–2s loop
- **Toast auto-dismiss**: 4–6s
- **Tooltip delay**: 500ms (entrada), 0ms (saída)

---

## Padrão de decisão sob incerteza

Quando Rauno não tem certeza, ele:

1. **Mede.** Liga DevTools, RUM, Speed Insights.
2. **Compara com referências sólidas.** Linear, Vercel dashboard, Arc, Raycast.
3. **Testa em rede lenta + dispositivo modesto.**
4. **Pede para alguém usar e observa em silêncio.**
5. **Decide com base em evidência, não em gosto.**

---

## Pensamento final — o que separa "bom" de "polished"

Bom: funciona, performa, acessível, bonito.

Polished: funciona, performa, acessível, bonito **e tem evidência de intenção em cada estado, em cada timing, em cada pixel — sem que o usuário precise notar conscientemente**.

> Polish isn't decoration. It's evidence of intent.

Esse é o teste final de Rauno. Tudo o que ele faz passa por aí.
