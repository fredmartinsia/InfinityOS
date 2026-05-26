---
tags: [meta, regras, protecao]
tipo: regras-do-vault
---

# 📋 Regras do Vault

> Estas regras protegem seu vault contra perda acidental e mantêm a estrutura
> consistente para o RAG funcionar bem. O Claude Code lê este arquivo e as
> respeita. Caminho do vault: `{{VAULT_PATH}}`

## 🛑 1. Proteção contra deleção (prioridade máxima)

Apagar arquivos/pastas ou movê-los para fora do vault **exige confirmação humana**.

- O hook `vault_guard.py` (PreToolUse) **bloqueia automaticamente** comandos
  destrutivos (`rm`, `rmdir`, `mv` para fora, truncamento via `>`) que toquem o vault.
- Para liberar UMA operação, o fluxo é:
  1. O Claude pergunta o que será apagado (via AskUserQuestion).
  2. Você responde **"Sim"**.
  3. Só então roda `python3 ~/.claude/scripts/vault_grant.py` (ticket de 120s, 1 uso).
  4. O hook consome o ticket e libera aquela operação.
- **Nunca** rode `vault_grant.py` preventivamente, em lote ou dentro de loop/squad.
  É a confirmação humana ativa que protege — processos automáticos nunca confirmam.
- Defina seu código de proteção com `python3 ~/.claude/scripts/vault_guard_setup.py`
  (só o hash SHA-256 fica salvo localmente, nunca em texto).

## ✏️ 2. Alterações de conteúdo são livres — mas preserve a identidade

Criar, adicionar e renomear dentro do vault é livre. **Não** reescreva a
identidade/contexto de uma entidade já documentada. Se uma mudança **contradiz**
(em vez de complementar) o que já está escrito, pare e pergunte.

## 🗂️ 3. Estrutura canônica

- **Squads** vivem em `SQUADS/` (top-level), nunca dentro de `Projetos/`.
- **Clones** vivem em `CLONES/`, um por pasta, com os arquivos numerados padrão.
- Índices e dashboards ficam em `_META/`.
- Templates reutilizáveis em `Templates/`.

## 🔄 4. Conflitos de sincronização

Se aparecerem pastas/arquivos com sufixo ` 2`, ` 3`, `(1)` etc., ou arquivos
sumirem, **pare**: é conflito de sync. Recomendação: manter o vault **100% local**
(evitar sincronizar a pasta de Documentos por serviços de nuvem que renomeiam em
conflito). Faça backup antes de operações em massa:

```bash
tar -czf ~/vault-backup-$(date +%Y%m%d-%H%M).tar.gz "{{VAULT_PATH}}"
```

## 💾 5. Backup defensivo

Antes de qualquer operação em massa (mover/reorganizar muitas notas), gere um
snapshot com o comando acima. Barato e salva o dia.
