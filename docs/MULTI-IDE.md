# Multi-IDE

O **Claude Code é o motor primário** — é onde hooks, skills, comandos, RAG e
roteamento rodam nativamente. As outras ferramentas consomem os mesmos ativos.

| Ferramenta | Como usa o InfinityOS |
|---|---|
| **Claude Code** | Completo e nativo. Tudo funciona out-of-the-box. |
| **VS Code** | Via extensão do Claude Code (lê o mesmo `~/.claude`). Ver `clients/vscode/`. |
| **Codex CLI** | Consome clones/squads como prompts portáveis + roteamento. Ver `clients/codex/`. |
| **Antigravity** | Mesmo modelo de consumo de prompts. Ver `clients/antigravity/`. |
| **Gemini CLI** | Usado como modelo roteado (contexto gigante) e standalone. Ver `clients/gemini-cli/`. |

## Como funciona o consumo "portável"

Cada clone tem um arquivo de system prompt pronto:

```
content/clones/<clone>/<clone>_02_SYSTEM_PROMPT_CLAUDE.md   (completo)
content/clones/<clone>/<clone>_02_SYSTEM_PROMPT_CHATGPT.md  (compacto, ≤8k)
```

Para usar um clone fora do Claude Code, copie o conteúdo do system prompt
apropriado e cole no cliente (Codex/Antigravity/Gemini). O roteador
(`~/.infinity-os/route.py`) ajuda a decidir qual modelo usar por tarefa.

Cada pasta em `clients/` traz o passo a passo específico da ferramenta.
