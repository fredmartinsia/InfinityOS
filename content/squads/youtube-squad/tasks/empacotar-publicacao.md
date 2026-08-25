---
task: empacotarPublicacao()
responsavel: "@youtube-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: titulo
    tipo: file
    origem: output_dir/publicacao/titulo.md
    obrigatorio: true
  - campo: descricao
    tipo: file
    origem: output_dir/publicacao/descricao.md
    obrigatorio: true
  - campo: tags
    tipo: file
    origem: output_dir/publicacao/tags.txt
    obrigatorio: true
  - campo: prompt_thumbnail
    tipo: file
    origem: output_dir/thumbnail/PROMPT-CHATGPT.md
    obrigatorio: true
  - campo: frases_thumbnail
    tipo: file
    origem: output_dir/thumbnail/FRASES.md
    obrigatorio: true
  - campo: entrega_chatgpt
    tipo: dir
    origem: output_dir/frames/entrega-chatgpt
    obrigatorio: true
  - campo: transcricao
    tipo: file
    origem: output_dir/transcricao/{id}-transcricao.txt
    obrigatorio: false

Saida:
  - campo: publicar_index
    tipo: file
    destino: output_dir/publicacao/PUBLICAR.md
    persistido: true

Checklist:
  - "[ ] Presenca de titulo.md, descricao.md e tags.txt confirmada"
  - "[ ] Thumbnail (PROMPT-CHATGPT.md + FRASES.md) e entrega-chatgpt presentes"
  - "[ ] checklists/publicacao-podcast.md rodado com veredito PASS/REVISE/FAIL"
  - "[ ] PUBLICAR.md gerado com titulo, descricao, tags, caminhos e veredito"
  - "[ ] Nenhum artefato critico faltando (FAIL se faltar titulo, descricao, tags ou links)"
---

# Task: Empacotar Publicacao

**Task ID:** YT-PUB-09
**Version:** 1.0.0
**Command:** `*empacotar`
**Agent:** YouTube Chief (youtube-chief)
**Purpose:** Reunir todos os artefatos de publicacao gerados pelas tasks anteriores em `output_dir/publicacao/`, validar o conjunto pelo `checklists/publicacao-podcast.md` e produzir um indice unico `PUBLICAR.md` que serve de fonte de verdade na hora de subir o episodio no YouTube. Sem este empacotamento, a equipe sobe video com peca faltando.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| titulo | file | `output_dir/publicacao/titulo.md` | Yes | Saida de `*gerar-titulo`; contem titulo principal + 2 alternativos A/B |
| descricao | file | `output_dir/publicacao/descricao.md` | Yes | Saida de `*gerar-descricao`; primeiras 2 linhas, blocos, capitulos, links e CTA |
| tags | file | `output_dir/publicacao/tags.txt` | Yes | Saida de `*gerar-tags`; lista de tags separadas por virgula, dentro do limite de caracteres |
| prompt_thumbnail | file | `output_dir/thumbnail/PROMPT-CHATGPT.md` | Yes | Saida de `*prompt-thumbnail`; prompt pronto para colar no ChatGPT/gerador de imagem |
| frases_thumbnail | file | `output_dir/thumbnail/FRASES.md` | Yes | Saida de `*frases-thumbnail`; frases curtas candidatas para a arte da thumbnail |
| entrega_chatgpt | dir | `output_dir/frames/entrega-chatgpt` | Yes | Pasta por pessoa com `frame-1..5.jpg` + `MAPA.txt`, saida do pipeline de frames |
| transcricao | file | `output_dir/transcricao/{id}-transcricao.txt` | No | Saida de `*transcrever`; usada como referencia de apoio, nao bloqueia o empacotamento |
| id | string | `episodio.yaml` | Yes | Identificador do episodio (ex.: `EP001`), usado nos caminhos e no cabecalho do indice |
| veredito_anterior | enum | checklists/output-quality.md | No | Resultado de checagens de qualidade ja rodadas, se houver |

---

## Preconditions

- As tasks de publicacao foram executadas e gravaram seus arquivos em `output_dir/publicacao/` e `output_dir/thumbnail/`.
- O pipeline de frames rodou e produziu `output_dir/frames/entrega-chatgpt/{nome}/` com os frames e o `MAPA.txt`.
- O `output_dir` do episodio existe no padrao `produtos/infinity-cast/episodios/{id}/`.
- O `checklists/publicacao-podcast.md` esta disponivel para ser rodado nesta etapa.
- O `id` do episodio esta confirmado e bate com o `episodio.yaml`.

---

## Referencia de Padrao de Empacotamento

Estude estes padroes antes de montar o indice. Um bom `PUBLICAR.md` faz o operador subir o video sem abrir mais nenhum arquivo:

1. **Tudo em uma tela:** titulo escolhido, descricao final e tags ficam visiveis no proprio indice, prontos para copiar e colar, sem caca a arquivos soltos.
2. **Caminho clicavel, nao descricao:** cada peca de midia (thumbnail, prompt, frases, frames) aparece como caminho relativo exato dentro do `output_dir`, nao como "esta na pasta de thumbnail".
3. **Veredito no topo:** PASS, REVISE ou FAIL aparece logo no inicio, com a data, para que ninguem suba um pacote REVISE achando que esta pronto.
4. **O que falta vira lista de acao:** se houver REVISE, o indice lista item a item o que esta pendente e qual task resolve (`*gerar-descricao`, `*frases-thumbnail`, etc.), nunca um texto vago.
5. **Rastreabilidade:** cada artefato aponta a task que o gerou, para que a correcao volte para o agente certo sem retrabalho.

---

## Execution Phases

### Phase 1: Conferir Presenca dos Artefatos
1. Verificar a existencia de cada artefato obrigatorio no `output_dir`:
   - `publicacao/titulo.md`
   - `publicacao/descricao.md`
   - `publicacao/tags.txt`
   - `thumbnail/PROMPT-CHATGPT.md`
   - `thumbnail/FRASES.md`
   - `frames/entrega-chatgpt/` (com ao menos uma subpasta por pessoa contendo `frame-1..5.jpg` e `MAPA.txt`)
2. Verificar a transcricao como artefato de apoio (nao bloqueante): `transcricao/{id}-transcricao.txt`.
3. Para cada artefato, registrar o status: PRESENTE, VAZIO (existe mas sem conteudo util) ou AUSENTE.
4. Abrir `titulo.md`, `descricao.md` e `tags.txt` e extrair o conteudo final que vai para o indice:
   - titulo principal escolhido (e os 2 alternativos A/B);
   - texto final da descricao (primeiras 2 linhas, capitulos, links, CTA);
   - linha de tags pronta para colar.
5. Confirmar os caminhos relativos da thumbnail (prompt + frases) e da entrega-chatgpt para citar no indice.

### Phase 2: Rodar o Checklist de Publicacao
1. Rodar `checklists/publicacao-podcast.md` contra o conjunto de artefatos coletado na Phase 1.
2. Marcar cada item do checklist como cumprido `[x]` ou pendente `[ ]`, com atencao redobrada aos itens marcados como `(CRITICAL)`.
3. Aplicar os criterios de veredito do checklist:
   - **PASS:** todos os itens criticos cumpridos e nenhum artefato obrigatorio ausente ou vazio.
   - **REVISE:** itens nao criticos pendentes, ou artefato presente mas com ajuste a fazer; o pacote nao esta pronto, mas o caminho de correcao e claro.
   - **FAIL:** algum artefato critico ausente ou vazio (titulo, descricao, tags ou links), ou um item `(CRITICAL)` nao cumprido.
4. Para cada item pendente, anotar: o que falta, qual artefato corrigir e qual task o regenera (ex.: titulo -> `*gerar-titulo`, descricao -> `*gerar-descricao`, tags -> `*gerar-tags`, prompt/frases -> `*prompt-thumbnail` / `*frases-thumbnail`, frames -> pipeline de frames via `*extrair-frames`).
5. Registrar o veredito final e a data da checagem.

### Phase 3: Gerar o Indice PUBLICAR.md
1. Montar `output_dir/publicacao/PUBLICAR.md` com o veredito no topo (PASS, REVISE ou FAIL) e a data.
2. Inserir o titulo escolhido (mais os alternativos A/B), a descricao final pronta para colar e a linha de tags.
3. Listar os caminhos relativos exatos de cada peca de midia: thumbnail (PROMPT-CHATGPT.md e FRASES.md) e o link da pasta `frames/entrega-chatgpt`.
4. Se o veredito for REVISE ou FAIL, incluir a secao "O que falta" com a lista de pendencias item a item, cada uma apontando a task que resolve.
5. Aplicar a regra de escrita do sua comunidade: portugues do Brasil, sem travessao (em dash). Usar dois-pontos, parenteses, virgula ou reescrever.
6. Salvar o arquivo e reportar ao operador o veredito e, se houver, as pendencias.

---

## Output Format

Escrever em `output_dir/publicacao/PUBLICAR.md`:

```markdown
# PUBLICAR: {id}

**Veredito:** {PASS | REVISE | FAIL}
**Data da checagem:** {AAAA-MM-DD}
**Canal:** {{{USER_NAME}} | Infinity Cast}
**Convidado:** {nome ou "sem convidado"}

---

## Titulo

> {titulo principal escolhido}

**Alternativos A/B:**
1. {alternativo A}
2. {alternativo B}

Fonte: `publicacao/titulo.md` (task `*gerar-titulo`)

## Descricao (pronta para colar)

```
{texto final da descricao: 2 primeiras linhas, blocos, capitulos, links, CTA}
```

Fonte: `publicacao/descricao.md` (task `*gerar-descricao`)

## Tags (pronta para colar)

```
{tag1, tag2, tag3, ...}
```

Fonte: `publicacao/tags.txt` (task `*gerar-tags`)

## Thumbnail

- Prompt: `thumbnail/PROMPT-CHATGPT.md` (task `*prompt-thumbnail`)
- Frases: `thumbnail/FRASES.md` (task `*frases-thumbnail`)
- Frames de referencia: `frames/entrega-chatgpt/` (pipeline `*extrair-frames`)

## Conferencia de Artefatos

| Artefato | Caminho | Status |
|----------|---------|--------|
| Titulo | publicacao/titulo.md | {PRESENTE / VAZIO / AUSENTE} |
| Descricao | publicacao/descricao.md | {PRESENTE / VAZIO / AUSENTE} |
| Tags | publicacao/tags.txt | {PRESENTE / VAZIO / AUSENTE} |
| Prompt thumbnail | thumbnail/PROMPT-CHATGPT.md | {PRESENTE / VAZIO / AUSENTE} |
| Frases thumbnail | thumbnail/FRASES.md | {PRESENTE / VAZIO / AUSENTE} |
| Entrega ChatGPT | frames/entrega-chatgpt/ | {PRESENTE / VAZIO / AUSENTE} |
| Transcricao (apoio) | transcricao/{id}-transcricao.txt | {PRESENTE / VAZIO / AUSENTE} |

## O que falta (apenas se REVISE ou FAIL)

- [ ] {pendencia 1} -> corrigir em {artefato} via {task}
- [ ] {pendencia 2} -> corrigir em {artefato} via {task}

## Veredito do Checklist

`checklists/publicacao-podcast.md`: {PASS | REVISE | FAIL}
{Resumo de uma linha do motivo do veredito.}
```

---

## Veto Conditions

- NEVER marcar o pacote como pronto (PASS) se faltar titulo, descricao, tags ou os links da descricao: artefato critico ausente ou vazio forca FAIL.
- NEVER omitir o veredito do checklist no topo do `PUBLICAR.md`.
- NEVER citar uma peca de midia (thumbnail, prompt, frases, frames) sem o caminho relativo exato dentro do `output_dir`.
- NEVER inventar conteudo de titulo, descricao ou tags: o indice copia o que as tasks geraram, nao reescreve.
- NEVER apagar ou sobrescrever os artefatos das tasks anteriores; o `PUBLICAR.md` apenas os referencia e consolida.
- NEVER usar travessao (em dash, o traco longo) em nenhuma parte do indice ou deste arquivo.
- NEVER entregar REVISE ou FAIL sem a secao "O que falta" listando cada pendencia e a task que a resolve.

---

## Completion Criteria

- [ ] Presenca de `titulo.md`, `descricao.md` e `tags.txt` conferida e registrada com status
- [ ] Presenca de `thumbnail/PROMPT-CHATGPT.md`, `thumbnail/FRASES.md` e `frames/entrega-chatgpt/` conferida
- [ ] Transcricao verificada como apoio (nao bloqueia)
- [ ] `checklists/publicacao-podcast.md` rodado com veredito PASS, REVISE ou FAIL e data
- [ ] `PUBLICAR.md` gerado com titulo escolhido, descricao final e tags prontas para colar
- [ ] Caminhos relativos da thumbnail (prompt + frases) e da entrega-chatgpt citados no indice
- [ ] Secao "O que falta" presente sempre que o veredito for REVISE ou FAIL, com a task de correcao por item
- [ ] Veredito do checklist registrado no topo do indice
- [ ] Arquivo salvo em `output_dir/publicacao/PUBLICAR.md`
- [ ] Sem travessao e em portugues do Brasil
- [ ] Concluido apenas com veredito PASS no checklist (REVISE ou FAIL retorna pendencias e nao fecha a task)
