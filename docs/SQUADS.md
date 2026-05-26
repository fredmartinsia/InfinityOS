# Squads

Squads são times multi-agente: um **chief** orquestrador roteia para
especialistas (clones) conforme a demanda. Cada squad tem `agents/`, `tasks/`,
`checklists/`, `data/` e um `README.md`.

Ficam em `content/squads/` no repo e são instalados em `~/.claude/commands/`.

## Como usar

```
/<nome-do-squad>          # abre o chief (ex.: /hormozi-squad)
/<squad>:tasks:<tarefa>   # roda uma tarefa específica
```

## Catálogo (17 squads)

| Squad | Agentes | Domínio |
|---|---|---|
| `advisory-board` | 11 | Conselho estratégico (Dalio, Munger, Thiel...) |
| `brand-squad` | 15 | Branding, posicionamento, naming |
| `business-plan-squad` | 8 | Plano de negócios, mercado, financeiro |
| `c-level-squad` | 6 | CxO (CIO/COO/CMO/CTO/CAIO) |
| `claude-code-mastery` | 8 | Configuração/otimização do Claude Code |
| `copy-master` | 33 | Copywriting (elite) |
| `copy-squad` | 23 | Copywriting (essencial) |
| `cybersecurity` | 15 | Pentest, recon, OWASP, incidentes |
| `data-squad` | 7 | Analytics, growth, retenção |
| `design-squad` | 8 | UX, design systems, fluxos |
| `design-system-squad` | 9 | Design systems (clone/auditoria/export) |
| `frontend-squad` | 8 | Landing pages, 3D, motion |
| `hormozi-squad` | 16 | Ofertas, pricing, escala |
| `legal-squad` | 6 | Contratos, compliance, IP |
| `movement` | 7 | Construção de movimentos |
| `storytelling` | 12 | Narrativa, pitch |
| `traffic-masters` | 16 | Tráfego pago (Meta/Google/TikTok) |

> Squads proprietários ou pessoais (ex.: Amazon listing/ads, capital, genealogia,
> youtube) **não** fazem parte deste repositório.

## Criar um novo squad

Use a skill `/opensquad` (criação/execução de squads) ou `/createclone` para um
squad de especialistas reais.
