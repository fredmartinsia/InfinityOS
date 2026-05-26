#!/usr/bin/env node
/**
 * render-preview.mjs — Gerador determinístico de preview.html
 *
 * Lê um DESIGN.md + tokens.json e produz preview.html standalone com:
 * - Color swatches grid
 * - Typography type ramp
 * - Spacing/radius scale
 * - Raw DESIGN.md renderizado
 *
 * Uso:
 *   node render-preview.mjs --design <path-to-DESIGN.md> --tokens <path-to-tokens.json> --output <path-to-preview.html>
 *
 * Sem LLM. Sem dependências externas (apenas Node stdlib).
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { argv } from 'node:process';

// ────────────────────────────────────────────────────────────
// CLI args
// ────────────────────────────────────────────────────────────
function parseArgs(args) {
  const out = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      out[key] = value;
      i++;
    }
  }
  return out;
}

const args = parseArgs(argv.slice(2));
const designPath = args.design;
const tokensPath = args.tokens;
const outputPath = args.output;

if (!designPath || !outputPath) {
  console.error('Uso: node render-preview.mjs --design <DESIGN.md> --output <preview.html> [--tokens <tokens.json>]');
  process.exit(1);
}

// ────────────────────────────────────────────────────────────
// Parse DESIGN.md frontmatter (YAML simples — sem dependência js-yaml)
// ────────────────────────────────────────────────────────────
function parseFrontmatter(md) {
  const match = md.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, body: md };

  const yamlText = match[1];
  const body = match[2];
  const frontmatter = parseSimpleYaml(yamlText);
  return { frontmatter, body };
}

function parseSimpleYaml(text) {
  const result = {};
  const lines = text.split('\n');
  const stack = [{ obj: result, indent: -1 }];

  for (const rawLine of lines) {
    if (!rawLine.trim() || rawLine.trim().startsWith('#')) continue;

    const indent = rawLine.match(/^ */)[0].length;
    const line = rawLine.trim();

    while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
      stack.pop();
    }

    const parent = stack[stack.length - 1].obj;
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;

    const key = line.slice(0, colonIdx).trim();
    const value = line.slice(colonIdx + 1).trim();

    if (value === '') {
      parent[key] = {};
      stack.push({ obj: parent[key], indent });
    } else {
      parent[key] = parseValue(value);
    }
  }
  return result;
}

function parseValue(v) {
  v = v.trim();
  if (v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1);
  if (v.startsWith("'") && v.endsWith("'")) return v.slice(1, -1);
  if (/^-?\d+\.?\d*$/.test(v)) return parseFloat(v);
  if (v === 'true') return true;
  if (v === 'false') return false;
  return v;
}

// ────────────────────────────────────────────────────────────
// HSL/luminance helpers
// ────────────────────────────────────────────────────────────
function hexToRgb(hex) {
  const h = hex.replace('#', '');
  const expanded = h.length === 3 ? h.split('').map(c => c + c).join('') : h;
  const num = parseInt(expanded, 16);
  return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
}

function luminance(hex) {
  const { r, g, b } = hexToRgb(hex);
  const [R, G, B] = [r, g, b].map(c => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

function contrastingTextColor(bgHex) {
  return luminance(bgHex) > 0.5 ? '#000000' : '#ffffff';
}

// ────────────────────────────────────────────────────────────
// Markdown to HTML (subset — headings, paragraphs, lists, code, tables)
// ────────────────────────────────────────────────────────────
function markdownToHtml(md) {
  let html = md;

  // Code fences
  html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (_, lang, code) => {
    return `<pre><code class="lang-${lang || 'text'}">${escapeHtml(code)}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');

  // Headings
  html = html.replace(/^###### (.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^##### (.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Bold/italic
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Lists
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // Tables (simples)
  html = html.replace(/^\|(.+)\|$/gm, (_, content) => {
    const cells = content.split('|').map(c => c.trim());
    if (cells.every(c => /^-+:?$/.test(c))) return ''; // separador
    return '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
  });
  html = html.replace(/(<tr>.*<\/tr>\n?)+/g, '<table>$&</table>');

  // Paragraphs (linhas que sobraram)
  html = html.split('\n\n').map(block => {
    if (block.trim().startsWith('<') || !block.trim()) return block;
    return `<p>${block.trim()}</p>`;
  }).join('\n\n');

  return html;
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ────────────────────────────────────────────────────────────
// Render sections
// ────────────────────────────────────────────────────────────
function renderColors(colors) {
  if (!colors || typeof colors !== 'object') return '';
  const swatches = Object.entries(colors).map(([name, value]) => {
    if (typeof value !== 'string' || !value.startsWith('#')) return '';
    const textColor = contrastingTextColor(value);
    return `
      <div class="swatch" style="background:${value};color:${textColor}">
        <div class="swatch-name">${name}</div>
        <div class="swatch-value">${value}</div>
      </div>
    `;
  }).join('');
  return `
    <section class="section">
      <h2>Colors</h2>
      <div class="swatches">${swatches}</div>
    </section>
  `;
}

function renderTypography(typography) {
  if (!typography || typeof typography !== 'object') return '';
  const samples = Object.entries(typography).map(([name, spec]) => {
    if (typeof spec !== 'object') return '';
    const { fontFamily = 'inherit', fontSize = '16', fontWeight = 400, lineHeight = 1.5, letterSpacing = 0 } = spec;
    const fs = typeof fontSize === 'number' ? `${fontSize}px` : fontSize;
    const ls = typeof letterSpacing === 'number' ? `${letterSpacing}px` : letterSpacing;
    return `
      <div class="type-sample">
        <div class="type-meta">
          <code>${name}</code>
          <span>${fs} / ${fontWeight} / lh ${lineHeight} / ls ${ls}</span>
        </div>
        <div class="type-preview" style="font-family:${fontFamily};font-size:${fs};font-weight:${fontWeight};line-height:${lineHeight};letter-spacing:${ls}">
          The quick brown fox jumps
        </div>
      </div>
    `;
  }).join('');
  return `
    <section class="section">
      <h2>Typography</h2>
      <div class="type-samples">${samples}</div>
    </section>
  `;
}

function renderSpacing(spacing) {
  if (!spacing || typeof spacing !== 'object') return '';
  const items = Object.entries(spacing).map(([name, value]) => {
    const px = typeof value === 'number' ? value : parseInt(value);
    return `
      <div class="spacing-item">
        <code>${name}</code>
        <div class="spacing-bar" style="width:${px}px"></div>
        <span>${px}px</span>
      </div>
    `;
  }).join('');
  return `
    <section class="section">
      <h2>Spacing</h2>
      <div class="spacing-items">${items}</div>
    </section>
  `;
}

function renderRadius(rounded) {
  if (!rounded || typeof rounded !== 'object') return '';
  const items = Object.entries(rounded).map(([name, value]) => {
    const px = typeof value === 'number' ? value : parseInt(value);
    return `
      <div class="radius-item">
        <div class="radius-box" style="border-radius:${px === 9999 ? '9999' : px}px"></div>
        <code>${name}</code>
        <span>${value}${typeof value === 'number' ? 'px' : ''}</span>
      </div>
    `;
  }).join('');
  return `
    <section class="section">
      <h2>Border Radius</h2>
      <div class="radius-items">${items}</div>
    </section>
  `;
}

// ────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────
const designMd = readFileSync(resolve(designPath), 'utf-8');
const { frontmatter, body } = parseFrontmatter(designMd);

let tokens = frontmatter;
if (tokensPath) {
  try {
    const tokensJson = JSON.parse(readFileSync(resolve(tokensPath), 'utf-8'));
    tokens = { ...frontmatter, ...tokensJson };
  } catch (e) {
    console.warn('⚠️ Não foi possível ler tokens.json — usando apenas frontmatter');
  }
}

const brandName = frontmatter.name || 'Design System';

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(brandName)} — Design System Preview</title>
<style>
  :root {
    --canvas: ${tokens.colors?.canvas || '#ffffff'};
    --ink: ${tokens.colors?.ink || tokens.colors?.text || '#0a0a0a'};
    --muted: ${tokens.colors?.muted || tokens.colors?.['text-muted'] || '#6b6b6b'};
    --hairline: ${tokens.colors?.hairline || tokens.colors?.border || '#e5e5e5'};
    --primary: ${tokens.colors?.primary || '#5e6ad2'};
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--canvas);
    color: var(--ink);
    line-height: 1.5;
    padding: 48px 64px;
    max-width: 1280px;
    margin: 0 auto;
  }
  header {
    border-bottom: 1px solid var(--hairline);
    padding-bottom: 32px;
    margin-bottom: 48px;
  }
  header h1 {
    font-size: 48px;
    font-weight: 600;
    letter-spacing: -1.5px;
    margin-bottom: 8px;
  }
  header p {
    color: var(--muted);
    font-size: 18px;
  }
  .section {
    margin-bottom: 64px;
    padding-bottom: 48px;
    border-bottom: 1px solid var(--hairline);
  }
  .section h2 {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
    margin-bottom: 24px;
  }
  /* Color swatches */
  .swatches {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
  }
  .swatch {
    aspect-ratio: 1.6;
    padding: 16px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    border: 1px solid rgba(0,0,0,0.08);
  }
  .swatch-name { font-weight: 600; font-size: 14px; }
  .swatch-value { font-family: ui-monospace, SF Mono, Menlo, monospace; font-size: 12px; opacity: 0.8; }
  /* Typography */
  .type-samples { display: flex; flex-direction: column; gap: 24px; }
  .type-sample {
    padding: 16px 0;
    border-top: 1px solid var(--hairline);
  }
  .type-sample:first-child { border-top: none; padding-top: 0; }
  .type-meta {
    display: flex;
    gap: 16px;
    align-items: baseline;
    margin-bottom: 12px;
    font-size: 12px;
    color: var(--muted);
    font-family: ui-monospace, SF Mono, Menlo, monospace;
  }
  .type-preview { color: var(--ink); }
  /* Spacing */
  .spacing-items { display: flex; flex-direction: column; gap: 12px; }
  .spacing-item {
    display: grid;
    grid-template-columns: 80px 1fr 80px;
    align-items: center;
    gap: 16px;
    font-family: ui-monospace, SF Mono, Menlo, monospace;
    font-size: 13px;
  }
  .spacing-bar {
    height: 24px;
    background: var(--primary);
    border-radius: 2px;
  }
  /* Radius */
  .radius-items {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 16px;
  }
  .radius-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  .radius-box {
    width: 80px;
    height: 80px;
    background: var(--primary);
    border: 1px solid rgba(0,0,0,0.1);
  }
  .radius-item code {
    font-family: ui-monospace, SF Mono, Menlo, monospace;
    font-size: 13px;
    font-weight: 600;
  }
  .radius-item span { font-size: 12px; color: var(--muted); }
  /* Raw DESIGN.md */
  .raw-doc {
    margin-top: 48px;
    padding-top: 48px;
    border-top: 1px solid var(--hairline);
  }
  .raw-doc h2 { font-size: 24px; margin-bottom: 16px; }
  .raw-doc-content {
    background: rgba(0,0,0,0.03);
    padding: 24px;
    border-radius: 8px;
    font-family: ui-monospace, SF Mono, Menlo, monospace;
    font-size: 13px;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-x: auto;
    max-height: 600px;
    overflow-y: auto;
  }
  .footer {
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid var(--hairline);
    text-align: center;
    font-size: 12px;
    color: var(--muted);
  }
</style>
</head>
<body>
  <header>
    <h1>${escapeHtml(brandName)}</h1>
    <p>${escapeHtml(frontmatter.description || 'Design System Preview')}</p>
  </header>

  ${renderColors(tokens.colors)}
  ${renderTypography(tokens.typography)}
  ${renderSpacing(tokens.spacing)}
  ${renderRadius(tokens.rounded)}

  <section class="raw-doc">
    <h2>📄 DESIGN.md (raw)</h2>
    <div class="raw-doc-content">${escapeHtml(designMd)}</div>
  </section>

  <div class="footer">
    Gerado por <code>design-system-squad</code> · ${new Date().toISOString().split('T')[0]}
  </div>
</body>
</html>`;

writeFileSync(resolve(outputPath), html, 'utf-8');
console.log(`✅ preview.html gerado em ${outputPath}`);
console.log(`   Tamanho: ${(html.length / 1024).toFixed(1)} KB`);
console.log(`   Para visualizar: open "${outputPath}"`);
