# 🧬 Martin Fowler :: Pensamento e Heurísticas

> Modelos de decisão de Fowler, ancorados nos frameworks reais (ver [[martin-fowler_06_KNOWLEDGE_COMPLETE]] e [[martin-fowler_11_SOURCES]]).

## Pergunta axial

**"Quanto custa mudar isso depois?"**

Toda decisão de arquitetura, para Fowler, gira em torno do custo de reversão. Arquitetura é justamente o conjunto de decisões difíceis de mudar; por isso as decisões importam, e por isso as melhores são as que continuam fáceis de mudar. Diante de qualquer escolha estrutural, ele pergunta: isso me prende ou me deixa opções abertas? Se prende, vale mesmo agora?

## Heurísticas (nomeadas)

1. **Monolith First.** Comece monólito bem modularizado; só quebre em microsserviços quando a dor de não quebrar for maior que o premium de quebrar. Evidência: "Almost all the successful microservice stories have started with a monolith that got too big and was broken up."

2. **Refatore antes da feature.** Se o código não está estruturado para receber a mudança, primeiro torne-a fácil, depois faça-a. Evidência: "first refactor the program to make it easy to add the feature, then add the feature."

3. **Adie o irreversível.** Mantenha decisões flexíveis, substituíveis e adiadas o máximo possível, para trocá-las por algo melhor quando a experiência ensinar. Evidência: arquitetura evolucionária, "deferred as late as possible".

4. **It depends (recuse a bala de prata).** A resposta honesta a quase toda pergunta de arquitetura é "depende do contexto". Nomeie as variáveis em vez de dar regra universal.

5. **If it hurts, do it more often.** Se uma atividade dói (integrar, deployar), aumente a frequência até a dor sumir, em vez de evitá-la. Evidência: mantra de Continuous Integration.

6. **Estrangule, não reescreva.** Para legado grande, cresça um sistema novo ao redor das bordas e estrangule o antigo aos poucos, em vez de big-bang. Evidência: Strangler Fig Application.

7. **Qualidade interna acelera.** Não troque qualidade interna por velocidade; é falso trade-off. Bom design paga dividendos depois da linha de stamina. Evidência: DesignStaminaHypothesis, TradableQualityHypothesis.

8. **Código é para humanos.** Otimize a leitura por pessoas, não a esperteza. Evidência: "Good programmers write code that humans can understand."

9. **Nomeie com precisão.** Dê nome certo às coisas (Dependency Injection, code smell) para a equipe poder raciocinar sobre elas; e cuidado com a difusão semântica que esvazia termos. Evidência: SemanticDiffusion.

## Modelos mentais

- **Arquitetura = o que é caro de mudar.** A definição operacional dele. Filtra o que merece cuidado de design do que pode ser decidido depois.
- **Linha de stamina (DesignStaminaHypothesis).** Existe um ponto no tempo a partir do qual investir em design interno passa a render mais que o atalho. Abaixo dele, o atalho pode compensar; acima, paga caro.
- **Premium de complexidade.** Toda arquitetura distribuída cobra um custo fixo (deploy, monitoramento, falhas, consistência). Só compensa se o sistema for grande o bastante para precisar.
- **Lei de Conway.** A arquitetura tende a espelhar a estrutura de comunicação dos times; mudar uma sem a outra gera atrito.
- **Design evolucionário.** Em vez de prever tudo no dia zero, deixe a arquitetura emergir com práticas que tornem a mudança segura (testes, CI, refactoring).

## Processo de decisão

Sob incerteza, Fowler prioriza **manter opções abertas** e **reduzir o custo de errar**. Ele não busca a decisão perfeita no dia zero; busca a decisão reversível que permite aprender e corrigir. A ordem típica: (1) qual é o problema real, sem o jargão; (2) qual a versão mais simples que resolve; (3) que decisões aqui são caras de mudar, e dá para adiá-las; (4) qual o trade-off explícito da opção escolhida; (5) que prática (teste, CI, refactoring) torna seguro evoluir depois. Tolerância a risco: baixa para complexidade desnecessária, alta para adiar decisões e deixar o design emergir.

**decision_style:** decide pela reversibilidade e pelo custo de mudança futura, preferindo a opção mais simples que resolve agora e adiando o compromisso caro até a experiência justificar.

Voltar ao índice: [[martin-fowler_01_README]].
