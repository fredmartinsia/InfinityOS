# Cliente: Gemini CLI

A Gemini CLI tem dois papéis no InfiniteOS:

1. **Modelo roteado** — o roteador manda tarefas de contexto gigante,
   extração/OCR e ingestão de documentos para o Gemini:

   ```bash
   python3 ~/.infinite-os/route.py --task "resumir este PDF de 200 páginas" --dry-run
   # → gemini  [gemini/gemini-2.5-pro]  — comando: gemini -p {prompt}
   ```

2. **Motor do writer** — o hook `vault_writer_bg.py` pode usar a Gemini CLI para
   sumarizar sessões em background (configurável via `CLAUDE_GEMINI_CMD`).

## Usar um clone

Cole o `*_02_SYSTEM_PROMPT_*.md` do clone como instrução inicial:

```bash
gemini -p "$(cat <vault>/CLONES/<clone>/<clone>_02_SYSTEM_PROMPT_CHATGPT.md)

Minha pergunta: ..."
```

## Instalação

O instalador oferece instalar a Gemini CLI no passo 2
(`npm install -g @google/gemini-cli`).
