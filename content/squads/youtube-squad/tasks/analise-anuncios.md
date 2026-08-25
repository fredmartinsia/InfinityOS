---
task: analiseAnuncios()
responsavel: "@tom-breeze"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: dados_campanhas
    tipo: file
    origem: User Input (export do Google Ads / YouTube Ads)
    obrigatorio: true
  - campo: objetivo
    tipo: enum
    origem: User Input
    obrigatorio: true

Saida:
  - campo: diagnostico_anuncios
    tipo: file
    destino: output_dir/anuncios/diagnostico-anuncios.md
    persistido: true

Checklist:
  - "[ ] Objetivo da campanha confirmado antes de analisar"
  - "[ ] Diagnostico feito por campanha/grupo a partir dos dados reais"
  - "[ ] Acoes de scaling e cutting definidas com criterio numerico"
  - "[ ] Recomendacoes de criativo e segmentacao baseadas no que os dados mostram"
  - "[ ] Nenhuma recomendacao sem dado que a sustente"
---

# Task: Analise de Anuncios

**Task ID:** YT-STR-05
**Version:** 1.0.0
**Command:** `*analise-anuncios`
**Agent:** Tom Breeze (tom-breeze)
**Purpose:** Analisar e otimizar campanhas de YouTube Ads (TrueView, In-stream e Discovery) ligadas aos canais do sua comunidade ({{USER_NAME}} e Infinity Cast), entregando um diagnostico fundamentado em dados e um plano claro do que escalar, do que cortar e do que ajustar em criativo e segmentacao para Portugal e Brasil.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| dados_campanhas | file | Export do Google Ads / YouTube Ads (CSV ou tabela colada) | Yes | Deve trazer por campanha/grupo: formato, gasto, impressoes, views, view rate, CPV, cliques, CTR, conversoes, CPA e periodo |
| objetivo | enum | User Input | Yes | `awareness`, `views`, `inscritos`, `trafego`, `leads` ou `vendas`; define qual metrica vira KPI principal |
| periodo | string | User Input | No | Janela analisada (ex.: "ultimos 30 dias"); sem ela, usar o periodo presente no export |
| orcamento | string | User Input | No | Orcamento diario/total atual e teto disponivel para scaling |
| mercado | enum | User Input | No | `Portugal`, `Brasil` ou `PT/BR`; afeta benchmarks de CPV/CPA e segmentacao |
| canal | enum | `episodio.yaml` ou User Input | No | `{{USER_NAME}}` ou `Infinity Cast`; orienta a leitura de criativo e tom |
| meta_kpi | string | User Input | No | Meta numerica do KPI (ex.: CPA alvo, CPV teto); se ausente, derivar referencia na Phase 1 |

---

## Preconditions

- O export de `dados_campanhas` existe e cobre um periodo com volume suficiente para decidir (regra pratica: cada campanha/grupo avaliado para scaling ou cutting precisa de um minimo de conversoes ou de gasto que torne o numero confiavel, nunca decidir no ruido).
- O `objetivo` da conta esta confirmado, para que a metrica certa seja tratada como KPI (ex.: em `vendas` o CPA manda; em `awareness` o CPV e o view rate mandam).
- Existe pelo menos um ponto de comparacao: meta de KPI, benchmark do mercado ou periodo anterior. Sem nenhuma referencia, a Phase 1 estabelece uma antes de julgar performance.
- Os formatos das campanhas estao identificados (TrueView in-stream, in-stream nao pulavel, In-feed/Discovery, bumper), porque cada formato tem leitura de metrica diferente.

---

## Referencia de Campeoes

Estude estes padroes de leitura de conta de YouTube Ads antes de diagnosticar. Eles separam o que e sinal real do que e ruido:

1. **Regra do gasto-antes-do-corte**: Nunca cortar um grupo antes de ele ter gasto o equivalente a 1 a 3 CPAs alvo sem converter. Cortar cedo demais mata grupos que ainda nao tiveram chance estatistica.
2. **View rate como termometro do criativo**: Em in-stream, view rate baixo (gente pulando) quase sempre acusa hook fraco nos primeiros 5 segundos, nao segmentacao errada. Olhe o criativo antes de mexer no publico.
3. **CTR x taxa de conversao, problemas diferentes**: CTR alto com conversao baixa indica promessa do anuncio desalinhada da landing/oferta. CTR baixo indica anuncio que nao convence a clicar. Tratar como dois diagnosticos separados.
4. **Escalar pelo que ja prova retorno, nao pelo que parece bonito**: So entra na lista de scaling o que bate o KPI com volume confiavel. Metrica de vaidade (muitas views, CPV baixo) sem o KPI do objetivo nao justifica aumentar orcamento.
5. **Escalada em degraus**: Subir orcamento de campanha vencedora em incrementos (ordem de 20 a 30 por cento) e reavaliar, em vez de dobrar de uma vez, para nao quebrar o aprendizado e estourar o CPA.

---

## Execution Phases

### Phase 1: Diagnostico das Campanhas
1. Ler `dados_campanhas` e organizar por campanha e por grupo de anuncios, registrando formato (in-stream, in-feed/Discovery, bumper), gasto, impressoes, views, view rate, CPV, cliques, CTR, conversoes e CPA.
2. Confirmar o `objetivo` e fixar o **KPI principal** que vai julgar cada linha:
   - `awareness` / `views`: CPV e view rate (custo por view e retencao do criativo).
   - `inscritos` / `trafego`: CTR, custo por clique e custo por inscrito quando rastreado.
   - `leads` / `vendas`: CPA e taxa de conversao (o resto vira metrica de apoio).
3. Estabelecer a referencia de comparacao: meta de KPI informada, benchmark do mercado (`Portugal`/`Brasil`) ou periodo anterior. Toda avaliacao de "bom" ou "ruim" precisa apontar para esse numero.
4. Classificar cada campanha/grupo em uma das faixas, sempre citando o numero que justifica:
   - **Vencedor:** bate o KPI com volume confiavel.
   - **Promissor:** perto do KPI, ainda em aprendizado ou com volume baixo.
   - **Em risco:** acima do CPV/CPA alvo, mas com sinais aproveitaveis (ex.: criativo ou publico salvavel).
   - **Drenando verba:** gasto relevante sem entregar o KPI e sem sinal de melhora.
5. Marcar onde o volume e insuficiente para decidir (poucas conversoes, gasto baixo) e tratar essas linhas como "observar", nunca como veredicto.

### Phase 2: Identificar o que Escalar e o que Cortar
1. **Lista de scaling:** selecionar campanhas/grupos `Vencedor` (e `Promissor` perto da meta com tendencia positiva) que sustentem aumento de verba.
   - Recomendar a escalada em degraus (incrementos da ordem de 20 a 30 por cento) com reavaliacao apos novo volume, em vez de saltos bruscos que quebram o aprendizado.
   - Apontar o teto: ate onde escalar antes do CPV/CPA comecar a subir alem do alvo.
2. **Lista de cutting:** selecionar campanhas/grupos `Drenando verba` que ja gastaram o equivalente a 1 a 3 CPAs alvo (ou janela suficiente) sem entregar o KPI.
   - Para cada corte, dizer o que fazer com a verba liberada (realocar para a lista de scaling ou para um novo teste).
3. **Lista de ajuste (nem escala, nem corta ainda):** campanhas/grupos `Em risco` ou `Promissor` que pedem mudanca de criativo, lance ou segmentacao antes de qualquer decisao de verba, com a hipotese do que esta segurando o resultado.
4. Para cada item das tres listas, registrar o gatilho numerico da decisao (ex.: "CPA 2,3x acima do alvo apos 1,8 CPA de gasto sem conversao" ou "CPV 18 por cento abaixo do alvo com view rate acima de 35 por cento").

### Phase 3: Recomendacoes de Criativo e Segmentacao
1. **Criativo:** a partir das metricas, indicar onde o criativo e o gargalo e o que testar.
   - View rate baixo em in-stream: refazer o hook dos primeiros 5 segundos (a regra do skip do TrueView), nao culpar o publico primeiro.
   - CTR baixo: revisar o CTA e a clareza da promessa no anuncio.
   - CTR alto com conversao baixa: alinhar a promessa do anuncio com a landing/oferta (problema de mensagem, nao de midia).
   - Sugerir variacoes de criativo a testar e a metrica que decide o vencedor.
2. **Segmentacao:** indicar ajustes de publico apoiados nos dados.
   - Concentrar verba nos publicos/posicionamentos que ja entregam o KPI; cortar ou reduzir os que so drenam.
   - Avaliar publicos por afinidade, intencao (in-market), palavras-chave, canais e placements pelo desempenho real, nunca por suposicao.
   - Considerar a separacao por mercado (`Portugal` x `Brasil`) quando os custos e a resposta divergirem, para nao misturar leituras de CPV/CPA.
3. Conectar tudo ao objetivo e ao KPI: cada recomendacao precisa dizer qual metrica deve melhorar e como sera medido o efeito.
4. Priorizar as recomendacoes por impacto esperado x esforco, deixando claro o que mexer primeiro.

---

## Output Format

Escrever em `output_dir/anuncios/diagnostico-anuncios.md`:

```markdown
# Diagnostico de Anuncios (YouTube Ads)

**Canal:** {{{USER_NAME}} | Infinity Cast}
**Objetivo:** {awareness | views | inscritos | trafego | leads | vendas}
**KPI principal:** {CPV | view rate | CTR | CPA | ...}
**Mercado:** {Portugal | Brasil | PT/BR}
**Periodo:** {janela analisada}
**Referencia:** {meta de KPI / benchmark / periodo anterior usado como comparacao}

## Panorama da Conta

| Campanha/Grupo | Formato | Gasto | CPV | View rate | CTR | Conversoes | CPA | KPI vs meta | Faixa |
|----------------|---------|-------|-----|-----------|-----|------------|-----|-------------|-------|
| {nome} | {in-stream/discovery/bumper} | {R$/EUR} | {valor} | {%} | {%} | {n} | {valor} | {+/- vs meta} | {Vencedor/Promissor/Em risco/Drenando} |

## Escalar (scaling)

1. {campanha/grupo}, gatilho: {numero que justifica}, acao: subir verba em {~20-30%} ate {teto}, reavaliar apos {volume}.

## Cortar (cutting)

1. {campanha/grupo}, gatilho: {gasto = N CPAs sem KPI}, acao: pausar, realocar verba para {destino}.

## Ajustar (antes de decidir verba)

1. {campanha/grupo}, hipotese: {o que segura o resultado}, teste: {criativo/lance/segmentacao}, metrica que decide: {KPI}.

## Recomendacoes de Criativo

- {recomendacao}, sintoma nos dados: {metrica}, o que testar: {variacao}, metrica que decide: {KPI}.

## Recomendacoes de Segmentacao

- {recomendacao}, apoio nos dados: {publico/placement e desempenho}, efeito esperado: {KPI}.

## Prioridade de Acao

| # | Acao | Lista | Impacto esperado | Esforco | Quando |
|---|------|-------|------------------|---------|--------|
| 1 | {acao} | {scaling/cutting/ajuste} | {alto/medio} | {baixo/medio} | {agora/proxima semana} |

## Itens em Observacao (volume insuficiente)

- {campanha/grupo}, motivo: {poucas conversoes / gasto baixo}, coletar mais {volume} antes de decidir.
```

---

## Veto Conditions

- NEVER fazer qualquer recomendacao (escalar, cortar, ajustar) sem um dado da conta que a sustente: toda decisao cita o numero que a justifica.
- NEVER cortar uma campanha/grupo antes de ela ter tido volume suficiente (gasto da ordem de 1 a 3 CPAs alvo sem KPI), para nao decidir no ruido.
- NEVER escalar uma campanha so por metrica de vaidade (muitas views, CPV baixo) quando o KPI do objetivo nao foi batido.
- NEVER misturar mercados (`Portugal` e `Brasil`) numa mesma leitura quando os custos divergem ao ponto de distorcer o diagnostico.
- NEVER usar travessao (em dash, o traco longo) em nenhum texto deste arquivo. Usar dois-pontos, parenteses, virgula ou reescrever.
- NEVER inventar benchmark, meta ou numero que nao venha do export, do User Input ou de uma referencia declarada.
- NEVER entregar diagnostico sem ao menos as listas de scaling e cutting (mesmo que uma delas venha vazia, com a justificativa).

---

## Completion Criteria

- [ ] Objetivo confirmado e KPI principal fixado a partir dele
- [ ] Referencia de comparacao estabelecida (meta, benchmark ou periodo anterior)
- [ ] Panorama da conta montado por campanha/grupo com as metricas reais
- [ ] Cada campanha/grupo classificado em faixa, com o numero que justifica
- [ ] Lista de scaling com gatilho numerico, degraus de aumento e teto
- [ ] Lista de cutting com gatilho de gasto/volume e destino da verba liberada
- [ ] Lista de ajuste com hipotese e metrica que decide
- [ ] Recomendacoes de criativo amarradas a sintomas nos dados
- [ ] Recomendacoes de segmentacao apoiadas no desempenho real dos publicos
- [ ] Prioridade de acao (impacto x esforco) definida
- [ ] Itens sem volume marcados como observacao, nao como veredicto
- [ ] Arquivo salvo em `output_dir/anuncios/diagnostico-anuncios.md` no formato do template
- [ ] Sem travessao e em portugues do Brasil
