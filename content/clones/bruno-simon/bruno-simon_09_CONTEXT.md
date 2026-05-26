---
name: Bruno Simon — Contexto Histórico
description: Linha do tempo da web 3D — WebGL → Three.js → R3F → era Vision Pro
type: clone-knowledge
clone: bruno-simon
---

# Contexto Histórico — Onde Bruno se posiciona

> Sem contexto histórico, a importância do Bruno fica invisível. Ele entrou no jogo em momento específico e deslocou um ponto fixo do ecossistema.

---

## 2010-2014 — A pré-história do 3D na web

WebGL foi padronizado em 2011 (Khronos Group). Era marginal — só rodava em desktop, exigia drivers OK, e a API crua era brutal: `gl.bufferData`, `gl.vertexAttribPointer`, `gl.drawElements`. Quem queria 3D no browser tinha que dominar OpenGL puro.

**Mr.doob (Ricardo Cabello)** lançou o **Three.js em 2010**, antes mesmo de WebGL ser padrão (rodava sobre canvas 2D inicialmente). Three.js virou a abstração que tornou WebGL escrevível por mortais — `Mesh`, `Camera`, `Scene` em vez de matriz de transformação na unha.

Nesse período, sites 3D eram raridade absoluta — algum protótipo no Mr.doob's Lab, alguma demo no Chrome Experiments. Para a web mainstream, 3D era curiosidade.

---

## 2015-2018 — A onda das agências criativas

Estúdios franceses (**Immersive Garden**, **Active Theory**, **Resn**) começam a usar Three.js em sites de marca de luxo — automotivo, moda, brinquedo. Awwwards e FWA criam categorias de Site of the Day premiando trabalhos com WebGL como diferencial.

Bruno está dentro desse movimento, como **lead developer da Immersive Garden**. Está ensinando WebGL/Three em programas franceses pós-graduação. Acumula expertise em silêncio. A community Three.js é pequena ainda — fórum oficial, alguns canais no Slack, alguns blog posts dispersos.

Recursos de aprendizado: zero estruturado. Dev tinha que cavar nos exemplos do GitHub do Three, traduzir tutoriais antigos do Mr.doob, ler livros (Lewis Lepton, Alan Anderson). Nada de curso decente.

---

## 2019 — bruno-simon.com explode

Bruno publica o portfólio dirigível em novembro de 2019. Awwwards Site of the Month, depois Site of the Year. **100M+ views cumulativos** segundo a FWA. Reddit r/webdev, Hacker News, Twitter — viralidade orgânica que devs raramente conseguem.

O significado: o **portfolio funciona como prova viva** de que Three.js é acessível, divertido e capaz de virar **identidade pessoal de um dev**. Antes do bruno-simon.com, ninguém conhecia "Bruno Simon". Depois dele, virou nome.

Crucial: **não é decoração 3D**. Cada elemento do site faz sentido — o carrinho leva você a sections reais (projects, contact). É funcional. Isso vira a tese: 3D na web só vale se for funcional.

---

## 2020-2022 — Three.js Journey nasce e cresce

Bruno larga agência. Lança o curso. Recebe demanda violenta de devs do mundo inteiro pedindo "como você fez aquilo". O curso é didático no sentido sério da palavra — começa do absoluto zero (o que é uma scene, o que é um mesh) e leva o aluno a fazer cenas próprias.

Em paralelo, **Paul Henschel (drcmda)** publica **React Three Fiber** (2019, mas atinge tração em 2020-2021). React + Three.js declarativo. O ecossistema **pmndrs** (Poimandres) cresce em volta — drei (helpers), react-spring (animação), zustand (state), jotai. R3F vira o padrão moderno de Three.js em React.

Bruno atualiza o curso para incluir **um capítulo R3F substancial** — lições 53+. Reconhece a importância de R3F sem abandonar Three.js puro. Esse equilíbrio é parte do porquê o curso é referência: cobre as duas culturas.

---

## 2023-2024 — Era pós-pandemia, AR/VR, Apple Vision Pro

Apple lança Vision Pro em 2024. **WebXR** ganha tração lenta mas real. Microsoft empurra **Babylon.js** como alternativa. Google empurra **model-viewer** como solução low-code. Mas Three.js continua sendo o padrão de fato.

Three.js ganha versionamento mais formal (r150+, r160+). API estabiliza. **TSL (Three Shading Language)** começa a ser explorada — uma forma de escrever shaders em JS que se compilam pra GLSL ou WGSL (WebGPU).

**WebGPU** começa a desembarcar em browsers (Chrome estável, Safari/Firefox em progresso). É o sucessor lógico de WebGL — mais moderno, paralelismo melhor, computação em GPU. Three.js já tem `WebGPURenderer` experimental. Bruno cobre superficialmente, espera maturar mais.

3D na web vira mainstream:
- **Configuradores de produto** em e-commerce (carros Tesla, sapatos Nike, móveis IKEA)
- **Walkthroughs imersivos** de imóveis e empreendimentos
- **Hero scenes** em landing pages premium (Linear, Stripe Showcase, agências)
- **Experiências de marca** em campanhas (Christmas micro-sites, lançamentos)

---

## 2025-2026 — Onde estamos agora

WebGPU está chegando ao tier 1 — Chrome desktop estável, Safari 18+, mobile próximo. Three.js já roda em WebGPU com perda mínima de performance.

**TSL** (Three Shading Language) ganha tração para escrever shaders sem GLSL bruto, com hot reload e melhor DX. Bruno está experimentando, ainda não é capítulo principal do curso.

**R3F v9+** estabilizado, ecossistema pmndrs maduro com dezenas de pacotes.

**Vision Pro** popularizou expectativas de imersão no consumidor médio — algumas marcas começam a fazer apps WebXR.

3D na web está no inflexão **mainstream**:
- Toda agência de design top tem alguém com Three.js no time
- Recrutadores filtram por "fez Three.js Journey"
- Cursos paralelos surgem (especialmente focados em R3F), mas o de Bruno permanece **referência canônica**

Bruno mantém o curso vivo — atualiza com TypeScript, adiciona capítulos, expande Discord. Faz raros projetos client-side. Continua sendo a figura central de uma comunidade que ele próprio formou.

---

## Onde Bruno está posicionado nesse mapa

- **Não é o pioneiro** da web 3D — Mr.doob, Patricio Gonzalez Vivo, Inigo Quilez vieram antes
- **Não é o cara dos efeitos malucos hardcore** — esse é o akella, ou o Inigo
- **Não é o líder do framework** — esse é o drcmda (R3F)
- **É o professor** — o que tornou a tecnologia ensinável, copiável, acessível

O legado de Bruno não é "ter feito o site de carrinho" — é **ter aberto a porta para uma geração de devs entrarem em web 3D sem se afogar na complexidade da API**. Ele democratizou Three.js da mesma forma que Wes Bos democratizou JavaScript moderno e Sarah Drasner democratizou Vue + animation.

Para o squad o negócio do usuário: Bruno representa **expertise técnica acessível e cautelosa**. Ele entra quando a peça pede 3D real, e ele sai (ou não entra) quando a peça pede só decoração — porque ele sabe o custo do que recomenda.
