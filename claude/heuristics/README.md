# Heuristicas de trabalho do o usuário

Acervo canonico e portavel das heuristicas de como colaborar com o usuário, destiladas
por engenharia reversa de 2706 prompts reais (claude-mem) + LightRAG + memorias.

## Estrutura de cada heuristica
Cada `.md` tem frontmatter YAML (parseavel por maquina) + corpo legivel:
`id, title, layer, confidence (0..1), deterministic, triggers, source, code_ref`,
seguido de: Regra, Quando aplicar, Como aplicar, Anti-padroes, Evidencia, Aplicacao deterministica.

## Tres camadas de uso
1. **Fonte canonica**: estes `.md` (portaveis para qualquer ferramenta).
2. **Claude Code**: cada heuristica com `instinct: true` vira um instinto injetado no
   SessionStart via `instincts.py` (nota de confianca que reforca/decai com o uso).
3. **Deterministico**: o que e regra fixa vira hook/script (custo de token zero).
   Ex: `no_emdash_guard.py` (proibicao do travessao) roda como PreToolUse.

### Ficha sem instinto no store nao e falha

Conferido em 2026-08-20: o acervo tem 22 fichas e o store `~/.claude/instincts/personal`
tem 21 instintos. A diferenca e proposital, nao um esquecimento a ser corrigido:

- `proibido-travessao` fica de fora porque o hook `no_emdash_guard.py` ja garante a regra
  por codigo. Injetar tambem seria pagar token por algo que nao pode falhar.
- `idioma-portugues-correto` tem o idioma base garantido pela config `language`. A parte
  que exige julgamento (pt-BR contra pt-PT conforme o publico) foi semeada a parte, como
  `portugues-pt-br-ou-pt-pt`.

Regra geral: ficha `deterministic: true` COM `code_ref` preenchido nao precisa de instinto.
Sem `code_ref`, ou vira hook, ou vira instinto. O que nao pode e ficar nas duas ausencias.

## Como replicar para outras ferramentas
- **Codex CLI / Google Antigravity**: copie o `AGENTS.md` (gerado aqui) para a raiz do
  projeto. Ambos leem esse arquivo automaticamente como regras do agente.
- **Cursor**: converta o `AGENTS.md` em `.cursor/rules/fred.mdc` (mesmo conteudo).
- **Claude Code**: ja integrado via instintos; as meta-heuristicas tambem entram no CLAUDE.md.

## Regra global inviolavel
Nunca usar o travessao (em dash, o traco longo de pontuacao) em nenhum texto. Trocar por
ponto, virgula, dois-pontos, parenteses, ou reescrever. Hifen comum e permitido.

Indice completo em [INDEX.md](INDEX.md).
