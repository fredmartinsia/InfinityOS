# Onboarding (pós-instalação)

Depois do `./install.sh`, abra o Claude Code e rode:

```
/onboarding
```

É uma **entrevista conversacional** (~20–30 min) que personaliza o ambiente ao
seu contexto. Você responde no fluxo, sem formulário.

## O que ele faz

1. **Entrevista** — identidade, negócios, projetos, clientes, stack técnica e
   estilo de trabalho.
2. **Organiza o vault** — cria índices, MOCs e dashboards a partir do que você
   contou (respeitando a estrutura de pastas escolhida na instalação).
3. **Popula a memória** — escreve as memórias do Claude Code
   (`~/.claude/projects/.../memory/`) com seu perfil, vocabulário e preferências.
4. **Confere os clones** — garante que os clones estão no vault e gera MOCs
   temáticos.

## Depois

- Reinicie o Claude Code para carregar as memórias.
- Teste um squad: `/<nome-do-squad>` (ex.: `/hormozi-squad`).
- É seguro rodar `/onboarding` de novo — ele não sobrescreve o que já existe sem
  necessidade.

> Respostas imperfeitas ajudam — o sistema ajusta com o tempo conforme você usa.
