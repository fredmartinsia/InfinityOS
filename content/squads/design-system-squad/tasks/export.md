# Task: *export — Exportar DESIGN.md para outros formatos

> **Converte tokens do DESIGN.md em formatos consumíveis por código (Tailwind config, CSS variables, Style Dictionary).**

## Quando usar

Você já tem `DESIGN.md` + `tokens.json` prontos e quer:
- Configurar Tailwind no seu projeto
- Gerar CSS custom properties (`--color-primary`, etc.)
- Distribuir tokens para iOS/Android via Style Dictionary

## Formatos suportados

| Formato | Output |
|---------|--------|
| `tailwind` | `tailwind.config.js` com `theme.extend.colors`, `fontFamily`, `fontSize`, `borderRadius`, `spacing` |
| `css-vars` | `tokens.css` com `:root { --color-primary: ...; }` + dark mode em `[data-theme="dark"]` |
| `style-dictionary` | `tokens/` directory no formato Style Dictionary com transforms para web/iOS/android |
| `json-w3c` | `tokens.json` no W3C Design Tokens spec |

## Workflow

### Passo 1: Receber path + formato

```
/design-system-chief *export <path-to-DESIGN.md> [formato]
```

Se formato omitido, perguntar:
```
🎯 Para qual formato exportar?
[A] tailwind        (tailwind.config.js)
[B] css-vars        (tokens.css com CSS custom properties)
[C] style-dictionary (multi-platform iOS/Android/Web)
[D] json-w3c        (W3C Design Tokens spec)
```

### Passo 2: Carregar tokens

Carregar `tokens.json` do mesmo diretório do DESIGN.md.

Se `tokens.json` não existir, parsear YAML frontmatter do DESIGN.md.

### Passo 3: Gerar arquivo de saída

#### Para Tailwind

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#5e6ad2',
        'primary-hover': '#7170fc',
        // ...
      },
      fontFamily: {
        display: ['"Söhne"', 'Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      fontSize: {
        'display-hero': ['64px', { lineHeight: '1.05', letterSpacing: '-1.5px' }],
        // ...
      },
      borderRadius: {
        xs: '4px', sm: '8px', md: '12px', lg: '16px', pill: '9999px',
      },
      spacing: {
        xxs: '4px', xs: '8px', sm: '12px', md: '16px', lg: '24px', xl: '32px', section: '96px',
      },
    },
  },
};
```

#### Para CSS vars

```css
:root {
  /* Colors */
  --color-primary: #5e6ad2;
  --color-primary-hover: #7170fc;
  /* ... */
  
  /* Typography */
  --font-display: "Söhne", "Inter", sans-serif;
  --font-body: "Inter", sans-serif;
  
  /* Type scale */
  --fs-display-hero: 64px;
  --lh-display-hero: 1.05;
  --ls-display-hero: -1.5px;
  /* ... */
  
  /* Rounded */
  --radius-xs: 4px;
  --radius-sm: 8px;
  /* ... */
  
  /* Spacing */
  --space-xs: 8px;
  --space-md: 16px;
  /* ... */
}

[data-theme="dark"] {
  --color-primary: #7884e8;
  /* dark mode overrides */
}
```

#### Para Style Dictionary

Gerar estrutura:
```
tokens/
├── color.json
├── typography.json
├── spacing.json
└── radius.json
```

E `config.js` com platforms (web, iOS, Android).

#### Para W3C Design Tokens

Já está no formato. Apenas validar e copiar como `tokens.w3c.json`.

### Passo 4: Salvar e reportar

Output em: `{cwd}/design system/{brand-slug}/exports/{format}/`

Reportar ao usuário:
```
✅ Exportado para {format}.

📂 Arquivo: {output_path}

Para integrar no seu projeto:
{instruções específicas por formato}
```

## Estimativa de tempo
1-2 minutos.
