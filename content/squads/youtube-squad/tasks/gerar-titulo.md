---
task: gerarTitulo()
responsavel: "@brian-dean"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: content_map
    tipo: file
    origem: output_dir/analise/content-map.md
    obrigatorio: true
  - campo: convidado
    tipo: string
    origem: episodio.yaml ou User Input
    obrigatorio: false
  - campo: keyword_principal
    tipo: string
    origem: content-map ou User Input
    obrigatorio: false

Saida:
  - campo: titulo_package
    tipo: file
    destino: output_dir/publicacao/titulo.md
    persistido: true

Checklist:
  - "[ ] Keyword principal definida a partir do content-map"
  - "[ ] 5 titulos gerados cobrindo 5 formulas distintas"
  - "[ ] Cada titulo dentro de 60-70 caracteres"
  - "[ ] 1 principal + 2 alternativos A/B escolhidos com justificativa"
  - "[ ] Nenhum titulo promete o que o episodio nao entrega"
---

# Task: Gerar Titulo

**Task ID:** YT-PUB-06
**Version:** 1.0.0
**Command:** `*gerar-titulo`
**Agent:** Brian Dean (brian-dean)
**Purpose:** Produzir o titulo do video otimizado para busca (SEO) e descoberta (GEO, sugeridos, browse), com a keyword principal e o nome do convidado quando relevante, em no maximo 60-70 caracteres, mais 2 alternativos para teste A/B.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| content_map | file | `output_dir/analise/content-map.md` | Yes | Mapa de conteudo gerado pela task `*analisar-conteudo` com angulo e temas |
| convidado | string | `episodio.yaml` ou User Input | No | Nome e, quando houver, sobrenome/handle do convidado do episodio |
| keyword_principal | string | content-map ou User Input | No | Termo de busca alvo; se ausente, deve ser derivado do content-map na Phase 1 |
| canal | enum | `episodio.yaml` ou User Input | No | `{{USER_NAME}}` ou `Infinity Cast` (define tom e quanto o convidado pesa) |
| mercado | enum | User Input | No | `Portugal`, `Brasil` ou `PT/BR`; afeta vocabulario e termos de busca |

---

## Preconditions

- `output_dir/analise/content-map.md` existe e contem o angulo central e os temas do episodio
- O angulo do episodio esta definido (titulo nao pode prometer fora do que o content-map registra)
- Se `keyword_principal` nao foi fornecida, o content-map tem material suficiente para deriva-la
- O nome do convidado (se houver) esta confirmado, sem erro de grafia

---

## Referencia de Campeoes

Estude estes padroes de titulo de alto CTR e boa indexacao antes de escrever. Eles juntam keyword no inicio + tensao/beneficio + (quando faz sentido) nome reconhecivel:

1. **"Como construir uma audiencia em Portugal do zero (em 2026)"**: How-to + keyword no inicio + ancora de tempo: serve busca e sugeridos ao mesmo tempo.
2. **"5 erros que destroem um podcast antes do episodio 10"**: Numero + custo implicito: especificidade que cria loop aberto sem ser clickbait.
3. **"O dinheiro que ninguem te conta sobre empreender em Portugal"**: Curiosidade + keyword: promete um conhecimento exclusivo que o episodio realmente entrega.
4. **"{Convidado}: a verdade sobre escalar negocio em PT e BR"**: Autoridade pelo nome do convidado primeiro: ganha buscas pelo nome dele e pela pauta.
5. **"Vale a pena empreender em Portugal hoje? (resposta honesta)"**: Pergunta direta que o publico ja digita na busca: alinha intencao de pesquisa com a resposta do episodio.

---

## Execution Phases

### Phase 1: Definir Keywords (SEO + GEO)
1. Ler `output_dir/analise/content-map.md` e extrair o angulo central e os 3 a 5 temas dominantes.
2. Definir a **keyword principal**: o termo que o publico-alvo digitaria na busca para chegar neste episodio (intencao de pesquisa real, nao jargao interno).
3. Listar 3 a 5 **keywords secundarias** (variacoes, termos relacionados, nome do convidado, nome da pauta) para informar titulos e a futura descricao.
4. Validar a keyword principal contra o mercado (`Portugal`, `Brasil` ou `PT/BR`): preferir o termo que o publico daquele mercado realmente usa.
5. Decidir se o **nome do convidado** entra no titulo: entra quando o convidado tem busca propria, autoridade reconhecida ou e a razao do episodio existir; fica de fora quando a pauta vende mais que o nome.

### Phase 2: Gerar 5 Titulos (5 formulas)
Gerar exatamente 5 titulos, um por formula, cada um carregando a keyword principal o mais a esquerda possivel:
1. **Pergunta:** transforma a keyword na duvida que o publico ja digita (ex.: "Vale a pena ... ?").
2. **Numero:** lista ou quantidade concreta (ex.: "5 erros ...", "3 verdades ...").
3. **Beneficio:** promete o ganho claro que o episodio entrega (ex.: "Como ... sem ...").
4. **Curiosidade:** abre um loop honesto, sem esconder o tema (ex.: "O que ninguem te conta sobre ...").
5. **Autoridade:** apoia no convidado ou na credencial (ex.: "{Convidado} explica como ...").

Para cada titulo:
- Manter entre 60 e 70 caracteres (incluindo espacos). Contar os caracteres e registrar o numero.
- Colocar a keyword principal nas primeiras palavras sempre que natural (peso de SEO e leitura no mobile).
- Aplicar a regra de escrita do sua comunidade: portugues do Brasil, sem travessao (em dash). Usar dois-pontos, parenteses, virgula ou reescrever.

### Phase 3: Escolher Principal + 2 Alternativos A/B
1. Avaliar os 5 titulos em 4 dimensoes (1 a 5 cada):
   - **Relevancia de busca:** a keyword principal aparece cedo e casa com a intencao de pesquisa?
   - **Atratividade (CTR):** cria curiosidade ou promessa que faz parar e clicar?
   - **Honestidade:** o episodio entrega exatamente o que o titulo promete?
   - **Clareza no mobile:** le-se bem nos primeiros caracteres, sem corte que mate o sentido?
2. Escolher o **titulo principal** (maior pontuacao total, com a melhor combinacao de busca + clique honesto).
3. Escolher **2 alternativos** para teste A/B: devem ser de formulas/angulos diferentes do principal (ex.: principal por beneficio, variantes por pergunta e por numero), para que o teste compare hipoteses distintas, nao sinonimos.
4. Escrever a **justificativa**: por que o principal venceu, qual hipotese cada alternativo testa e em que cenario voce trocaria.

---

## Output Format

Escrever em `output_dir/publicacao/titulo.md`:

```markdown
# Titulo do Episodio

**Episodio:** {id}
**Canal:** {{{USER_NAME}} | Infinity Cast}
**Convidado:** {nome ou "sem convidado"}
**Mercado:** {Portugal | Brasil | PT/BR}

## Keyword

- **Principal:** {keyword principal}
- **Secundarias:** {kw2}, {kw3}, {kw4}, {kw5}

## Titulo Principal

> {titulo escolhido}

- Formula: {pergunta | numero | beneficio | curiosidade | autoridade}
- Caracteres: {NN} (limite 70)

## Alternativos para A/B

1. {alternativo A}, formula: {tipo}, {NN} chars, hipotese: {o que testa}
2. {alternativo B}, formula: {tipo}, {NN} chars, hipotese: {o que testa}

## Justificativa

{Por que o principal venceu nas 4 dimensoes, qual hipotese cada alternativo testa
e em que cenario o titulo seria trocado.}

## Banco completo (5 titulos)

| # | Titulo | Formula | Chars | Relevancia | CTR | Honestidade | Mobile | Total |
|---|--------|---------|-------|------------|-----|-------------|--------|-------|
| 1 | {titulo} | {formula} | {NN} | X | X | X | X | XX |
| 2 | {titulo} | {formula} | {NN} | X | X | X | X | XX |
| 3 | {titulo} | {formula} | {NN} | X | X | X | X | XX |
| 4 | {titulo} | {formula} | {NN} | X | X | X | X | XX |
| 5 | {titulo} | {formula} | {NN} | X | X | X | X | XX |
```

---

## Veto Conditions

- NEVER usar clickbait que o episodio nao entrega: toda promessa do titulo precisa estar no content-map.
- NEVER passar de 70 caracteres em nenhum titulo (principal ou alternativos).
- NEVER usar travessao (em dash, o traco longo) em nenhum titulo ou texto deste arquivo.
- NEVER inventar dados, numeros ou citacoes do convidado que nao constem do content-map.
- NEVER entregar menos de 5 titulos no banco completo, ou menos de 2 alternativos A/B.
- NEVER errar a grafia do nome do convidado nem traduzir um nome proprio.
- NEVER esconder o tema atras de curiosidade vazia que nao deixe claro do que o episodio trata.

---

## Completion Criteria

- [ ] Keyword principal definida e justificada a partir do content-map
- [ ] 3 a 5 keywords secundarias listadas
- [ ] 5 titulos gerados, um por formula (pergunta, numero, beneficio, curiosidade, autoridade)
- [ ] Cada titulo dentro de 60-70 caracteres, com contagem registrada
- [ ] Titulo principal escolhido com pontuacao nas 4 dimensoes
- [ ] 2 alternativos A/B de formulas diferentes do principal
- [ ] Justificativa escrita (porque venceu, hipotese de cada alternativo)
- [ ] Decisao sobre o nome do convidado registrada
- [ ] Arquivo salvo em `output_dir/publicacao/titulo.md` no formato do template
- [ ] Sem travessao e em portugues do Brasil
