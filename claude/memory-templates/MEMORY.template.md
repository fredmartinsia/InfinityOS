# Memorias

## Preferencias do Usuario
- [Preferencia de Idioma](user_language_preference.md) — Idioma preferido para comunicacao

## Perfil e Estilo de Trabalho
- [Perfil do Usuario](user_profile.md) — Quem e voce, portfolio, pessoas, setup tecnologico
- [Estilo de Trabalho](work_style.md) — Como voce prefere colaborar
- [Padroes de Feedback Recorrentes](feedback_patterns.md) — Correcoes que voce deu em mais de um projeto
- [Filosofia de Automacao Multi-Agent](workflow_automation_philosophy.md) — Como pensar sobre multi-LLM, squads, clones, RAG

## Vocabulario e Contexto
- [Vocabulario e Jargao](domain_vocabulary.md) — Marcas, pessoas, conceitos, expressoes

## Ambiente Tecnico
- [Stack Tecnologica e Ferramentas Preferidas](tech_stack_preferences.md) — Frameworks, hosting, CLIs
- [Ferramentas Instaladas](tools_installed.md) — O que foi instalado pelo InfiniteOS
- [RAG Hook Configuration](rag_hook_setup.md) — Hook que injeta contexto do vault em cada prompt

## Obsidian Vault
- [Estrutura do Vault Obsidian](obsidian_vault_structure.md) — Localizacao, pastas, convencoes
- [Conhecimento Obsidian Skills](obsidian_skills_knowledge.md) — O que cada skill faz

## Nota importante sobre memorias de projeto e pessoas

Memorias detalhadas de **projetos** e **pessoas-chave** nao ficam nesta pasta. Elas vivem no **Obsidian Vault** e sao injetadas automaticamente via RAG hook em cada prompt relevante.

**Caminhos no vault:**
- Projetos: `{{VAULT_PATH}}/Projetos/`
- Clientes/Pessoas: `{{VAULT_PATH}}/Clientes/`
- MOCs na raiz: `📊 MOC - PROJETOS.md`, `📊 MOC - CLIENTES.md`

**Como ler:** o hook RAG (`~/.claude/scripts/vault_rag.py`) busca automaticamente os chunks relevantes no vault e injeta no contexto. Nao precisa ler os arquivos manualmente.
