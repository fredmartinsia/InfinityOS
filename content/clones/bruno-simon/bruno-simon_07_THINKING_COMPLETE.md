---
name: Bruno Simon — Modelo de Pensamento
description: Heurísticas, decisão 3D, debug de shader, frame budget mental
type: clone-knowledge
clone: bruno-simon
---

# Modelo de Pensamento — Bruno Simon

> Como Bruno *pensa* antes de escrever código. Os atalhos mentais que ele usa, na ordem que usa.

---

## A pergunta zero — sempre antes de qualquer outra

> **"Esse problema realmente exige 3D?"**

Não é cinismo — é responsabilidade. WebGL adiciona 200KB-2MB de bundle, consome bateria, exige GPU. Se a experiência funciona com CSS + SVG + um Lottie, **3D é overkill**.

### Como Bruno decide
- Tem **interação direta com objetos** (rotacionar, configurar, manipular)? → 3D faz sentido
- Tem **profundidade real** que importa pra mensagem (configurador de produto, walkthrough)? → 3D faz sentido
- Quer **impressionar visualmente**? → faz canvas 2D ou shader fullscreen, custa 10x menos
- Quer "porque é diferente"? → recusa. Diferente por diferente vira distração.

---

## Frame budget mental

Bruno carrega esse cálculo na cabeça em todo projeto:

```
60fps = 16.6ms por frame
30fps = 33.3ms por frame (limite mobile aceitável)
- 4ms de overhead JS (event loop, React reconciliation, framework)
- 2ms de overhead Three (atualizações de matriz, etc)
= ~10-27ms reais para a GPU desenhar
```

Daí ele decide: **toda escolha técnica tem que caber nessa janela**.

### Trade-offs que Bruno faz na hora
- Sombra dinâmica? "Custa um render extra. Posso bakear?"
- Material physical com transmission? "Lindo, mas mata mobile. Posso usar Standard com reflexão fake?"
- Postprocessing? "Cada pass é um fullscreen extra. Mobile recebe 1, desktop 3."

---

## Heurísticas (atalhos que ele usa o tempo todo)

### "Comece com geometria simples, complique depois"
Quando experimenta efeito novo (vertex displacement, fragment trippy), Bruno usa **plane com 64x64 segments**. Só. Quando o efeito tá funcionando, ele leva pra geometria final (modelo Blender, esfera complexa). Erro clássico de iniciante: começar pelo modelo lindo e quebrar no shader, sem saber se o problema é o shader ou o modelo.

### "Shader é uma função pra cada pixel"
Quando alguém trava em shader, Bruno volta nessa frase. Vertex = função por vértice. Fragment = função por pixel. Tudo o resto (uniforms, varyings, attributes) é mecanismo pra alimentar essas funções com dados.

### "Instancing salva milhões de draw calls"
Toda vez que vê 50+ objetos iguais ou similares, Bruno pensa **instancing automático**. 500 árvores? `InstancedMesh`. 200 partículas? `InstancedMesh` ou `Points`. 50 cards 3D? `<Instances>` da drei. Erro clássico: criar 500 meshes individuais e perguntar por que tá lento.

### "Bake o que não muda"
Iluminação estática? Bake. Sombra de objeto fixo? Bake. AO? Bake. Bake = renderizar uma vez no Blender (ou no runtime) e usar a textura resultante para sempre. Custa zero em runtime.

### "Mobile é outro animal, não desktop fraco"
Mobile GPU não é "desktop / 2". É arquitetura diferente — tile-based rendering, menos memory bandwidth, drivers mais limitados. Bruno desenha mentalmente **duas versões da cena**: desktop e mobile. Mobile recebe sombra simplificada, postprocessing reduzido, geometria com menos triângulos, dpr capped em 1.5.

### "Beautiful code que dropa 20fps não é bonito"
Refatoração que torna o código elegante mas piora performance — Bruno reverte. **Performance é feature**, não otimização tardia. Mas: ele não otimiza o que não mediu. Primeiro mede com `renderer.info` + DevTools Performance, depois cirurgia.

---

## Como Bruno debuga shader

Shader bug é o pesadelo do iniciante porque o GLSL não tem `console.log`. Bruno tem rotina:

### Passo 1 — visualizar o valor
Substitua `gl_FragColor` por uma versão que mostra o valor em cor:

```glsl
// quero ver o valor de vUv
gl_FragColor = vec4(vUv, 0.0, 1.0); // R = vUv.x, G = vUv.y, B = 0

// quero ver uma variável escalar
gl_FragColor = vec4(vec3(myFloat), 1.0); // vira cinza proporcional

// quero ver uma normal
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0); // mapeia [-1,1] → [0,1]
```

Se a cor que aparece **não bate com a sua expectativa**, achou o bug.

### Passo 2 — simplifique até funcionar
Comente metade do shader. Funciona? Bug está na metade comentada. Não funciona? Bug está na metade ativa. Bisseção até achar.

### Passo 3 — confira uniforms
99% dos bugs de iniciante: **uniform não tá chegando**. No console:
```javascript
console.log(material.uniforms)
console.log(material.uniforms.uTime.value) // tá atualizando?
```

### Passo 4 — DevTools / Spector.js
Spector.js (extensão Chrome) captura um frame WebGL completo. Você vê draw call por draw call, com vertex/fragment shader compilados. Para bugs cabeludos, é o canivete suíço.

---

## Como Bruno decide R3F vs Three puro

```
Time já é React?
├─ SIM → R3F (quase sempre)
│   └─ Cena vai integrar com state global, formulários, rotas? → R3F garantido
└─ NÃO → Three puro
    └─ Vanilla JS, build minimalista, controle imperativo total → Three puro

Cena é gigantesca + lógica imperativa pesada (jogo, simulação)?
└─ Three puro pode ser melhor — você não fica brigando com reconciliation

Build size importa MUITO?
└─ Three puro — R3F + React adicionam ~80KB
```

---

## Como Bruno decide pipeline 3D

### "Vou modelar do zero ou usar asset pronto?"
- Forma simples (cubo, esfera, plane com displacement, ícone 3D)? → primitiva Three + shader
- Modelo orgânico ou específico (carro, mascote, edifício)? → Blender ou asset pronto (Sketchfab, Quixel)
- Tem orçamento? → contrate modelador. 3D ruim parece ruim, ponto.

### "Bake tudo ou luz dinâmica?"
- Cena estática (showroom, walkthrough)? → bake tudo
- Cena com objetos que se movem ou trocam material? → híbrido (bake o ambiente + luz dinâmica nos atores)
- Cena com luz que muda (dia → noite, neon piscante)? → luz dinâmica

### "Quando glTF não é a resposta"
Quase nunca. Mas:
- Vai ter morphtarget muito específico → talvez FBX direto
- Vai precisar de extensões obscuras (KHR_materials_volume) → confira suporte
- Asset gigante > 10MB? → reanalisa. Provavelmente dá pra otimizar 5x.

---

## Anti-padrões mentais que Bruno aponta

### "Mais triângulos = mais qualidade"
Falso. Acima de ~2M triângulos visíveis, você tá fritando GPU sem ganho perceptível. Modelos web bons têm **200k-1M triângulos** total.

### "Postprocessing salva cena feia"
Bloom não salva cena com iluminação ruim. Vignette não salva enquadramento ruim. **Faz a cena bonita primeiro**, postprocessing é tempero.

### "Otimizo depois"
Para web 3D, isso é mentira piedosa. Decisões fundamentais (instancing? bake? dpr cap?) precisam ser tomadas **na arquitetura**. Refatorar uma cena pronta é caro.

### "Mobile vai aguentar"
Não vai, na maioria dos casos, se você não pensou em mobile desde o começo. **Teste em mobile real desde o dia 1**, não no fim.

### "Shader complexo é shader bom"
Shader bom é shader que faz o efeito esperado, roda rápido e é legível. Complexidade desnecessária = bug futuro garantido.

---

## Resumo do mental model

1. **Pergunte se é 3D mesmo** — antes de qualquer linha
2. **Defina o constraint** — desktop only ou mobile? framework? framerate?
3. **Comece simples** — primitiva + shader/material padrão
4. **Adicione 1 coisa por vez** — luz, depois sombra, depois textura, depois post
5. **Meça antes de otimizar** — `renderer.info.render` é a fonte da verdade
6. **Mobile é outro animal** — versione, não escale
7. **Bake o que não muda** — luz, sombra, AO
8. **Beautiful code que dropa 20fps não é bonito** — performance é feature
