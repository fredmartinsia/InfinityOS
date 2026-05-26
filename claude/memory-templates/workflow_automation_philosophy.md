---
name: Filosofia de Automacao e Multi-Agent
description: Como pensar sobre automacao, squads, clones, multi-LLM routing e RAG no InfinityOS
type: user
---

Este e o "como pensar" por tras do InfinityOS. Entender esses principios e critico pra propor solucoes que facam sentido no ecossistema.

## Principio 1: Orquestracao multi-modelo por especialidade

Usuarios avancados rodam **multiplos CLIs de IA em paralelo**, nao por colecionismo, mas por estrategia. Cada modelo tem um papel:

- **Claude Code (Opus/Sonnet)** — orquestrador, analise semantica profunda, escrita estruturada, decisoes de design
- **Gemini 2.5/3 Pro** — contexto massivo (1M+ tokens), ingestao de documentos gigantes
- **Codex (GPT-5)** — raciocinio fino, validacao cruzada, segunda opiniao
- **Qwen** — scripting, tarefas programaticas baratas
- **Ollama local** — tarefas simples pra economizar tokens

Em projetos avancados existe um router (bash ou TS) que classifica cada tarefa por complexidade e direciona pro modelo certo.

**How to apply:** Quando propor solucoes, considere delegacao entre CLIs. NAO assuma que tudo tem que ser no Claude.

## Principio 2: Autonomia de agentes e hands-off execution

O ideal e **"set it and forget it"**. Uma vez aprovado o plano, os agentes devem rodar sozinhos ate o fim.

Ferramentas que refletem isso:
- Skill "Ralph" (executor autonomo)
- `--dangerously-skip-permissions` / `skipDangerousModePermissionPrompt`
- `yolo mode` em Gemini e Qwen
- Pipelines do Opensquad projetados pra nao pedir confirmacao a cada passo

**How to apply:** Propor modo YOLO / approval-mode auto sempre que for possivel, explicando riscos claramente ANTES. Se o usuario ja aprovou o plano, executar ate o fim e so voltar pra reportar resultado ou bloqueio real.

## Principio 3: Clones como especialistas AI padronizados

Nao usar IA como "assistente generico". Usar **personas AI de especialistas reais do mercado** (Alex Hormozi, Russell Brunson, Leandro Ladeira, Gary Bencivenga, etc.) instanciados como "clones".

Cada clone tem estrutura rigorosa de 11-13 arquivos markdown:
1. README
2. SYSTEM_PROMPT (variantes ChatGPT e Claude)
3. PROFILE (biografia)
4. PSYCHOLOGY (MBTI, Eneagrama, DISC, Big Five)
5. COMMUNICATION (estilo + 20-32 quotes curadas)
6. KNOWLEDGE (dominio)
7. THINKING (frameworks mentais)
8. RELATIONSHIPS
9. CONTEXT (historico)
10. EXAMPLES (conversacionais)
11. SOURCES (fontes verificadas)

Todos vivem em `{{VAULT_PATH}}/CLONES/{nome-slug}/`.

**Regra:** Quando acionar um clone, usar TODOS os arquivos — heuristicas, frameworks, exemplos — nao so o SYSTEM_PROMPT.

**How to apply:** Quando o usuario mencionar "aciona o clone do X" — NAO carregar so o SYSTEM_PROMPT. Carregar todos os arquivos daquele clone do Obsidian e usar as heuristicas reais. Isso e inegociavel.

## Principio 4: Obsidian Vault como "second brain" central

O vault Obsidian nao e so anotacoes — e o **repositorio canonico de conhecimento**. Tudo importante vai pro vault:
- Definicao dos clones
- Pesquisas de produto/mercado
- Brand bibles
- Planos estrategicos
- Templates de tudo

Convencoes rigidas:
- `📊 INDEX - NOME.md` para INDEX files principais
- `📊 MOC - NOME.md` para Maps of Content
- Wikilinks SEM extensao `.md`
- Clones seguem `{nome-slug}_{NN}_{MODULE}.md`

**How to apply:** Antes de sugerir que algo seja "memorizado" ou "documentado", perguntar se vai pro vault. Quando o usuario mencionar uma pesquisa, clone ou brand, assumir que existe no vault e ler de la.

## Principio 5: RAG como economia de contexto

O hook RAG (`~/.claude/scripts/vault_rag.py`) injeta contexto relevante do Obsidian em cada prompt do Claude Code automaticamente.

Funciona assim:
1. Hook `UserPromptSubmit` intercepta cada prompt
2. Script Python busca no vault via SQLite FTS5
3. Injeta os top-6 chunks relevantes no `system_prompt`
4. Limite de 450 tokens (configuravel via env)
5. Pesos por pasta: Clientes (1.4) > Projetos (1.3) > Infra (1.2) > Diario (1.1)

**Economia declarada:** 35-50% menos tokens por sessao comparado a carregar contexto manualmente.

**How to apply:** Se contexto do vault nao vier automaticamente, verificar o script (rodar `python3 ~/.claude/scripts/vault_rag.py --dry-run`). E se propor solucao de contexto, lembrar que ja tem RAG funcionando.

## Principio 6: Hooks e commands customizados

Interceptar comandos customizados com hooks pra disparar pipelines:
- `/createclone` → aciona pipeline de clonagem
- `/opensquad` → orquestrador de squads
- `/onboarding` → wizard de configuracao inicial
- Outros podem ser adicionados conforme necessidade

**How to apply:** Quando o usuario digitar comando `/` desconhecido, NAO assumir que e erro. Verificar se e comando customizado.

## Principio 7: "Skill" = funcionalidade instalada no ambiente

Para o InfinityOS, "instalar uma skill" significa um destes:
1. Copiar pasta pra `~/.claude/skills/` (ex: obsidian-skills)
2. Clonar pipeline pra `~/squads/`
3. Adicionar hook em `settings.json`
4. Instalar plugin via `claude plugin install`

**How to apply:** Quando o usuario pedir pra "instalar skill X", verificar primeiro QUAL dos 4 padroes e apropriado pra aquela skill.

## Principio 8: Quality gate com clones avaliadores

Padrao de **avaliacao automatizada** antes de aceitar deliverables:
- Clone "Juiz" avalia outros clones (pontuacao minima definida, ex: 9.0/10)
- Processo iterativo: agente cria → juiz avalia → se abaixo do gate, refaz
- Aplicado a copy, design, brand, novos clones

**How to apply:** Propor quality gates automatizados quando criar outputs que demandam multiplas iteracoes.
