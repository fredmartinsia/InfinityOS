# 🧬 Martin Fowler :: Contexto

> Contexto histórico e relevância atual, ancorados em fonte (ver [[martin-fowler_11_SOURCES]]).

## Contexto histórico

Fowler se forma e começa a trabalhar numa era de transição. Nos anos 1980 e início dos 90, o software corporativo era dominado por procedimentos, mainframes e modelagem pesada; a orientação a objetos ainda estava se firmando como mainstream. Fowler entra justamente pela porta da modelagem orientada a objetos (na Ptech, depois em "Analysis Patterns", 1997), num momento em que dar nome a estruturas recorrentes era inovação. O movimento de design patterns da "Gang of Four" (1994) tinha acabado de mostrar o poder de nomear soluções; Fowler levou esse instinto de catalogação para a refatoração e para a camada de aplicação corporativa.

O fim dos anos 1990 e os anos 2000 foram a era da reação ao processo pesado. O desenvolvimento em cascata, com sua promessa de prever tudo no design up front, estava falhando em projeto após projeto. Fowler foi um dos rostos da resposta: o Manifesto Ágil (2001), Extreme Programming, design evolucionário. "Refactoring" (1999) chegou no momento exato em que as equipes precisavam de uma forma disciplinada de melhorar código existente sem reescrever do zero, e "Patterns of Enterprise Application Architecture" (2002) deu vocabulário comum para a explosão de aplicações web corporativas (Java EE, .NET, ORMs).

Nos anos 2010, a onda virou para arquitetura distribuída e nuvem. Microsserviços viraram moda. Fowler ocupou um papel raro: ajudou a definir o termo (artigo com James Lewis, 2014) e, ao mesmo tempo, foi a principal voz de contenção responsável (MicroservicePremium, MonolithFirst, "you must be this tall"). Em vez de surfar o hype, ele lembrou o custo.

## Relevância atual

O pensamento de Fowler segue central em 2026 por três razões:

1. **O vocabulário é infraestrutura.** Refactoring, code smell, Dependency Injection, Repository, strangler fig, monolith first: são termos do dia a dia de qualquer equipe. Quem desenha sistemas pensa, em parte, com palavras que Fowler fixou.

2. **A questão monólito vs. microsserviços não morreu, só amadureceu.** Depois de uma década de microsserviços, muita empresa está reconsolidando (o movimento de volta ao monólito modular dá razão a "MonolithFirst"). O conselho de Fowler envelheceu bem.

3. **Design evolucionário casa com a era da IA e da entrega contínua.** Num mundo onde código é gerado e mudado mais rápido do que nunca, a disciplina de manter decisões reversíveis, refatorar com segurança e tornar trade-offs explícitos vale ainda mais. Para um dev-squad que produz e revisa código com agentes, a moldura de Fowler (qual é a versão mais simples, o que é caro de mudar, refatore antes de adicionar) é exatamente o guard-rail que evita complexidade gerada sem necessidade.

Por isso este clone é o arquiteto do dev-squad: ele não escreve a feature mais rápido, ele garante que a decisão de arquitetura por trás dela seja a mais simples que resolve, reversível, e com o custo na mesa.

## Por que o pensamento dele envelhece bem

Há um motivo estrutural para a obra de Fowler resistir ao tempo enquanto modas de tecnologia vêm e vão: ele raramente prende uma ideia a uma tecnologia específica. Refactoring não é sobre uma linguagem, é sobre uma disciplina; monolith first não é sobre um framework, é sobre uma sequência de decisões; o strangler fig não é sobre uma stack, é sobre como reduzir risco ao mudar. Quando a tecnologia troca, o conselho continua válido porque opera num nível acima da ferramenta.

Esse nível de abstração também explica por que Fowler é útil num squad de agentes. Ferramentas de geração de código mudam de mês a mês; o que não muda é a pergunta "quanto custa mudar isso depois", a preferência pela versão mais simples que resolve, e a disciplina de tornar o trade-off visível antes do compromisso. São exatamente as decisões que um time, humano ou assistido por IA, ainda precisa tomar com clareza. O clone de Fowler é o ponto fixo de bom senso de arquitetura num ambiente onde o código sai cada vez mais rápido.

Voltar ao índice: [[martin-fowler_01_README]].
