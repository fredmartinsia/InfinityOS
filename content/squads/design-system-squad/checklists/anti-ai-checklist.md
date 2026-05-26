# Anti-IA Checklist — Validação obrigatória do DESIGN.md

> Executado pelo `quality-auditor`. **5 verificações binárias + bônus**. Qualquer falha bloqueia o output.

---

## ✅ Verificação 1 — Fontes

### Bloqueia se:
- `Inter` aparece como `fontFamily` primária no `typography:` SEM rationale documentado em Typography section do DESIGN.md
- Alguma fonte proprietária (SF Pro, Söhne, Geist, Aeonik, Helvetica Now) não tem comentário `# substitute:` próximo

### Como verificar:

```bash
# 1. Inter como primária?
INTER_USED=$(jq -r '.typography | to_entries[] | .value.fontFamily' tokens.json | grep -i "Inter" | wc -l)

# 2. Tem rationale?
INTER_RATIONALE=$(grep -ic "Inter.*porque\|Inter.*because\|Inter foi escolhid\|Inter chosen" DESIGN.md)

if [ $INTER_USED -gt 0 ] && [ $INTER_RATIONALE -eq 0 ]; then
  echo "BLOCK: Inter usada sem rationale"
fi

# 3. Fontes proprietárias com substitute?
PROPRIETARY=("SF Pro" "Söhne" "Geist" "Aeonik" "Helvetica Now")
for font in "${PROPRIETARY[@]}"; do
  if grep -q "$font" tokens.json; then
    if ! grep -A2 "$font" DESIGN.md | grep -q "substitute"; then
      echo "BLOCK: $font sem substitute documentado"
    fi
  fi
done
```

### Como corrigir:
- Se Inter genuinamente é a melhor escolha: adicionar parágrafo em Typography explicando por quê (custo, acessibilidade, fallback universal, archetype específico)
- Se não: trocar por alternativa em `data/font-substitutes.md`
- Para fontes proprietárias: adicionar `# substitute: Inter weight 500 with font-feature-settings: "ss01"` no YAML

---

## ✅ Verificação 2 — Saturação de cores

### Bloqueia se:
- `colors.primary` tem HSL saturation > 80% E não está justificada
- Mais de 12 cores nomeadas no `colors:` (palette inflada)

### Como verificar:

```javascript
// Pseudocódigo
const primary = tokens.colors.primary;
const { h, s, l } = hexToHSL(primary);
const archetype = readArchetype(); // do reference-engine

if (s > 80) {
  if (!['marketing-gradient', 'material-elevation'].includes(archetype)) {
    if (!designMd.includes('saturação') && !designMd.includes('vibrant')) {
      throw new Error('BLOCK: Primária com saturação > 80% sem rationale');
    }
  }
}

const colorCount = Object.keys(tokens.colors).length;
if (colorCount > 12) {
  throw new Error(`BLOCK: ${colorCount} cores nomeadas (limite 12)`);
}
```

### Como corrigir:
- Reduzir saturação da primária (alvo ~50-70%) OU adicionar rationale em Overview
- Consolidar palette (remover variações de uma mesma cor; usar apenas semantic + brand essential)

---

## ✅ Verificação 3 — Signature Component declarado

### Bloqueia se:
- Overview section não menciona explicitamente um signature component

### Como verificar:

```bash
SIGNATURE_PATTERNS=(
  "signature component"
  "signature is"
  "marca registrada"
  "what makes this DS instantly recognizable"
  "signature of the brand"
  "the signature element"
)

OVERVIEW=$(sed -n '/^## Overview/,/^## /p' DESIGN.md)

FOUND=0
for pattern in "${SIGNATURE_PATTERNS[@]}"; do
  if echo "$OVERVIEW" | grep -iq "$pattern"; then
    FOUND=1
    break
  fi
done

if [ $FOUND -eq 0 ]; then
  echo "BLOCK: Signature component não declarado em Overview"
fi
```

### Como corrigir:
Adicionar 1 frase em Overview no padrão:
> "What makes this DS instantly recognizable is the {component-name}, which {description of unique characteristic}. It appears in {3 contexts}."

Exemplos:
- Linear: "the dark product UI panels framed in `{colors.surface-dark}`"
- Vercel: "the shadow-as-border treatment (`0px 0px 0px 1px rgba(0,0,0,0.08)`) used on every card"
- Stripe: "multi-layer blue-tinted shadows (`rgba(50,50,93,0.25)`)"

---

## ✅ Verificação 4 — Letter-spacing custom em display

### Bloqueia se:
- Qualquer entry em `typography:` com `fontSize >= 32px` tem `letterSpacing: 0` ou ausente

### Como verificar:

```javascript
const violations = [];
for (const [key, value] of Object.entries(tokens.typography)) {
  const fontSize = parseInt(value.fontSize);
  const letterSpacing = parseFloat(value.letterSpacing) || 0;
  
  if (fontSize >= 32 && letterSpacing === 0) {
    violations.push(`${key} (${fontSize}px) tem letterSpacing 0`);
  }
}

if (violations.length > 0) {
  throw new Error(`BLOCK: ${violations.length} entries display sem letter-spacing custom: ${violations.join(', ')}`);
}
```

### Como corrigir:
Aplicar tabela do `erik-spiekermann`:

| fontSize | letterSpacing alvo |
|----------|--------------------|
| 28-40px | -0.02em a -0.03em |
| 48-72px | -0.03em a -0.05em |
| 80px+ | -0.04em a -0.06em |

Em px (assumindo 16px = 1em):
- 32px → -0.7px
- 48px → -1.4px
- 64px → -2.0px
- 80px → -2.5px
- 96px → -3.5px

---

## ✅ Verificação 5 — Cliché Blacklist

### Bloqueia se:
- DESIGN.md contém qualquer termo da lista "banimento estrito" em `data/cliche-blacklist.md`

### Como verificar:

```bash
BLACKLIST=(
  "empower" "empowering" "seamless" "seamlessly"
  "delightful" "delight" "intentional" "thoughtful"
  "leveraging" "leverage" "ecosystem"
  "At its core"
  "Crafted with care"
  "Beautifully designed"
  "Elevates the user experience"
  "Brings to life the brand"
  "Pixel-perfect"
  "Best-in-class"
)

for term in "${BLACKLIST[@]}"; do
  count=$(grep -ic "$term" DESIGN.md)
  if [ $count -gt 0 ]; then
    echo "BLOCK: Clichê detectado: '$term' ($count ocorrência(s))"
  fi
done
```

### Como corrigir:
Voice-writer reescreve a frase com **especificidade radical**:
- "elegant" → "Söhne weight 300 with -0.01em letter-spacing"
- "modern" → "post-2020 SaaS standards" ou cite uma marca de referência
- "clean" → "white canvas, hairline borders, no shadows"
- "empower" → corte e diga o que de fato faz

---

## ✅ Bônus — Negações da Referência de Contraste

### Bloqueia se:
- Alguma negation (do `reference-engine`) não tem correspondente em "Don'ts" section

### Como verificar:

```bash
NEGATIONS=$(jq -r '.references.contrast.explicit_negations[]' references.json)
DONTS_SECTION=$(sed -n '/^### Don.t/,/^### /p' DESIGN.md)

while IFS= read -r negation; do
  # Negations vêm como "NÃO usar X". Buscar palavra-chave em Don'ts
  keyword=$(echo "$negation" | sed 's/NÃO usar //I')
  if ! echo "$DONTS_SECTION" | grep -iq "$keyword"; then
    echo "BLOCK: Negation '$negation' não virou Don't"
  fi
done <<< "$NEGATIONS"
```

### Como corrigir:
Voice-writer adiciona Don't correspondente. Ex: se negation é "NÃO usar gradients no canvas", adicionar:
```markdown
- **Don't** use gradients on canvas — quebra o feeling de premium contido (anti-padrão herdado de marketing-gradient archetype)
```

---

## Output do Quality Auditor

### Se PASS:
```json
{
  "status": "pass",
  "score": 9.2,
  "checks_passed": ["fontes", "saturacao", "signature", "letter-spacing", "cliches", "negacoes"],
  "approval_message": "✅ DESIGN.md aprovado."
}
```

### Se FAIL:
```json
{
  "status": "fail",
  "score": 6.5,
  "failures": [
    {"check": "signature", "issue": "...", "fix": "...", "responsible_agent": "voice-writer"},
    {"check": "letter-spacing", "issue": "...", "fix": "...", "responsible_agent": "erik-spiekermann"}
  ]
}
```
