---
task: extrairFrames()
responsavel: "@youtube-researcher"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: video
    tipo: string
    origem: episodio.yaml
    obrigatorio: true
  - campo: id
    tipo: string
    origem: episodio.yaml
    obrigatorio: true
  - campo: pessoas
    tipo: lista
    origem: episodio.yaml
    obrigatorio: true
  - campo: output_dir
    tipo: string
    origem: episodio.yaml
    obrigatorio: true

Saida:
  - campo: frames_entrega
    tipo: arquivos
    destino: "{output_dir}/frames/entrega-chatgpt/{nome}/frame-1..5.jpg + MAPA.txt"
    persistido: true
  - campo: contact_sheets
    tipo: arquivos
    destino: "{output_dir}/frames/qc/SHEET-{nome}.jpg"
    persistido: true

Checklist:
  - "[ ] run_pipeline.py rodado com --steps frames,score,crops,sheets,entrega"
  - "[ ] scores.csv gerado e conferido (sem 0 frames aprovados)"
  - "[ ] Contact sheets SHEET-{nome}.jpg gerados para cada pessoa"
  - "[ ] Contact sheets apresentados ao {{USER_NAME}} (selecao final dos herois e HUMANA)"
  - "[ ] entrega-chatgpt/{nome}/ com 5 frames + MAPA.txt por pessoa"
---

# Task: Extrair Frames

**Task ID:** YT-PUB-02
**Version:** 1.0.0
**Command:** `*extrair-frames`
**Agent:** YouTube Researcher (youtube-researcher)
**Purpose:** Extrair frames do video do episodio, pontuar e ranquear cada frame (rosto, nitidez, olhos, sorriso, iluminacao), recortar rostos por pessoa, gerar contact sheets de revisao e empacotar os 5 melhores frames de cada pessoa em `entrega-chatgpt/` com um `MAPA.txt`, prontos para virar matéria-prima da thumbnail.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| video | string | episodio.yaml | Yes | Caminho para o arquivo de video (mp4) do episodio |
| id | string | episodio.yaml | Yes | Identificador do episodio (ex: EP001), define o nome dos arquivos |
| fps | number | episodio.yaml | No | Frames por segundo a extrair (default 1) |
| topn | number | episodio.yaml | No | Quantos frames manter no ranking (default 80) |
| pessoas | lista | episodio.yaml | Yes | Lista de pessoas com `nome` e `lado` (esquerda/direita) para recorte por pessoa |
| output_dir | string | episodio.yaml | Yes | Pasta de saida do episodio (`produtos/infinity-cast/episodios/{id}/`) |

---

## Preconditions

- Arquivo de video do episodio existe e o caminho em `video` esta correto
- `episodio.yaml` preenchido com `id`, `pessoas` (nome + lado) e `output_dir`
- Dependencias instaladas: `ffmpeg`, `opencv-python`, `numpy`, `Pillow`, `rembg` (modelo u2net)
- Pasta `output_dir` reservada para este episodio (nenhum asset de outro episodio mora ali)
- Se o episodio tiver duas pessoas, cada uma deve ter o `lado` correto (esquerda/direita) para o recorte por lado funcionar

---

## Reference

Antes de extrair, alinhe a janela de captura com o objetivo (matéria-prima de thumbnail). Frames bons para thumbnail compartilham 5 sinais que o `score_frames.py` pontua:

1. **Rosto presente e grande**: rosto detectado, ocupando area util do quadro (recorte limpo depois)
2. **Nitidez**: frame sem motion blur (variancia de Laplaciano alta)
3. **Olhos abertos**: olhar para a camera ou para o interlocutor, nunca piscando
4. **Expressao**: sorriso, surpresa ou reacao forte vende mais que cara neutra
5. **Iluminacao**: rosto bem exposto, sem estourar nem afundar nas sombras

O pipeline ja foi validado rodando no EP001: a selecao automatica entrega 5 candidatos por pessoa, mas a escolha do heroi final e sempre HUMANA ({{USER_NAME}} decide olhando os contact sheets).

---

## Execution Phases

### Phase 1: Extracao, Pontuacao e Empacotamento (run_pipeline.py)
1. Garanta que `cwd` esta em `squads/youtube-squad/_scripts/pipeline/` e que o `episodio.yaml` aponta para o video e o `output_dir` certos.
2. Valide antes de rodar (mostra os comandos sem executar):
   ```bash
   python3 run_pipeline.py episodio.yaml --steps frames,score,crops,sheets,entrega --dry-run
   ```
3. Rode o pipeline de frames de ponta a ponta:
   ```bash
   python3 run_pipeline.py episodio.yaml --steps frames,score,crops,sheets,entrega
   ```
4. O que cada step faz:
   - `frames` (`extract_frames.sh`): extrai frames brutos a `fps` para `frames/raw/`
   - `score` (`score_frames.py`): pontua e ranqueia (rosto, nitidez, olhos, sorriso, iluminacao), gera `frames/scores.csv` e separa o `topn` em `frames/top/{esquerda,direita}/`
   - `crops` (`crop_by_side.py`): recorta o rosto de cada pessoa pelo `lado` em `frames/cand_{nome}/`
   - `sheets` (`contact_sheet.py`): monta a grade de revisao `frames/qc/SHEET-{nome}.jpg`
   - `entrega`: empacota os 5 melhores de cada pessoa em `frames/entrega-chatgpt/{nome}/frame-1..5.jpg` + `MAPA.txt`

### Phase 2: Conferencia dos Scores e Sheets
1. Abra `frames/scores.csv` e confirme que o ranking nao esta vazio (ha frames aprovados, nao apenas linhas com score zerado).
2. Se a contagem de frames aprovados for 0 ou muito baixa, NAO prossiga: ajuste e reprocesse (ver Veto Conditions):
   - Ampliar/mover a janela de captura (intervalo do video usado)
   - Aumentar o `fps` (ex: de 1 para 2) para mais candidatos
   - Afrouxar os limiares de pontuacao no `score_frames.py` se o material for naturalmente escuro ou de baixa nitidez
3. Confirme que existe um `frames/qc/SHEET-{nome}.jpg` para cada pessoa do `episodio.yaml`.
4. Confirme que `frames/entrega-chatgpt/{nome}/` tem 5 frames e o `MAPA.txt` correspondente.

### Phase 3: Selecao Final (HUMANA)
1. Apresente ao {{USER_NAME}} os contact sheets `frames/qc/SHEET-{nome}.jpg`, um por pessoa.
2. Deixe explicito: a selecao automatica e ponto de partida, mas a escolha do frame heroi de cada pessoa e do {{USER_NAME}}.
3. Registre a decisao do {{USER_NAME}} (qual frame por pessoa) para a task seguinte de thumbnail consumir.
4. Se o {{USER_NAME}} rejeitar todos os candidatos de uma pessoa, volte a Phase 1 com janela/fps/limiares ajustados.

---

## Output Format

```
{output_dir}/frames/
├── raw/                          frames brutos f00001.jpg, f00002.jpg ...
├── scores.csv                    ranking completo (rosto, nitidez, olhos, sorriso, iluminacao)
├── top/
│   ├── esquerda/                 melhores frames do lado esquerdo
│   └── direita/                  melhores frames do lado direito
├── cand_{nome}/                  crops de rosto por pessoa
├── qc/
│   └── SHEET-{nome}.jpg          contact sheet de revisao por pessoa
└── entrega-chatgpt/
    └── {nome}/
        ├── frame-1.jpg ... frame-5.jpg   os 5 melhores da pessoa
        └── MAPA.txt              mapeia frame-N -> arquivo original + score
```

Resumo de handoff para o {{USER_NAME}}:

```markdown
## Frames extraidos, {id}

**Pessoas:** {lista de nomes}
**Frames brutos:** {N} (fps {fps})
**Frames no ranking:** {topn}

### Contact sheets (selecao final HUMANA)
- {nome}: frames/qc/SHEET-{nome}.jpg
- ...

### Entrega pronta
- frames/entrega-chatgpt/{nome}/frame-1..5.jpg + MAPA.txt
```

---

## Veto Conditions

- NEVER prosseguir com 0 frames aprovados, ajustar janela de captura, `fps` ou limiares de pontuacao e reprocessar
- NEVER sobrescrever assets de outro episodio, tudo deve ser gravado dentro de `output_dir`; nunca tocar o video-fonte
- NEVER tratar a selecao automatica como final, o heroi de cada pessoa e escolhido pelo {{USER_NAME}} nos contact sheets
- NEVER entregar `entrega-chatgpt/{nome}/` sem o `MAPA.txt` correspondente
- NEVER seguir para a thumbnail se faltar contact sheet de alguma pessoa do `episodio.yaml`

---

## Completion Criteria

- [ ] `run_pipeline.py` rodado com `--steps frames,score,crops,sheets,entrega`
- [ ] `frames/raw/` populado e `frames/scores.csv` com ranking nao vazio
- [ ] `frames/top/{esquerda,direita}/` e `frames/cand_{nome}/` gerados
- [ ] Contact sheets `frames/qc/SHEET-{nome}.jpg` gerados para todas as pessoas
- [ ] Contact sheets apresentados ao {{USER_NAME}} e selecao final registrada (HUMANA)
- [ ] `frames/entrega-chatgpt/{nome}/frame-1..5.jpg` + `MAPA.txt` prontos por pessoa
- [ ] Nenhum asset gravado fora de `output_dir`
