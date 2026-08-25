# Checklist de Completude do Pacote de Publicacao, YouTube Squad

**Checklist ID:** YT-CL-002
**Referenced by:** tasks/empacotar-publicacao.md
**Purpose:** Validar a completude do pacote de publicacao de um episodio do Infinity Cast (e videos do canal {{USER_NAME}}) antes de subir no YouTube. Garante que todos os artefatos gerados pelas tasks de publicacao existam, estejam preenchidos e sigam o padrao sua comunidade, evitando que a equipe suba video com peca faltando.

[[LLM: INSTRUCOES DE INICIALIZACAO

Este checklist valida o PACOTE DE PUBLICACAO consolidado pela task `*empacotar` (tasks/empacotar-publicacao.md). Ele e o gate de qualidade rodado na Phase 2 dessa task, antes de gerar o `PUBLICAR.md`.

ESCOPO DOS ARTEFATOS (todos relativos ao output_dir do episodio, padrao `produtos/infinity-cast/episodios/{id}/`):
- Transcricao: `transcricao/{id}-transcricao.txt` (+ srt/vtt/json)
- Frames: `frames/qc/SHEET-{nome}.jpg`, `frames/entrega-chatgpt/{pessoa}/frame-1..5.jpg` + `MAPA.txt`
- Thumbnail: `thumbnail/PROMPT-CHATGPT.md`, `thumbnail/FRASES.md`
- Publicacao: `publicacao/titulo.md`, `publicacao/descricao.md`, `publicacao/tags.txt`

ABORDAGEM DE EXECUCAO:
1. Para cada secao, verificar cada item contra os artefatos reais no `output_dir` (existencia E conteudo util, nunca arquivo vazio).
2. Marcar cada item como [x] cumprido, [ ] pendente ou [N/A] nao aplicavel (ex.: sem convidado, sem srt/vtt).
3. Itens marcados com (CRITICAL) bloqueiam a entrega: se um deles ficar [ ], o veredito e FAIL.
4. Para cada item pendente, anotar o que falta e qual task o regenera (ex.: titulo -> `*gerar-titulo`, descricao -> `*gerar-descricao`, tags -> `*gerar-tags`, prompt -> `*prompt-thumbnail`, frases -> `*frases-thumbnail`, frames -> `*extrair-frames` / `*empacotar`).
5. Aplicar a regra de escrita do sua comunidade em todo artefato textual: portugues do Brasil, SEM travessao (em dash, o traco longo). Usar ponto, virgula, dois-pontos, parenteses ou reescrever.

Itens CRITICAL estao marcados com o sufixo (CRITICAL).]]

---

## 1. Transcricao

- [ ] Arquivo `transcricao/{id}-transcricao.txt` existe e tem texto util, nao esta vazio (CRITICAL)
- [ ] O `{id}` no nome do arquivo bate com o `id` do `episodio.yaml`
- [ ] Legendas com timestamps geradas (`.srt` e/ou `.vtt`) para apoiar os capitulos da descricao
- [ ] JSON com segmentacao (`.json`) presente quando o pipeline o produziu (apoio, nao bloqueia)
- [ ] Texto em portugues do Brasil, sem travessao

## 2. Frames

- [ ] Contact sheets de QC gerados em `frames/qc/SHEET-{nome}.jpg`, um por pessoa
- [ ] Pasta `frames/entrega-chatgpt/{pessoa}/` existe para cada pessoa do `episodio.yaml` (CRITICAL)
- [ ] Cada pessoa tem os 5 frames `frame-1.jpg` ate `frame-5.jpg`, sem buraco na sequencia (CRITICAL)
- [ ] `MAPA.txt` presente em cada `frames/entrega-chatgpt/{pessoa}/`, mapeando frame para a origem (CRITICAL)
- [ ] Frames sao nitidos e usaveis (rosto visivel, sem corte ruim), coerentes com o `SHEET` de QC

## 3. Thumbnail

- [ ] Prompt para ChatGPT gerado em `thumbnail/PROMPT-CHATGPT.md`, pronto para colar (CRITICAL)
- [ ] `thumbnail/FRASES.md` traz 3 frases rankeadas por CTR, da mais forte para a mais fraca (CRITICAL)
- [ ] Cada frase tem a palavra-chave destacada (em maiuscula ou marcada), guiando a arte (CRITICAL)
- [ ] Teste de legibilidade a 120px citado: a frase escolhida ainda le no tamanho de feed
- [ ] Identidade visual sua comunidade respeitada no prompt: laranja sobre preto
- [ ] Prompt e frases em portugues do Brasil, sem travessao

## 4. Titulo

- [ ] `publicacao/titulo.md` existe e traz o titulo principal escolhido (CRITICAL)
- [ ] Pelo menos 2 alternativos A/B listados alem do principal
- [ ] Titulo principal tem no maximo 70 caracteres
- [ ] Keyword principal do episodio presente no titulo
- [ ] Titulo em portugues do Brasil, sem travessao, sem promessa que o episodio nao cumpre

## 5. Descricao

- [ ] `publicacao/descricao.md` existe e abre com gancho nas 2 primeiras linhas (CRITICAL)
- [ ] Capitulos com timestamps presentes, comecando em `00:00`, em ordem crescente (CRITICAL)
- [ ] LINKS confirmados pelo {{USER_NAME}} inseridos: nada de placeholder ou link inventado (CRITICAL)
- [ ] CTA do sua comunidade presente (inscrever, seguir, link do clube)
- [ ] Hashtags relevantes ao final da descricao
- [ ] Timestamps dos capitulos batem com os marcos da transcricao (`.srt`/`.vtt`)
- [ ] Descricao em portugues do Brasil, sem travessao

## 6. Tags

- [ ] `publicacao/tags.txt` existe e nao esta vazio (CRITICAL)
- [ ] Total de caracteres da linha de tags dentro do limite de 500 (CRITICAL)
- [ ] Tags separadas por virgula, sem duplicatas, cobrindo a keyword principal e variacoes

## 7. Escrita e Identidade

- [ ] Nenhum artefato textual usa travessao (em dash, o traco longo) (CRITICAL)
- [ ] Todos os textos em portugues do Brasil
- [ ] Tom e identidade sua comunidade mantidos (laranja sobre preto na thumbnail; sem achismo sem dados)
- [ ] Caminhos citados sao relativos exatos dentro do `output_dir`, nao descricoes vagas

---

## PASS/FAIL Criteria

**PASS:** Todos os itens (CRITICAL) marcados [x], nenhum artefato obrigatorio ausente ou vazio, e menos de 2 falhas em itens nao criticos.

**REVISE:** Todos os itens (CRITICAL) marcados [x], porem com 2 ou mais falhas em itens nao criticos (ex.: faltou `.srt`, hashtags ausentes, alternativo A/B faltando). O pacote nao esta pronto, mas o caminho de correcao e claro: listar cada pendencia com a task que a resolve.

**FAIL:** Qualquer item (CRITICAL) sem marcar. Forca FAIL imediato se faltar titulo, descricao, links da descricao ou tags, ou se um artefato critico estiver presente mas vazio.

**Mapa de correcao por artefato:**
- Transcricao -> task `*transcrever`
- Frames (entrega-chatgpt / MAPA.txt) -> task `*extrair-frames` (reempacotar via `*empacotar`)
- Prompt da thumbnail -> task `*prompt-thumbnail`
- Frases da thumbnail -> task `*frases-thumbnail`
- Titulo -> task `*gerar-titulo`
- Descricao -> task `*gerar-descricao`
- Tags -> task `*gerar-tags`

**Regra de fechamento:** a task `*empacotar` so registra o pacote como pronto com veredito PASS. REVISE ou FAIL retorna pendencias na secao "O que falta" do `PUBLICAR.md` e nao fecha a publicacao.
