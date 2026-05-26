# Task: *create — Criar Design System do zero

> **Workflow de 10 passos com 2 checkpoints. Executado pelo `design-system-chief`.**

## Pré-requisito

Antes de iniciar, o usuário precisa ter `brand.md` produzido pelo `brand-squad` em algum dos caminhos esperados:
- `{cwd}/output/{brand-slug}/brand.md` (preferido)
- `{cwd}/brand/brand.md`
- `{cwd}/{brand-slug}/brand.md`

Se não tiver, `brand-bridge` falha cedo (passo 2).

## Workflow

### Passo 1: Brief intake (chief)

Perguntar ao usuário em uma única mensagem (formato bloco):

```
🎯 Vamos criar um Design System novo.

Para começar, me responda:

1. Nome da marca (e slug, se quiser sobrescrever)
2. Objetivo principal deste DS
   ├─ Web (site marketing + SaaS)
   ├─ Mobile (app)
   ├─ Cross-platform (web + mobile + email)
   └─ Print/Identidade
3. Modo dark é obrigatório? [Sim / Não / Auto]
4. Fontes proprietárias permitidas (Söhne, Geist, etc.)? [Sim / Não]
5. Há paleta/identidade existente que devo respeitar? [Não / Sim — anexe info]
6. Prazo / urgência? [Hoje / Esta semana / Próximas 2 semanas]
```

Salvar em `briefing.json` (memória da sessão).

### Passo 2: Brand bridge

Acionar `@brand-bridge`. Ele tenta ler `brand.md`. Se não encontrar, falha com:
```
⚠️ brand.md não encontrado. Rode /brand-chief *create primeiro.
```
E PARAR.

Se encontrar, retorna `brand_data.json` com 6 campos: brand_name, brand_slug, positioning, archetype_jung, mood, audience, constraints.

### Passo 3: Reference + archetype

Acionar `@reference-engine`. Ele:
1. Classifica em 1 dos 11 archetypes visuais (`data/archetypes.yaml`)
2. Seleciona 3 referências dos 71 (Primária + Tom + Contraste)
3. Popula `explicit_negations` baseado na referência de Contraste

Output: `references_and_archetype.json`.

### Passo 4: 🛑 CHECKPOINT 1 — Alinhamento estratégico

Chief apresenta ao usuário:

```
✅ Análise concluída.

Archetype escolhido: {archetype}
   Rationale: {archetype_rationale}

Referências:
├─ Primária:  {primary.name}    — {primary.why}
├─ Tom:       {tone.name}       — {tone.why}
└─ Contraste: {contrast.name}   — {contrast.why}
   Negações ativas:
   • {explicit_negations[0]}
   • {explicit_negations[1]}
   • ...

Aprovar e continuar?
[A] Aprovar, ir para criação de tokens
[B] Trocar archetype para X
[C] Trocar referência (especifique qual: primária, tom, contraste, e por qual)
```

Se [B] ou [C]: re-rodar passo 3 com ajustes.

### Passo 5: Token architecture

Acionar `@nathan-curtis` para definir estrutura YAML. Em par, acionar `@erik-spiekermann` para preencher os valores tipográficos (font, size, weight, line-height, letter-spacing).

Output: 
- `frontmatter.yaml` (entra no DESIGN.md)
- `tokens.json` (machine-readable)

### Passo 6: Component authoring

Acionar `@brad-frost`. Ele:
1. Lê `data/component-canon.yaml` (must + optional para o archetype escolhido)
2. Lê DESIGN.md da referência primária
3. Escreve seção Components (30-50 componentes no padrão exato)
4. Identifica e declara o **signature component**

Output: `components_section.md`.

### Passo 7: Voice writing

Acionar `@voice-writer`. Ele:
1. Lê DESIGN.md da referência de Tom
2. Extrai 5 quotes literais de cadência
3. Escreve Overview, Whitespace Philosophy, Do's & Don'ts (consumindo `explicit_negations`), Agent Prompt Guide
4. Auto-verifica contra `data/cliche-blacklist.md`

Output: `narrative_sections.md`.

### Passo 8: Preview render

Chief consolida:
```
DESIGN.md =
  --- frontmatter.yaml ---
  + Overview (de narrative_sections)
  + Colors section (gerada de tokens.json)
  + Typography section (gerada de tokens.json)
  + Layout / Spacing
  + Elevation & Depth
  + Shapes
  + Components (de components_section)
  + Do's and Don'ts (de narrative_sections)
  + Responsive
  + Agent Prompt Guide (de narrative_sections)
```

Salva em `{cwd}/design system/{brand-slug}/DESIGN.md`.

Invoca:
```bash
node ~/.claude/commands/design-system-squad/scripts/render-preview.mjs \
  --design "{cwd}/design system/{brand-slug}/DESIGN.md" \
  --tokens "{cwd}/design system/{brand-slug}/tokens.json" \
  --output "{cwd}/design system/{brand-slug}/preview.html"
```

### Passo 9: Quality audit

Acionar `@quality-auditor`. Ele roda 5 verificações + bônus:
1. Fontes (Inter sem rationale → block)
2. Saturação de cores (>80% sem rationale → block)
3. Signature component (declarado? → ok / não → block)
4. Letter-spacing custom em display (≥32px com -0 → block)
5. Cliché blacklist (qualquer match → block)
+ Negações da referência de Contraste viraram Don'ts

Se PASS → Passo 10.
Se FAIL → loop: identificar agente responsável, re-rodar com fix, re-auditar (máx 3 tentativas).

### Passo 10: 🛑 CHECKPOINT 2 — Validação visual

Chief apresenta ao usuário:

```
✅ DESIGN.md gerado e aprovado pelo quality-auditor.
Score: {score}/10

📂 Arquivos prontos em: {cwd}/design system/{brand-slug}/
   ├─ DESIGN.md ({line_count} linhas — alvo 300-600)
   ├─ preview.html (abra no browser)
   ├─ tokens.json (W3C format)
   └─ README.md

🔗 Para abrir o preview:
   open "{cwd}/design system/{brand-slug}/preview.html"

Abra e me diga:
[A] Aprovado, finalizar
[B] Iterar X (especifique: cor, tipografia, componente, etc.)
[C] Comparar lado-a-lado com {primary.name} (referência primária)
```

Se [A]: gerar `README.md` final (template) e fechar com mensagem de sucesso.

Se [B]: identificar agente responsável pela mudança, re-acionar com instrução específica, re-rodar audit + checkpoint.

Se [C]: abrir DESIGN.md da referência primária + DESIGN.md gerado lado a lado para comparação visual.

## Template do README.md final

```markdown
# Design System — {Brand Name}

> Gerado pelo `design-system-squad` em {data}. Padrão DESIGN.md de Alan Nicholas.

## Como usar este DS

### 1. Para gerar UI com qualquer LLM (Claude, ChatGPT, Lovable, v0, Stitch)

Cole o conteúdo de `DESIGN.md` no system prompt. Use a seção "Agent Prompt Guide" para prompts de componentes específicos.

### 2. Para gerar Tailwind config

```bash
/design-system-chief *export "{cwd}/design system/{brand-slug}/DESIGN.md"
```

### 3. Para iterar este DS

```bash
/design-system-chief *create
```

Vai detectar DS existente e oferecer iteração ou versão 2.

## Arquivos

- **DESIGN.md** — Documento principal (legível por humanos e LLMs)
- **preview.html** — Visualização standalone (abre no browser)
- **tokens.json** — Tokens W3C format para automação

## Archetype: {archetype}
## Score de qualidade: {score}/10
## Referências usadas:
- Primária: {primary.name}
- Tom: {tone.name}
- Contraste (negação): {contrast.name}
```

## Estimativa de tempo

- Total: 8-15 minutos
- Etapas com LLM: 5, 6, 7, 9 (~70% do tempo)
- Etapas determinísticas: 1, 2, 3, 8 (~30% do tempo)
- Checkpoints: latência depende do usuário
