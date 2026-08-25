# Atualizar quem já tem uma versão antiga instalada

Este guia é para quem instalou o InfinityOS antes e vai atualizar. Se é a sua
primeira instalação, vá direto para o [INSTALL.md](INSTALL.md).

## A regra que vale acima de tudo

**A atualização nunca apaga o que é seu.** Squad que você criou, nota que você
escreveu, ajuste que você fez: nada disso é tocado. Se você editou um arquivo
que veio do pacote, a sua versão é guardada ao lado com o sufixo `.seu`, em vez
de ser perdida.

Antes de qualquer coisa, o instalador faz um backup completo e diz onde ele
ficou. Se algo der errado, é só copiar de volta.

## Como atualizar

```bash
cd infinity-os
git pull
./install.sh
```

O instalador percebe sozinho que já existe uma instalação e muda de
comportamento. Ele não vai repetir perguntas que você já respondeu.

## O que acontece no passo 2

Logo no começo, ele mostra um retrato do que encontrou no seu computador:

- qual versão você tem hoje e qual é a nova
- quantos squads, skills e scripts estão instalados
- onde está o seu vault, quantos clones e quantas notas suas existem nele
- se o LightRAG já está instalado

Depois, separa o que veio do pacote do que é seu. Um squad que existe no seu
computador mas não existe no pacote foi criado por você. Ele aparece numa lista
à parte, e não é tocado em nenhuma hipótese.

Aí você escolhe entre três modos:

| Modo | O que faz | Quando usar |
|---|---|---|
| **Atualizar preservando** | Atualiza o conteúdo do pacote e mantém tudo que é seu. Arquivo do pacote que você editou vira `.seu` ao lado do novo. | O padrão, serve para quase todo mundo |
| **Só adicionar o que falta** | Instala apenas o que ainda não existe. Não altera nada que já está aí. | Se você mexeu muito e não quer risco nenhum |
| **Reinstalar do zero** | Apaga a instalação do sistema e refaz. Faz backup completo antes. Suas notas do vault continuam intocadas. | Se a instalação atual está quebrada |

## O vault bagunçado

Se o seu vault já tem mais de dez notas, o instalador **não cria pasta nenhuma
por cima**. Isso é proposital: mexer na estrutura de um vault em uso é
justamente o que costuma piorar a bagunça.

A arrumação é feita depois, por uma conversa guiada. Abra o Claude Code e rode:

```
/organizar-vault
```

O que ela faz, nesta ordem:

1. **Mostra um retrato antes de propor qualquer coisa**: quantas notas soltas na
   raiz, quantas pastas com pouquíssimo conteúdo, notas órfãs (sem nenhum link),
   duplicatas prováveis (arquivo com sufixo ` 2` ou `(1)`, que quase sempre é
   conflito de sincronização), pastas com nome parecido que deveriam ser uma só.
2. **Faz poucas perguntas, e só as que mudam o resultado**: se você atende
   clientes ou toca projetos próprios, se tem mais de uma marca, o que você quer
   que o sistema lembre sozinho, e qual é o seu maior incômodo hoje.
3. **Mostra o mapa de antes e depois**, pasta por pasta, e o que não será tocado.
4. **Só então move**, depois da sua confirmação, com backup feito e um registro
   de cada movimento, para você poder desfazer.

Nada é apagado. Duplicata suspeita vai para uma pasta de quarentena chamada
`_revisar-duplicatas/`, para você decidir depois com calma.

## As chaves de API

Se você já configurou alguma chave, o instalador detecta, testa contra a API e
não pergunta de novo. Só pergunta pelas que faltam.

Para rodar só esse passo, a qualquer momento:

```bash
./install.sh --step=25
```

Para cada provedor que faltar, ele abre a página de cadastro no seu navegador,
espera você gerar a chave, testa se ela funciona de verdade e só então guarda,
em `~/.config`, com permissão restrita. Nenhuma chave entra no repositório.

## O LightRAG

É a memória de longo prazo do sistema, o que faz ele lembrar do seu contexto
entre conversas diferentes. Sem ele o harness funciona, mas perde essa memória.

O instalador verifica se você já tem. Se tiver e estiver funcionando, não mexe.
Se não tiver, ele checa os pré-requisitos um a um, instala o que falta e explica
o que está fazendo.

Para rodar só esse passo:

```bash
./install.sh --step=65
```

## Rodar um passo específico

Todo passo pode ser executado isolado, sem refazer o resto:

```bash
./install.sh --step=05   # detectar instalação anterior
./install.sh --step=20   # escolher o modelo local pelo seu hardware
./install.sh --step=25   # chaves de API
./install.sh --step=65   # LightRAG
./install.sh --step=70   # verificação final
```

Isso é útil quando algo falha no meio: você corrige e retoma daquele ponto, sem
começar tudo de novo.

## Se algo der errado

O backup fica em `~/.infinity-os-backup-<data>-<hora>`. O log completo da
instalação fica em `~/.infinity-os-install.log`, e mostra exatamente onde parou.
