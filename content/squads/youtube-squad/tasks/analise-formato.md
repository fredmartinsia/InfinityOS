---
task: analiseFormato()
responsavel: "@matt-gielen"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: formato_proposto
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: nicho
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: regiao
    tipo: enum
    origem: User Input
    obrigatorio: true

Saida:
  - campo: analise_formato
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Scan de canais do nicho concluido (@youtube-researcher)"
  - "[ ] Casos do formato identificados com metricas reais (@matt-gielen)"
  - "[ ] Veredito vai/nao-vai emitido com fundamento data-driven"
  - "[ ] 5+ casos comprovados com links (ou alternativa apresentada)"
---

# Task: Analise de Formato

**Task ID:** YT-STR-03
**Version:** 1.0.0
**Command:** `*analise-formato`
**Agent:** Matt Gielen (matt-gielen)
**Purpose:** Validar, com dados e nao com achismo, se um formato proposto funciona em canais semelhantes. Entregar veredito vai/nao-vai sustentado por 5 ou mais casos comprovados com links, ou uma alternativa modelada quando o formato nao se sustentar.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| formato_proposto | string | User prompt | Yes | Descricao clara do formato (estrutura, duracao, estilo, ex: "lista top 10 com narracao", "entrevista longa de podcast", "reacao a noticias") |
| nicho | string | User prompt | Yes | Nicho ou tema do canal (ex: empreendedorismo, financas pessoais, tecnologia) |
| regiao | enum | User prompt | Yes | BR, PT, USA, ou cross-cultural (BR+USA -> PT/EU) |
| canal_referencia | string | User prompt | No | Canal alvo do sua comunidade ({{USER_NAME}}, Infinity Cast) ou outro |
| objetivo | string | User prompt | No | Meta do formato (retencao, alcance, autoridade, conversao) |
| restricoes | string | User prompt | No | Limites de producao (orcamento, equipe, frequencia, equipamentos) |

---

## Preconditions

- Formato proposto descrito de forma concreta (nao basta "um video legal"; precisa de estrutura identificavel)
- Nicho definido o suficiente para o scan localizar canais comparaveis
- Regiao escolhida; se for cross-cultural, o scan deve cobrir BR e USA como referencia para projetar em PT/EU
- Pesquisa previa obrigatoria: nenhum veredito sai sem o scan do `@youtube-researcher` (premissa inegociavel do squad: nada comeca em estrategia sem passar por pesquisa)

---

## Casos de Referencia (modelagem)

Use estes formatos comprovados como ancora mental antes de avaliar o formato proposto. Cada um carrega uma logica de retencao distinta:

1. **Lista ranqueada com payoff progressivo** (top N, contagem regressiva), segura retencao porque o espectador espera o item 1; funciona em nichos de curiosidade e consumo
2. **Entrevista/podcast longo com clipes derivados**: autoridade e tempo de sessao alto; o video longo alimenta cortes verticais que puxam alcance de volta
3. **Reacao/comentario sobre evento atual**: surfa picos de busca (timing); validade curta, mas pico de impressao alto
4. **Tutorial/how-to com resultado tangivel**: search-friendly e durabilidade (cauda longa de SEO); retencao depende do payoff no inicio
5. **Documentario/narrativa de caso (storytelling)**: retencao por arco; alto custo de producao, alto teto de viralizacao
6. **Vlog/bastidores de autoridade**: relacao e recorrencia; depende de personagem ja conhecido, fraco para canal novo

Cada caso tem um perfil de risco: o que retem em um nicho pode afundar em outro. A modelagem so vale quando os casos sao do MESMO nicho e regiao comparavel.

---

## Execution Phases

### Phase 1: Scan de Canais do Nicho (@youtube-researcher)
1. Mapear de 8 a 15 canais ativos no nicho informado, priorizando os que crescem nos ultimos 12 meses (nao apenas os gigantes ja consolidados)
2. Para regiao cross-cultural, montar dois conjuntos: canais BR e canais USA do mesmo nicho, para depois projetar a leitura em PT/EU
3. Para cada canal, registrar: nome, link, faixa de inscritos, frequencia de publicacao e formatos dominantes que usa
4. Marcar quais desses canais ja usam (ou ja testaram) o formato proposto
5. Entregar a lista bruta de candidatos ao `@matt-gielen`, sem julgar ainda (separar coleta de analise)

### Phase 2: Identificacao de Casos com Metricas (@matt-gielen)
1. A partir do scan, isolar videos especificos que usam o formato proposto (nao basta o canal usar; precisa do video concreto com link)
2. Para cada caso, coletar e registrar metricas observaveis: views, data de publicacao, inscritos do canal na epoca, e a razao views/inscritos (proxy de outlier)
3. Classificar cada caso como: outlier (views muito acima da media do canal), na media, ou fracasso (abaixo da media)
4. Buscar minimo de 5 casos validados (outliers ou consistentes) do MESMO nicho; se a regiao for cross-cultural, casos BR e USA contam, desde que projetaveis para PT/EU
5. Cruzar com o `data/formatos-validados.yaml` do squad: o formato ja consta como validado? Os casos novos confirmam ou contradizem o registro?
6. Registrar o contra-exemplo quando existir (formato que falhou em canal comparavel), isso fortalece o veredito, nao enfraquece

### Phase 3: Veredito (@matt-gielen) + Sintese (@youtube-chief)
1. Emitir o veredito com base na contagem e na qualidade dos casos:
   - **VAI**: 5 ou mais casos validados no nicho/regiao, com pelo menos 2 outliers; formato comprovadamente replicavel
   - **VAI COM AJUSTE**: formato funciona, mas exige adaptacao (duracao, gancho, frequencia) para o canal/regiao do sua comunidade; descrever o ajuste
   - **NAO-VAI**: menos de 5 casos validados, ou casos so existem em contexto nao replicavel (canal gigante, nicho diferente); apresentar alternativa
2. Quando NAO-VAI: apresentar 1 formato alternativo modelado, tambem com 5 casos comprovados, que entrega o mesmo objetivo do formato proposto
3. Aplicar leitura cross-cultural: o que os casos BR/USA indicam sobre o comportamento esperado em PT/EU (audiencia, ritmo, referencias culturais)
4. Listar riscos de producao e condicoes para o formato funcionar no canal alvo
5. `@youtube-chief` sintetiza e fecha a recomendacao final para o {{USER_NAME}}

---

## Output Format

```markdown
## Analise de Formato, Veredito

**Formato proposto:** {formato_proposto}
**Nicho:** {nicho}
**Regiao:** {regiao}
**Canal alvo:** {canal_referencia}

### Veredito: {VAI | VAI COM AJUSTE | NAO-VAI}

**Fundamento (1 linha):** {por que, ancorado nos dados}

### Casos Comprovados ({contagem} de 5+)

| # | Canal | Video (link) | Views | Inscritos (epoca) | Views/Insc | Classe | Regiao |
|---|-------|--------------|-------|-------------------|-----------|--------|--------|
| 1 | {canal} | {link} | {views} | {insc} | {ratio} | outlier/media/fracasso | BR/USA/PT |
| 2 | ... | ... | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... | ... | ... |

### Contra-exemplo (se existir)
{caso em que o formato falhou em canal comparavel + link + por que falhou}

### Leitura Cross-Cultural (BR/USA -> PT/EU)
{o que os casos indicam sobre o comportamento esperado da audiencia PT/EU}

### Ajuste recomendado (se VAI COM AJUSTE)
{duracao, gancho, frequencia, ou estrutura a adaptar para o canal alvo}

### Alternativa modelada (somente se NAO-VAI)
**Formato alternativo:** {nome}
**Por que entrega o mesmo objetivo:** {justificativa}
| # | Canal | Video (link) | Views | Views/Insc | Regiao |
|---|-------|--------------|-------|-----------|--------|
| 1 | ... | ... | ... | ... | ... |
... (5 casos)

### Riscos e Condicoes de Producao
- {risco/condicao 1}
- {risco/condicao 2}

### Recomendacao final (@youtube-chief)
{1 paragrafo de sintese acionavel}
```

---

## Veto Conditions

- NEVER aprovar um formato (veredito VAI) sem 5 casos validados com links verificaveis; menos de 5 casos so permite NAO-VAI com alternativa
- NEVER emitir veredito sem o scan previo do `@youtube-researcher`, pesquisa primeiro, analise depois
- NEVER tratar como caso valido um video sem link ou sem metrica observavel; achismo nao entra
- NEVER usar caso de canal gigante (alcance movido por marca, nao por formato) como prova de que o formato funciona para canal em crescimento
- NEVER projetar BR/USA -> PT/EU sem registrar a logica cross-cultural; nao basta copiar o numero
- NEVER usar travessao (em dash) em nenhuma parte do output; use ponto, virgula, dois-pontos ou parenteses
- NEVER entregar veredito NAO-VAI sem uma alternativa modelada (com seus proprios 5 casos)

---

## Completion Criteria

- [ ] Scan de canais do nicho concluido com 8 a 15 candidatos listados (`@youtube-researcher`)
- [ ] Casos do formato isolados em videos especificos, cada um com link
- [ ] Metricas observaveis coletadas por caso (views, inscritos, razao views/inscritos, classe)
- [ ] Veredito emitido: VAI, VAI COM AJUSTE, ou NAO-VAI, com fundamento data-driven
- [ ] 5 ou mais casos comprovados anexados ao veredito (ou alternativa modelada com seus 5 casos)
- [ ] Leitura cross-cultural BR/USA -> PT/EU aplicada quando a regiao exigir
- [ ] Cruzamento com `data/formatos-validados.yaml` registrado (confirma ou contradiz)
- [ ] Riscos e condicoes de producao listados
- [ ] Sintese final do `@youtube-chief` entregue
- [ ] Output formatado conforme o template, sem travessao
