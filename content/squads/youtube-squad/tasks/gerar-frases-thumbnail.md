---
task: gerarFrasesThumbnail()
responsavel: "@paddy-galloway"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: content_map
    tipo: string
    origem: analise/content-map.md
    obrigatorio: true
  - campo: nicho
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: convidado
    tipo: string
    origem: episodio.yaml
    obrigatorio: true

Saida:
  - campo: frases_thumbnail
    tipo: string
    destino: output_dir/thumbnail/FRASES.md
    persistido: true

Checklist:
  - "[ ] 8-10 candidatas geradas em angulos distintos (numero/metodo, tensao fe x dinheiro, acusacao/identidade, jornada)"
  - "[ ] Cada candidata com palavra-chave entre colchetes e no maximo ~5 palavras grandes"
  - "[ ] Candidatas ranqueadas por CTR potencial com gatilho explicado (curiosity gap, tabu, numero)"
  - "[ ] TOP 3 + recomendacao A/B entregues"
  - "[ ] Nenhuma afirmacao sensivel (teologia da prosperidade exploratoria) na lista final"
---

# Task: Gerar Frases de Thumbnail

**Task ID:** YT-PUB-05
**Version:** 1.0.0
**Command:** `*frases-thumbnail`
**Agent:** Paddy Galloway (paddy-galloway) com modelagem de formato de Matt Gielen (matt-gielen)
**Purpose:** Produzir 3 variacoes de frase de impacto para a thumbnail no padrao validado do Infinity Cast (ex.: `E PECADO [PROSPERAR]?` do EP001), cada uma com a palavra-chave entre colchetes (que vai na caixa laranja sobre fundo preto) e no maximo cinco palavras grandes, ranqueadas por potencial de CTR.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| content_map | string | `analise/content-map.md` (saida de `*analisar-conteudo`) | Sim | Deve conter angulo central + lista de ganchos/dores do episodio |
| nicho | string | User prompt | Sim | Nicho do episodio (ex.: fe x dinheiro, empreendedorismo, imigracao PT) |
| convidado | string | `episodio.yaml` (campo pessoas) | Sim | Nome do convidado e papel (ex.: Pastor, especialista) |
| angulo | string | `content-map.md` ou User prompt | Nao | Angulo dominante a priorizar, se ja decidido pelo Chief |
| numeros | string | `content-map.md` ou produto do convidado | Nao | Quantificacoes disponiveis (ex.: 40 inimigos, 147 leis, 6 paises) |
| mercado | enum | User prompt | Nao | BR, PT ou ambos (PT exige tom mais sobrio, ver R8/dor #4) |

---

## Preconditions

- `analise/content-map.md` existe e foi gerado por `*analisar-conteudo`; angulo central e ganchos identificados.
- Nicho e convidado confirmados (a frase precisa bater na dor real do publico, nao em achismo).
- Dossie de modelagem do episodio (ranking de headlines + plano A/B) disponivel quando houver; na ausencia, usar `data/referencias-cross-cultural.yaml` e `data/thumbnail-briefing.yaml` secao 6 como base.

---

## Padrao de Referencia (EP001)

Estudar o ranking validado de frases do EP001 (Pastor Adeildo Silva) antes de gerar. Cada caso prova um gatilho:

1. **`E PECADO [PROSPERAR]?`** (campea) - 3 palavras, pergunta-tabu pura, bate na dor #1 universal (culpa fe x ambicao), replica o padrao Deive Leonardo (10,3 mi subs). Como pergunta vira debate, nao venda exploratoria.
2. **`DEUS QUER VOCE [RICO]?`** - curiosity gap maximo, dor #1, gera comentario.
3. **`VOCE ORA E CONTINUA [QUEBRADO]`** - dor #2 (oro e continuo quebrado) + espelho identitario, altissimo CTR.
4. **`OS 40 INIMIGOS DA [PROSPERIDADE]`** - numero (R6) + casa com o produto do convidado. A mais segura.
5. **`PROSPERAR NA ERA DA [IA]`** - angulo inedito (R10), menos dor mas otima para variacao de teste.

Regras de formato modeladas (Matt Gielen, secao 2 do dossie): R4 (1 palavra-gatilho destacada), R6 (numero aumenta CTR), R7 (pergunta-tabu / curiosity gap performa no nicho fe+dinheiro), R8 (cross-cultural PT pede tom premium, nunca clickbait gritante).

---

## Execution Phases

### Fase 1: Geracao por Angulos Distintos
1. Ler o angulo central e os ganchos/dores em `content-map.md`; mapear quais dores cruzadas o episodio ativa.
2. Gerar **8 a 10 candidatas**, cobrindo OBRIGATORIAMENTE os quatro angulos abaixo (minimo 2 por angulo):
   - **Numero / metodo:** quantificacao do produto ou da jornada (ex.: `OS 40 INIMIGOS DA [PROSPERIDADE]`, `AS 147 LEIS DA [RIQUEZA]`). Usa R6.
   - **Tensao fe x dinheiro (ou tensao central do nicho):** o cruzamento exato do episodio em forma de pergunta (ex.: `FE [DA] DINHEIRO?`, `DEUS QUER VOCE [RICO]?`). Usa R7.
   - **Acusacao / identidade com "voce":** espelho identitario que confronta o espectador (ex.: `VOCE ORA E CONTINUA [QUEBRADO]`). Alto CTR por reconhecimento pessoal.
   - **Jornada:** transformacao aspiracional do convidado (ex.: `DO [NADA] A 6 PAISES`). Numero + arco narrativo.
3. Para CADA candidata:
   - Marcar a **palavra-chave entre colchetes** (sera a unica em laranja na caixa, sobre o preto).
   - Garantir **no maximo cinco palavras grandes** (palavras curtas como artigos/preposicoes nao contam como peso visual, mas evitar poluir).
   - Rodar o teste "eu pararia o scroll?": se a frase nao gera curiosidade ou reconhecimento imediato, descartar ou reescrever.

### Fase 2: Ranqueamento por CTR Potencial
1. Pontuar cada candidata em 4 dimensoes (1 a 5 cada):
   - **Curiosity gap:** abre um loop que so o clique fecha?
   - **Forca da dor:** bate em uma dor cruzada real (content-map) e nao em tema generico?
   - **Brevidade / leitura no mobile:** legivel em menos de 1 segundo, dentro do limite de ~5 palavras grandes?
   - **Diferenciacao - risco:** soa premium e debate (pergunta) e NAO promessa exploratoria? (penalizar afirmacao sensivel)
2. Para cada candidata, nomear o **gatilho dominante**: curiosity gap, tabu (pergunta-tabu), numero, ou espelho identitario.
3. Somar e ranquear. Empate desempata pela menor contagem de palavras e pelo menor risco de tom.

### Fase 3: TOP 3 + Recomendacao A/B
1. Selecionar as **3 frases melhor pontuadas**, garantindo diversidade de angulo (idealmente nao todas do mesmo angulo).
2. Montar a recomendacao A/B no padrao do dossie:
   - **Thumb A (curiosidade-tabu, maximo CTR):** a frase mais forte em curiosity gap/tabu.
   - **Thumb B (autoridade/metodo, lead qualificado):** a frase de numero/metodo, fallback seguro para o publico PT.
3. Escrever o racional de cada escolha e a recomendacao de rodada (YouTube Test & Compare, se elegivel, ou troca manual em 48h comparando CTR/retencao).
4. Persistir tudo em `output_dir/thumbnail/FRASES.md` com TOP 3, banco completo (8-10) e plano A/B.

---

## Output Format

Arquivo: `output_dir/thumbnail/FRASES.md`

```markdown
# Frases de Thumbnail - {id} ({convidado})

**Nicho:** {nicho}
**Mercado:** {BR / PT / ambos}
**Angulo central:** {do content-map}

## TOP 3 (ranqueadas)

| Rank | Frase | Palavra-chave (laranja) | Angulo | Gatilho | Curiosity | Dor | Brevidade | Risco-inv | Total |
|------|-------|-------------------------|--------|---------|-----------|-----|-----------|-----------|-------|
| 1 | `{FRASE [CHAVE]?}` | {CHAVE} | {angulo} | {gatilho} | X | X | X | X | XX |
| 2 | ... | ... | ... | ... | X | X | X | X | XX |
| 3 | ... | ... | ... | ... | X | X | X | X | XX |

## Recomendacao A/B

- **Thumb A (curiosidade-tabu, maximo CTR):** `{frase 1}` - {racional}
- **Thumb B (autoridade/metodo, lead qualificado):** `{frase de numero/metodo}` - {racional, fallback PT}
- **Como rodar:** {YouTube Test & Compare ou troca manual 48h, metrica = CTR + retencao}

## Banco completo (8-10 candidatas)

1. `{FRASE [CHAVE]}` - angulo {x} - gatilho {y} - nota {NN}
2. ...
...

## Riscos / mitigacao

- Tom teologia da prosperidade (dor #4, forte em PT): usar pergunta, nunca afirmacao de "fe garante riqueza".
- Nao usar testemunho sensivel do convidado como isca de clique.
```

---

## Veto Conditions

- NEVER entregar frase com mais de ~5 palavras grandes (quebra a leitura no mobile e o padrao de thumbnail).
- NEVER entregar frase sem palavra-chave destacada entre colchetes (a caixa laranja exige UMA palavra-gatilho).
- NEVER usar afirmacao sensivel que prometa riqueza pela fe (ex.: `ESSE PASTOR VAI TE FAZER RICO`); quando o tema for fe x dinheiro, usar pergunta-tabu, nunca afirmacao exploratoria.
- NEVER usar testemunho intimo do convidado (violencia, doenca, perdao) como isca de clique.
- NEVER usar travessao (em dash) em qualquer frase ou texto do arquivo.
- NEVER entregar menos de 8 candidatas no banco completo nem menos de 3 no TOP.

---

## Completion Criteria

- [ ] 8 a 10 candidatas geradas cobrindo os 4 angulos (numero/metodo, tensao fe x dinheiro, acusacao/identidade, jornada)
- [ ] Toda candidata com palavra-chave entre colchetes e no maximo ~5 palavras grandes
- [ ] Cada candidata pontuada nas 4 dimensoes e com gatilho dominante nomeado
- [ ] TOP 3 ranqueadas com diversidade de angulo
- [ ] Recomendacao A/B (Thumb A tabu + Thumb B metodo) com racional e modo de rodar
- [ ] Nenhuma afirmacao sensivel / teologia da prosperidade exploratoria na lista
- [ ] Riscos e mitigacao documentados
- [ ] Saida gravada em `output_dir/thumbnail/FRASES.md` no formato do template, sem travessao
