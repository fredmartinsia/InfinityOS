---
name: organizar-vault
description: Diagnostica e reorganiza um vault Obsidian bagunçado (pastas de projeto espalhadas, memória sem estrutura, notas soltas, nomes inconsistentes), tipicamente de quem instalou uma versão anterior do InfinityOS. Faz varredura de leitura, entrevista curta, propõe um mapa de antes e depois, e só move depois de confirmação, sempre com backup. Nunca apaga nada. Invoque quando o usuário disser "meu vault está bagunçado", "organizar o vault", "arrumar o Obsidian", ou depois de uma atualização do InfinityOS quando notas antigas estão espalhadas.
---

# Organizar Vault: Diagnóstico e Reorganização Segura

Você vai ajudar alguém que não é programador a arrumar o vault Obsidian dela, que
ficou bagunçado com o tempo (ou depois de instalar uma versão antiga do
InfinityOS). Fale em português simples. Toda vez que usar um termo técnico
(vault, wikilink, backlink, frontmatter, etc.) explique em uma frase o que
significa, na hora, sem assumir que a pessoa sabe.

## Regra de ouro, repita isso pra pessoa logo no início

**Nada é apagado, nunca. Reorganizar aqui significa mover de lugar, e mover só
acontece depois que você confirmar o plano. Antes do primeiro movimento, eu
crio uma cópia de segurança (backup) completa do vault inteiro, com a data no
nome, guardada fora da pasta do vault. Se alguma coisa não ficar do jeito que
você queria, dá pra voltar usando essa cópia.**

Diga isso com as suas palavras no início da conversa, antes de rodar qualquer
coisa.

## Pré-requisitos

1. Pergunte o caminho do vault, se ainda não souber (ex: memória
   `obsidian_vault_structure.md` em `~/.claude/projects/*/memory/`, ou
   pergunte direto: "Onde fica seu vault do Obsidian? Pode colar o caminho
   completo, tipo `/Users/nome/Documents/Obsidian Vault`").
2. Confirme que o caminho existe e parece um vault (tem uma pasta
   `.obsidian` dentro; se não tiver, avise a pessoa e confirme antes de
   continuar, pode ser o caminho errado).
3. Guarde o caminho como `$VAULT_PATH` pelo resto da conversa.

Nunca peça pra pessoa fechar o Obsidian. Os movimentos de arquivo funcionam
com o Obsidian aberto ou fechado; se estiver aberto, ele detecta as mudanças
sozinho.

## FASE 1: Diagnóstico automático (não pergunte nada ainda)

Rode o script de varredura, que só lê o vault, não muda nada nele:

```bash
python3 "{caminho-desta-skill}/reference/diagnostico.py" "$VAULT_PATH"
```

Isso evita você (o modelo) ter que ler o vault inteiro nota por nota, o que
gastaria muito contexto à toa: o script já devolve os números prontos.

O script te dá, entre outras coisas:
- quantas notas existem, quantas pastas de primeiro nível (as pastas que
  ficam direto dentro da pasta do vault), qual a profundidade máxima (quantos
  níveis de pasta dentro de pasta existem)
- quantos arquivos estão soltos direto na raiz do vault
- quantas pastas estão vazias ou "quase vazias" (menos de 3 notas dentro),
  sinal de fragmentação, ou seja, conteúdo espalhado em pastas demais
- quantas notas são "órfãs": não têm nenhum link chegando (backlink, ou seja,
  nenhuma outra nota aponta pra ela) nem nenhum link saindo dela. Costuma
  significar que a nota ficou esquecida, ninguém mais acha ela navegando
- duplicatas prováveis: mesmo nome de arquivo em pastas diferentes, e um
  grupo à parte para o sinal mais forte de todos, nome com sufixo " 2" ou
  "(1)", que é a marca clássica de conflito de sincronização (quando dois
  dispositivos salvaram a mesma nota ao mesmo tempo e o serviço de nuvem não
  soube resolver, e criou uma cópia com esse sufixo)
- pastas de primeiro nível com nome parecido, candidatas a virar uma só

O script também separa o que é **estrutura do InfinityOS** (pastas `CLONES`,
`SQUADS`, `DECISOES`, `_META`, `_memory`, `_opensquad`, `Templates`) do que é
**conteúdo próprio da pessoa**. A regra prática: estrutura do InfinityOS só se
mexe se a própria pessoa pedir explicitamente; o foco da reorganização é o
conteúdo dela.

Se quiser os dados também em formato de máquina (para montar o plano da FASE
3 com mais precisão, sem adivinhar), rode com `--json`:

```bash
python3 "{caminho-desta-skill}/reference/diagnostico.py" "$VAULT_PATH" --json
```

### Apresente o retrato

Monte uma tabela simples com os números reais (não invente, não arredonde pra
mais bonito). Por exemplo:

| Métrica | Valor |
|---|---|
| Notas no total | 342 |
| Pastas de primeiro nível | 11 |
| Profundidade máxima de pastas | 6 |
| Arquivos soltos na raiz | 14 |
| Pastas vazias ou quase vazias | 9 |
| Notas órfãs | 47 |
| Duplicatas por conflito de sincronização | 6 grupos |
| Duplicatas por nome repetido | 3 grupos |

Depois da tabela, liste em 3 a 6 frases o que mais chama atenção (o maior
problema, o segundo maior, etc.), sempre citando o número. Não proponha nada
ainda. Feche a FASE 1 perguntando se pode seguir pra entrevista.

## FASE 2: Entrevista curta (use AskUserQuestion)

Só faça as perguntas cuja resposta muda o que você vai propor. São no máximo
4 perguntas, cada uma com 2 a 4 opções (a ferramenta AskUserQuestion sempre
sugere combinar perguntas relacionadas numa única chamada, quando possível).

1. **"Hoje, como você trabalha?"**
   - Atendo clientes (presto serviço pra outras pessoas ou empresas)
   - Toco projetos próprios (meus negócios, meu conteúdo)
   - Os dois

2. **"Você toca mais de uma empresa ou marca?"**
   - Não, só uma
   - Sim, duas ou três
   - Sim, várias (mais de três)

3. **"O que você quer que o sistema lembre sozinho, sem você ter que
   organizar na mão?"**
   - Decisões importantes (o que ficou combinado, o que mudou de rumo)
   - Reuniões (resumo do que foi falado)
   - Aprendizados e insights (coisas que você descobriu e quer guardar)
   - Nada disso, prefiro anotar do meu jeito

4. **"Qual o incômodo maior hoje?"**
   - Não acho as coisas (sei que a nota existe, mas não lembro onde)
   - Tenho duplicata e bagunça (arquivos repetidos, pastas confusas)
   - Não sei onde salvar coisa nova (fico sem saber em que pasta colocar)

Anote as respostas. Elas decidem a topologia (a forma como as pastas vão ficar
organizadas) que você vai propor na FASE 3. Não existe estrutura fixa: por
exemplo, se a pessoa atende clientes E toca projetos próprios, provavelmente
faz sentido separar `Clientes/` de `Projetos/`; se ela só tem projetos
próprios, talvez nem precise dessa separação. Se ela tem várias marcas, talvez
cada marca vire uma pasta de primeiro nível. Use julgamento, não um molde
pronto.

## FASE 3: Proposta (mapa de antes e depois)

Monte uma tabela ou lista pasta por pasta, mostrando exatamente o que vai pra
onde. Formato sugerido:

```
ANTES                              DEPOIS                              MOTIVO
Diario/2026/                       Diario/2026/                        fica igual
Projeto X/                         Clientes/Projeto X/                 e cliente (FASE 2, pergunta 1)
Projetos Ativos/                   Projetos/                           nome parecido com "Projetos", junta as duas
Ideia 2.md (raiz)                  _revisar-duplicatas/Ideia 2.md      duplicata provavel, voce decide depois
nota solta na raiz.md              Inbox/nota solta na raiz.md         arquivo solto vai pra uma pasta de entrada
```

Regras pra montar esse mapa:
- **Duplicata suspeita nunca é apagada.** Ela vai para uma pasta de
  quarentena chamada `_revisar-duplicatas/` (dentro do próprio vault), pra
  pessoa decidir com calma qual versão manter. Deixe isso bem claro na
  proposta.
- Pastas vazias ou quase vazias: proponha juntar com a pasta mais parecida,
  ou avise que vai virar uma pasta "Arquivo" ou "Antigos" se o conteúdo for
  velho e ninguém souber pra onde vai.
- Notas soltas na raiz: proponha um destino (uma pasta "Inbox" ou a pasta de
  primeiro nível mais óbvia pelo conteúdo da nota).
- Estrutura do InfinityOS (`CLONES`, `SQUADS`, `DECISOES`, `_META`, `_memory`,
  `_opensquad`, `Templates`) **não é tocada**, a menos que a pessoa peça.
- Diga explicitamente, numa lista separada, **o que NÃO vai ser tocado**
  (tudo que fica exatamente onde está).

Termine a FASE 3 com uma pergunta de confirmação (AskUserQuestion), por
exemplo:
- "Pode seguir com esse plano?"
- "Quero ajustar algo antes"
- "Cancelar, não quero mexer agora"

Só avance pra FASE 4 se a resposta for claramente positiva. Se a pessoa
pedir ajuste, refaça o mapa e pergunte de novo.

## FASE 4: Execução segura

Esta é a fase mais delicada. Siga a ordem à risca.

### 1. Backup completo, antes de qualquer movimento

```bash
mkdir -p ~/vault-backups
tar -czf ~/vault-backups/vault-backup-$(date +%Y%m%d-%H%M).tar.gz -C "$(dirname "$VAULT_PATH")" "$(basename "$VAULT_PATH")"
```

Confirme que o arquivo foi criado (`ls -lh ~/vault-backups/`) e informe o
caminho completo pra pessoa: *"Backup salvo em
`~/vault-backups/vault-backup-AAAAMMDD-HHMM.tar.gz`. Se algo sair errado, é
só descompactar esse arquivo pra recuperar o vault como ele estava antes."*

Esse comando só lê o vault e escreve um arquivo novo fora dele: não apaga nem
move nada de dentro do vault, então não esbarra em nenhuma proteção.

### 2. Crie o arquivo de registro

Antes do primeiro movimento, crie (com a ferramenta Write, nunca via Bash,
porque o vault é protegido por um hook que só libera escrita através das
ferramentas normais de edição) o arquivo de registro. Prefira dentro de
`_META/` se essa pasta existir; senão, direto na raiz do vault:

```
$VAULT_PATH/_META/📋 REGISTRO - Reorganizacao do Vault (AAAA-MM-DD).md
```

Conteúdo inicial:

```markdown
---
tipo: registro-reorganizacao
data: AAAA-MM-DD
---

# Registro da reorganização do vault

Backup completo salvo antes de começar em:
`~/vault-backups/vault-backup-AAAAMMDD-HHMM.tar.gz`

Cada linha abaixo é um movimento feito. Pra desfazer um movimento, basta
mover o arquivo de volta do caminho "para" pro caminho "de".

| De | Para |
|---|---|
```

Depois de CADA lote de movimentos (veja o passo 4), adicione as linhas novas
nessa tabela usando Edit. Isso deixa o histórico completo dentro do próprio
vault, não só na conversa, então a pessoa consegue desfazer mesmo dias depois.

### 3. Duplicatas suspeitas vão para quarentena, nunca são apagadas

Para cada duplicata provável identificada na FASE 1/3:

```bash
mkdir -p "$VAULT_PATH/_revisar-duplicatas"
```

Mova as cópias suspeitas pra lá (mantendo os nomes originais, ou prefixando
com o nome da pasta de origem se dois arquivos suspeitos tiverem o mesmo
nome, pra uma não sobrescrever a outra). A nota "original" (a mais recente ou
mais completa, use bom senso e, se não for óbvio, pergunte) pode ficar no
lugar novo definitivo; só a(s) cópia(s) duvidosa(s) vai(vão) pra quarentena.

### 4. Trabalhe em lotes

Não mova tudo de uma vez. Separe o mapa da FASE 3 em lotes de tamanho
razoável (por exemplo, por pasta de primeiro nível, ou uns 20 a 30 arquivos
por vez). Para cada lote:

1. Mova os arquivos e pastas do lote (comando `mv`, dentro do vault,
   permitido pelo hook de proteção porque origem e destino continuam dentro
   do vault; só é bloqueado mover pra FORA do vault ou apagar).
2. Registre os movimentos desse lote no arquivo de registro (passo 2).
3. Rode a checagem de links (próximo item) considerando só os movimentos
   desse lote.
4. Mostre o progresso pra pessoa: *"Lote 2 de 5 concluído, X arquivos
   movidos. Continuo?"*
5. Só siga pro próximo lote depois que a pessoa confirmar (ou combine
   previamente rodar tudo sem pausa, se ela preferir).

Se a pessoa quiser parar no meio, pare depois de terminar o lote atual (nunca
no meio de um lote). Como cada lote já foi registrado e os links dele já
foram checados, o vault fica num estado consistente mesmo se parar ali,
faltando só os lotes seguintes, que podem ser retomados depois nesta mesma
skill.

### 5. Corrija ou avise sobre links quebrados

Mover uma nota pode quebrar link interno (aquele texto `[[Nome da Nota]]` ou
`[[Pasta/Nome da Nota]]` que faz uma nota apontar pra outra dentro do
Obsidian). Um wikilink simples, sem barra, tipo `[[Reunião]]`, normalmente
continua funcionando depois de mover a nota, porque o Obsidian resolve pelo
nome, não pelo caminho. Já um link com caminho (`[[Pasta/Reunião]]`) ou um
link estilo markdown (`[texto](Pasta/Reunião.md)`) quebra, porque aponta pro
caminho antigo.

Depois de cada lote, monte um `movimentos.json` com o formato:

```json
[{"de": "Diario/Ideia.md", "para": "Projetos/Cliente A/Ideia.md"}]
```

E rode:

```bash
python3 "{caminho-desta-skill}/reference/checar_links.py" "$VAULT_PATH" movimentos.json
```

Isso mostra o que encontrou, sem mudar nada ainda. Revise a lista com a
pessoa se for curta, ou, se for grande e os movimentos forem só de pasta
(sem trocar o nome do arquivo), pode rodar com `--fix` pra corrigir os links
com caminho automaticamente:

```bash
python3 "{caminho-desta-skill}/reference/checar_links.py" "$VAULT_PATH" movimentos.json --fix
```

O `--fix` só mexe em links que têm caminho (path). Wikilinks simples citando
um nome que mudou de verdade (renomeação, não só mudança de pasta) aparecem
numa lista à parte, marcados como "revisar na mão": não são corrigidos
sozinhos porque um nome pode ser ambíguo. Mostre essa lista pra pessoa
explicando: *"Estes aqui podem ter quebrado porque o nome da nota mudou.
Confere se ainda fazem sentido."*

### 6. Fechamento

Ao terminar todos os lotes (ou quando a pessoa decidir parar), resuma:
- quantos arquivos foram movidos no total
- onde está o backup
- onde está o arquivo de registro (`_META/📋 REGISTRO...md`)
- quantas duplicatas foram pra `_revisar-duplicatas/` e que ela precisa
  decidir o que fazer com elas quando puder (comparar as duas versões,
  apagar a que não serve, na mão, direto no Obsidian ou no Finder/Explorer,
  já que esta skill nunca apaga nada sozinha)
- quantos links foram corrigidos automaticamente e quantos precisam de
  revisão manual

## Regras duras (não negociáveis)

- **Nunca apague nada.** Nenhum comando `rm`, nenhum "limpar", nenhum
  "descartar". Só mover.
- **Nunca mova nada sem confirmação explícita** do plano da FASE 3.
- **Backup sempre antes do primeiro movimento**, sem exceção, mesmo que a
  pessoa diga que não precisa.
- **Duplicata vai pra quarentena (`_revisar-duplicatas/`), nunca é apagada.**
- **Registre cada movimento** no arquivo dentro do vault, pra dar pra
  desfazer.
- **Trabalhe em lotes**, sempre num estado consistente entre um lote e outro.
- **Nunca use travessão (em dash)** em nenhum texto que você escrever,
  incluindo dentro dos arquivos do vault. Use vírgula, ponto, dois-pontos,
  parênteses, ou reescreva a frase. Hífen comum em palavra composta
  (`quase-vazia`, por exemplo) pode.
- **Não invente estrutura de pasta fixa.** A organização final sai das
  respostas da FASE 2 e do que já existe no vault, não de um molde genérico.
- Se em algum momento o comando de mover for bloqueado por um aviso de
  proteção do vault (hook de segurança), é porque o destino calculado caiu
  fora da pasta do vault por engano, ou porque o comando parece uma
  exclusão. Pare, confira o caminho, e nunca tente contornar a proteção.

## Retomar depois de uma pausa

Se a pessoa voltar numa conversa nova pra continuar uma reorganização
começada antes, procure o arquivo `_META/📋 REGISTRO - Reorganizacao...md`
mais recente dentro do vault: ele mostra o que já foi feito. Rode o
diagnóstico de novo (FASE 1) pra ver o estado atual, e retome dali, sem
repetir a entrevista se as respostas da FASE 2 ainda estiverem óbvias pelo
contexto (pergunte se mudou algo antes de assumir).
