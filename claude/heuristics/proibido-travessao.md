---
id: proibido-travessao
title: Proibido o travessao / em dash
layer: deterministico
domain: estilo
confidence: 0.95
deterministic: true
triggers: [*]
source: CLAUDE.md + hook
code_ref: no_emdash_guard.py
---

> Nunca use o traco longo de pontuacao (em dash, en dash) em nenhum texto; hifen comum e permitido. Aplicado por hook (codigo), nao por heuristica.

## Regra
Nunca use o travessao longo (em dash, en dash, horizontal bar) em copy, post, email, documento, codigo ou mensagem. Troque por ponto, virgula, dois-pontos, parenteses ou reescreva. Hifen comum em palavras compostas e permitido.

## Quando aplicar
Todo texto gerado para o usuÃ¡rio.

## Como aplicar
- Gravar arquivo: o hook no_emdash_guard.py bloqueia automaticamente (PreToolUse Write/Edit).
- No chat: auto-policie, o codigo nao intercepta o chat.

## Anti-padroes
- Usar o caractere de traco longo em qualquer lugar.

## Evidencia
- Regra global do CLAUDE.md. 65 prompts contem o caractere no input (regra e de saida). Qwen confirmou determinismo, confianca 1.0.

## Aplicacao deterministica
Aplicada/apoiada por codigo: `no_emdash_guard.py`. Onde possivel, o codigo executa a regra; o modelo nao precisa lembrar dela.
