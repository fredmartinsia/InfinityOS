# Task: *clone — Clonar DS de URL existente

> **Delega para a skill `design-md` (Alan Nicholas) que faz extração estática de URL pública.**

## Quando usar

Use quando você quer **replicar o DS de um site existente** (ex: clonar Linear, Vercel, ou um concorrente) em vez de criar do zero.

Para criar do zero a partir de briefing de marca, use `*create`.

## Workflow

### Passo 1: Validar URL

Chief recebe URL do usuário. Valida:
- URL bem formada (https://...)
- Aviso se URL parece ser SPA pesado (skill design-md tem limitação para SPAs)

### Passo 2: Invocar skill design-md

Executar:

```bash
# Se a skill estiver instalada via npm
npx @aiox/design-md extract \
  --url "{user_url}" \
  --output "{cwd}/design system/{brand-slug}/" \
  --provider claude-cli
```

Ou se estiver localmente em `$HOME/Desktop/DESIGN SYSTEM/design-md/`:

```bash
node "$HOME/Desktop/DESIGN SYSTEM/design-md/run.cjs" \
  --url "{user_url}" \
  --output "{cwd}/design system/{brand-slug}/"
```

### Passo 3: Mostrar output

Skill `design-md` gera:
- `DESIGN.md`
- `tokens.json`
- `extraction-log.yaml` (provenance)
- `quality-score.json` (A-F)
- `lint-report.json` (Google spec lint)
- `preview.html` (standalone)

### Passo 4: Auditoria adicional (opcional)

Oferecer ao usuário:
```
🔍 DS clonado. Quer que eu rode auditoria anti-IA além da qualidade já reportada?
[Sim] → roda quality-auditor do squad por cima
[Não] → fecha como está
```

## Limitações da skill design-md (avisar usuário)

- ❌ SPAs pesados (Next.js, React puro com SSR mínimo) podem falhar — content-validation gate
- ❌ Sites com bot protection (Cloudflare aggressive)
- ❌ Sites paywalled

Se falhar, sugerir:
- Tentar URL específica (ex: `linear.app/blog` em vez de `linear.app`)
- Fazer manualmente via `*create` usando o site como referência informal

## Estimativa de tempo

- 1-3 minutos (na maioria dos sites estáticos)
- Pode levar 5-10 min em sites maiores ou se LLM precisar retry
