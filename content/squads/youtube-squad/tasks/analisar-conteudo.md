---
task: analisarConteudo()
responsavel: "@youtube-researcher"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: transcricao_txt
    tipo: file
    origem: Pipeline (transcrever-episodio)
    obrigatorio: true
  - campo: transcricao_srt
    tipo: file
    origem: Pipeline (transcrever-episodio)
    obrigatorio: true
  - campo: id
    tipo: string
    origem: episodio.yaml
    obrigatorio: true
  - campo: output_dir
    tipo: path
    origem: episodio.yaml
    obrigatorio: true
  - campo: roteiro
    tipo: file
    origem: episodio.yaml
    obrigatorio: false

Saida:
  - campo: content_map
    tipo: file
    destino: "{output_dir}/analise/content-map.md"
    persistido: true

Checklist:
  - "[ ] Transcricao inteira lida (txt e srt cruzados)"
  - "[ ] Temas principais mapeados com peso por tempo dedicado"
  - "[ ] 10 a 20 ganchos citaveis extraidos, cada um com timestamp real"
  - "[ ] Angulo mais forte identificado e cruzado com o nicho fe + negocios"
  - "[ ] Capitulos cronologicos gerados a partir do srt"
  - "[ ] 3 a 5 momentos virais marcados com timestamp"
---

# Task: Analisar Conteudo

**Task ID:** YT-PUB-03
**Version:** 1.0.0
**Command:** `*analisar-conteudo`
**Agent:** YouTube Researcher (youtube-researcher) com modelagem de Matt Gielen (matt-gielen)
**Purpose:** Ler a transcricao do episodio (txt + srt) e extrair a materia-prima de embalagem: temas, ganchos citaveis, angulo, capitulos e cortes virais. Esse content-map alimenta titulo, descricao e thumbnail. Sem ele, a embalagem vira achismo.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| transcricao_txt | file | Pipeline (transcrever-episodio) | Yes | Arquivo `{output_dir}/transcricao/{id}-transcricao.txt` existe e tem texto |
| transcricao_srt | file | Pipeline (transcrever-episodio) | Yes | Arquivo `.srt` existe com timestamps no formato `HH:MM:SS,mmm` |
| id | string | episodio.yaml | Yes | ID do episodio (ex: EP001) |
| output_dir | path | episodio.yaml | Yes | Diretorio do episodio (`produtos/infinity-cast/episodios/{id}/`) |
| roteiro | file | episodio.yaml | No | Roteiro original, se houver, para validar intencao do episodio |
| canal | enum | episodio.yaml ou User | No | `infinity-cast` (podcast) ou `fred-martins` (canal pessoal). Default: infinity-cast |

---

## Preconditions

- A task `*transcrever` (transcrever-episodio.md) ja rodou e gerou `txt` + `srt` validos em `{output_dir}/transcricao/`.
- O `srt` tem timestamps reais (nao placeholders). Sem timestamps, esta task NAO pode gerar ganchos nem cortes e deve abortar.
- O diretorio `{output_dir}/analise/` existe ou pode ser criado.
- Identidade do canal definida: nicho fe + negocios, mercado Portugal e Brasil, marca sua comunidade (laranja sobre preto).

---

## Reference: Angulos que Performam (fe + negocios)

Antes de escolher o angulo, calibre pelo que costuma puxar CTR e retencao neste nicho. Use como lente, nunca como invencao de conteudo que nao foi dito:

1. **Tabu / Verdade incomoda**: o convidado diz algo que o publico pensa mas nao fala em voz alta (ex: "dizimo nao te deixa rico"). Alto poder de clique se a frase for real.
2. **Numero / Especificidade**: valor, prazo ou quantidade concreta dita no episodio (ex: "perdi 200 mil e voltei em 18 meses"). Numero ancora a promessa.
3. **Jornada / Transformacao**: antes e depois pessoal do convidado (faliu, se reergueu, fundou). Gera curiosidade e identificacao.
4. **IA / Futuro**: quando o episodio toca ferramentas, automacao ou o que muda no trabalho. Tema quente, bom para o canal pessoal.
5. **Fe x Dinheiro (tensao)**: o atrito entre crenca e ambicao, que e o territorio central do sua comunidade. Costuma ser o angulo mais forte quando aparece.

---

## Execution Phases

### Phase 1: Leitura e Mapeamento de Temas
1. Ler a transcricao `txt` inteira, do inicio ao fim. Nao pular blocos.
2. Abrir o `srt` em paralelo para ancorar cada trecho relevante a um timestamp real.
3. Se houver `roteiro`, ler para entender a intencao declarada do episodio (sem deixar o roteiro sobrescrever o que foi de fato dito).
4. Identificar de 4 a 8 TEMAS principais que estruturam a conversa.
5. Atribuir PESO a cada tema pelo tempo dedicado (estimar minutos a partir dos timestamps do srt) e marcar a faixa `[HH:MM - HH:MM]` de cada um.
6. Ordenar os temas por peso decrescente. O tema de maior peso e candidato natural a titulo e thumbnail.

### Phase 2: Extracao de Ganchos Citaveis
1. Varrer a transcricao em busca de 10 a 20 frases citaveis: afirmacoes fortes, contradicoes, confissoes, numeros, viradas de raciocinio.
2. Para CADA gancho registrar: o timestamp real (`HH:MM:SS` vindo do srt), a frase transcrita o mais proxima possivel do que foi dito, e quem falou ({{USER_NAME}} ou convidado, quando identificavel).
3. Priorizar frases que funcionam fora de contexto (passam sozinhas como corte ou frase de thumbnail).
4. Descartar frases vagas, mucetas ("entao", "sabe", "tipo") e qualquer coisa cuja origem voce nao consiga apontar no srt.

### Phase 3: Identificacao do Angulo
1. Cruzar os temas de maior peso (Phase 1) com os ganchos mais fortes (Phase 2).
2. Classificar o angulo dominante usando a Reference acima (tabu, numero, jornada, IA, fe x dinheiro). Pode haver um angulo primario e um secundario.
3. Escrever uma frase de tese: qual e a promessa central que o episodio entrega ao espectador.
4. Justificar a escolha do angulo com pelo menos 1 gancho com timestamp que o sustente.
5. Sinalizar o encaixe no nicho fe + negocios e no canal alvo (infinity-cast vs fred-martins).

### Phase 4: Geracao de Capitulos
1. A partir do `srt`, segmentar o episodio em CAPITULOS cronologicos (tipicamente 6 a 12, dependendo da duracao).
2. Cada capitulo recebe: timestamp de inicio no formato `MM:SS` ou `HH:MM:SS` (o primeiro DEVE ser `00:00`) e um titulo curto e descritivo (3 a 7 palavras).
3. Garantir ordem cronologica estritamente crescente e ausencia de buracos grandes ou sobreposicao.
4. Esses capitulos sao copiaveis direto para a descricao do YouTube (formato de timestamps clicaveis).

### Phase 5: Marcacao de Momentos Virais (Cortes)
1. Selecionar de 3 a 5 MOMENTOS VIRAIS candidatos a corte (Shorts/Reels) a partir dos ganchos mais fortes.
2. Para cada corte registrar: timestamp de inicio e fim aproximados (`HH:MM:SS - HH:MM:SS`), o gancho central, e por que viraliza (tabu, numero, emocao, virada).
3. Preferir trechos que tenham comeco, tensao e desfecho dentro de 15 a 60 segundos.
4. Ordenar do mais forte para o mais fraco.

### Phase 6: Consolidacao
1. Montar o arquivo `{output_dir}/analise/content-map.md` no formato de Output abaixo.
2. Revisar: todo timestamp existe no srt; nenhuma frase foi inventada; capitulos cronologicos.
3. Salvar e reportar o caminho do arquivo gerado.

---

## Output Format

Arquivo: `{output_dir}/analise/content-map.md`

```markdown
# Content Map, {id}

**Canal:** {infinity-cast | fred-martins}
**Duracao:** {HH:MM:SS}
**Fonte:** transcricao/{id}-transcricao.txt + .srt

## Temas (por peso)

| # | Tema | Faixa | Peso (min) | Titulo? |
|---|------|-------|------------|---------|
| 1 | {tema} | [00:00 - 00:00] | {min} | sim/nao |

## Ganchos Citaveis

| # | Timestamp | Frase | Quem |
|---|-----------|-------|------|
| 1 | 00:00:00 | "{frase real}" | {{{USER_NAME}}/convidado} |

(10 a 20 linhas)

## Angulo

- **Primario:** {tabu | numero | jornada | IA | fe x dinheiro}
- **Secundario:** {...}
- **Tese:** {frase de promessa central}
- **Sustentacao:** gancho #{n} @ {timestamp}
- **Encaixe nicho/canal:** {nota}

## Capitulos (descricao)

00:00 {titulo capitulo 1}
00:00 {titulo capitulo 2}
...

## Cortes Virais

| # | Inicio - Fim | Gancho | Por que viraliza |
|---|--------------|--------|------------------|
| 1 | 00:00:00 - 00:00:00 | "{gancho}" | {motivo} |

(3 a 5 linhas)
```

---

## Veto Conditions

- NEVER inventar dados, frases, numeros ou afirmacoes que nao foram ditos no episodio. Toda informacao vem da transcricao.
- NEVER registrar um gancho ou corte sem timestamp real extraido do srt.
- NEVER entregar capitulos fora de ordem cronologica ou sem o `00:00` inicial.
- NEVER usar travessao (em dash) em nenhum trecho do content-map.
- NEVER reescrever a identidade do episodio para forcar um angulo: o angulo emerge do conteudo, nao o contrario.
- NEVER seguir se o srt nao tiver timestamps reais. Abortar e reportar dependencia em `*transcrever`.

---

## Completion Criteria

- [ ] Transcricao inteira lida, txt e srt cruzados
- [ ] 4 a 8 temas mapeados com peso por tempo e faixa de timestamp
- [ ] 10 a 20 ganchos citaveis, cada um com timestamp real e autor quando identificavel
- [ ] Angulo primario (e secundario, se houver) identificado, com tese e gancho de sustentacao
- [ ] Angulo cruzado com o nicho fe + negocios e o canal alvo
- [ ] Capitulos cronologicos comecando em `00:00`, copiaveis para a descricao
- [ ] 3 a 5 cortes virais com timestamp inicio-fim e justificativa
- [ ] Arquivo `{output_dir}/analise/content-map.md` salvo no formato do template
- [ ] Nenhum dado inventado; todo timestamp confere com o srt
- [ ] Caminho do content-map.md reportado para as proximas tasks (`*gerar-titulo`, `*gerar-descricao`, `*gerar-prompt-thumbnail`)
