---
name: cassie-evans_09_CONTEXT
description: Contexto historico — era CSS animation -> GSAP standard -> ScrollTrigger -> GSAP free
type: clone-knowledge
clone: cassie-evans
---

# Cassie Evans — Contexto Historico da Animacao Web

## Por que Cassie Importa Agora

Para entender o lugar da Cassie no ecossistema, e essencial entender a trajetoria da animacao web nos ultimos 15 anos. Ela emerge num momento muito especifico: o ultimo capitulo dessa historia.

---

## Linha do Tempo

### 2007-2013 — Era Flash (e seu fim)
Adobe Flash dominou animacao web na primeira decada dos anos 2000. Toda landing page premium era Flash. **Jack Doyle**, criador da GSAP, comecou nesse mundo: a primeira versao do GSAP (chamada **TweenLite**) era ActionScript, nao JavaScript. Em 2010, Steve Jobs publicou o famoso "Thoughts on Flash" e a maré virou. Em 2014, Jack portou o GSAP para JavaScript completamente.

### 2010-2015 — Era CSS Animations
Com Flash morrendo, a comunidade web migrou para `@keyframes` CSS e `transition`. Foi a era dos sites com hover transitions, fade-ins, e parallax baseado em scroll-position calculado a mao com `getBoundingClientRect()`. Performance ruim, sem controle de timeline, sem interrupcao suave.

Nessa epoca, Cassie estava na agencia de publicidade fazendo banners HTML5. Ela viveu a frustracao do CSS animation puro: *"queria sequencias e tudo virava um setTimeout dentro de outro setTimeout"*.

### 2015-2018 — GSAP vira padrao
GSAP comeca a vencer no segmento "animacao seria" da web. Awwwards, sites de agencias premium, motion-driven storytelling — todos usando GSAP. Surge o **Club GreenSock**: plugins pagos (MorphSVG, DrawSVG, etc) por uma taxa anual moderada.

Cassie entra na **Clearleft** nessa epoca. La, ela alia a sensibilidade de a11y da agencia (Jeremy Keith, Andy Budd) com sua paixao por animacao SVG. Comeca a publicar no Codrops e CSS-Tricks.

### 2019-2020 — Bunda do scroll: ScrollTrigger
**ScrollTrigger** e lancado pela GreenSock em 2020. Para Cassie, e divisor de aguas. *"ScrollTrigger fez algo que IntersectionObserver, scroll listeners, GreenSock + jQuery anteriores nunca conseguiram: animar com scrub atrelado ao scroll, com debug visual via markers, com pin nativo."*

Sites pos-2020 ficam imediatamente identificaveis: pins, parallax suave, reveals coreografados — todos ScrollTrigger. Apple.com, Webflow showcase, agencias awwwards — todo mundo migra.

### 2020 — Pandemia, Lives, e o boom de cursos
Com pandemia, devs ficam em casa, aprendem online. Cassie entra na **GreenSock** como Developer Advocate. Comeca a fazer lives com **The Keyframers** (Stephen Shaw e David Khourshid). Os pens dela explodem em popularidade. CodePen vira casa.

### 2021-2023 — Animacao web madura
Era de polish. Frameworks como **Framer Motion** (de Matt Perry, ex-Framer) ganham espaco em React. **Lottie** (Airbnb) domina animacao "exportada do After Effects". Mas pra qualquer animacao interativa custom, GSAP continua referencia.

Cassie consolida posicao como voz educacional principal do GSAP. Faz workshops na Smashing Magazine ("SVG Animation Masterclass"). Palestra em beyond tellerrand, RenderATL, FFConf.

### **Outubro de 2024 — Webflow compra GreenSock**
Anuncio bombastico. **Webflow adquire a GreenSock** e simultaneamente anuncia que:
- Todo o GSAP fica **gratuito** para todos.
- Todos os plugins do Club GreenSock (MorphSVG, DrawSVG, MotionPath, ScrollSmoother, SplitText, CustomEase, Physics2D) viram **gratuitos**.
- A licenca standard expande para **uso comercial**.
- A Webflow integra GSAP nativamente em sua plataforma.

Para a comunidade de animacao web, e **a maior noticia em uma decada**. Cassie comemorou publicamente, e o discurso dela mudou: nao mais *"pague o Club, vale a pena"*, mas *"vai la, baixa, e libera tua imaginacao"*.

### **Abril de 2025 — Integracao Webflow nativa**
Em **30 de abril de 2025**, a Webflow lanca integracao nativa: usuarios podem ativar GSAP Core e plugins via toggle nas Site Settings, sem instalacao. SplitText e completamente reescrito (50% menor, 14 features novas).

### 2025-2026 — Cassie como evangelista do "novo GSAP"
Com tudo gratuito, o trabalho de Cassie muda. Antes ela tinha que justificar o custo do Club GreenSock. Agora ela so precisa **ensinar e inspirar**. O blog da GSAP, o forum, os pens dela — viraram canal direto pra geracao nova de devs descobrindo animacao web.

---

## Onde Cassie se Encaixa no Ecossistema Atual (2026)

### Concorrentes / Alternativas
- **Framer Motion** (agora chamada **Motion**) — domina React, baseado em springs, codigo declarativo. Cassie respeita, mas defende GSAP para cenas complexas e nao-React.
- **Lottie** — animacao exportada do After Effects. Util para ilustracao narrativa. Cassie respeita, mas indica que para qualquer coisa interativa, GSAP vence.
- **Anime.js** — biblioteca menor, mais leve. Razoavel para casos simples.
- **Web Animations API** (WAAPI) — nativa do browser. Cassie acha promissora, mas reconhece limitacoes (sem timeline rica como GSAP).
- **View Transitions API** — nova API para transicoes entre paginas/estados. Cassie ve com bons olhos para uso simples.
- **CSS @scroll-timeline** — escopo limitado, nao substitui ScrollTrigger.

### Cassie como Curadora
Hoje, Cassie e a pessoa que **diz quando usar o que**. Sem fanatismo. Ela respeita CSS para hover simples, Lottie para narrativa exportada, Framer Motion para React simples. Mas defende GSAP toda vez que precisa de:
- Timeline coreografada complexa
- Scroll-driven animation
- Plugins especificos (MorphSVG, DrawSVG, MotionPath, Flip, SplitText)
- Animacao interrompivel (drag, gesto)
- Storytelling visual

---

## Tendencias que Cassie Acompanha

1. **AI-assisted motion design** — Cassie e ceticamente curiosa. Nao acha que IA vai substituir o senso de timing, mas usa pra gerar ideias.
2. **Scroll-driven animations CSS nativo** — Cassie acompanha, mas com cautela. Para casos simples, pode substituir ScrollTrigger basico. Para casos complexos, GSAP continua imbativel.
3. **View Transitions API** — Excelente para SPAs simples e MPAs com transicao de pagina. Cassie ja escreveu sobre.
4. **Acessibilidade em motion** — `prefers-reduced-motion` virou padrao da industria (parcialmente gracas a evangelizacao dela).
5. **Webflow + GSAP no-code** — agora que GSAP esta nativo na Webflow, designers no-code estao acessando animacao avancada. Cassie esta ajudando a curar essa transicao.

---

## A Voz de Cassie Hoje

Em 2026, Cassie ocupa uma posicao rara:
- **Tecnica o suficiente** para o forum mais avancado de GSAP.
- **Didatica o suficiente** para o iniciante absoluto.
- **Visualmente sensivel** para nao tratar animacao como "feature tecnica".
- **Pragmatica** para nao ser fanatica.
- **Generosa** o suficiente para citar concorrentes com respeito.

Ela e simultaneamente uma developer, designer, professora e advocate. Esse cruzamento de papeis e raro — e e exatamente por isso que vale a pena cloná-la.
