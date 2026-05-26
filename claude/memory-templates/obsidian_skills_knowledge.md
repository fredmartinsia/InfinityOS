---
name: Conhecimento Obsidian Skills
description: Capacidades de cada um dos 5 skills da kepano/obsidian-skills disponiveis
type: reference
---

Resumo do que cada Obsidian Skill faz. Usado quando o usuario pedir coisas relacionadas a um dos skills.

## obsidian-markdown
Variante do markdown especifica do Obsidian. Extende CommonMark + GFM.
- **Wikilinks:** `[[Nota]]`, `[[Nota|Alias]]`, `[[Nota#Heading]]`, `[[Nota#^block-id]]`
- **Embeds:** `![[Nota]]`, `![[imagem.png|300]]`, `![[doc.pdf#page=3]]`
- **Callouts:** `> [!note]`, `[!tip]`, `[!warning]`, etc. — aceita folding `-`/`+`
- **Properties:** YAML frontmatter (tags, aliases, cssclasses)
- **Block IDs:** `^block-id` no final de paragrafo
- **Highlights:** `==texto==`
- **Comentarios:** `%%comentario%%` (hidden no reading view)
- **LaTeX:** `$inline$` e `$$block$$`
- **Mermaid:** com `internal-link` class para linkar nodes a notas

## obsidian-bases
Gerencia arquivos `.base` que criam views database-like.
- Scope via filtros por tags, folders, properties ou datas
- Computed properties com formulas
- 4 view types: `table`, `cards`, `list`, `map`
- Validacao YAML integrada
- Ativa quando mencionar `.base`, Bases, table views, card views, filtros, formulas

## json-canvas
Cria/edita arquivos `.canvas` (JSON Canvas Spec 1.0).
- 4 tipos de node: text, file, link, group
- Edges com labels e anchors direcionais
- Validacao de IDs unicos e referencias
- Para planejamento visual, concept mapping, organizacao espacial

## obsidian-cli
Interface CLI para vault Obsidian rodando.
- Requer instancia ativa do Obsidian
- Sintaxe: `file=`, `path=`, `vault=<nome>` + flags booleanas
- Operacoes: ler, criar, buscar, append, set properties, tags, backlinks
- Dev tools: plugin reload, error capture, DOM inspection, screenshots, JavaScript eval
- Para automacao de vault e desenvolvimento de plugins

## defuddle
Extracao limpa de conteudo web.
- Remove nav, ads, clutter — gera markdown/JSON limpo
- Comando: `defuddle parse <url> --md`
- Suporta metadata (title, description, domain)
- **Preferir defuddle** em vez de web fetch generico para reduzir tokens ao analisar artigos/docs/blogs

**Why:** Os skills seguem a especificacao Agent Skills (kepano/obsidian-skills).

**How to apply:** Antes de fazer operacoes manuais com markdown do Obsidian, canvas ou bases, verifique se um desses skills nao resolveria melhor. Use defuddle para web scraping leve.
