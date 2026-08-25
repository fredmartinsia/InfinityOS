---
task: transcreverEpisodio()
responsavel: "@youtube-researcher"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: video
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: id
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: output_dir
    tipo: string
    origem: episodio.yaml
    obrigatorio: true
  - campo: lang
    tipo: enum
    origem: episodio.yaml
    obrigatorio: false

Saida:
  - campo: transcricao_paths
    tipo: object
    destino: Filesystem
    persistido: true

Checklist:
  - "[ ] Video-fonte confirmado como existente antes de qualquer extracao"
  - "[ ] Transcricao previa verificada e reaproveitada quando ja existe"
  - "[ ] run_pipeline.py executado com --steps audio,transcribe"
  - "[ ] {id}-transcricao.txt gerado e nao vazio"
  - "[ ] Arquivos srt/vtt/json com timestamps disponiveis"
---

# Task: Transcrever Episodio

**Task ID:** YT-PUB-01
**Version:** 1.0.0
**Command:** `*transcrever`
**Agent:** YouTube Researcher (youtube-researcher)
**Purpose:** Extrair o audio do video-fonte em 16kHz mono e transcrever com mlx_whisper (modelo large-v3-turbo, idioma pt) gerando o texto puro em txt mais os arquivos com timestamps (srt, vtt, json) que alimentam capitulos, content map e legendas.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| video | string | episodio.yaml ou User prompt | Yes | Caminho de um arquivo mp4 que existe no disco |
| id | string | episodio.yaml | Yes | Identificador do episodio, ex: EP001, usado como prefixo dos arquivos |
| output_dir | string | episodio.yaml | Yes | Pasta destino, padrao produtos/infinity-cast/episodios/{id}/ |
| lang | enum | episodio.yaml | No | Idioma do audio. Default pt. Outros valores so com confirmacao explicita |

---

## Preconditions

- O arquivo de video existe no caminho informado e esta legivel
- O manifesto episodio.yaml do episodio esta preenchido (id, video, output_dir)
- Dependencias do pipeline instaladas: ffmpeg e python3 -m mlx_whisper com o modelo mlx-community/whisper-large-v3-turbo (Apple Silicon)
- O idioma do audio esta definido (default pt); se houver duvida real sobre o idioma, confirmar antes de rodar

---

## Champion Reference

Padroes de transcricao validados no fluxo Infinity Cast antes de rodar:

1. **EP001 (piloto validado)**: pipeline rodado de ponta a ponta gerou transcricao limpa de ~70 minutos de audio em pt, base de todo o content map e dos capitulos.
2. **Audio 16kHz mono**: taxa e canal exigidos pelo mlx_whisper para maxima precisao; nunca transcrever direto do mp4 em alta taxa.
3. **large-v3-turbo em pt**: modelo escolhido por equilibrio entre qualidade de transcricao em portugues e tempo de processamento no Mac Apple Silicon.
4. **Reaproveitamento de transcricao**: episodio ja transcrito nunca e reprocessado: economiza minutos de GPU e protege ajustes manuais feitos no texto.
5. **Saida em quatro formatos**: txt para leitura e analise; srt e vtt para legendas e capitulos; json para timestamps granulares por segmento.

---

## Execution Phases

### Phase 1: Validacao e Reaproveitamento
1. Confirmar que o arquivo de video informado em `video` existe no disco; se nao existir, VETAR e pedir o caminho correto antes de qualquer outra acao
2. Confirmar idioma esperado em `lang` (default pt); se o conteudo aparenta outro idioma, confirmar antes de prosseguir
3. Verificar se ja existe transcricao em `output_dir/transcricao/`:
   - Procurar por `{id}-transcricao.txt` e companheiros `{id}-transcricao.{srt,vtt,json}`
   - Se existirem e o txt nao estiver vazio, REAPROVEITAR: reportar os caminhos e NAO retranscrever
   - NUNCA apagar ou sobrescrever transcricao existente sem confirmacao explicita do {{USER_NAME}}

### Phase 2: Extracao de Audio e Transcricao
1. Rodar o orquestrador do pipeline limitado as duas etapas de audio e transcricao:
   ```bash
   python3 _scripts/pipeline/run_pipeline.py <episodio.yaml> --steps audio,transcribe
   ```
2. A etapa `audio` converte o mp4 em mp3 16kHz mono dentro de `output_dir/transcricao/{id}-audio.mp3`
3. A etapa `transcribe` chama o mlx_whisper (large-v3-turbo, idioma de `lang`) sobre o audio extraido
4. Aguardar a conclusao: o mlx_whisper roda alguns minutos para ~70 minutos de audio; nao interromper o processo no meio
5. Em caso de duvida antes de executar, validar com `--dry-run` para ver os comandos sem rodar

### Phase 3: Confirmacao da Saida
1. Confirmar que `output_dir/transcricao/{id}-transcricao.txt` foi gerado
2. Confirmar que o txt NAO esta vazio (texto puro do episodio presente)
3. Confirmar que os arquivos com timestamps existem: `{id}-transcricao.srt`, `{id}-transcricao.vtt`, `{id}-transcricao.json`
4. Reportar os caminhos completos dos quatro arquivos para a etapa seguinte (`*extrair-frames` e `*analisar-conteudo`)

---

## Output Format

```markdown
## Transcricao, {id}

**Video-fonte:** {video}
**Idioma:** {lang}
**Status:** Gerada | Reaproveitada (ja existia)

### Arquivos gerados
- Texto puro: {output_dir}/transcricao/{id}-transcricao.txt
- Legenda SRT: {output_dir}/transcricao/{id}-transcricao.srt
- Legenda VTT: {output_dir}/transcricao/{id}-transcricao.vtt
- Timestamps JSON: {output_dir}/transcricao/{id}-transcricao.json
- Audio extraido: {output_dir}/transcricao/{id}-audio.mp3

### Verificacao
- txt nao vazio: sim | nao
- timestamps disponiveis (srt/vtt/json): sim | nao
- Pronto para *extrair-frames e *analisar-conteudo: sim | nao
```

---

## Veto Conditions

- NEVER prosseguir sem que o video-fonte exista e seja legivel
- NEVER assumir idioma errado; transcrever em pt por default e so mudar com confirmacao
- NEVER apagar ou sobrescrever transcricao existente sem confirmacao explicita do {{USER_NAME}}
- NEVER retranscrever um episodio que ja tem `{id}-transcricao.txt` valido em `output_dir/transcricao/`
- NEVER entregar a etapa com o txt vazio ou sem os arquivos de timestamps
- NEVER transcrever direto do mp4 em alta taxa; o audio deve ser 16kHz mono via etapa `audio`

---

## Completion Criteria

- [ ] Video-fonte confirmado como existente e legivel
- [ ] Idioma confirmado (default pt) antes de rodar
- [ ] Transcricao previa verificada; reaproveitada quando ja existe e valida
- [ ] run_pipeline.py executado com --steps audio,transcribe (ou reaproveitamento documentado)
- [ ] {id}-transcricao.txt gerado e nao vazio
- [ ] Arquivos {id}-transcricao.srt, .vtt e .json presentes com timestamps
- [ ] Caminhos dos quatro arquivos reportados para *extrair-frames e *analisar-conteudo
- [ ] Output formatado conforme o template
