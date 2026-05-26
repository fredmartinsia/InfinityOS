# Roteamento de modelos

O InfinityOS escolhe o modelo certo para cada tarefa — barateando o que dá e
mantendo qualidade onde importa. O roteador fica em `~/.infinity-os/route.py` e a
config em `~/.infinity-os/router.config.yaml`.

## Lógica

1. **Tipo de tarefa** (override) tem prioridade: `huge_context`, `image_generation`,
   `code_refactor`, `cross_validation`.
2. Senão, usa a **complexidade** estimada (0–10) por heurística de palavras-chave:
   - `0–2` → **Claude** (resolve inline)
   - `3–6` → **Gemini** (documentos grandes, extração, OCR)
   - `7–10` → **Qwen/Ollama** (raciocínio de código, refactors)
3. **Fallback**: se o modelo preferido não estiver instalado, cai para o próximo
   da cadeia, terminando sempre no Claude (que está sempre presente).

## Uso

```bash
python3 ~/.infinity-os/route.py --task "refatorar esta função recursiva"
python3 ~/.infinity-os/route.py --task "resumir este PDF de 200 páginas" --dry-run
python3 ~/.infinity-os/route.py --type image_generation
python3 ~/.infinity-os/route.py --score 8 --json
```

Exemplo de saída:

```
→ qwen  [ollama/qwen3-coder:30b]  — complexidade 9/10
```

## Config (`router.config.yaml`)

Editável à mão. Define os alvos (provider/modelo/comando), as faixas de
complexidade, os overrides por tipo e as cadeias de fallback. O modelo local
(`qwen`) é ajustado na instalação conforme o seu hardware
(ver [HARDWARE-REQUIREMENTS.md](HARDWARE-REQUIREMENTS.md)).

> Sem `pyyaml` instalado, o `route.py` usa defaults embutidos equivalentes — ele
> nunca quebra por falta de dependência.
