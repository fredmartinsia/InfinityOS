---
task: gerarPromptThumbnail()
responsavel: "@paddy-galloway"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: id
    tipo: string
    origem: episodio.yaml
    obrigatorio: true
  - campo: angulo
    tipo: string
    origem: analise/content-map.md
    obrigatorio: true
  - campo: frase_escolhida
    tipo: string
    origem: thumbnail/FRASES.md
    obrigatorio: true
  - campo: frames_entrega
    tipo: path
    origem: frames/entrega-chatgpt/{nome}/
    obrigatorio: true
  - campo: briefing
    tipo: yaml
    origem: data/thumbnail-briefing.yaml
    obrigatorio: true

Saida:
  - campo: prompt_thumbnail
    tipo: markdown
    destino: output_dir/thumbnail/PROMPT-CHATGPT.md
    persistido: true

Checklist:
  - "[ ] Frase, angulo e 2 frames-heroi confirmados com o {{USER_NAME}} (elicit)"
  - "[ ] Prompt do ChatGPT montado na paleta laranja sobre preto (Modo A sem texto, Modo B com texto)"
  - "[ ] Passo a passo Canva escrito (recorte dos 2 rostos reais, caixa laranja, asterisco + seta)"
  - "[ ] Teste de 120px citado como criterio de aprovacao"
---

# Task: Gerar Prompt de Thumbnail

**Task ID:** YT-PUB-04
**Version:** 1.0.0
**Command:** `*prompt-thumbnail`
**Agent:** Paddy Galloway (paddy-galloway)
**Purpose:** Produzir o prompt pronto para colar no ChatGPT que gera o fundo/arte da thumbnail no padrao sua comunidade (laranja sobre preto), acompanhado do passo a passo de montagem em dois modos (Modo A: fundo no ChatGPT mais rostos reais no Canva; Modo B: tudo no ChatGPT). A thumbnail nao e arte decorativa, e uma isca de atencao que precisa funcionar em 1 segundo no tamanho de miniatura no celular.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| id | string | episodio.yaml | Sim | ID do episodio (ex.: ep001), usado no output_dir |
| angulo | string | analise/content-map.md | Sim | Angulo editorial escolhido para a thumb (tese/gancho do episodio) |
| frase_escolhida | string | thumbnail/FRASES.md | Sim | Frase-gancho com a palavra-chave entre [ ] que vai na caixa laranja |
| frames_entrega | path | frames/entrega-chatgpt/{nome}/ | Sim | Pasta com os 5 frames-candidato por pessoa mais MAPA.txt |
| briefing | yaml | data/thumbnail-briefing.yaml | Sim | Paleta, layout 3 zonas, especificacoes tecnicas, elementos de marca |
| modo | enum | User prompt | Nao | A (rostos reais no Canva, recomendado para podcast) ou B (tudo no ChatGPT, rascunho rapido). Default: A |

---

## Preconditions

- `analise/content-map.md` existe e o angulo da thumb esta definido (vem de `*analisar-conteudo`).
- `thumbnail/FRASES.md` existe e ha pelo menos uma frase ranqueada (vem de `*frases-thumbnail`).
- `frames/entrega-chatgpt/{nome}/` existe com os frames-heroi por pessoa (host na esquerda, convidado na direita) e o `MAPA.txt` (vem de `*extrair-frames`).
- `data/thumbnail-briefing.yaml` carregado: paleta laranja `#FF6B00` sobre preto `#0D0D0D`, layout de 3 zonas, rim light, asterisco e seta laranja, teste de 120px.

---

## Padrao de Referencia (sua comunidade)

Antes de montar o prompt, internalize a assinatura visual do canal. Nao copiar genericos, replicar ESTE padrao:

1. **Formula vencedora do nicho:** 2 rostos (host esquerda mais convidado direita) + fundo escuro + 1 palavra destacada. Validada em Ed Mylett, Flow, PrimoCast, Diary of a CEO.
2. **Laranja sobre preto e a diferenciacao real:** os concorrentes de fe mais negocios usam verde, verde-limao ou dourado. O laranja `#FF6B00` sobre preto `#0D0D0D` esta livre nesse cruzamento. Nunca abrir mao disso.
3. **Numero quando houver:** quantificacao aumenta CTR (40 inimigos, 147 leis, 6 paises). Se a frase tem numero, ele e heroi.
4. **Pergunta-tabu performa mais** no nicho fe mais dinheiro. Frase sempre como pergunta, nunca como afirmacao categorica.
5. **Calibracao Portugal:** estilo BR ainda e diferenciador em PT, mas evitar parecer clickbait gritante. Paleta premium (laranja mais preto, sem vermelho gritante) e autoridade serena.
6. **Evitar caixa vermelha mais seta estilo Valuetainment** (sinaliza news/drama). Seta laranja, se usar, discreta.

---

## Execution Phases

### Phase 1: Confirmacao com o {{USER_NAME}} (ELICIT obrigatorio)

Antes de gerar qualquer prompt, apresentar ao {{USER_NAME}} e aguardar confirmacao:

1. **A frase escolhida** (de `thumbnail/FRASES.md`), com a palavra-chave entre [ ] que ira para a caixa laranja. Mostrar o ranking de CTR e a recomendacao, mas a palavra final e do {{USER_NAME}}.
2. **O angulo** (de `analise/content-map.md`): confirmar que a frase casa com a tese do episodio.
3. **Os 2 frames-heroi:** um para o host (lado esquerdo) e um para o convidado (lado direito), escolhidos de `frames/entrega-chatgpt/{nome}/`. Apresentar as opcoes do MAPA.txt e pedir confirmacao da dupla (expressao forte, olhos abertos, recorte limpo).
4. **O modo de producao:** Modo A (recomendado, mantem rosto real) ou Modo B (rascunho rapido). Confirmar.

Nao avancar para a Phase 2 sem o "ok" do {{USER_NAME}} nos quatro pontos. Se faltar frase ou frame, voltar para `*frases-thumbnail` ou `*extrair-frames`.

### Phase 2: Montagem do prompt do ChatGPT

Montar o bloco de prompt pronto para colar no ChatGPT, sempre na paleta da marca.

1. **Fundo:** preto/charcoal (`#0D0D0D` a `#1A1A1A`) com glow laranja central (`rgba(255,107,0,0.24)`) e vinheta escura nas bordas para dar profundidade.
2. **Imagem central cinematografica e escura:** a cena tematica que casa com o angulo (silhuetas, luz dramatica laranja-quente, atmosfera epica), no terco superior-central, atras/entre onde os rostos entram.
3. **Paleta travada:** laranja `#FF6B00` como cor-assinatura e destaque, preto dominando o fundo. Sem roxo, sem verde, sem vermelho gritante. Gold (`#FFD600`) so como toque premium pontual (ex.: numero), com parcimonia.
4. **Proporcao:** 1280x720 (16:9), composicao limpa com zona segura no canto inferior direito (timestamp do video cobre).
5. **Modo A (recomendado):** o ChatGPT gera SOMENTE o fundo mais glow mais imagem central, SEM TEXTO e SEM ROSTOS. Os 2 rostos reais e a tipografia entram depois no Canva. Deixar isso explicito no prompt ("nao gerar texto, nao gerar pessoas").
6. **Modo B (rascunho rapido):** o ChatGPT gera tudo de uma vez, incluindo a frase-gancho com a palavra-chave em caixa laranja e os dois rostos "parecidos". Avisar que e rascunho e que o texto deve ser revisado.

### Phase 3: Passo a passo de montagem no Canva (Modo A)

Escrever o roteiro de montagem que o {{USER_NAME}} segue depois de gerar o fundo:

1. Abrir o Canva em 1280x720 e colocar o fundo gerado pelo ChatGPT.
2. **Remover o fundo** dos 2 rostos reais (rembg ou removedor do Canva). Posicionar {{USER_NAME}}/host na esquerda (~1/3 da largura) e o convidado na direita (~1/3). Aplicar **rim light laranja** (luz de contorno) e sombra para descolar do fundo.
3. Inserir a **frase-gancho** em fonte bold condensada maiuscula (Anton, Archivo Black ou Montserrat Black), branca com contorno/sombra preta forte, maximo ~5 palavras, sem cobrir os olhos/rostos.
4. Colocar a **palavra-chave** (a que estava entre [ ]) dentro de uma **caixa retangular laranja `#FF6B00`** com texto branco ou preto (o que tiver mais contraste).
5. Adicionar a assinatura do canal: **asterisco/sparkle laranja** no canto superior direito e **seta laranja curva discreta** apontando do texto para o convidado.
6. **Teste de 120px:** reduzir a thumbnail para ~120px de largura e confirmar que a frase ainda le e os rostos ainda tem expressao. Se nao passar, voltar e simplificar.
7. Exportar PNG/JPG de alta qualidade, abaixo de 2 MB.

---

## Output Format

Gravar em `output_dir/thumbnail/PROMPT-CHATGPT.md` (output_dir = `produtos/infinity-cast/episodios/{id}/`):

```markdown
# PROMPT DE THUMBNAIL, {id}

**Angulo:** {angulo}
**Frase escolhida:** {frase com [palavra-chave]}
**Frame host (esquerda):** {caminho do frame escolhido}
**Frame convidado (direita):** {caminho do frame escolhido}
**Modo:** {A | B}

---

## PROMPT PARA COLAR NO CHATGPT

> {bloco de prompt completo, em portugues, descrevendo fundo preto/charcoal,
> glow laranja central, imagem central cinematografica, paleta #FF6B00 sobre
> #0D0D0D, 1280x720, zona segura no canto inferior direito.
> Modo A: SEM texto e SEM rostos. Modo B: COM frase + caixa laranja + rostos.}

---

## PASSO A PASSO DE MONTAGEM (Modo A, Canva)

1. Canva 1280x720 + fundo gerado.
2. Remover fundo dos 2 rostos reais + rim light laranja + sombra; host esquerda, convidado direita.
3. Frase bold maiuscula branca com contorno preto, ate ~5 palavras.
4. Caixa laranja #FF6B00 na palavra-chave.
5. Asterisco laranja (canto sup. direito) + seta laranja discreta para o convidado.
6. TESTE 120px: reduzir e confirmar leitura da frase e expressao dos rostos.
7. Exportar PNG/JPG < 2 MB.

## ALTERNATIVA (Modo B, tudo no ChatGPT)
{prompt unico com texto e rostos, marcado como rascunho a revisar}
```

---

## Veto Conditions

- NEVER fugir da paleta laranja sobre preto. Roxo, verde ou vermelho gritante como cor principal estao proibidos. O preto domina o fundo, o laranja `#FF6B00` e o destaque.
- NEVER usar rosto gerado por IA quando ha rosto real disponivel em `frames/entrega-chatgpt/`. No Modo A os rostos sao sempre os reais recortados no Canva.
- NEVER avancar para gerar o prompt sem a confirmacao do {{USER_NAME}} sobre frase, angulo e os 2 frames-heroi (elicit obrigatorio).
- NEVER usar afirmacao categorica do tipo "fe garante riqueza". Frase do nicho fe mais dinheiro sempre como pergunta.
- NEVER usar caixa vermelha mais seta estilo news/drama.
- NEVER usar travessao (em dash, o traco longo) em nenhum texto do prompt ou do passo a passo. Usar virgula, dois-pontos, parenteses ou reescrever.

---

## Completion Criteria

- [ ] Frase, angulo e os 2 frames-heroi confirmados com o {{USER_NAME}} (elicit)
- [ ] Prompt do ChatGPT montado na paleta laranja `#FF6B00` sobre preto `#0D0D0D`, 1280x720
- [ ] Modo A descrito (fundo sem texto e sem rostos) e Modo B descrito (tudo no ChatGPT) conforme o modo escolhido
- [ ] Passo a passo de montagem no Canva escrito (recorte dos 2 rostos reais, rim light, caixa laranja na palavra-chave, asterisco e seta laranja)
- [ ] Teste de 120px citado como criterio de aprovacao
- [ ] Arquivo gravado em `output_dir/thumbnail/PROMPT-CHATGPT.md`
- [ ] Nenhum travessao no texto produzido
