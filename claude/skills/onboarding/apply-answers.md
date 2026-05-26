# Apply Answers — Logica de Escrita

Detalhes de como aplicar as respostas da entrevista da FASE 1 nos arquivos do sistema (FASES 2 e 3).

## Variaveis Coletadas na Entrevista

| Variavel | Origem | Onde aplica |
|---|---|---|
| `{{USER_NAME}}` | nome completo | user_profile, company, dashboards, docs |
| `{{USER_NICK}}` | apelido | saudacoes, tom |
| `{{USER_EMAIL}}` | email | user_profile |
| `{{USER_ROLE}}` | papel profissional | user_profile |
| `{{LANGUAGE}}` | idioma saida | settings.json, user_language_preference, company |
| `{{BUSINESSES_LIST}}` | lista dos negocios | user_profile, MOC-NEGOCIOS |
| `{{ACTIVE_PROJECTS}}` | lista projetos | user_profile, MOC-PROJETOS, Projetos/{slug}/ |
| `{{STAKEHOLDERS_LIST}}` | pessoas-chave | user_profile, MOC-CLIENTES, Clientes/{slug} |
| `{{TECH_STACK}}` | frameworks + hosting + DB + CLIs | tech_stack_preferences |
| `{{DESIGN_PREFERENCES}}` | UI/design preferences | tech_stack_preferences |
| `{{GOTCHAS}}` | gotchas tecnicos | tech_stack_preferences |
| `{{AUTONOMY_PREFERENCE}}` | texto sobre autonomia | work_style |
| `{{PLANNING_PREFERENCE}}` | plano antes ou direto | work_style |
| `{{CREATIVE_ITERATION}}` | iteracao em copy/design | work_style |
| `{{QUALITY_BAR}}` | padrao de entrega | work_style |
| `{{TONE}}` | tom preferido | work_style, company |
| `{{VOCABULARY_NOTES}}` | expressoes/jargao | work_style, domain_vocabulary |
| `{{BRANDS_LIST}}` | marcas citadas | domain_vocabulary |
| `{{PEOPLE_LIST}}` | pessoas citadas | domain_vocabulary |
| `{{CONCEPTS_LIST}}` | siglas e conceitos | domain_vocabulary |
| `{{VAULT_PATH}}` | path do vault | vault_rag.py via env, varias memorias |
| `{{PROJECT_SLUG}}` | slug do HOME | path da memoria |
| `{{COMPANY_NAME}}` | primeiro negocio | opensquad company.md |
| `{{IDES_USED}}` | IDEs em uso | opensquad preferences.md |

## Como Slugificar

- Nome de projeto: lowercase, espacos → hifens, remover acentos, max 40 chars
  - "Minha Empresa" → `minha-empresa`
  - "Pesquisa de mercado 2026" → `pesquisa-de-mercado-2026`
- Nome de pessoa: mesma regra, preservar hifens existentes
  - "Fernando da Silva" → `fernando-da-silva`
  - "Maria João" → `maria-joao`

## Ordem de Escrita (FASE 3)

**Passo 1 — Backup:**
```bash
TS=$(date +%Y%m%d-%H%M%S)
cp -R ~/.claude/projects/*/memory/ ~/.infinite-os-backup-$TS/memory/
```

**Passo 2 — Identificar path da memoria:**
```bash
MEM_DIR=~/.claude/projects/$(echo $HOME | sed 's|/|-|g')/memory
# Ex: ~/.claude/projects/-Users-joao/memory
```

Se o diretorio nao existe, cria.

**Passo 3 — Reescrever arquivos** (substitui `{{PLACEHOLDER}}` pelos valores):

Ordem recomendada (menos dependencias primeiro):
1. `user_language_preference.md` → `{{LANGUAGE}}`
2. `user_profile.md` → todas as variaveis de identidade e negocio
3. `tech_stack_preferences.md`
4. `work_style.md`
5. `domain_vocabulary.md`
6. `obsidian_vault_structure.md`
7. `rag_hook_setup.md`
8. `MEMORY.md` (indice ja esta OK, so valida links)

**Passo 4 — Opensquad:**
9. `~/_opensquad/_memory/company.md` (primeira empresa do mentorado)
10. `~/_opensquad/_memory/preferences.md`

## Como Escrever Arquivos

Use Write ou Edit tools. Para cada template:

1. Leia o `.template.md` do `~/.claude/skills/onboarding/templates/` ou do install (os templates em `memory-templates/` foram copiados pelo install).
2. Substitua `{{VARIAVEIS}}` pelos valores.
3. Remova qualquer `.template` do nome do arquivo.
4. Escreva no destino.

Exemplo pra user_profile:
```
origem:  memory-templates/user_profile.template.md  (ja foi copiado para $MEM_DIR/user_profile.template.md)
destino: $MEM_DIR/user_profile.md
acao:    ler origem, substituir placeholders, escrever destino, deletar origem com .template
```

## Tratamento de Casos Vazios

Se o mentorado disser "nao tenho negocio ainda":
- `{{BUSINESSES_LIST}}` → `"Nenhum negocio ativo no momento. Em exploracao."`
- `{{COMPANY_NAME}}` → usar `{{USER_NAME}}` como brand pessoal
- `{{COMPANY_SUMMARY}}` → "Marca pessoal de {{USER_NAME}}, em fase de exploracao."

Se vazio em stack:
- `{{TECH_STACK}}` → `"Nao definido ainda — preencher conforme uso se consolide."`

Nunca deixe `{{VARIAVEL}}` cru no arquivo final. Sempre substitua por algo — mesmo que seja "a definir".

## Criacao de Arquivos no Vault (FASE 2)

Para **cada projeto citado**, cria:
```
{{VAULT_PATH}}/Projetos/{project-slug}/README.md
```

Conteudo baseado em `templates/projeto.md`.

Para **cada cliente/pessoa citada**, cria:
```
{{VAULT_PATH}}/Clientes/{person-slug}.md
```

Conteudo baseado em `templates/cliente.md`.

Se a pasta `Projetos/` ou `Clientes/` ja tiver subpastas com mesmo nome, NAO sobrescreve — pula e avisa o mentorado: "A pasta X ja existe, nao sobrescrevi. Pode abrir e adicionar as infos manualmente."

## MOCs (FASE 2, apos stubs criados)

### `📊 MOC - PROJETOS.md`
```markdown
---
tags: [moc, projetos]
---

# 📊 MOC - PROJETOS

## Ativos
- [[Projetos/{slug-1}/README|{nome-1}]]
- [[Projetos/{slug-2}/README|{nome-2}]]
...

## Em Arquivamento
(vazio inicialmente)
```

### `📊 MOC - CLIENTES.md`
```markdown
---
tags: [moc, clientes]
---

# 📊 MOC - CLIENTES

## Ativos
- [[Clientes/{slug-1}|{nome-1}]] — {tipo-1}
...
```

### `📊 MOC - NEGOCIOS.md`
```markdown
---
tags: [moc, negocios]
---

# 📊 MOC - NEGOCIOS

## {{COMPANY_NAME}}
- Nicho: {nicho}
- Fase: {fase}
- Pessoas: {pessoas}

(outros negocios em sequencia)
```

## Dashboard Overview

Usa `templates/dashboard-overview.md` e substitui.
