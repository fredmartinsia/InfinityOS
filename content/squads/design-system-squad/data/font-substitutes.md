# Font Substitutes — Mapas de fontes proprietárias para fallbacks livres

Quando o DS ideal usaria fonte proprietária, sempre documentar substituto livre/auto-hospedado. Use este mapa.

## Sans-serif

| Original (proprietária/paga) | Substituto livre | Notas |
|------------------------------|------------------|-------|
| **SF Pro Display / SF Pro Text** (Apple) | **Inter** weight 500/600 com `font-feature-settings: "ss01"` | Inter tem ligaduras parecidas; ss01 ativa o "1" sem serif |
| **Söhne** (Klim) | **Inter** weight 500 + letter-spacing -0.01em | Inter weight 500 é o ponto-de-partida; tracking sutil aproxima |
| **Geist Sans** (Vercel) | **Inter** com `-feature-settings: "cv11", "ss01"` | Geist é open mas tem features específicas (cv11 = single-storey g) |
| **Aeonik** (CoType) | **Manrope** (free) ou **Plus Jakarta Sans** | Geometric similar, weight ramp comparável |
| **Helvetica Now** (Monotype) | **Inter** ou **Neue Haas Grotesk Display** (Adobe) | Inter é o substituto democrático; weight 500 default |
| **Neue Haas Grotesk** | **Inter** weight 400 ou **Work Sans** | Compromisso fiel ao Helvetica original |
| **Nike Futura ND** | **Bebas Neue** ou **Anton** | Bold display geométrica, uppercase |
| **Linear Display/Text** (custom) | **Inter** com tracking custom (-0.024em em 80px) | Tracking aproxima feeling |
| **Porsche Next** | **Roboto Condensed** medium | Geometric automotive |
| **Stripe sohne-var** | **Inter** weight 300 (peso leve é a assinatura) | Inter 300 com `font-stretch` ajustado |

## Serif (editorial)

| Original | Substituto | Notas |
|----------|-----------|-------|
| **Tiempos Headline** (Klim) | **Lora** ou **Source Serif Pro** | Editorial moderna |
| **Copernicus** (Klim) | **Lora** weight 500 | Slab-serif feeling |
| **Cormorant Garamond** (free) | (já é livre) | Excelente para display elegante |
| **GT Sectra** | **Playfair Display** | Display alta-classe |
| **Söhne Buch** (variante serifada) | **EB Garamond** | Editorial clássica |

## Mono

| Original | Substituto | Notas |
|----------|-----------|-------|
| **Geist Mono** (Vercel) | **JetBrains Mono** | Leitura excelente, ligaduras |
| **Berkeley Mono** (Berkeley Graphics) | **IBM Plex Mono** | Quadrado, técnico |
| **SF Mono** (Apple) | **JetBrains Mono** ou **Cascadia Code** | Cascadia para Windows feel |
| **Söhne Mono** | **JetBrains Mono** | Próximo o suficiente |

## Stylistic Sets (importantes)

Para preservar feeling proprietário com fontes livres, use `font-feature-settings`:

```css
/* Inter feeling Geist (1 single-storey) */
.geist-feel {
  font-family: 'Inter', sans-serif;
  font-feature-settings: "cv11", "ss01";
}

/* Inter feeling Söhne (clean ligatures) */
.sohne-feel {
  font-family: 'Inter', sans-serif;
  font-feature-settings: "liga", "ss03";
}

/* Inter feeling SF Pro (vertical numbers) */
.sf-pro-feel {
  font-family: 'Inter', sans-serif;
  font-feature-settings: "tnum";
}
```

## Hospedagem

Sempre que possível, **self-host** as fontes (Google Fonts ou repos próprios):
- Performance (sem dependência externa)
- Privacy (sem fetch para Google)
- Versionamento (sem mudança silenciosa)

Para Inter: usar [rsms.me/inter](https://rsms.me/inter/) ou Google Fonts CDN com `display: swap`.

## Regra de ouro do squad

Toda vez que `token-architect` (com persona Spiekermann) escolher uma fonte proprietária no YAML frontmatter, deve incluir:

```yaml
typography:
  display-xl:
    fontFamily: '"Söhne Buch", "Inter", system-ui, sans-serif'
    # substitute: Inter weight 500 with font-feature-settings: "liga", "ss03"
```

O comentário `# substitute:` é lido pelo `quality-auditor` para validar que o fallback foi documentado.
