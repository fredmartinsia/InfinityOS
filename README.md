<div align="center">

# 🧠 InfinityOS

**Um sistema operacional de orquestração de agentes — replicável em qualquer máquina.**

Clones de especialistas, squads multi-agente, RAG automático com Obsidian e
roteamento inteligente de modelos (Claude, Gemini, Qwen, Ollama) — tudo
instalável com um comando.

</div>

---

## ⚡ Quickstart

```bash
git clone <URL-DO-REPO> infinity-os
cd infinity-os
./install.sh
```

O instalador é **guiado e à prova de erros**: ele detecta seu computador,
pergunta antes de instalar qualquer coisa e usa defaults seguros (basta
apertar Enter). Ao final, abra o Claude Code e rode:

```
/onboarding
```

…para a entrevista que personaliza tudo ao seu jeito.

---

## 🎁 O que você recebe

| Camada | Conteúdo |
|---|---|
| **Motor (Claude Code)** | Hooks de RAG e proteção do vault, skills (`createclone`, `opensquad`, `obsidian-*`), comandos de squads. |
| **Conhecimento (Obsidian)** | Vault estruturado, regras canônicas, RAG indexado e pronto na 1ª sessão. |
| **Conteúdo** | Clones de especialistas (12 arquivos cada) + squads multi-agente prontos para uso. |
| **Roteamento** | Camada que escolhe o modelo certo por tarefa (Claude / Gemini / Qwen / Ollama) com fallback. |
| **Frameworks** | AIOX (via `npx`) + opensquad para pipelines complexos. |
| **Multi-IDE** | Claude Code (primário); guias para VS Code, Codex, Antigravity e Gemini CLI. |

---

## 🧩 Pré-requisitos

O instalador **verifica e oferece instalar** o que faltar. Você só precisa
chegar com:

- macOS, Linux ou WSL (Windows nativo: previsto para fase 2)
- `git` e `python3` ≥ 3.9
- Claude Code CLI (recomendado)

Opcionais que o instalador propõe configurar: **Obsidian**, **Ollama**,
**Gemini CLI**, **Qwen-Code CLI**, **Codex CLI**, **gh**.

---

## 🔒 Privacidade

Este repositório contém **apenas estrutura, templates e ativos reutilizáveis** —
nenhum dado pessoal ou de projeto. Um gate automatizado (`scripts/sanitize-check.sh`
+ `gitleaks`) bloqueia qualquer push que contenha segredos ou PII.

---

## 📚 Documentação

- [`docs/INSTALL.md`](docs/INSTALL.md) — instalação passo a passo
- [`docs/ONBOARDING.md`](docs/ONBOARDING.md) — a entrevista pós-instalação
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — como as camadas se conectam
- [`docs/MODEL-ROUTING.md`](docs/MODEL-ROUTING.md) — roteamento de modelos
- [`docs/MULTI-IDE.md`](docs/MULTI-IDE.md) — usar em outras IDEs
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) — problemas comuns

> Para desinstalar: `./uninstall.sh` (restaura o backup feito antes da instalação).
