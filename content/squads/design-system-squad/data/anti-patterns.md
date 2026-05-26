# Anti-Patterns — Proibições do Design System Squad

Lista negra de padrões que fazem um Design System parecer "gerado por IA". O `quality-auditor` bloqueia outputs que infringem estas regras sem rationale explícito.

---

## 🚫 TIPOGRAFIA

### Inter como fonte default sem rationale
**Por quê:** Inter virou a "Helvetica da era IA" — todo Design System gerado por LLM cai nela. É segura, gratuita, mas indistinta.
**Quando permitir:** Apenas se o brand brief pedir explicitamente, OU se o archetype for `polaris-friendly` (onde Inter cabe). Mesmo assim, exigir letter-spacing custom.
**Alternativas-padrão:** Geist, Söhne (com Inter weight 500 como fallback), Aeonik, Neue Haas Grotesk, IBM Plex Sans, JetBrains Mono.

### Letter-spacing sempre 0
**Por quê:** Os 71 referenciais TODOS usam letter-spacing negativo medido nos display sizes (Vercel -2.4px, Linear -3.0px, Stripe -1.4px). Outputs sem isso parecem "default".
**Regra:** Display ≥ 32px deve ter letter-spacing entre -0.02em e -0.05em, justificado.

### Type ramp genérico (12/14/16/20/24/32/48)
**Por quê:** Todo type scale do Tailwind default. Marca não emerge.
**Regra:** Pelo menos 2 dos 8+ steps precisam de valor não-padrão (ex: body em 17px estilo Apple, ou caption-tabular em 11px específico).

### Sem substitute font documentado
**Por quê:** Quando a fonte ideal é proprietária (SF Pro, Söhne, Geist), o DESIGN.md profissional sempre lista o fallback livre. Output sem isso é incompleto.
**Regra:** Toda font-family proprietária precisa ter `substitute:` no YAML frontmatter ou parágrafo no Typography section.

---

## 🚫 COR

### Primária com saturação > 80% sem rationale
**Por quê:** "#6366f1" (Indigo-500 do Tailwind) e "#8b5cf6" (Violet-500) são os "Inter das cores" — saturados, vibrantes, indistintos.
**Regra:** Primária com saturação > 80% só permitida se: (a) brand brief pedir vibrância explicitamente, OU (b) for archetype `marketing-gradient`/`material-elevation`. Sempre justificar.
**Alternativas:** desaturados (Linear lavender #5e6ad2, Stripe purple #533afd, Claude coral #cc785c), ou cores com luminance ajustada.

### Palette com mais de 12 cores nomeadas
**Por quê:** Palette inflada parece "gerei tudo que pude". Marcas reais são econômicas (Apple usa 1 azul de ação).
**Regra:** Máximo 12 cores nomeadas no frontmatter. Se precisar mais, justificar (ex: dark/light variants ou semantic ramps separados).

### Primary + Secondary + Tertiary todos com mesma saturação
**Por quê:** Hierarquia falsa. Em DS reais, secondary é geralmente desaturado/neutro.
**Regra:** Pelo menos 1 das tier (secondary OU tertiary) precisa ser neutro ou desaturado.

### Verde para success, vermelho para error, amarelo para warning — sem ajuste
**Por quê:** Default. Sem voz.
**Regra:** Tons semânticos precisam estar harmonizados com a paleta (não verde-tailwind 500 chapado).

---

## 🚫 ESTRUTURA

### Sem signature component declarado
**Por quê:** Cada um dos 71 DESIGN.md tem 1 componente "marca registrada" (Linear product UI panels, Vercel shadow-as-border, Stripe blue-tinted shadows, Apple drop shadow único, Nike uppercase Futura ND, Claude code mockup cards).
**Regra:** O DESIGN.md gerado precisa explicitar QUAL é o seu signature component na seção Overview ou Components.

### Sem Do's and Don'ts
**Por quê:** Anti-patterns explícitos com motivo é a marca de DS profissional. Sem isso, vira lista de tokens.
**Regra:** Mínimo 4 Do's e 4 Don'ts, cada um com motivo (1 frase explicando POR QUE).

### Sem Agent Prompt Guide
**Por quê:** É o que torna o DESIGN.md útil para LLMs gerarem código consistente. Sem ele, o DS é só documentação morta.
**Regra:** Seção obrigatória com 3+ exemplos de prompts copia-cola para gerar componentes.

### DESIGN.md com menos de 250 linhas
**Por quê:** Os 71 referenciais têm média de 432 linhas. Output curto = output raso.
**Regra:** Mínimo 300 linhas, alvo 400-600.

---

## 🚫 MOVIMENTO/ANIMAÇÃO

### Animação < 150ms sem `prefers-reduced-motion`
**Por quê:** Risco para epiléticos + má prática de acessibilidade.
**Regra:** Toda animação documentada precisa ter duração ≥ 150ms OU contar com `@media (prefers-reduced-motion: reduce)`.

### Easing default `ease`
**Por quê:** Default browser. Sem voz.
**Regra:** Documentar curve específica (ex: `cubic-bezier(0.16, 1, 0.3, 1)` para "spring out").

---

## 🚫 ACESSIBILIDADE

### Contraste menor que WCAG AA sem flag
**Por quê:** Inacessível.
**Regra:** Body text ≥ 4.5:1 contra background. Display ≥ 3:1. Output que falha precisa flag explícita "decorative only".

### Touch targets < 44px sem rationale
**Por quê:** Mobile inacessível.
**Regra:** Botões e links primários ≥ 44×44px no mobile.

---

## 🚫 NARRATIVA

### Frases-clichê de IA (ver `cliche-blacklist.md`)
**Por quê:** "empower", "seamless", "delightful", "intentional" — frases mortas que LLMs adoram.
**Regra:** `voice-writer` é bloqueado se output contiver mais de 1 ocorrência da blacklist.

### Sem rationale histórico/de marca
**Por quê:** "We chose blue because it conveys trust" é genérico. "Apple chose Action Blue (#0066cc) because every interactive signal across 4 decades of products has been blue, and breaking this would confuse 1B+ users" é editorial.
**Regra:** Overview precisa ter ≥ 2 fatos específicos sobre a marca/contexto/setor.
