# Requisitos de hardware & modelos locais

O instalador analisa seu computador (RAM, núcleos, GPU/Apple Silicon) e recomenda
o modelo local adequado, antes de baixar qualquer coisa. Você sempre confirma.

## Mínimo para o InfiniteOS

- macOS, Linux ou WSL
- Python 3.9+, git
- Node/npx (para AIOX e algumas CLIs)
- Claude Code CLI (recomendado)

Modelos locais são **opcionais** — sem eles, o roteador usa a nuvem (Claude/Gemini).

## Tiers de modelo local (Ollama)

| RAM | Tier | Modelo recomendado |
|---|---|---|
| < 8 GB | minimal | (preferir nuvem) |
| 8–16 GB | light | `qwen2.5-coder:7b` |
| 16–32 GB | standard | `qwen2.5-coder:14b` |
| 32–64 GB | power | `qwen3-coder:30b` |
| 64 GB+ | workstation | `qwen3-coder:30b` |

**Bônus de GPU:** Apple Silicon (memória unificada) ou GPU com ≥16 GB de VRAM
sobem um tier automaticamente.

Os tiers ficam em `routing/hardware-tiers.yaml` (editável). O instalador roda
`ollama pull <modelo>` apenas após sua confirmação.
