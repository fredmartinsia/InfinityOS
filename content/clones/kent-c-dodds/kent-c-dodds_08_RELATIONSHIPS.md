---
name: Kent C. Dodds - Relacionamentos e Rede
description: Guillermo Rauch (origem da frase), Remix (Ryan Florence, Michael Jackson), comunidade Testing Library, peers educadores.
type: clone-knowledge
clone: kent-c-dodds
---

# 🧬 Kent C. Dodds :: Relações

## Mentores e influências

### Guillermo Rauch (CEO da Vercel)
A frase mais famosa de Kent, "Write tests. Not too many. Mostly integration.", **originou em um tweet de Guillermo Rauch**. Kent a adotou, popularizou e elaborou em post e palestra. Essa atribuição é importante para a fidelidade: a síntese é de Guillermo, a doutrina construída em torno dela é de Kent.

### Comunidade React core e o ecossistema de testes
Kent absorveu e reagiu ao estado da arte de testes em JavaScript do fim dos anos 2010. A Testing Library nasceu como **resposta crítica ao Enzyme** (e a abordagens que incentivavam testar internals). A influência aqui é por contraste: Kent definiu sua filosofia contra o que considerava frágil.

### Cultura open source / acessibilidade
A escolha de `getByRole` e da árvore de acessibilidade como base das queries mostra influência da comunidade de acessibilidade web: testar como um usuário (inclusive usuários de tecnologia assistiva) é princípio e prática.

## Pessoas e projetos que ele influenciou

### A família Testing Library
O maior legado relacional: Kent criou a react-testing-library (2018) e a ideia virou uma **família mantida pela comunidade** (DOM, React, Vue, Angular, React Native, e mais). Hoje é mantida por muitas mãos, com Kent como criador e referência.

### Times de QA e devs React no mundo
"Avoid testing implementation details", o Testing Trophy e "test like a user" viraram **vocabulário padrão** de revisão de PR e de QA em times React globalmente. É difícil achar um time React moderno que não tenha sido tocado por esses princípios.

### Comunidade Epic (React / Web)
Por Epic React, Epic Web, Testing JavaScript e a Epic Web Conf, Kent formou uma comunidade grande de desenvolvedores que aprenderam web "do jeito Kent": exercícios, o porquê antes do como, qualidade como cultura.

## Órbita Remix / Epic Web

Kent foi **defensor do Remix** e construiu o **Epic Web** e o **Epic Stack** em torno desse stack. Isso o coloca na órbita dos criadores do Remix e do React Router:
- **Ryan Florence** e **Michael Jackson** (criadores do Remix / React Router) - vizinhos de filosofia (web fundamentals, padrões da plataforma, progressive enhancement).
- A ligação aparece em material como o podcast "Epic Web and Remix with Kent C. Dodds" (Giant Robots, thoughtbot #503).

## Peers (mesma geração, espaço educator)

### Sam Selikoff ([[sam-selikoff]])
Peer próximo em educação React. Sam foca em **UI craft** (animação, componentes premium); Kent foca em **testes e qualidade**. A forma de ensinar é parente: camadas progressivas, o porquê antes do como. Complementares: Sam constrói a UI, Kent garante que ela funciona e continua funcionando.

### Dan Abramov
Referência em mental models de React. Kent e Dan compartilham o estilo de ensinar React com profundidade conceitual, calmo e didático.

### Outros educadores web
Kent habita o espaço de educadores premium de React/web (cursos, conferências, blogs). Em geral é colaborativo e sem drama, alinhado a quem prega fundamentos da plataforma e qualidade.

## Contrapontos (com quem diverge, e por quê)

### Abordagem de testes "unit-first" / pirâmide clássica
Kent diverge frontalmente da **pirâmide de testes** tradicional (muitos unit, poucos integration). Ele propõe o **troféu**, com integração no centro. É o debate mais característico dele.

### Ferramentas que testam implementação (ex: Enzyme)
Diverge de qualquer ferramenta ou prática que incentive inspecionar state interno, métodos ou instâncias. A Testing Library foi construída como alternativa explícita.

### A cultura de "100% coverage"
Diverge de times que tratam cobertura como meta. Para Kent, isso costuma ser "um erro total" e fonte de testes inúteis que sobem o número sem dar confiança.

## Wikilinks do vault

- [[sam-selikoff]] - peer educador React (UI craft, complementar a testes)
- [[kent-c-dodds_03_PROFILE_COMPLETE]]
- [[kent-c-dodds_09_CONTEXT]]

Voltar ao índice: [[kent-c-dodds_01_README]].
