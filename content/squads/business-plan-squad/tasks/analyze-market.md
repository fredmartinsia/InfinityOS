# Task: analyze-market

> **Análise de mercado completa: TAM/SAM/SOM (método MIT) + concorrentes (método Porter).**

## Quando usar
- O usuário precisa dimensionar o mercado e mapear concorrentes
- Standalone (sem BP completo) ou como parte do workflow `create-business-plan`

## Pré-requisitos
- Negócio descrito (tipo, oferta, geografia)
- Beachhead market hipotético definido (mesmo que ainda não validado)

## Workflow

### Etapa 1 — Sizing (Bill Aulet)
Acionar `/bill-aulet`. Ele vai:
1. Confirmar o beachhead market (se ainda não definido, ajuda a escolher)
2. Definir End User Profile (não confundir com persona)
3. Calcular TAM via 2 métodos:
   - **Top-down:** dados secundários de mercado (relatórios setoriais, estatísticas governamentais)
   - **Bottom-up:** estimativa unidade por unidade (N de clientes × ticket médio anual)
4. Triangular os dois resultados — discrepância grande = erro de premissa
5. Definir SAM (serviceable addressable — quem o negócio consegue atender com modelo atual)
6. Definir SOM (serviceable obtainable — fatia realista nos primeiros 3-5 anos)
7. Listar os "próximos 10 clientes" — nomes ou perfis específicos

### Etapa 2 — Estrutura competitiva (Michael Porter)
Acionar `/michael-porter`. Ele vai:
1. Aplicar as **5 Forças** ao setor:
   - Ameaça de novos entrantes (barreiras de entrada)
   - Poder de barganha dos fornecedores
   - Poder de barganha dos compradores
   - Ameaça de produtos substitutos
   - Rivalidade entre competidores existentes
2. Avaliar atratividade estrutural do setor (alta / média / baixa)
3. Listar 5-10 concorrentes diretos com:
   - Modelo de negócio
   - Posicionamento (Cost / Differentiation / Focus)
   - Tamanho estimado
   - Pontos fortes e fracos
4. Mapear a cadeia de valor do negócio do usuário
5. Recomendar estratégia genérica defensável (alerta para "stuck in the middle")

### Etapa 3 — Consolidação (Business Plan Chief)
Entregar relatório "Market Analysis Dossier" com:
- **Seção 1 — Tamanho de Mercado:** TAM/SAM/SOM com método mostrado
- **Seção 2 — Beachhead Market:** definição + End User Profile + DMU
- **Seção 3 — Estrutura Setorial:** 5 Forças + atratividade
- **Seção 4 — Mapa Concorrencial:** 5-10 concorrentes analisados
- **Seção 5 — Cadeia de Valor:** onde o negócio adiciona valor único
- **Seção 6 — Estratégia Genérica Recomendada:** com trade-offs explícitos
- **Seção 7 — Próximos 10 Clientes:** lista nominal ou por perfil específico

## Tempo estimado
- 2-4 horas (mercado simples) a 6-8 horas (mercado complexo internacional)

## Quality Gates
- [ ] TAM tem método bottom-up + top-down (não só top-down)
- [ ] Beachhead market é específico (não "todo mundo que pode comprar")
- [ ] Concorrentes têm pontos fracos identificados (não só pontos fortes)
- [ ] Estratégia genérica é UMA (não híbrida)
- [ ] Próximos 10 clientes são acionáveis (nomes ou perfis específicos)
