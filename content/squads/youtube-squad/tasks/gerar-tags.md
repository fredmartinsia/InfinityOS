---
task: gerarTags()
responsavel: "@brian-dean"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: keyword_principal
    tipo: string
    origem: titulo.md
    obrigatorio: true
  - campo: content_map
    tipo: string
    origem: analise/content-map.md
    obrigatorio: true
  - campo: convidado
    tipo: string
    origem: episodio.yaml
    obrigatorio: false
  - campo: output_dir
    tipo: string
    origem: episodio.yaml
    obrigatorio: true

Saida:
  - campo: tags_paths
    tipo: object
    destino: Filesystem
    persistido: true

Checklist:
  - "[ ] Keyword principal herdada do titulo e usada como primeira tag"
  - "[ ] Entre 15 e 30 tags balanceando head, long-tail e entidades"
  - "[ ] Entidades incluidas: convidado, Infinity Cast, sua comunidade, {{USER_NAME}}"
  - "[ ] tags.txt em uma linha separada por virgula com total <= 500 caracteres"
  - "[ ] Lista comentada gravada no .md explicando o papel de cada bloco"
---

# Task: Gerar Tags

**Task ID:** YT-PUB-08
**Version:** 1.0.0
**Command:** `*gerar-tags`
**Agent:** Brian Dean (brian-dean)
**Purpose:** Montar de 15 a 30 tags de YouTube para o episodio combinando a keyword principal (herdada do titulo), keywords secundarias derivadas do content map, entidades nomeadas (convidado, marca Infinity Cast, sua comunidade, {{USER_NAME}}) e variacoes long-tail, respeitando o limite duro de 500 caracteres do campo de tags do YouTube e sem nenhum tag-stuffing.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| keyword_principal | string | titulo.md (output de `*gerar-titulo`) | Yes | Termo de busca central do video, primeira tag da lista |
| content_map | string | analise/content-map.md (output de `*analisar-conteudo`) | Yes | Mapa de temas, blocos e entidades do episodio |
| convidado | string | episodio.yaml (pessoas[].nome) | No | Nome do convidado quando o episodio tem entrevista |
| output_dir | string | episodio.yaml | Yes | Pasta destino, padrao produtos/infinity-cast/episodios/{id}/ |

---

## Preconditions

- O titulo do episodio ja existe em `output_dir/publicacao/titulo.md` e a keyword principal esta identificavel nele
- O content map ja existe em `output_dir/analise/content-map.md` com os temas e entidades do episodio
- O nome do convidado, quando houver, esta disponivel no episodio.yaml ou no content map
- A pasta `output_dir/publicacao/` existe ou pode ser criada para receber `tags.txt`

---

## Champion Reference

Padroes de tags validados antes de montar a lista:

1. **Keyword principal em primeiro**: a primeira tag e a mesma frase de busca usada no titulo; o YouTube da mais peso a tag inicial, entao ela nunca e desperdicada com termo generico.
2. **Pilha head + long-tail (Brian Dean)**: combinar termos curtos de alto volume (head) com frases longas e especificas (long-tail) cobre tanto a busca ampla quanto a intencao de nicho, sem competir so onde e impossivel ranquear.
3. **Entidades nomeadas**: convidado, marca (Infinity Cast), canal ({{USER_NAME}}) e organizacao (sua comunidade) ancoram o video no grafo de conhecimento e ajudam recomendacao por associacao.
4. **Sem tag-stuffing**: cada tag descreve de fato o conteudo do episodio; encher de termos populares irrelevantes nao ajuda ranqueamento e contraria as diretrizes do YouTube.
5. **Limite de 500 caracteres**: o campo de tags do YouTube corta em 500 caracteres no total (incluindo virgulas); a lista e construida ja respeitando esse teto, com as tags mais valiosas primeiro para nada importante ser cortado.

---

## Execution Phases

### Phase 1: Derivar Keywords do Titulo e do Content Map
1. Ler `output_dir/publicacao/titulo.md` e extrair a keyword principal (a frase de busca central do titulo); ela sera a primeira tag
2. Ler `output_dir/analise/content-map.md` e mapear:
   - Temas e sub-temas tratados no episodio (viram keywords secundarias)
   - Entidades nomeadas: convidado, marcas, lugares, conceitos centrais
   - Termos que o publico Portugal/Brasil realmente usaria para buscar esse assunto
3. Listar variacoes naturais da keyword principal (singular/plural, sinonimos, formas com e sem o nome do convidado)
4. Confirmar o nome do convidado pelo episodio.yaml ou content map; se nao houver convidado, pular as tags de entidade-convidado

### Phase 2: Montar a Lista de 15 a 30 Tags
1. Posicionar a keyword principal como tag numero 1
2. Adicionar keywords secundarias (head) derivadas dos temas do content map, da mais relevante para a menos relevante
3. Adicionar variacoes long-tail (frases de 3+ palavras) que descrevem angulos especificos do episodio
4. Adicionar as tags de entidade obrigatorias quando aplicaveis:
   - Convidado (nome completo e, se houver, forma como e mais conhecido)
   - Infinity Cast (nome do podcast)
   - sua comunidade (organizacao)
   - {{USER_NAME}} (canal/host)
5. Garantir o balanceamento: nem so head (genérico demais), nem so long-tail (volume baixo demais); a regra pratica e keyword principal + bloco head + bloco long-tail + bloco de entidades
6. Manter o total entre 15 e 30 tags; cada tag precisa descrever de fato algo presente no episodio

### Phase 3: Validar o Limite de Caracteres
1. Montar a string final em uma unica linha, tags separadas por virgula (sem virgula final)
2. Contar o total de caracteres da string, incluindo as virgulas separadoras
3. Se o total passar de 500 caracteres, cortar as tags menos valiosas (sempre as do final, nunca a keyword principal nem as entidades obrigatorias) ate ficar dentro do limite
4. Reconfirmar que sobraram pelo menos 15 tags depois do corte; se cair abaixo de 15, encurtar tags long-tail em vez de remover blocos inteiros
5. Gravar a string final em `output_dir/publicacao/tags.txt` (uma linha)
6. Gravar a lista comentada no .md de resposta, explicando o papel de cada bloco (keyword principal, head, long-tail, entidades) e a contagem de caracteres

---

## Output Format

`output_dir/publicacao/tags.txt` (uma unica linha, separada por virgula, total <= 500 caracteres):

```text
keyword principal, keyword secundaria 1, keyword secundaria 2, frase long-tail 1, frase long-tail 2, nome do convidado, Infinity Cast, sua comunidade, {{USER_NAME}}
```

Lista comentada na resposta:

```markdown
## Tags, {id}

**Keyword principal (tag 1):** {keyword_principal}
**Total de tags:** {n} (entre 15 e 30)
**Total de caracteres:** {n}/500

### Blocos
- Head (volume): {tag, tag, tag}
- Long-tail (especificas): {frase, frase, frase}
- Entidades: {convidado}, Infinity Cast, sua comunidade, {{USER_NAME}}

### Verificacao
- Keyword principal como tag 1: sim
- 15 a 30 tags: sim
- Total <= 500 caracteres: sim
- Sem tag-stuffing/irrelevancia: sim
- tags.txt gravado em: {output_dir}/publicacao/tags.txt
```

---

## Veto Conditions

- NEVER fazer tag-stuffing nem incluir tags irrelevantes ao conteudo do episodio
- NEVER ultrapassar 500 caracteres no total da string (incluindo virgulas)
- NEVER deixar a lista com menos de 15 ou mais de 30 tags
- NEVER usar a primeira posicao com termo generico; a tag 1 e sempre a keyword principal do titulo
- NEVER omitir as entidades obrigatorias aplicaveis (convidado quando existe, Infinity Cast, sua comunidade, {{USER_NAME}})
- NEVER inventar temas que nao estao no content map só para encher a lista

---

## Completion Criteria

- [ ] Keyword principal herdada do titulo e posicionada como tag 1
- [ ] Keywords secundarias e entidades derivadas do content map
- [ ] Convidado incluido quando o episodio tem entrevista
- [ ] Entidades Infinity Cast, sua comunidade e {{USER_NAME}} presentes
- [ ] Lista com 15 a 30 tags balanceando head + long-tail + entidades
- [ ] tags.txt gravado em uma unica linha separada por virgula
- [ ] Total da string <= 500 caracteres (incluindo virgulas)
- [ ] Lista comentada gravada no .md com blocos e contagem de caracteres
- [ ] Output formatado conforme o template
