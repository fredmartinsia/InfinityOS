# Instalação

## TL;DR

```bash
git clone <URL-DO-REPO> infinity-os
cd infinity-os
./install.sh
```

Depois, no Claude Code: `/onboarding`.

## O que o instalador faz (8 passos)

1. **Preflight** — detecta SO, RAM, GPU e checa pré-requisitos.
2. **CLIs** — para cada ferramenta ausente (Ollama, Gemini, Qwen-Code, Codex, gh),
   pergunta se pode instalar.
3. **Modelo local** — recomenda e (com seu OK) baixa um modelo Ollama compatível.
4. **Núcleo Claude Code** — backup, scripts/skills, `settings.json`, roteador,
   proteção do vault.
5. **AIOX** — opcionalmente roda `npx aiox-core@latest install`.
6. **Conteúdo** — instala squads (`~/.claude/commands/`) e clones (vault/CLONES).
7. **Obsidian + RAG** — detecta/instala o Obsidian, monta a estrutura do vault
   sob medida e constrói o índice de RAG.
8. **Verificação** — smoke test de tudo.

## Defaults seguros

- Enter = "sim" nos passos com default positivo.
- Nada é instalado sem confirmação.
- Antes de tocar no `~/.claude`, é feito **backup** em `~/.infinity-os-backup-<data>`.

## Flags

```bash
./install.sh -y           # aceita defaults (não-interativo)
./install.sh --step=30    # roda só um passo
```

Variáveis úteis para CI/testes (pulam etapas de rede):
`INFINITY_OS_SKIP_CLIS`, `INFINITY_OS_SKIP_MODELS`, `INFINITY_OS_SKIP_AIOX`,
`INFINITY_OS_SKIP_PLUGINS` (todas = `1` para pular).

## Desinstalar

```bash
./uninstall.sh
```

Restaura o backup mais recente do `~/.claude`. Plugins e conteúdo do vault não são
removidos automaticamente.
