# Checklist: Output Quality

> Critérios de qualidade para qualquer entrega do `frontend-squad`. Cada item é PASS / FAIL / NA. Nada é entregue ao usuário sem rodar este checklist.

## Performance

- [ ] **LCP (Largest Contentful Paint)** < 2.5s em mobile mid-tier
- [ ] **INP (Interaction to Next Paint)** < 200ms em interações típicas
- [ ] **CLS (Cumulative Layout Shift)** < 0.1
- [ ] **Lighthouse Performance** ≥ 90 (LP), ≥ 88 (site institucional com 3D), ≥ 92 (SaaS sem hero pesado)
- [ ] **Bundle JS inicial** < 250KB gzipped (sem 3D); < 500KB (com 3D)
- [ ] Imagens em formato moderno (WebP/AVIF) com fallback se necessário
- [ ] Imagens com `loading="lazy"` (exceto hero) e `width`/`height` definidos
- [ ] Fontes carregadas com `font-display: swap` ou `optional`
- [ ] Sem requests bloqueantes no critical path

## Acessibilidade

- [ ] **axe-core** zero violations críticas (WCAG AA)
- [ ] **Contraste de cor** ≥ 4.5:1 para texto normal, ≥ 3:1 para texto grande, em TODOS os estados (default, hover, focus, disabled)
- [ ] **Keyboard navigation** completa: Tab funciona em ordem visual, Enter ativa botões/links, Esc fecha modais
- [ ] **Focus visible** em todos os elementos interativos (não removido com `outline: none` sem substituto)
- [ ] **Skip links** em sites multi-página
- [ ] **Headings hierarchy** lógica (h1 único, h2 → h3 sem pulos)
- [ ] **ARIA labels** em ícones-botões sem texto
- [ ] **ARIA live** para mensagens dinâmicas (toast, errors em form)
- [ ] **prefers-reduced-motion** respeitado: animações simplificadas ou removidas
- [ ] **Screen reader test** em pelo menos uma tela (VoiceOver / NVDA)

## Design system fidelity

- [ ] **Zero hex inline** — toda cor referencia token do design system
- [ ] **Zero pixel mágico** — espacamentos via tokens (`--space-1`, `--space-2`...)
- [ ] **Tipografia** usa apenas as fontes definidas no design system
- [ ] **Componentes base** (Button, Input, Card) consumidos do design system, não recriados
- [ ] **Dark mode** (se design system suporta) funciona sem flash, persiste entre páginas
- [ ] **Tokens semânticos** usados (color-bg-surface) em vez de tokens primitivos (gray-100)

## Código

- [ ] **TypeScript strict** ativado e sem erros
- [ ] **Sem console.log** ou TODO em código entregue
- [ ] **Sem código morto** (componentes não usados, imports não usados)
- [ ] **Componentes** com props tipadas e uma responsabilidade clara
- [ ] **Server components** onde não precisa interatividade (Next.js)
- [ ] **Client components** apenas onde estritamente necessário
- [ ] **Cleanup de side effects** em useEffect (event listeners, timers, ScrollTrigger)
- [ ] **Imports organizados** (externos → internos → tipos)

## Responsividade

- [ ] **Mobile (375px)** funcional e polido
- [ ] **Tablet (768px)** funcional
- [ ] **Desktop (1280-1920px)** polido
- [ ] **Wide (>1920px)** não quebra (max-width definido onde precisa)
- [ ] **Sem scroll horizontal** acidental em nenhuma viewport
- [ ] **Touch targets** ≥ 44x44px no mobile

## Estados visuais

Para cada elemento interativo:
- [ ] **Default state** definido
- [ ] **Hover state** com transição em < 100ms (desktop)
- [ ] **Focus state** visível e diferente de hover
- [ ] **Active/pressed state** com feedback tátil-visual
- [ ] **Loading state** (se ação é assíncrona) com skeleton ou spinner contextual
- [ ] **Disabled state** com contraste ≥ 3:1
- [ ] **Error state** com mensagem clara e cor + ícone (não só cor)
- [ ] **Empty state** para listas/queries vazias com CTA ou explicação

## SEO básico

- [ ] **`<title>`** descritivo e único por página
- [ ] **`<meta name="description">`** entre 120-160 caracteres
- [ ] **Open Graph tags** (og:title, og:description, og:image) presentes
- [ ] **Imagens com `alt`** descritivo (ou `alt=""` para decorativas)
- [ ] **Sitemap.xml** se site multi-página
- [ ] **Schema.org markup** onde fizer sentido (Organization, Product, FAQPage)

## Análise final

- [ ] **Top 3 forças** do output documentadas em `report.md`
- [ ] **Top 3 limitações conhecidas** documentadas em `report.md`
- [ ] **Próximos passos** sugeridos em `report.md`
- [ ] **Performance budget vs medido** documentado

## Veredito

- ✅ **PRONTO** — todos os críticos PASS, máximo 3 NA justificadas
- ⚠️ **PRONTO COM RESSALVAS** — máximo 5 FAIL não-críticos, com plano de correção
- ❌ **NÃO PRONTO** — críticos com FAIL ou ≥ 6 não-críticos com FAIL

Critérios críticos (FAIL aqui = não pronto):
- LCP, INP, CLS dentro de threshold
- axe sem violations críticas
- Keyboard nav funciona
- prefers-reduced-motion respeitado
- Zero hex inline (design system fidelity)
- Sem console.log/TODO
