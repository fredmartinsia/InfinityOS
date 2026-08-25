---
task: planejamentoMensal()
responsavel: "@youtube-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: canal
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: frequencia
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: temas_semente
    tipo: string
    origem: User Input
    obrigatorio: false

Saida:
  - campo: calendario_mensal
    tipo: markdown
    destino: produtos/{canal}/planejamento/calendario-{mes}.md
    persistido: true

Checklist:
  - "[ ] Briefing rapido respondido (frequencia, eventos do mes, videos prontos)"
  - "[ ] 20-30 temas candidatos pesquisados antes da selecao final"
  - "[ ] Cada slot tem formato validado com 5+ casos comprovados (link + canal + views)"
  - "[ ] Cada slot tem titulo + descricao SEO/GEO + thumbnail conceitual"
  - "[ ] Mix balanceado (magnet + engajamento + conversao)"
  - "[ ] Calendario completo do mes (cada video modelado)"
---

# Task: Planejamento Mensal

**Task ID:** YT-STR-06
**Version:** 1.0.0
**Command:** `*planejamento-mensal`
**Agent:** @youtube-chief (orquestra @youtube-researcher, @matt-gielen, @derral-eves, @brian-dean)
**Purpose:** Produzir o calendario de conteudo do mes inteiro, onde cada video sai modelado: tema validado, formato com 5+ casos comprovados, titulo, descricao SEO/GEO e thumbnail conceitual. Nenhum slot entra no calendario sem formato validado.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| canal | string | User prompt | Yes | Canal alvo: {{USER_NAME}} (individual) ou Infinity Cast (podcast). Nicho e regiao (PT/BR) carregados da memoria |
| frequencia | string | User prompt | Yes | Videos por semana (ex: 1/sem, 2/sem). Define o total de slots = videos/semana x 4 |
| temas_semente | string | User prompt | No | Temas ou eventos que o {{USER_NAME}} ja quer cobrir no mes (lancamento, sazonalidade, data importante) |
| videos_prontos | string | User prompt | No | Videos ja gravados ou parcialmente prontos a encaixar no calendario |
| formato_novo | string | User prompt | No | Se o {{USER_NAME}} quer testar formato novo ou manter o primario validado |

---

## Preconditions

- Consultoria inicial do canal ja realizada (formato primario definido em sessao anterior)
- Perfil do canal alvo carregado em memoria (`_memory/memories.md`, tag `canal:`)
- Contexto do projeto lido: `_opensquad/_memory/company.md` e `brand/guidelines/brand-map.md`
- Aprendizados de meses anteriores consultados antes de propor o mix
- Identidade sua comunidade confirmada para thumbnails: laranja sobre preto

---

## Champion Reference

Estude estes padroes de calendario antes de montar (modelagem cross-cultural BR + USA validando o que faz sentido em PT/EU):

1. **Mix magnet + engajamento + conversao** (modelo Derral Eves, The YouTube Formula), todo mes precisa de videos de alta busca organica (puxam tráfego novo) somados a videos de community building e a pelo menos um video com CTA direto para produto ou lead
2. **Modelagem por tema, nao por canal** (Matt Gielen, Little Monster Media), para cada tema, achar 3+ canais que ja fizeram esse assunto e bater 100k+ views, e copiar a estrutura, nao inventar
3. **Title-thumbnail como par** (Paddy Galloway), o conceito de thumbnail e o titulo nascem juntos, nunca como peca isolada
4. **SEO + GEO por video** (Brian Dean, Backlinko), cada slot leva keyword principal, secundarias e descricao que o YouTube e os motores generativos conseguem ler
5. **Slot ancora vs slot de apoio**: distinguir o video carro-chefe do mes (potencial outlier, 10x baseline) dos videos de manutencao de ritmo, para alocar esforco de producao com criterio

---

## Execution Phases

### Phase 1: Briefing Rapido (@youtube-chief)
1. Perguntar ao {{USER_NAME}}, antes de qualquer pesquisa:
   - Quantos videos consegue publicar por semana?
   - Tem tema ou evento especifico do mes que faz sentido cobrir? (lancamento, sazonalidade, data)
   - Tem algum video ja gravado ou parcialmente pronto?
   - Quer testar formato novo ou manter o primario validado?
   - Algum topico que esta com vontade de fazer agora?
2. Calcular o total de slots: videos por semana x 4 semanas
3. Confirmar o plano antes de acionar o squad (sequencia + estimativa + entregavel)

### Phase 2: Pesquisa de Pauta (@youtube-researcher)
1. Trends do nicho nos ultimos 90 dias (Google Trends + YouTube)
2. Top videos do nicho nos ultimos 30 dias (o que esta viralizando agora, BR/USA/PT)
3. Comment mining cross-platform: top 20-30 duvidas, dores e desejos do publico (YouTube + Instagram + Reddit + Quora)
4. Pesquisa sazonal: datas e eventos do mes relevantes para o nicho e para a regiao alvo
5. Perguntas quentes no Reddit/Quora do nicho
6. Posts virais em IG/X/LinkedIn (discussoes do momento)
7. Entregar lista de 20-30 temas candidatos ranqueados por: volume de busca, engajamento em comentarios, frequencia de pergunta no Reddit/Quora, validacao em outros canais

### Phase 3: Modelagem de Formato (@matt-gielen)
1. Selecionar os temas finalistas (igual ao total de slots calculado na Phase 1)
2. Para cada tema finalista, identificar o formato vencedor com **5+ casos comprovados** (link + canal + view count), priorizando referencias BR e USA que ainda nao chegaram a PT/EU
3. Definir estrutura recomendada por slot: duracao, segmentacao, padrao de hook que funcionou no tema, stakes que sustentaram retencao
4. Mapear o estilo de thumbnail dos top videos de cada tema (insumo para o conceito visual)
5. Marcar claramente qualquer formato sem 5+ casos como hipotese de teste, nao como slot validado

### Phase 4: Validacao Estrategica (@derral-eves)
1. Conferir se o mix esta balanceado: educativo + entretenimento + conversao
2. Garantir presenca de videos magnet (alta busca organica) e de videos de engajamento (community building)
3. Avaliar se a frequencia proposta e sustentavel dada a capacidade declarada
4. Sinalizar videos com potencial de outlier (10x baseline) e quais sao ancora vs apoio
5. Marcar quais videos podem virar ads depois (sinalizar para envolver @tom-breeze no fim do mes)

### Phase 5: SEO/GEO por Video (@brian-dean)
Para cada slot do calendario, entregar:
1. Titulo principal + 2 alternativas A/B
2. Descricao completa com SEO + GEO + CTA + links da gravacao
3. Keyword principal + 5 secundarias
4. Tags relevantes
5. Capitulos do YouTube quando aplicavel

### Phase 6: Sintese e Calendario (@youtube-chief)
1. Montar a tabela do calendario com um slot por data: tema, formato validado, titulo, descricao (resumo + link para a descricao completa), thumbnail conceitual, estrutura, referencias modeladas
2. Confirmar que **todo slot** carrega formato validado (5+ casos) ou esta marcado como hipotese de teste com justificativa
3. Definir o plano de execucao por semana (que video em cada semana, com seu papel: magnet, teste, engajamento, conversao)
4. Listar metricas a monitorar e agendar a revisao de fim de mes
5. Rodar o gate `checklists/output-quality.md` antes de entregar
6. Persistir o calendario e os aprendizados em `_memory/memories.md` (tag `canal:`)

---

## Output Format

```markdown
## Calendario Mensal de Conteudo

**Canal:** {canal}
**Mes:** {mes/ano}
**Frequencia:** {videos/semana} ({total} slots)
**Mix alvo:** {X magnet / Y engajamento / Z conversao}

### Calendario (um slot por data)

| Semana | Data | Tema | Formato validado (5+ casos) | Titulo | Descricao SEO/GEO | Thumbnail conceitual | Estrutura | Referencias modeladas | Papel |
|--------|------|------|-----------------------------|--------|-------------------|----------------------|-----------|-----------------------|-------|
| 1 | YYYY-MM-DD | {tema} | {formato} + [5 links: canal/views] | "{titulo}" | {keyword + resumo + link descricao} | {visual, laranja sobre preto} | {hook + corpo + CTA} | {3+ links} | magnet |
| 1 | YYYY-MM-DD | ... | ... | ... | ... | ... | ... | ... | engajamento |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Plano de Execucao por Semana
- **Semana 1:** {video(s)} -> {papel: puxar tráfego novo / magnet}
- **Semana 2:** {video(s)} -> {papel: teste de formato ou conteudo de autoridade}
- **Semana 3:** {video(s)} -> {papel: engajamento / conversa com a community}
- **Semana 4:** {video(s)} -> {papel: conversao / CTA direto para produto ou lead}

### Videos Ancora vs Apoio
- **Ancora (potencial outlier):** {video}, {justificativa baseada em modelagem}
- **Apoio (manutencao de ritmo):** {videos}

### Candidatos a Ads (fim do mes)
- {video} -> sinalizar @tom-breeze

### Metricas a Monitorar
- CTR medio (alvo: 5-10%)
- AVD vs duracao media (alvo: acima de 50%)
- Inscritos novos por video
- Comentarios (qualidade, nao so quantidade)

### Proxima Sessao
- Revisao de performance no fim do mes
- Ajustes no calendario do mes seguinte
```

---

## Veto Conditions

- NEVER colocar um slot no calendario sem formato validado com 5+ casos comprovados (ou explicitamente marcado como hipotese de teste)
- NEVER usar travessao (em dash) em titulo, descricao, thumbnail ou qualquer parte do calendario
- NEVER montar o calendario sem pesquisa previa (20-30 temas candidatos) feita pelo @youtube-researcher
- NEVER fechar o mes so com videos magnet: tem que haver mix (engajamento + conversao)
- NEVER propor frequencia acima da capacidade declarada pelo {{USER_NAME}} no briefing
- NEVER entregar slot sem o pacote completo: tema + formato + titulo + descricao SEO/GEO + thumbnail conceitual
- NEVER basear selecao de tema em achismo sem dados de busca, comentarios ou validacao em outros canais
- NEVER usar identidade visual fora do padrao sua comunidade (laranja sobre preto) nos conceitos de thumbnail

---

## Completion Criteria

- [ ] Briefing rapido respondido (frequencia, eventos, videos prontos, formato novo ou primario)
- [ ] 20-30 temas candidatos pesquisados e ranqueados antes da selecao final
- [ ] Cada slot do calendario tem formato validado com 5+ casos (link + canal + view count) ou marcado como hipotese de teste
- [ ] Cada slot entrega titulo + 2 alternativas A/B
- [ ] Cada slot entrega descricao completa com SEO + GEO + CTA + links
- [ ] Cada slot entrega keyword principal + 5 secundarias e tags
- [ ] Cada slot entrega thumbnail conceitual (descricao visual, laranja sobre preto)
- [ ] Cada slot tem 3+ referencias modeladas com link
- [ ] Mix balanceado validado (magnet + engajamento + conversao)
- [ ] Frequencia confirmada como sustentavel dada a capacidade declarada
- [ ] Videos ancora vs apoio identificados; candidatos a ads sinalizados
- [ ] Calendario completo do mes (cada video modelado), tabela por data
- [ ] Gate `checklists/output-quality.md` aprovado
- [ ] Aprendizados persistidos em `_memory/memories.md` (tag `canal:`)
- [ ] Nenhum travessao em todo o output
