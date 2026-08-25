---
task: planoMonetizacao()
responsavel: "@roberto-blake"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: canal_dados
    tipo: object
    origem: User Input ou diagnostico de canal
    obrigatorio: true
  - campo: audiencia
    tipo: object
    origem: User Input ou data/analytics
    obrigatorio: true
  - campo: oferta_atual
    tipo: object
    origem: User Input
    obrigatorio: false

Saida:
  - campo: plano_monetizacao
    tipo: file
    destino: output_dir/estrategia/plano-monetizacao.md
    persistido: true

Checklist:
  - "[ ] Dados reais do canal coletados antes de qualquer recomendacao"
  - "[ ] Fontes de receita aplicaveis mapeadas (AdSense, afiliados, infoprodutos, brand deals)"
  - "[ ] Cada fonte priorizada por esforco x retorno com nota"
  - "[ ] Cronograma com prazos (30, 60, 90 dias e 6-12 meses)"
  - "[ ] Stack de receita montado com ordem de ativacao"
---

# Task: Plano de Monetizacao

**Task ID:** YT-STR-04
**Version:** 1.0.0
**Command:** `*plano-monetizacao`
**Agent:** Roberto Blake (roberto-blake)
**Purpose:** Construir uma estrategia de receita stackeada para os canais do sua comunidade ({{USER_NAME}} e Infinity Cast), combinando AdSense, afiliados, infoprodutos e brand deals, priorizada por esforco x retorno e organizada em um cronograma com prazos claros, sempre ancorada nos dados reais do canal e nunca em achismo.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| canal_dados | object | User Input ou `*diagnosticar-canal` | Yes | Inscritos, views/mes, RPM/CPM atual, horas assistidas, status de monetizacao (apto ou nao ao YPP) |
| audiencia | object | User Input ou data/analytics | Yes | Geografia (PT/BR), faixa etaria, intencao (curiosidade vs compra), nivel de confianca no criador |
| oferta_atual | object | User Input | No | Produtos, servicos ou mentorias ja existentes do {{USER_NAME}}/sua comunidade que possam ser ofertados ao publico |
| canal | enum | `episodio.yaml` ou User Input | No | `{{USER_NAME}}` ou `Infinity Cast`; muda o mix de receita ideal |
| mercado | enum | User Input | No | `Portugal`, `Brasil` ou `PT/BR`; afeta RPM, parceiros de afiliados e poder de compra |
| meta_receita | string | User Input | No | Objetivo declarado (ex.: primeira receita, R$/EUR mensal alvo, prazo) |

---

## Preconditions

- Dados reais do canal disponiveis: no minimo inscritos, views/mes e status de monetizacao. Sem esses dados, a task NAO recomenda.
- Perfil da audiencia conhecido (geografia e intencao), porque ele define quais fontes de receita convertem.
- Clareza sobre se o canal ja esta apto ao YouTube Partner Program (afeta se AdSense entra agora ou depois).
- Se houver `oferta_atual`, ela esta descrita o suficiente para estimar ticket e margem.

---

## Referencia de Modelos

Estude estes modelos de monetizacao stackeada antes de montar o plano. A logica e sempre a mesma: empilhar fontes que somam sem competir, comecando pelas de menor esforco e maior previsibilidade e subindo para as de maior retorno por espectador.

1. **AdSense (base passiva):** receita por mil views (RPM). Baixo esforco depois do YPP, mas RPM em PT/BR e modesto. Serve de piso, nunca de teto. Cresce com volume de views, nao com esforco extra por video.
2. **Afiliados (primeira camada ativa):** comissao por indicacao de ferramentas e produtos que o publico ja usaria. Esforco baixo a medio (links, mencoes honestas), retorno proporcional a confianca da audiencia. Ideal como segunda fonte porque nao exige produto proprio.
3. **Brand deals / patrocinio (escala por autoridade):** marca paga por insercao ou episodio patrocinado. Retorno alto por entrega, mas depende de audiencia qualificada e media kit. Esforco de prospeccao e negociacao. Entra quando o canal tem numeros que justificam um valor de tabela.
4. **Infoproduto / mentoria (maior retorno por espectador):** curso, comunidade ou mentoria do proprio {{USER_NAME}}/sua comunidade. Maior esforco de criacao, maior margem e maior retorno por espectador convertido. E o topo do stack porque transforma audiencia em cliente direto, sem intermediario.
5. **Stack combinado (o objetivo):** os quatro rodando juntos, cada um cobrindo uma faixa de intencao do publico (assiste de graca, clica afiliado, ve patrocinio, compra oferta). Diversificacao reduz dependencia do RPM do YouTube e protege a receita de mudancas de algoritmo.

---

## Execution Phases

### Phase 1: Mapear Fontes de Receita Aplicaveis
1. Coletar e registrar os dados reais do canal: inscritos, views/mes, RPM/CPM atual (se monetizado), horas assistidas, status no YPP, mercado dominante (PT/BR) e perfil da audiencia.
2. Para cada uma das quatro fontes (AdSense, afiliados, infoprodutos, brand deals), decidir **aplicabilidade agora**:
   - **AdSense:** aplicavel apenas se o canal ja atingiu os requisitos do YPP. Se nao atingiu, marcar como "futuro" e estimar quando (com base no ritmo de inscritos/horas).
   - **Afiliados:** aplicavel em quase qualquer estagio, desde que existam produtos/ferramentas relevantes e que a audiencia confie no criador.
   - **Brand deals:** aplicavel quando ha audiencia qualificada e numeros suficientes para um media kit. Se ainda nao, marcar como "futuro" com gatilho (ex.: ao atingir X views/mes).
   - **Infoprodutos:** aplicavel se ha (ou da para criar) uma oferta do {{USER_NAME}}/sua comunidade que resolva uma dor do publico. Usar `oferta_atual` quando existir.
3. Para cada fonte aplicavel, estimar o **potencial de receita** com base nos dados (nao em medias genericas da internet): ex.: AdSense = views/mes x RPM do mercado; afiliados = views x taxa de clique x comissao plausivel; infoproduto = audiencia x taxa de conversao conservadora x ticket.
4. Descartar explicitamente fontes que nao se aplicam ainda e registrar o porque (transparencia para o {{USER_NAME}} decidir).

### Phase 2: Priorizar por Esforco x Retorno
1. Pontuar cada fonte aplicavel em duas dimensoes (1 a 5):
   - **Esforco:** quanto tempo/recurso ate a primeira receita (1 = baixissimo, 5 = altissimo).
   - **Retorno:** potencial de receita e margem para esta audiencia (1 = marginal, 5 = transformador).
2. Calcular a prioridade: preferir alto retorno com baixo esforco primeiro (quick wins), depois alto retorno com alto esforco (apostas), deixando baixo retorno por ultimo.
3. Classificar cada fonte em uma faixa de ativacao:
   - **Ativar agora:** quick wins aplicaveis com os dados atuais.
   - **Construir em paralelo:** exige preparo (media kit, oferta), mas ja deve comecar.
   - **Aguardar gatilho:** depende de marco do canal (YPP, X views/mes); registrar o gatilho exato.
4. Garantir que o resultado e um **stack** e nao uma fonte unica: a recomendacao final empilha pelo menos duas fontes ativas e mapeia o caminho ate as demais.

### Phase 3: Cronograma com Prazos
1. Distribuir as fontes priorizadas em um cronograma com janelas claras:
   - **0-30 dias:** o que ativar imediatamente (quick wins, primeiros links de afiliado, configuracao de AdSense se apto).
   - **30-60 dias:** o que construir (media kit para brand deals, esboco de oferta/infoproduto, parcerias de afiliado).
   - **60-90 dias:** primeiras vendas/insercoes da camada de maior retorno (infoproduto piloto, primeiro brand deal).
   - **6-12 meses:** stack completo rodando e otimizacao (escalar a fonte de melhor retorno por espectador).
2. Para cada janela, definir **acao concreta**, **responsavel** ({{USER_NAME}}, equipe ou agente do squad) e **metrica de sucesso** (ex.: primeiro EUR/R$ de afiliado, media kit pronto, taxa de conversao do piloto).
3. Marcar os **gatilhos de progressao**: o que precisa ser verdade para passar de uma fase para a proxima (ex.: "so prospectar brand deal apos atingir X views/mes").
4. Fechar com uma recomendacao de foco unica: dada a realidade atual do canal, qual a UMA fonte que merece mais energia agora, para o {{USER_NAME}} nao se dispersar.

---

## Output Format

Escrever em `output_dir/estrategia/plano-monetizacao.md`:

```markdown
# Plano de Monetizacao

**Canal:** {{{USER_NAME}} | Infinity Cast}
**Mercado:** {Portugal | Brasil | PT/BR}
**Meta de receita:** {meta declarada ou "nao definida"}

## Dados do Canal (base da recomendacao)

- Inscritos: {N}
- Views/mes: {N}
- RPM/CPM atual: {valor ou "nao monetizado"}
- Status YPP: {apto | nao apto | estimativa de quando}
- Audiencia: {geografia, intencao, nivel de confianca}

## Fontes Mapeadas

| Fonte | Aplicavel agora? | Potencial estimado | Base do calculo |
|-------|------------------|--------------------|-----------------|
| AdSense | {sim/futuro} | {valor} | {views x RPM} |
| Afiliados | {sim/futuro} | {valor} | {views x CTR x comissao} |
| Brand deals | {sim/futuro} | {valor} | {numeros do media kit} |
| Infoproduto/mentoria | {sim/futuro} | {valor} | {audiencia x conversao x ticket} |

## Priorizacao (Esforco x Retorno)

| Fonte | Esforco (1-5) | Retorno (1-5) | Faixa | Justificativa |
|-------|---------------|---------------|-------|---------------|
| {fonte} | X | X | {ativar agora / construir / aguardar gatilho} | {por que} |

## Stack Recomendado

> {Quais fontes empilhar e em que ordem de ativacao, e por que somam sem competir.}

## Cronograma

### 0-30 dias
- Acao: {...} | Responsavel: {...} | Sucesso: {...}

### 30-60 dias
- Acao: {...} | Responsavel: {...} | Sucesso: {...}

### 60-90 dias
- Acao: {...} | Responsavel: {...} | Sucesso: {...}

### 6-12 meses
- Acao: {...} | Responsavel: {...} | Sucesso: {...}

## Gatilhos de Progressao

- {O que precisa ser verdade para avancar de fase}

## Foco Unico Agora

> {A UMA fonte que merece mais energia hoje, dada a realidade atual do canal, com o porque.}
```

---

## Veto Conditions

- NEVER fazer qualquer recomendacao de monetizacao sem os dados reais do canal (inscritos, views, status de monetizacao). Sem dados, parar e pedir os dados.
- NEVER inventar RPM, taxas de conversao ou comissoes: usar numeros plausiveis e declarar a base de cada estimativa.
- NEVER recomendar AdSense como fonte ativa para um canal que ainda nao atingiu o YPP; marcar como futuro com prazo.
- NEVER entregar fonte unica quando o objetivo e um stack: o plano precisa empilhar pelo menos duas fontes ativas.
- NEVER ignorar a diferenca de mercado (PT vs BR) no calculo de RPM, parceiros de afiliados e poder de compra.
- NEVER recomendar infoproduto que contradiga a identidade do criador ou ofereca algo que o publico nao confia que o {{USER_NAME}} entrega.
- NEVER usar travessao (em dash, o traco longo) em nenhuma parte deste arquivo; usar dois-pontos, parenteses, virgula ou reescrever.

---

## Completion Criteria

- [ ] Dados reais do canal coletados e registrados antes de qualquer recomendacao
- [ ] As quatro fontes (AdSense, afiliados, infoprodutos, brand deals) avaliadas quanto a aplicabilidade agora
- [ ] Potencial de cada fonte estimado com a base de calculo declarada
- [ ] Cada fonte priorizada por esforco x retorno com nota (1-5) e justificativa
- [ ] Cada fonte classificada em faixa de ativacao (ativar agora / construir / aguardar gatilho)
- [ ] Stack recomendado com ordem de ativacao e por que as fontes somam sem competir
- [ ] Cronograma preenchido nas janelas 0-30, 30-60, 60-90 dias e 6-12 meses, com acao, responsavel e metrica
- [ ] Gatilhos de progressao entre fases registrados
- [ ] Foco unico agora declarado, ancorado na realidade do canal
- [ ] Arquivo salvo em `output_dir/estrategia/plano-monetizacao.md` no formato do template
- [ ] Sem travessao e em portugues do Brasil
