# Task: *audit — Auditar DESIGN.md existente

> **Roda checklist anti-IA + comparação com padrão dos 71 referenciais. Não modifica o arquivo.**

## Quando usar

- Você tem um DESIGN.md gerado por outra ferramenta/AI e quer saber se está no padrão
- Você quer revisar um DS existente antes de adotar
- Você quer comparar 2 DS

## Workflow

### Passo 1: Receber path

Chief recebe `<path>` do DESIGN.md. Validar que existe.

### Passo 2: Acionar quality-auditor

Acionar `@quality-auditor` com:
- DESIGN.md path
- tokens.json path (opcional, se existir lado a lado)
- Sem referência de Contraste (para audit autônomo, sem squad context)

Quality-auditor roda 5 verificações:
1. Fontes (Inter sem rationale)
2. Saturação de cores
3. Signature component declarado
4. Letter-spacing custom em display
5. Cliché blacklist

### Passo 3: Comparação estrutural com os 71

Chief faz comparação adicional:

| Critério | Padrão dos 71 | DESIGN.md auditado | Status |
|----------|---------------|--------------------|--------|
| Linhas totais | 300-600 | {actual} | {ok/curto/longo} |
| Seções obrigatórias | 9 (Overview, Colors, Typography, Layout, Elevation, Shapes, Components, Do's/Don'ts, Responsive, Agent Prompt) | {found} | {ok/missing} |
| Componentes documentados | 20-50 | {actual} | {ok/poucos/demais} |
| Frontmatter YAML válido | sim | {valid?} | {ok/error} |
| Cores nomeadas | ≤ 12 | {actual} | {ok/inflado} |
| Typography entries | 8-15 | {actual} | {ok} |
| Spacing scale múltiplo de 4 | sim | {check} | {ok/violação} |

### Passo 4: Score consolidado e relatório

```
📋 AUDITORIA DESIGN.md

Arquivo: {path}
Score consolidado: {7.2}/10

✅ Pontos fortes:
  - {3-5 pontos do que está bom}

⚠️ Pontos a melhorar:
  - {3-7 falhas específicas + onde corrigir}

🚫 Bloqueios graves (parece "feito por IA"):
  - {0-3 itens críticos}

📂 Comparação com padrão dos 71:
  {tabela acima}

🎯 Recomendação:
  [Aprovar como está / Iterar pontos X / Refazer do zero]
```

## Saída

Apenas relatório (não modifica o arquivo). Salvo em `{cwd}/design system/audit-{timestamp}.md`.

## Estimativa de tempo
2-5 minutos.
