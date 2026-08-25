# Squad: YouTube, Consultoria, Pesquisa e Modelagem de Canais

> Squad robusto e replicável de 6 especialistas reais clonados + 1 Chefe Orquestrador + 1 Pesquisador Multi-Plataforma. Calibrado para canais em Portugal/Europa, modelando o que já funciona em canais brasileiros e americanos. Cobre canal individual, podcast, vlog e formatos híbridos.

---

## Time

| Agente | Especialidade | Acionar para |
|--------|--------------|-------------|
| 🎯 **Chefe de YouTube** | Orquestrador | Ponto de entrada, sempre começa aqui |
| 🔍 **Pesquisador YouTube** | Research Multi-Plataforma | Pesquisa em Google, Reddit, Quora, IG, FB, X, LinkedIn, YouTube (vídeos+comentários) |
| 📊 **Derral Eves** | The YouTube Formula / Channel Audits | Consultoria de canal + analytics profundo |
| 🧬 **Matt Gielen** | Little Monster Media / Data-Driven Modeling | Modelagem de canais e validação de formatos |
| ⚡ **Paddy Galloway** | Modelagem Viral / Retention | Thumbnails, hooks, retenção, virality |
| 🔎 **Brian Dean** | Backlinko / First Page Videos | SEO/GEO, keyword research, otimização de título e descrição |
| 💰 **Roberto Blake** | Creative Rebel / Revenue Streams | Monetização e decisões de formato |
| 🎯 **Tom Breeze** | Viewability / YouTube Ads | Anúncios e campanhas pagas |

---

## Como usar

```
/opensquad run youtube-squad
```

ou pelo alias:

```
/chefeyoutube
```

O Chefe vai:
1. Ler contexto do canal (existente ou novo)
2. Perguntar o objetivo da sessão
3. Apresentar plano com especialistas e ordem
4. **Sempre começar por pesquisa antes de qualquer planejamento**
5. Executar e sintetizar
6. Registrar aprendizados em `_memory/memories.md`

Você também pode acionar especialistas individuais diretamente. Exemplo:
- "Brian Dean, otimize o título e descrição do meu vídeo X"
- "Tom Breeze, analise o desempenho da minha campanha Y"

---

## Premissas inegociáveis

1. **Nenhum planejamento sem pesquisa prévia** (vídeo, canal, calendário, roteiro, thumbnail)
2. **Toda modelagem usa formatos validados** que já funcionaram em canais semelhantes
3. **Pesquisa de comentários obrigatória**: minerar dúvidas, desafios, desejos do público
4. **Modelagem cross-cultural**: BR + USA como referência para canais em PT/EU (sempre um passo à frente)
5. **Cobertura ampla**: canal individual, podcast, vlog, formatos híbridos
6. **Consultoria inicial sempre cobre** capa, foto, bio, link, formato preferencial, frequência
7. **Workflow de vídeo novo** sempre começa perguntando "Você já tem tema?" e "Já tem ideia?"
8. **Output completo** entrega: título + descrição (SEO+GEO) + estrutura + thumbnail conceitual + referências modeladas

---

## Tipos de demanda suportados

| Situação | Especialistas acionados | Estimativa |
|----------|------------------------|-----------|
| Diagnóstico de canal novo | Researcher → Derral → Matt → Chief | 60-90min |
| Planejamento mensal (calendário) | Researcher → Matt → Derral → Brian → Chief | 120-180min |
| Planejamento de vídeo único | Researcher → Matt → Paddy → Brian | 30-45min |
| Análise de formato proposto | Researcher → Matt | 20-30min |
| Sugestão de novos formatos | Researcher → Matt | 25-35min |
| Decisão estratégica (podcast junto/separado etc) | Derral → Matt → Roberto | 30-45min |
| Otimização SEO de vídeo existente | Researcher → Brian → Paddy | 15-20min |
| Análise de métricas (YouTube API) | Derral → Matt | 30-45min |
| Análise/otimização de anúncios | Tom Breeze | 20-30min |
| Plano de monetização | Roberto → Derral | 30-45min |
| Consultoria estratégica completa (90 dias) | Todos → síntese | 90-120min |

---

## Casos de uso reais (canais {{USER_NAME}})

### {{USER_NAME}} (canal individual)
- Diagnóstico inicial → recomendações de capa, bio, link, formato preferencial
- Planejamento mensal de conteúdo modelando canais BR/USA do nicho
- Otimização SEO de vídeos antigos para reganhar tração

### Infinity Cast (podcast)
- **Decisão estratégica:** "Faço podcast junto com canal {{USER_NAME}} ou separado?"
- Pesquisa de podcasts top no nicho (BR/USA/PT/EU)
- Modelagem de formato (duração, estrutura, hooks de podcast em vídeo)
- Plano de lançamento do podcast (primeiros 10 episódios)

### Outros canais (replicabilidade)
- Squad agnóstico, basta informar o canal alvo no briefing
- Chief lê contexto, pesquisa o nicho, executa pipeline completo

---

## Status dos clones

| Clone | Vault | Status |
|-------|-------|--------|
| paddy-galloway | `/Obsidian Vault/CLONES/paddy-galloway/` | ✅ agent_ready (12 arquivos completos) |
| tom-breeze | `/Obsidian Vault/CLONES/tom-breeze/` | 🔄 a clonar |
| derral-eves | `/Obsidian Vault/CLONES/derral-eves/` | 🔄 a clonar |
| matt-gielen | `/Obsidian Vault/CLONES/matt-gielen/` | 🔄 a clonar |
| brian-dean | `/Obsidian Vault/CLONES/brian-dean/` | 🔄 a clonar |
| roberto-blake | `/Obsidian Vault/CLONES/roberto-blake/` | 🔄 a clonar |

Para clones aprofundados (12 arquivos completos no Obsidian Vault), execute:

```
/createclone Tom Breeze
/createclone Derral Eves
/createclone Matt Gielen
/createclone Brian Dean
/createclone Roberto Blake
```

---

## Capacidades do Pesquisador (multi-plataforma)

O `youtube-researcher` pesquisa em:

- **Buscadores:** Google, DuckDuckGo, Brave, Google Trends
- **YouTube:** vídeos relacionados + comentários (top 50-100 por vídeo)
- **Comunidades:** Reddit, Quora
- **Redes sociais:** Instagram, Facebook, X (Twitter), LinkedIn

E entrega relatórios estruturados com:
- Top tópicos do nicho
- Top dúvidas/dores/desejos extraídos de comentários
- Top formatos validados com canais referência
- Top vídeos modelo com hooks/estrutura/thumbnail analisados
- Recomendações concretas de modelagem

---

## Arquivos do squad

```
squads/youtube-squad/
├── squad.yaml                              # Configuração master
├── README.md                               # Este arquivo
├── squad-party.csv                         # Lista de agentes
├── agents/
│   ├── youtube-chief.agent.md              # Chefe orquestrador
│   ├── youtube-researcher.agent.md         # Pesquisador multi-plataforma
│   ├── derral-eves.agent.md                # Consultoria + analytics
│   ├── matt-gielen.agent.md                # Modelagem data-driven
│   ├── paddy-galloway.agent.md             # Thumbnails + virality
│   ├── brian-dean.agent.md                 # SEO/GEO YouTube
│   ├── roberto-blake.agent.md              # Monetização
│   └── tom-breeze.agent.md                 # YouTube Ads
├── _memory/
│   └── memories.md                         # Aprendizados acumulados por sessão
├── _briefings/
│   ├── consultoria-inicial-template.md     # Template de diagnóstico
│   ├── planejamento-mensal-template.md     # Template de calendário
│   ├── planejamento-video-template.md      # Template de vídeo único
│   └── modelagem-cross-cultural.md         # Regras BR/USA → PT/EU
└── output/                                 # Artefatos gerados (planos, calendários, etc.)
```

---

## Integrações futuras

- **YouTube Data API v3**: para métricas em tempo real do canal
- **DuckDuckGo API** (chave Duck5), para busca de tópicos
- **Reddit API (PRAW)**: para mineração de comunidades
- **Apify Actors**: para scraping de Instagram, Facebook, X, LinkedIn
- **TubeBuddy/VidIQ**: para dados complementares se disponíveis

---

*v1.0, Criado em 2026-04-30 para sua comunidade (multi-canal)*
