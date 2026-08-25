---
task: otimizarSeo()
responsavel: "@brian-dean"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: video_atual
    tipo: object
    origem: User Input
    obrigatorio: true
  - campo: keyword_alvo
    tipo: string
    origem: User Input
    obrigatorio: false
  - campo: desempenho_atual
    tipo: object
    origem: User Input ou YouTube Studio
    obrigatorio: false

Saida:
  - campo: pacote_seo_revisado
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Titulo, descricao e tags atuais auditados com diagnostico do desempenho"
  - "[ ] Keyword research feito (principal + secundarias + long-tail)"
  - "[ ] Promessa central do video preservada (nao reposicionada)"
  - "[ ] Titulo, descricao e tags revisados entregues com justificativa"
  - "[ ] Sem travessao e em portugues do Brasil"
---

# Task: Otimizar SEO

**Task ID:** YT-STR-02
**Version:** 1.0.0
**Command:** `*otimizar-seo`
**Agent:** Brian Dean (brian-dean)
**Purpose:** Reotimizar titulo, descricao e tags de um video JA publicado, partindo de keyword research atualizado e do que comprovadamente performa no nicho, para recuperar ou ampliar a descoberta por busca (SEO), sugeridos, browse e search generativo (GEO), sem nunca alterar a promessa central do video.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| video_atual | object | User Input | Yes | URL/ID do video + titulo, descricao e tags atuais (o que esta publicado hoje) |
| keyword_alvo | string | User Input | No | Keyword alvo desejada; se ausente, deve ser derivada do conteudo e do research na Phase 2 |
| desempenho_atual | object | User Input ou YouTube Studio | No | Impressoes, CTR, fontes de trafego, retencao, idade do video; orienta o diagnostico da Phase 1 |
| canal | enum | User Input | No | `{{USER_NAME}}` ou `Infinity Cast`; define tom e quanto o nome do convidado pesa |
| mercado | enum | User Input | No | `Portugal`, `Brasil` ou `PT/BR`; afeta vocabulario e os termos de busca usados |
| promessa_central | string | User Input ou inferida do video | No | O que o video efetivamente entrega; e o limite que a reotimizacao NAO pode cruzar |

---

## Preconditions

- O video ja esta publicado e os textos atuais (titulo, descricao, tags) estao disponiveis para auditoria
- A promessa central do video esta clara (assistir/ler o conteudo ou receber do usuario), pois ela e a trava da reotimizacao
- Ha acesso a pelo menos um sinal de desempenho (CTR, impressoes ou fontes de trafego) ou a aceitacao explicita de auditar sem dados de Studio
- Se a `keyword_alvo` nao foi fornecida, o conteudo do video tem material suficiente para deriva-la via research

---

## Referencia de Campeoes

Estude estes padroes de reotimizacao antes de entregar. Eles mostram como recuperar descoberta sem trair o que o video entrega:

1. **Realinhar a keyword com a busca real:** trocar um termo de jargao interno por aquele que o publico digita ("captacao de recursos" vira "como conseguir investimento", se for isso que o video resolve). Sobe relevancia sem mudar a promessa.
2. **Mover a keyword para a esquerda:** titulo que comecava com floreio ("Conversa incrivel sobre...") passa a comecar pela keyword ("Empreender em Portugal: ..."). Mesmo video, leitura no mobile e peso de SEO melhores.
3. **Reescrever os primeiros 125 caracteres da descricao:** o trecho que aparece na busca e nos sugeridos passa a responder a intencao de pesquisa em 2 a 3 frases extraiveis (serve SEO e GEO ao mesmo tempo).
4. **Capitulos como keywords:** adicionar/renomear capitulos com os termos secundarios que o video realmente cobre, ganhando indexacao de trechos sem inventar conteudo.
5. **Limpar tags infladas:** remover tags genericas ("viral, incrivel, podcast") e manter principal + variacoes + nome do convidado + long-tails que casam com o conteudo. Menos ruido, mais sinal.

---

## Execution Phases

### Phase 1: Auditar o Estado Atual (titulo, descricao, tags e desempenho)
1. Registrar os textos publicados hoje: titulo atual, descricao atual e lista de tags atual, exatamente como estao.
2. Cruzar com os sinais de `desempenho_atual` quando houver:
   - **CTR baixo com impressoes altas:** problema de titulo/promessa de clique (mais do que de SEO).
   - **Impressoes baixas com retencao boa:** problema de descoberta (keyword/descricao/tags fracas) ou video subindo pouco no browse e sugeridos.
   - **Trafego so de "Externo/Direto":** o video nao esta sendo encontrado por busca nem sugerido dentro do YouTube.
3. Diagnosticar o titulo atual: a keyword aparece? aparece cedo? o comprimento corta no mobile? a promessa de clique e honesta?
4. Diagnosticar a descricao atual: os primeiros 125 caracteres respondem a uma intencao de busca? ha capitulos? ha estrutura (resumo, para quem, links, CTA) ou e uma linha vazia?
5. Diagnosticar as tags atuais: estao infladas com genericos? cobrem a keyword principal e as variacoes? ha tags irrelevantes que so adicionam ruido?
6. Confirmar e fixar a **promessa central** do video. Tudo daqui pra frente otimiza a descoberta DESSA promessa, nunca a substitui.

### Phase 2: Keyword Research (SEO + GEO)
1. Aplicar o YouTube Suggest Method: digitar o tema e a keyword candidata na busca do YouTube e coletar as sugestoes automaticas (o que o publico realmente procura).
2. Cruzar com o mercado (`Portugal`, `Brasil` ou `PT/BR`): preferir o termo que o publico daquele mercado de fato usa, nao o sinonimo "mais bonito".
3. Definir a **keyword principal** revisada: maior casamento entre intencao de busca real e a promessa central ja fixada na Phase 1.
4. Listar 3 a 8 **keywords secundarias e long-tails** (variacoes, termos relacionados, nome do convidado, nome da pauta) para alimentar descricao, capitulos e tags.
5. Comparar com o que performa no nicho: olhar como videos que rankeiam para esses termos estruturam titulo e descricao, e registrar o que da pra adotar sem copiar nem prometer alem do conteudo.
6. Decidir se o **nome do convidado** entra: entra quando tem busca propria ou autoridade reconhecida; fica de fora quando a pauta vende mais que o nome.

### Phase 3: Entregar o Pacote Revisado (titulo + descricao + tags + justificativa)
1. **Titulo novo:** reescrever carregando a keyword principal o mais a esquerda possivel, dentro de 60 a 70 caracteres, contando e registrando o numero. Manter a promessa central; melhorar so a busca e o clique honesto.
2. **Descricao nova:** estruturar nesta ordem, com a keyword principal nos primeiros 125 caracteres:
   - Linha 1: hook resumido com a keyword principal, extraivel em 2 a 3 frases (serve SEO e GEO).
   - O que o video cobre, com keywords secundarias de forma natural (sem stuffing).
   - Para quem e, qual problema resolve, qual valor entrega.
   - Capitulos (timestamps) nomeados com keywords secundarias reais do video.
   - Links mencionados e videos relacionados.
   - CTA de inscricao do canal.
   - 3 a 5 hashtags relevantes (nao um amontoado).
3. **Tags revisadas:** keyword principal + variacoes + nome do convidado (se entrou) + long-tails que casam com o conteudo. Remover genericos e irrelevantes. Manter o conjunto enxuto.
4. **Justificativa:** para cada bloco (titulo, descricao, tags), explicar o que mudou, por que mudou (qual sinal da Phase 1 ou achado da Phase 2 motivou) e por que a promessa central continua intacta.
5. Aplicar a regra de escrita do sua comunidade em todo o pacote: portugues do Brasil, sem travessao (em dash). Usar dois-pontos, parenteses, virgula ou reescrever.

---

## Output Format

```markdown
## Pacote SEO Revisado

**Video:** {url ou id}
**Canal:** {{{USER_NAME}} | Infinity Cast}
**Mercado:** {Portugal | Brasil | PT/BR}
**Promessa central (inalterada):** {o que o video entrega}

### Diagnostico do Atual

| Elemento | Atual | Problema identificado | Sinal de desempenho |
|----------|-------|-----------------------|---------------------|
| Titulo | {titulo atual} | {diagnostico} | {CTR/impressoes se houver} |
| Descricao | {resumo do que existe} | {diagnostico} | {fontes de trafego se houver} |
| Tags | {tags atuais} | {diagnostico} |, |

### Keyword

- **Principal (revisada):** {keyword}
- **Secundarias / long-tail:** {kw2}, {kw3}, {kw4}, {kw5}
- **Convidado no titulo:** {sim/nao + motivo}

### Titulo Novo

> {titulo revisado}

- Caracteres: {NN} (limite 70)
- Keyword na posicao: {inicio | meio}

### Descricao Nova

```
[Linha 1: hook com keyword principal, primeiros 125 caracteres]

[O que o video cobre, com keywords secundarias]

[Para quem e / qual problema resolve / qual valor entrega]

Capitulos:
0:00, Introducao
...

Links mencionados:
- ...

Videos relacionados:
- ...

Inscreve-te no canal: [link]

#hashtag1 #hashtag2 #hashtag3
```

### Tags Revisadas

{tag1}, {tag2}, {tag3}, {tag4}, {tag5}, ...

### Justificativa

- **Titulo:** {o que mudou e por que; promessa preservada porque ...}
- **Descricao:** {o que mudou e por que; promessa preservada porque ...}
- **Tags:** {o que entrou, o que saiu e por que}
```

---

## Veto Conditions

- NEVER mudar a promessa central do video: a reotimizacao melhora a descoberta do que o video entrega, nunca reposiciona o video para outro tema.
- NEVER prometer no titulo ou na descricao algo que o video nao entrega (clickbait destroi retencao e ranking).
- NEVER usar travessao (em dash, o traco longo) em nenhum texto deste pacote.
- NEVER fazer keyword stuffing (repetir a keyword e variacoes ate virar lista) no titulo, na descricao ou nas tags.
- NEVER passar de 70 caracteres no titulo novo.
- NEVER inventar dados, numeros, citacoes ou capitulos que nao existam no conteudo real do video.
- NEVER encher de tags genericas ("viral, incrivel, must-watch") nem deixar tags irrelevantes ao tema.
- NEVER otimizar so para a maquina: o titulo e os primeiros 125 caracteres precisam servir o humano e o search ao mesmo tempo.

---

## Completion Criteria

- [ ] Titulo, descricao e tags atuais auditados, com o estado publicado registrado
- [ ] Desempenho atual interpretado (CTR, impressoes, fontes de trafego) ou auditoria sem dados aceita explicitamente
- [ ] Promessa central confirmada e fixada como trava da reotimizacao
- [ ] Keyword research feito: principal revisada + 3 a 8 secundarias/long-tail
- [ ] Decisao sobre o nome do convidado registrada
- [ ] Titulo novo dentro de 60-70 caracteres, com keyword cedo e contagem registrada
- [ ] Descricao nova estruturada (hook com keyword nos primeiros 125 chars, capitulos, links, CTA, hashtags)
- [ ] Tags revisadas: enxutas, relevantes, sem genericos
- [ ] Justificativa escrita por bloco (titulo, descricao, tags), provando que a promessa central nao mudou
- [ ] Pacote SEO revisado entregue no formato do template
- [ ] Sem travessao e em portugues do Brasil
