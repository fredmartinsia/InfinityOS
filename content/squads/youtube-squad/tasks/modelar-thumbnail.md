---
task: modelarThumbnail()
responsavel: "@paddy-galloway"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: tema_episodio
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: nicho
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: convidado
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: dossie_modelagem
    tipo: file
    destino: squads/youtube-squad/output/{episodio}-thumbnail-modelagem.md
    persistido: true

Checklist:
  - "[ ] 10-15 referencias por mercado (BR + USA + PT) com links reais validados"
  - "[ ] Regras de modelagem extraidas com casos (5+) por regra"
  - "[ ] Conceito de thumbnail amarrado as regras (R1-R10)"
  - "[ ] Ranking de frases por potencial de CTR"
  - "[ ] Plano de teste A/B (Thumb A x Thumb B) com riscos e mitigacao"
---

# Task: Modelar Thumbnail

**Task ID:** YT-STR-01
**Version:** 1.0.0
**Command:** `*modelar-thumbnail`
**Agent:** Paddy Galloway (paddy-galloway) e Matt Gielen (matt-gielen), com apoio de @youtube-researcher na coleta
**Purpose:** Antes de desenhar qualquer thumbnail, validar referencias reais (BR + USA + PT) que JA funcionaram no nicho, extrair regras de modelagem dos vencedores e propor conceito mais plano A/B. Produz o dossie de modelagem que serve de base para `*prompt-thumbnail` e `*frases-thumbnail`. Replica fielmente o que foi feito no EP001.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| tema_episodio | string | User prompt | Yes | Tema central do episodio e identificador `{episodio}` (ex: infinity-cast-ep002) |
| nicho | string | User prompt | Yes | Nicho de cruzamento (ex: fe + negocios, financas pessoais, tecnologia + IA) |
| convidado | string | User prompt | No | Nome e enquadramento do convidado, quando houver |
| canal | string | User prompt | No | Canal alvo ({{USER_NAME}} ou Infinity Cast); define mercado primario PT/BR |
| frames_disponiveis | path | Pipeline (`*extrair-frames`) | No | Banco de frames HERO ja validado para amarrar o conceito |
| dores_mapeadas | path | `*analisar-conteudo` | No | content-map.md com dores cruzadas para alinhar copy das frases |

---

## Preconditions

- Tema e nicho do episodio claramente definidos
- Acesso a web ao vivo (researcher) para levantar referencias com links reais; nenhuma referencia pode ser citada de memoria
- Mercado primario do canal identificado (Infinity Cast e {{USER_NAME}} operam Portugal/Brasil)
- Se houver frames ja extraidos, eles devem estar disponiveis para amarrar o conceito a frames reais

---

## Champion Reference

Estude estas referencias reais (validadas no EP001, com links) antes de modelar. Sao a prova de que o padrao funciona no nicho fe + negocios cruzando os 3 mercados:

1. **Deive Leonardo, "Ter Dinheiro e Pecado ou Nao?"** (https://www.youtube.com/watch?v=nkf7OiTrH7k), 1 rosto, luz dramatica, pergunta-tabu pura. Canal de 10,3 mi inscritos. Prova de que pergunta-tabu sobre dinheiro performa no nicho fe.
2. **Diary of a CEO, Mo Gawdat sobre IA** (https://www.youtube.com/watch?v=RwlgFC6S-OE), 1 rosto, fundo escuro, numero de choque ("3 YEARS"). Prova de CTR alto do angulo IA + futuro.
3. **Ed Mylett e Joe Dispenza, "Unlock the Power of Your Mind"** (https://www.youtube.com/@EdMylett), 2 rostos, fundo escuro com glow quente, 1 palavra destacada. 2,4 mi views (top do canal). Template entrevista de alto CTR.
4. **Jota Jota #024, "POR QUE TER FE?" (Tiago Brunet)** (https://www.youtube.com/watch?v=WdHJgvHItMA), 2 rostos, fundo escuro, pergunta-tabu curta como headline. Benchmark BR do nicho fe.
5. **45 Graus (Jose Maria Pimentel)** (https://www.youtube.com/@45_graus), sobrio/editorial, 1 rosto, fundo neutro, numero do ep. Premio Podes 2022. Referencia do tom PT sobrio que precisa ser respeitado na calibracao cross-cultural.

---

## Execution Phases

### Phase 1: Levantamento de Referencias (@youtube-researcher, web ao vivo)
1. Levantar 10-15 thumbnails de referencia POR MERCADO, totalizando os 3 blocos: Brasil, USA/UK, Portugal/EU.
2. Para cada referencia registrar: canal/video, link real (URL), layout observado (numero de rostos, fundo, palavra destacada, cor de marca, numero/quantificacao).
3. Aplicar os filtros do briefing cross-cultural: BR 100k+ inscritos ativos nos ultimos 12 meses; USA 500k+ ativos; PT/EU os 3 melhores do idioma alvo, mesmo que o nicho seja incipiente.
4. Anotar metricas de prova quando disponiveis (views do video, inscritos do canal) com a fonte. Ser honesto sobre limitacoes: se a view por video nao for confirmavel ao vivo, citar a fonte externa (agregador) e marcar como direcional.
5. Identificar a referencia PT mais proxima do nicho (mesmo que sobria/generica) para servir de baliza de calibracao.

### Phase 2: Extracao de Regras (@matt-gielen)
1. Extrair as regras recorrentes dos vencedores, cada regra sustentada por 5+ casos das referencias coletadas. As regras-base do nicho entrevista business/fe (confirmadas no EP001) sao o ponto de partida:
   - **R1 Fundo escuro domina** (preto/charcoal).
   - **R2 Dois rostos** = formato entrevista de alto CTR (host + convidado).
   - **R3 Expressao intensa**, nunca neutra; olhos dirigidos.
   - **R4 Uma palavra destacada** em cor de contraste (substantivo-gatilho).
   - **R5 Cor de marca = assinatura**; mapear qual cor esta LIVRE no cruzamento do nicho.
   - **R6 Numero/quantificacao** aumenta CTR.
   - **R7 Copy de pergunta-tabu / curiosity gap**.
2. Adicionar regras de calibracao cross-cultural a partir do briefing:
   - **R8 Cross-cultural PT:** estilo BR e diferenciador em PT (nao saturado), MAS risco de soar clickbait/exploratorio; preferir paleta premium e expressao de autoridade serena.
   - **R9 Anti-padrao** observado no nicho (ex: caixa + seta vermelha sinaliza news/drama, nao premium) a ser evitado.
   - **R10 Angulo inexplorado** (gap de cobertura): apontar o que BR/USA ja fazem e PT/EU ainda nao, como trunfo de ineditismo.
3. Para cada regra, escrever a coluna "Aplicacao ao episodio": como ela se traduz no conceito concreto deste tema/convidado.

### Phase 3: Conceito e Plano A/B (@paddy-galloway)
1. Definir o **layout final** amarrado as regras (cada decisao referenciando a regra que a justifica): fundo, posicao dos rostos, glow/iluminacao, expressoes, texto, numero, anti-padroes evitados.
2. Indicar os **frames recomendados** do banco validado (principal e variacao contextual), quando houver frames extraidos.
3. Produzir um **ranking de frases** por potencial de CTR. Criterio: curiosity gap + palavra-gatilho + brevidade + alinhamento as dores + diferenciacao, menos risco de soar exploratorio. Marcar a palavra que vai em cor de contraste com colchetes, ex: `E PECADO [PROSPERAR]?`.
4. Montar o **plano de teste A/B**:
   - **Thumb A** = curiosidade-tabu, maximo CTR (frase mais agressiva + frame de maior expressao).
   - **Thumb B** = autoridade/metodo, lead qualificado (numero/produto + frame de conviccao); serve de fallback seguro se A soar agressiva demais para o publico PT.
   - Definir como rodar o teste (YouTube Test & Compare se elegivel, ou troca manual em 48h comparando CTR/retencao).
5. Listar **riscos e mitigacao** (ex: tom teologia da prosperidade em PT: usar pergunta, nunca afirmacao; nao usar conteudo sensivel como isca de clique).

---

## Output Format

Arquivo: `squads/youtube-squad/output/{episodio}-thumbnail-modelagem.md` (mesmo formato do dossie EP001).

```markdown
# Dossie de Modelagem, Thumbnail {Canal} {Episodio} ({Convidado})

> YouTube Squad - Sessao de thumbnail - Canal: {canal}
> Pipeline: Researcher (web ao vivo, BR + USA + PT) -> Matt Gielen (modelagem) -> Paddy Galloway (conceito) -> Chief (sintese)
> Regra cumprida: thumbnail so foi ao Paddy depois de referencias reais com links.

---

## 1. Referencias modeladas (Researcher, web ao vivo, com links reais)

### Brasil
| Canal / Video | Link | Layout |
|---|---|---|
| {canal/video} | {url} | {n rostos, fundo, palavra, cor, numero} |

### USA / UK
| Canal / Video | Link | Layout |
|---|---|---|
| {canal/video} | {url} | {layout} |

### Portugal / EU
| Canal / Video | Link | Layout |
|---|---|---|
| {canal/video} | {url} | {layout} |

> Limitacao honesta: {o que nao foi confirmavel ao vivo e qual a fonte das metricas citadas}

---

## 2. Regras modeladas (Matt Gielen, padroes dos vencedores)

| # | Regra | Casos (5+) | Aplicacao ao episodio |
|---|-------|-----------|----------------------|
| R1 | Fundo escuro domina | {casos} | {aplicacao} |
| ... | ... | ... | ... |
| R10 | Angulo inexplorado | {gap} | {trunfo} |

---

## 3. Comment mining, dores cruzadas (BR + USA + PT)

{lista priorizada das dores mais recorrentes nos 3 mercados, com fonte/direcionalidade}

---

## 4. Conceito de thumbnail validado (Paddy Galloway)

**Layout final (amarrado as regras):**
- {decisao} [R#]
- ...

**Frames recomendados (do banco validado):**
- Principal: {frame}
- Variacao contextual: {frame}

---

## 5. Ranking das frases por potencial de CTR (Paddy Galloway)

| Rank | Frase | Por que |
|------|-------|---------|
| 1 | `FRASE [PALAVRA]` | {justificativa} |
| ... | ... | ... |

---

## 6. Plano de teste A/B

- **Thumb A (curiosidade-tabu, maximo CTR):** {frames} + frase {frase A} + {detalhes}
- **Thumb B (autoridade/metodo, lead qualificado):** {frames} + frase {frase B} + {numero em destaque}
- Como rodar: {Test & Compare ou troca manual 48h, metricas comparadas}

**Riscos / mitigacao:**
- {risco} -> {mitigacao}
```

---

## Veto Conditions

- NEVER planejar ou desenhar thumbnail sem referencias validadas com links reais (a regra #2 do squad: thumbnail so vai ao conceito depois das referencias com URL)
- NEVER citar referencia de memoria; toda referencia precisa de link clicavel coletado ao vivo
- NEVER inventar metricas (views/inscritos); se nao confirmavel, marcar como direcional e citar a fonte (sem achismo sem dados)
- NEVER fechar conceito sem extrair pelo menos R1-R7 com 5+ casos cada
- NEVER pular o plano A/B nem omitir riscos de calibracao cross-cultural (tom exploratorio em PT)
- NEVER usar travessao (em dash) em nenhum texto do dossie; identidade visual sua comunidade = laranja sobre preto

---

## Completion Criteria

- [ ] 10-15 referencias coletadas POR mercado (BR + USA + PT) com links reais validados
- [ ] Layout de cada referencia registrado (rostos, fundo, palavra, cor, numero)
- [ ] Limitacoes de confirmacao de metricas declaradas com a fonte
- [ ] Regras de modelagem extraidas (R1-R7 base + R8-R10 cross-cultural), cada uma com 5+ casos
- [ ] Coluna "Aplicacao ao episodio" preenchida por regra
- [ ] Dores cruzadas dos 3 mercados mapeadas e priorizadas
- [ ] Conceito de thumbnail amarrado as regras, com frames recomendados quando houver
- [ ] Ranking de frases por potencial de CTR com a palavra-gatilho destacada em colchetes
- [ ] Plano de teste A/B (Thumb A x Thumb B) definido, com metodo de rodar o teste
- [ ] Riscos e mitigacao listados (foco no tom PT)
- [ ] Dossie salvo em `squads/youtube-squad/output/{episodio}-thumbnail-modelagem.md` no formato do EP001
