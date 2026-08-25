---
task: gerarDescricao()
responsavel: "@brian-dean + @tom-breeze"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: content_map
    tipo: file
    origem: analise/content-map.md
    obrigatorio: true
  - campo: roteiro_html
    tipo: file
    origem: roteiro do episodio (HTML)
    obrigatorio: true
  - campo: convidado
    tipo: string
    origem: episodio.yaml + roteiro
    obrigatorio: true
  - campo: links_confirmados
    tipo: object
    origem: User Input (elicit)
    obrigatorio: true

Saida:
  - campo: descricao
    tipo: file
    destino: output_dir/publicacao/descricao.md
    persistido: true

Checklist:
  - "[ ] Links/CTAs candidatos extraidos do roteiro HTML (Mapa de CTAs + Stack final + handles)"
  - "[ ] {{USER_NAME}} confirmou/editou os links via elicit (so pediu o que faltava)"
  - "[ ] Gancho de 2-3 linhas escrito com keyword principal nas primeiras 150 caracteres"
  - "[ ] Capitulos com timestamps gerados a partir do content-map"
  - "[ ] Bloco de LINKS preenchido SO com links confirmados"
  - "[ ] CTA sua comunidade presente"
  - "[ ] Hashtags e keywords SEO/GEO aplicadas"
  - "[ ] Nenhum travessao no texto final"
---

# Task: Gerar Descricao

**Task ID:** YT-PUB-07
**Version:** 1.0.0
**Command:** `*gerar-descricao`
**Agent:** Brian Dean (brian-dean) lidera SEO/GEO e estrutura; Tom Breeze (tom-breeze) valida CTAs e ordem de conversao.
**Purpose:** Montar a descricao completa de YouTube do episodio com OS LINKS reais da gravacao (convidado, ofertas, patrocinador, sua comunidade, {{USER_NAME}}), capitulos navegaveis, gancho otimizado e camada SEO/GEO. A descricao nunca pode sair sem os links confirmados pelo {{USER_NAME}}.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| content_map | file | `analise/content-map.md` (saida de `*analisar-conteudo`) | Yes | Tem capitulos com timestamps e temas |
| roteiro_html | file | Roteiro HTML do episodio (ex: `infinity-cast-ep001-adeildo-silva.html`) | Yes | Contem blocos `cta-block` (Mapa de CTAs) e Stack final de links |
| convidado | string | `episodio.yaml` + roteiro | Yes | Nome do convidado e funcao (mentor, autor, etc.) |
| links_confirmados | object | User Input via elicit | Yes | Cada link confirmado pelo {{USER_NAME}} (URL real, nunca inventada) |
| output_dir | string | `episodio.yaml` | Yes | `produtos/infinity-cast/episodios/{id}/` |
| keyword_principal | string | Saida de `*gerar-titulo` / `*otimizar-seo` | No | Frase-foco do episodio para o gancho |

---

## Preconditions

- `analise/content-map.md` existe e tem os capitulos com timestamps (rodar `*analisar-conteudo` antes).
- O roteiro HTML do episodio esta acessivel (e a fonte dos links candidatos).
- O convidado e parceiros estao identificados.
- `elicit: true` obriga confirmacao humana dos links antes de escrever a descricao. Nenhum link entra sem o {{USER_NAME}} confirmar.

---

## Champion Reference

Estude estas descricoes campeas antes de escrever (o padrao que converte no YouTube de podcast):

1. **Diary of a CEO (Steven Bartlett)**: Gancho curto de 2 linhas, capitulos com timestamps detalhados, bloco de links do convidado primeiro, depois patrocinadores, depois canal. Ordem de conversao: convidado gera reciprocidade, CTA do canal colhe.
2. **Flow Podcast (BR)**: Bloco de "Assista tambem" + handles do convidado em destaque + patrocinadores agrupados. Hashtags so 3, no fim.
3. **Brian Dean / Backlinko**: Keyword principal nos primeiros 150 caracteres (acima da dobra do "mostrar mais"), descricao densa em entidades para SEO/GEO, link unico e limpo por destino.
4. **PrimoCast (BR)**: CTA de comunidade repetido no inicio e no fim, sempre com beneficio concreto antes do link.
5. **Stack final do EP001 (Infinity Cast)**: Checklist de links ja existe no roteiro: Instagram do convidado, evento, ofertas/livros, ministerio, Instagram do {{USER_NAME}}, sua comunidade, patrocinadores. Essa lista e o gabarito de extracao.

---

## Execution Phases

### Phase 0: Extracao de Links Candidatos (do roteiro HTML)

1. Abrir o roteiro HTML do episodio e varrer:
   - **Mapa de CTAs:** todos os blocos `cta-block` (no EP001: sua comunidade x3, VV Studio, VV Traffic Data). Cada um indica um destino que precisa de link.
   - **Stack final / checklist de descricao:** o callout "stack final de links" e o texto de encerramento do {{USER_NAME}} (no EP001: Instagram do Adeildo, Mansa Musa, Os 40 Inimigos da Prosperidade na Hotmart, Wook, Ministerio Santuario de Cristo, Instagram do {{USER_NAME}}, sua comunidade, VV Studio, VV Traffic Data, QR Code criadores do Norte).
   - **@handles e nomes proprios:** convidado, parceiros, ofertas e livros citados ao longo dos blocos.
2. Montar uma lista de candidatos agrupada por categoria:
   - Convidado (Instagram/redes, site, ofertas, livros, evento, ministerio)
   - Patrocinador oficial
   - Agencia parceira
   - sua comunidade (comunidade)
   - {{USER_NAME}} (Instagram/canal)
   - Livros/eventos citados
3. Marcar cada candidato com status `[falta URL]` quando o roteiro cita o destino mas nao traz a URL. NUNCA preencher URL por conta propria.

### Phase 1: Elicit, Confirmar os Links com o {{USER_NAME}}

1. Apresentar ao {{USER_NAME}} a lista de candidatos extraidos, ja agrupada, pedindo SO o que falta.
2. Para cada categoria, perguntar de forma objetiva (exemplo de prompt de elicit abaixo):

```
Extrai estes destinos de link do roteiro do EP{id}. Me confirma ou cola a URL real de cada um (deixa em branco o que nao tiver):

CONVIDADO ({convidado})
- Instagram do convidado: {url ou cola aqui}
- Oferta/curso citado ({nome}): {url}
- Livros ({nome}): {url}
- Evento ({nome}): {url}
- Ministerio/projeto ({nome}): {url}

PATROCINADOR
- {patrocinador} (link/QR): {url}

AGENCIA PARCEIRA
- {agencia}: {url}

sua comunidade
- Comunidade sua comunidade: {url}

FRED MARTINS
- Instagram do {{USER_NAME}}: {url}
- Canal/outros: {url}

Algum link a MAIS que eu nao peguei no roteiro?
```

3. Regras do elicit:
   - Pedir SO o que faltar. Se o roteiro ja trouxe a URL, mostrar e pedir confirmacao (sim/editar).
   - Aceitar adicoes do {{USER_NAME}} (link novo que nao estava no roteiro).
   - Aceitar remocoes (destino que nao vai entrar nesse episodio).
   - Travar a tarefa ate ter pelo menos: sua comunidade + 1 link do convidado confirmados. Sem isso, NAO escrever a descricao.
4. Registrar `links_confirmados` (categoria, rotulo, URL final).

### Phase 2: Gancho (2-3 linhas)

1. Escrever 2 a 3 linhas que vendem o episodio para quem clicou em "mostrar mais".
2. Colocar a `keyword_principal` nos primeiros 150 caracteres (SEO/GEO: e o que o YouTube e os motores de resposta leem com mais peso).
3. Usar a tese do episodio + tensao do convidado (no EP001: "cara improvavel que escolheu o diferente", business, prosperidade e IA).
4. Encerrar o gancho com uma frase-isca que justifica assistir ate o fim. Sem clickbait que o video nao entrega.

### Phase 3: Capitulos com Timestamps

1. Puxar os capitulos do `content-map.md` (cada capitulo tem inicio em mm:ss e tema).
2. Formatar como lista de timestamps do YouTube (cada linha = `mm:ss Titulo do capitulo`). O primeiro DEVE ser `00:00`.
3. Titulos de capitulo curtos, com entidade/keyword quando natural (ajuda SEO/GEO e a navegacao).
4. Garantir ordem cronologica e timestamps crescentes (requisito do YouTube para ativar a barra de capitulos).

### Phase 4: Bloco de LINKS e CTAs (ordem de conversao, Tom Breeze)

1. Inserir SO os `links_confirmados`. Nada de placeholder, nada de URL inventada.
2. Ordem recomendada (reciprocidade antes da colheita):
   - **Convidado primeiro** (Instagram, ofertas, livros, evento), devolve valor ao convidado e a audiencia.
   - **sua comunidade** (CTA principal da casa).
   - **Patrocinador oficial** e **agencia parceira**.
   - **{{USER_NAME}}** (Instagram/canal).
   - **Livros/eventos citados** que nao sejam do convidado.
3. Cada link com rotulo claro e beneficio curto antes da URL (1 linha). Um destino, um link limpo.

### Phase 5: CTA sua comunidade (bloco dedicado)

1. Escrever o CTA do sua comunidade com beneficio concreto (comunidade de empreendedores e empresarios aplicando business, prosperidade e IA no dia a dia) seguido do link confirmado.
2. Tom de convite, alinhado ao roteiro. E o CTA prioritario da casa: aparece no bloco de links E tem destaque proprio.

### Phase 6: Hashtags + Keywords (SEO/GEO, Brian Dean)

1. Listar 3 a 5 hashtags no fim (nicho + nome do programa + convidado quando relevante). Ex: `#InfinityCast #Empreendedorismo #InteligenciaArtificial`.
2. Garantir que a descricao cobre as entidades-chave do episodio (nomes proprios, temas, lugares) para SEO/GEO, sem keyword stuffing.
3. Repetir naturalmente a keyword principal 2 a 3 vezes ao longo do texto (gancho, um capitulo, fecho).

### Phase 7: Gravar e Validar

1. Gravar em `output_dir/publicacao/descricao.md`.
2. Rodar a checagem final contra `checklists/publicacao-podcast.md` e `checklists/output-quality.md`.
3. Confirmar Veto Conditions abaixo (sem links = nao publica; sem travessao).

---

## Output Format

Gravar em `output_dir/publicacao/descricao.md`:

```markdown
# Descricao · {Programa} · EP {id} · {Convidado}

## Gancho
{2 a 3 linhas, keyword principal nos primeiros 150 caracteres}

## Capitulos
00:00 {capitulo 0}
{mm:ss} {capitulo 1}
{mm:ss} {capitulo 2}
...

## Links do episodio

CONVIDADO · {Convidado}
- Instagram: {url confirmada}
- {Oferta/livro/evento}: {url confirmada}

sua comunidade · nossa comunidade
- {beneficio curto}: {url confirmada}

PATROCINADOR · {patrocinador}
- {rotulo}: {url confirmada}

AGENCIA PARCEIRA · {agencia}
- {rotulo}: {url confirmada}

FRED MARTINS
- Instagram: {url confirmada}

## sua comunidade
{CTA com beneficio concreto} → {url confirmada}

## Hashtags
#{tag1} #{tag2} #{tag3}

---
SEO/GEO: keyword principal = "{keyword}". Entidades cobertas: {lista}.
```

Bloco final de relatorio (no console, nao no arquivo):

```markdown
## Resumo da Descricao

**Episodio:** {id} · {Convidado}
**Links confirmados:** {n} (de {m} candidatos extraidos)
**Faltando ({{USER_NAME}} deixou em branco):** {lista ou "nenhum"}
**Keyword principal:** {keyword}
**Capitulos:** {n}
**Arquivo:** output_dir/publicacao/descricao.md
```

---

## Veto Conditions

- NEVER gerar a descricao sem os links confirmados pelo {{USER_NAME}} (no minimo sua comunidade + 1 link do convidado).
- NEVER inventar, adivinhar ou completar uma URL. Se o {{USER_NAME}} deixou em branco, o destino sai da descricao (ou fica como `[falta link]` apenas no relatorio, nunca no arquivo final publicavel).
- NEVER pular a fase de extracao do roteiro HTML, os candidatos vem do Mapa de CTAs e do Stack final.
- NEVER usar travessao (em dash, o traco longo) em nenhuma parte do texto.
- NEVER comecar os capitulos sem `00:00`, nem fora de ordem cronologica.
- NEVER usar clickbait no gancho que o conteudo do episodio nao entrega.
- NEVER misturar a identidade do convidado ou dos parceiros (manter exatamente como no roteiro).

---

## Completion Criteria

- [ ] Links/CTAs candidatos extraidos do roteiro HTML (Mapa de CTAs + Stack final + handles)
- [ ] Elicit executado: {{USER_NAME}} confirmou/editou os links, so foi pedido o que faltava
- [ ] Gancho de 2-3 linhas com keyword principal nos primeiros 150 caracteres
- [ ] Capitulos com timestamps gerados do content-map, comecando em 00:00 e em ordem
- [ ] Bloco de LINKS preenchido SO com links confirmados, na ordem de conversao
- [ ] CTA sua comunidade presente com beneficio + link confirmado
- [ ] Hashtags (3 a 5) e keywords SEO/GEO aplicadas
- [ ] Nenhum travessao no texto final
- [ ] Arquivo gravado em output_dir/publicacao/descricao.md
- [ ] Checagem rodada contra checklists/publicacao-podcast.md e checklists/output-quality.md
