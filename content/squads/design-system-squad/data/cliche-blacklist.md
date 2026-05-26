# Cliche Blacklist — Frases banidas no `voice-writer`

Estas frases são marca-d'água de "texto gerado por IA". Se aparecerem no DESIGN.md gerado, o `quality-auditor` bloqueia e força reescrita.

## Verbos/adjetivos genéricos (banimento estrito — 0 ocorrências)

- **empower / empowering** — "We empower users to..." → cortar e dizer o que de fato faz
- **seamless / seamlessly** — "Seamless integration" → ou descrever HOW, ou cortar
- **delightful / delight** — "Delightful interactions" → mostrar exemplo, não adjetivar
- **intentional / thoughtful** — "Thoughtfully designed" → todo design é "intencional", não adiciona info
- **bold / boldness** (sem contexto) — "Bold typography" sem peso/tamanho específico
- **clarity** (genérico) — "Clarity through hierarchy" → mostrar a hierarquia
- **modern / contemporary** — vagos, podem aparecer em 100% dos DS
- **clean** (sem qualificar) — "Clean lines" → o que SÃO as linhas?
- **elegant / sophisticated** — sem evidência específica
- **leveraging / leverage** — "Leveraging design tokens" → "using" basta
- **journey** (UX clichê) — "User journey" → "fluxo" ou "tarefa" são mais precisos
- **ecosystem** (sem ser literal) — "Brand ecosystem" se não há sistema interconectado, é fluff

## Frases-padrão de IA (banimento estrito)

- "At its core, ..."
- "It's important to note that..."
- "In today's fast-paced world..."
- "Our design system embraces..."
- "Crafted with care..."
- "Beautifully designed..."
- "Perfectly balanced..."
- "Strikes the right balance between..."
- "A harmonious blend of..."
- "Elevates the user experience"
- "Brings to life the brand"
- "Speaks to the user"
- "Pixel-perfect"
- "Best-in-class"

## Limite tolerado (máximo 1 ocorrência justificada)

- "Foundation / foundational" — só se houver capítulo "Foundation" estrutural
- "Principle / principles" — só na seção Principles, com lista
- "System / systematic" — só se for sobre sistematização real

## Substitutos preferidos

| Em vez de... | Use... |
|--------------|--------|
| "Empowers users to..." | "Lets users..." / "Allows users to..." / nomeia a ação |
| "Seamless integration" | "Renders inline without page reload" / específico |
| "Delightful animations" | "150ms ease-out fade-in on scroll" / específico |
| "Thoughtfully designed" | nada — apenas mostre |
| "Bold typography" | "84px Geist weight 600 with -2.4px letter-spacing" |
| "Clean interface" | "White canvas, hairline borders, no shadows" |
| "Modern design" | nomeia o decade ou referência ("post-2020 SaaS standards") |
| "Leveraging tokens" | "Using `{colors.primary}` token" |

## Detecção

O `quality-auditor` roda este comando antes de fechar:

```bash
# Pseudocódigo
for term in cliche_blacklist:
    if count(term, DESIGN.md) > 0:
        block(reason=f"Clichê detectado: '{term}'. Reescreva sendo específico.")
```

## Por que isso importa

Os 71 DESIGN.md de referência se diferenciam por **especificidade radical**:

- Stripe não diz "elegant typography" — diz "Söhne weight 300 with ss01 stylistic set; the leveza é a assinatura"
- Apple não diz "clean and modern" — diz "17px body text (not 16). Apple breaks the SaaS convention"
- Vercel não diz "minimalist" — diz "compression as identity. Geist Sans uses -2.4px to -2.88px letter-spacing — the most aggressive negative tracking of any major design system"

**Especificidade > poesia.** Sempre.
