# 🎨 Design System Squad

> Squad multi-agente que cria Design Systems profissionais no padrão DESIGN.md (Alan Nicholas / Google spec). Combate o "design genérico de IA" usando 71 referências reais como base, archetypes para classificar, e checklist anti-IA para validar.

## Quando usar

Use este squad quando precisar **criar um Design System novo do zero** para uma marca/produto, com qualidade profissional comparável a Linear, Vercel, Stripe, Apple, Nike, Claude.

NÃO use para:
- Clonar Design System de URL existente → use a skill `design-md` direto
- Auditar interface pronta → use `/design-squad`
- Criar identidade visual de marca → use `/brand-chief` ANTES (este squad consome o output)

## Comandos

| Comando | O que faz |
|---------|-----------|
| `/design-system-chief` | Abre menu do orquestrador |
| `/design-system-chief *create` | Workflow completo de criação (10 passos) |
| `/design-system-chief *clone <url>` | Clona DS de URL existente (delega para skill design-md) |
| `/design-system-chief *audit <path>` | Audita DESIGN.md existente vs padrão dos 71 |
| `/design-system-chief *export <path>` | Exporta para tailwind.config.js / tokens.css |
| `/alan-nicholas` | Acesso direto ao clone (método design.md, archetypes) |
| `/brad-frost` | Acesso direto ao clone (atomic design, components) |
| `/nathan-curtis` | Acesso direto ao clone (design tokens, taxonomia) |
| `/erik-spiekermann` | Acesso direto ao clone (tipografia editorial) |

## Time

### Tier 0 — Orquestrador
- 🎯 **design-system-chief** — Roteia tarefas, valida outputs, gerencia checkpoints

### Tier 1 — Clones reais (autoridades do domínio)
- 🧪 **Alan Nicholas** — Método design.md, archetypes, anti-padrões, "data first"
- 🧱 **Brad Frost** — Atomic Design, Pattern Lab, component canon
- 🎟️ **Nathan Curtis** — Design tokens W3C, taxonomia, naming
- ✍️ **Erik Spiekermann** — Tipografia editorial, type ramps, letter-spacing custom

### Tier 2 — Especialistas funcionais
- 🌉 **brand-bridge** — Lê output do brand-squad
- 🧭 **reference-engine** — Seleciona 3 referências (Primária + Tom + Contraste) + classifica em 1 dos 11 archetypes
- 📝 **voice-writer** — Escreve seções narrativas com rationale editorial
- 🛡️ **quality-auditor** — Roda checklist anti-IA antes de fechar

## Output

Quando você roda `/design-system-chief *create` dentro de um projeto, o squad cria:

```
{seu-projeto}/design system/{brand-slug}/
├── DESIGN.md          # 300-600 linhas no padrão dos 71 (YAML frontmatter + 9 seções markdown)
├── preview.html       # Standalone, abre no browser, mostra swatches + type ramp + components
├── tokens.json        # Versão machine-readable dos tokens
└── README.md          # Como usar este DS
```

## Pré-requisito

Antes de rodar `*create`, você precisa ter um **brand.md** produzido pelo `brand-squad`:

```
{seu-projeto}/output/{brand-slug}/brand.md
```

Se ele não existir, o `brand-bridge` falha cedo e instrui rodar `/brand-chief` primeiro.

## Workflow `*create` em 10 passos (com 2 checkpoints)

1. Brief intake (chief pergunta: marca, objetivo, público, modo dark, fonts, prazo)
2. Brand bridge (lê output do brand-squad)
3. Reference + Archetype (3 referências + 1 dos 11 archetypes)
4. **CHECKPOINT 1** — usuário aprova archetype + 3 referências
5. Token architecture (Curtis + Spiekermann)
6. Component authoring (Frost — 20-50 componentes do canon)
7. Voice writing (Overview + princípios + Do's/Don'ts + Whitespace + Agent Prompt Guide)
8. Preview render (script Node, sem LLM)
9. Quality audit (5 verificações anti-IA)
10. **CHECKPOINT 2** — usuário abre preview.html e aprova/itera

## 7 guardrails anti-IA ativos

1. Reference Engine com slot de **negação** (Contraste) — força decisão em vez de média
2. 71 referências reais locais em `data/reference-systems/` (sem inventar do zero)
3. Archetype classification antes de gerar tokens
4. `voice-writer` recebe quotes literais e imita cadência (não parafraseia)
5. Blacklist de clichês ativa
6. `quality-auditor` bloqueia: Inter sem rationale, primárias com saturação > 80%, falta de signature component, falta de letter-spacing negativo medido
7. `preview.html` renderizado dá feedback visual real antes do checkpoint final

## Material de apoio

- `data/reference-systems/` — 71 DESIGN.md reais (Linear, Vercel, Stripe, Apple, Nike, Claude...)
- `data/archetypes.yaml` — 11 perfis visuais
- `data/anti-patterns.md` — proibições com motivo
- `data/font-substitutes.md` — fontes proprietárias → fallbacks
- `data/component-canon.yaml` — 20-50 componentes obrigatórios
- `data/cliche-blacklist.md` — frases banidas no voice-writer
