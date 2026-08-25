---
task: decisaoEstrategica()
responsavel: "@derral-eves, @matt-gielen, @roberto-blake"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: duvida
    tipo: string
    origem: User Input
    obrigatorio: true
  - campo: contexto_canal
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: decisao_fundamentada
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Duvida estrategica reformulada como escolha entre opcoes concretas"
  - "[ ] Impacto algoritmico avaliado por opcao (@derral-eves)"
  - "[ ] Casos reais de canais para cada caminho, com links (@matt-gielen)"
  - "[ ] Impacto em monetizacao avaliado por opcao (@roberto-blake)"
  - "[ ] Recomendacao unica com pros/contras e condicoes de reversao"
---

# Task: Decisao Estrategica

**Task ID:** YT-STR-07
**Version:** 1.0.0
**Command:** `*decisao-estrategica`
**Agent:** Derral Eves (derral-eves), Matt Gielen (matt-gielen) e Roberto Blake (roberto-blake)
**Purpose:** Resolver uma duvida estrategica de canal (ex: lancar o podcast junto ou separado do canal {{USER_NAME}}, qual frequencia sustentar, vertical x horizontal, ingles x portugues) com uma recomendacao unica e fundamentada. A decisao sai sustentada por tres leituras independentes (algoritmo, modelagem de mercado, monetizacao) e por casos reais de canais que escolheram cada caminho, nunca por achismo.

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| duvida | string | User prompt | Yes | A duvida estrategica enunciada como escolha (ex: "podcast no mesmo canal do {{USER_NAME}} ou em canal proprio?", "publicar 1x ou 2x por semana?", "apostar em shorts verticais ou so longos?") |
| contexto_canal | string | User prompt | Yes | Estado atual do canal: nome, nicho, inscritos, frequencia atual, formatos, regiao (BR/PT/cross), e o objetivo de 6 a 12 meses |
| restricoes | string | User prompt | No | Limites reais (equipe, orcamento, tempo de gravacao, equipamentos, capacidade de edicao) |
| horizonte | string | User prompt | No | Prazo da decisao (curto: 3 meses; medio: 6 a 12 meses; longo: 12+ meses) |
| reversibilidade_desejada | string | User prompt | No | Se o {{USER_NAME}} quer um caminho facilmente reversivel ou aceita uma aposta de difícil volta |

---

## Preconditions

- A duvida vem enunciada como uma escolha entre opcoes concretas; se vier vaga ("o que faco com o podcast?"), o `@youtube-chief` reformula em opcoes A/B (ou A/B/C) antes de seguir
- Contexto do canal preenchido o suficiente para localizar canais comparaveis (mesmo nicho, faixa de inscritos parecida, regiao projetavel)
- Pesquisa previa obrigatoria: nenhuma das tres leituras sai sem o scan de canais do `@youtube-researcher` (premissa inegociavel do squad: nada comeca em estrategia sem passar por pesquisa)
- A regiao do canal esta definida; se for cross-cultural (BR/USA como referencia para projetar em PT/EU), o scan cobre os dois mercados

---

## Duvidas Estrategicas Recorrentes (mapa de referencia)

Use este mapa como ancora antes de avaliar a duvida especifica. Cada eixo tem uma logica dominante e um trade-off conhecido:

1. **Podcast junto x separado do canal**: junto soma watch time e aproveita a base existente, mas dilui o sinal de tema para o algoritmo e pode confundir a audiencia do canal principal; separado constroi identidade limpa, porem parte do zero em descoberta. O eixo decisivo costuma ser quanto o tema do podcast se sobrepoe ao do canal mae.
2. **Frequencia (1x x 2x+ por semana)**: mais frequencia acelera aprendizado do algoritmo e ocupa mais espaco no feed, mas so vale se a qualidade nao cair; consistencia sustentavel vence pico insustentavel.
3. **Vertical x horizontal (shorts x longos)**: shorts puxam alcance e novos inscritos, longos sustentam watch time e monetizacao; o erro comum e tratar como rivais em vez de funil (short atrai, longo retem e monetiza).
4. **Idioma (portugues x ingles)**: ingles abre teto de audiencia global, mas joga o canal contra uma concorrencia muito maior e enfraquece a conexao com a base PT/BR; portugues protege a relevancia local e o CPM de nichos premium em PT/EU.
5. **Nicho focado x amplo**: foco acelera autoridade e recomendacao, amplitude protege contra esgotamento de pauta; canal novo quase sempre ganha com foco antes de abrir.
6. **Cadencia de upload fixa x oportunista**: grade fixa treina audiencia e algoritmo; oportunista surfa picos de busca, mas perde previsibilidade de retencao.

A leitura so vale quando os casos usados sao do MESMO nicho e de regiao comparavel ou projetavel. Caso de canal gigante (movido por marca, nao pela escolha) nao prova a escolha.

---

## Execution Phases

### Phase 0: Reformulacao da Duvida (@youtube-chief)
1. Converter a duvida em opcoes concretas e mutuamente comparaveis: Opcao A, Opcao B (e C se existir um meio-termo real)
2. Explicitar o objetivo contra o qual cada opcao sera medida (alcance, watch time, autoridade, monetizacao, sustentabilidade de producao)
3. Acionar o scan do `@youtube-researcher`: mapear de 8 a 15 canais do nicho que escolheram cada caminho, com nome, link, faixa de inscritos, frequencia, formatos e regiao; para cross-cultural, montar conjunto BR e conjunto USA
4. Entregar a lista bruta de candidatos para as tres leituras, sem julgar ainda (coleta separada de analise)

### Phase 1: Impacto Algoritmico (@derral-eves)
1. Avaliar como cada opcao afeta os sinais que o YouTube usa para distribuir: consistencia de tema do canal, watch time agregado, CTR esperado, velocidade inicial de impressoes e retencao por sessao
2. Para "junto x separado": medir o custo de diluir o sinal de tema de um canal versus o custo de partir do zero em descoberta em um canal novo
3. Para "frequencia": projetar o efeito no ritmo de aprendizado do algoritmo e o risco de canibalizar impressoes entre videos proximos
4. Para "vertical x horizontal": ler o papel de cada formato no funil (short como porta de entrada, longo como retencao e monetizacao) e o efeito no perfil de audiencia recomendada
5. Apontar, por opcao, o principal ganho e o principal risco algoritmico, ancorando em como canais comparaveis se comportaram apos a mesma escolha

### Phase 2: Modelagem de Casos Reais (@matt-gielen)
1. A partir do scan, isolar canais especificos que escolheram cada caminho (nao basta citar; precisa do canal concreto com link)
2. Para cada caso, coletar metricas observaveis: faixa de inscritos antes e depois da escolha, frequencia, e quando possivel a trajetoria de crescimento apos a decisao (acelerou, estagnou, regrediu)
3. Buscar minimo de 3 casos por opcao (idealmente do MESMO nicho); para cross-cultural, casos BR e USA contam, desde que projetaveis para PT/EU
4. Registrar pelo menos 1 contra-exemplo quando existir (canal que fez a escolha e se deu mal), fortalece a decisao, nao enfraquece
5. Cruzar com `data/formatos-validados.yaml` e `data/referencias-cross-cultural.yaml`: a escolha ja consta como validada? Os casos novos confirmam ou contradizem o registro?

### Phase 3: Impacto em Monetizacao (@roberto-blake)
1. Avaliar como cada opcao afeta as fontes de receita: AdSense (CPM/RPM do nicho e da regiao), patrocinios e brand deals, produtos proprios e membros/comunidade
2. Para "junto x separado": comparar manter uma base monetizavel unica versus construir duas audiencias com potenciais de receita distintos
3. Para "idioma" e "regiao": ler o efeito no CPM (PT/EU x global) e na atratividade para patrocinadores locais versus internacionais
4. Para "frequencia" e "formato": projetar o custo de producao por opcao contra o retorno esperado, sinalizando o ponto de esgotamento (quando produzir mais derruba a margem)
5. Apontar, por opcao, o cenario de receita de 6 a 12 meses e o principal risco de monetizacao

### Phase 4: Sintese e Recomendacao (@youtube-chief)
1. Reunir as tres leituras (algoritmo, casos, monetizacao) e checar onde convergem e onde divergem
2. Quando as leituras divergem, explicitar o trade-off para o {{USER_NAME}} (ex: a opcao melhor para alcance e a pior para monetizacao no curto prazo) em vez de esconder a tensao
3. Emitir UMA recomendacao clara (Opcao A, B ou C), com o fundamento de uma linha ancorado nos dados das tres leituras
4. Listar pros e contras de cada opcao lado a lado, para o {{USER_NAME}} ver o que abre mao ao escolher
5. Aplicar leitura cross-cultural quando a regiao exigir: o que os casos BR/USA indicam sobre o comportamento esperado em PT/EU
6. Definir condicoes de reversao e o gatilho de revisao (que metrica, em quanto tempo, dispara reavaliar a decisao)

---

## Output Format

```markdown
## Decisao Estrategica, Recomendacao

**Duvida:** {duvida}
**Canal / contexto:** {contexto_canal}
**Objetivo medido:** {objetivo}
**Horizonte:** {horizonte}

### Opcoes em comparacao
- **Opcao A:** {descricao}
- **Opcao B:** {descricao}
- **Opcao C (se houver):** {descricao}

### Recomendacao: {Opcao A | B | C}
**Fundamento (1 linha):** {por que, ancorado nas tres leituras}

### Pros e Contras (lado a lado)

| Eixo | Opcao A | Opcao B |
|------|---------|---------|
| Algoritmo (@derral-eves) | {ganho / risco} | {ganho / risco} |
| Modelagem de mercado (@matt-gielen) | {o que os casos mostram} | {o que os casos mostram} |
| Monetizacao (@roberto-blake) | {cenario de receita} | {cenario de receita} |
| Custo / esforco de producao | {alto/medio/baixo} | {alto/medio/baixo} |
| Reversibilidade | {facil/dificil} | {facil/dificil} |

### Casos Reais por Opcao (minimo 3 por caminho)

**Quem escolheu a Opcao A:**
| # | Canal | Link | Inscritos | Resultado apos a escolha | Regiao |
|---|-------|------|-----------|--------------------------|--------|
| 1 | {canal} | {link} | {faixa} | acelerou/estagnou/regrediu | BR/USA/PT |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

**Quem escolheu a Opcao B:**
| # | Canal | Link | Inscritos | Resultado apos a escolha | Regiao |
|---|-------|------|-----------|--------------------------|--------|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

### Contra-exemplo (se existir)
{canal que fez a escolha recomendada e se deu mal + link + por que falhou}

### Leitura Cross-Cultural (BR/USA -> PT/EU)
{o que os casos indicam sobre o comportamento esperado da audiencia PT/EU}

### Trade-off principal (o que o {{USER_NAME}} abre mao)
{a tensao mais importante entre as leituras, dita sem rodeio}

### Condicoes de reversao e gatilho de revisao
- **Reverter se:** {condicao concreta}
- **Revisar a decisao quando:** {metrica} {nao atingir/cair abaixo de} {limiar} em {prazo}

### Recomendacao final (@youtube-chief)
{1 paragrafo de sintese acionavel para o {{USER_NAME}}}
```

---

## Veto Conditions

- NEVER entregar uma recomendacao sem casos reais de canais para cada opcao; minimo de 3 casos por caminho, com links verificaveis, ou a decisao nao sai
- NEVER decidir sem as tres leituras (algoritmo, casos, monetizacao); uma leitura faltando invalida a sintese
- NEVER pular o scan previo do `@youtube-researcher`, pesquisa primeiro, decisao depois
- NEVER usar caso de canal gigante (resultado movido por marca, nao pela escolha) como prova de que a escolha funciona para canal em crescimento
- NEVER esconder o trade-off quando as leituras divergem; a tensao tem que aparecer para o {{USER_NAME}}
- NEVER projetar BR/USA -> PT/EU sem registrar a logica cross-cultural; nao basta copiar o numero
- NEVER entregar mais de uma recomendacao final ("depende"): a task existe para decidir; o "depende" vira condicao de reversao, nao indecisao
- NEVER usar travessao (em dash) em nenhuma parte do output; use ponto, virgula, dois-pontos ou parenteses

---

## Completion Criteria

- [ ] Duvida reformulada como escolha entre opcoes concretas e comparaveis (`@youtube-chief`)
- [ ] Scan de canais que escolheram cada caminho concluido (`@youtube-researcher`)
- [ ] Impacto algoritmico avaliado por opcao, com ganho e risco principais (`@derral-eves`)
- [ ] Minimo de 3 casos reais por opcao, cada um com link e resultado apos a escolha (`@matt-gielen`)
- [ ] Contra-exemplo registrado quando existir
- [ ] Impacto em monetizacao avaliado por opcao, com cenario de 6 a 12 meses (`@roberto-blake`)
- [ ] Cruzamento com `data/formatos-validados.yaml` e `data/referencias-cross-cultural.yaml` registrado
- [ ] Leitura cross-cultural BR/USA -> PT/EU aplicada quando a regiao exigir
- [ ] Recomendacao unica emitida, com pros/contras lado a lado e fundamento data-driven
- [ ] Trade-off principal explicitado e condicoes de reversao definidas
- [ ] Sintese final do `@youtube-chief` entregue
- [ ] Output formatado conforme o template, sem travessao
