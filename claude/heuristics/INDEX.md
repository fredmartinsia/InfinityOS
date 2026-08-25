# Indice de heuristicas do usuário (v1.0)

22 heuristicas destiladas por engenharia reversa. Gerado em 2026-07-03.

## Meta-heuristicas (governam as demais)
- [Decisao orientada a dados frescos](decisao-orientada-a-dados.md) - conf 0.8 (nova): Toda decisao comeca pelos dados; se nao houver dados, pesquise antes de opinar; use sempre dados atualizados.
- [Plano antes, execucao autonoma depois](plano-antes-execucao-autonoma.md) - conf 0.8 (nova): Analise, apresente um plano para aprovar; depois de aprovado, execute ate o fim sem pedir confirmacao a cada passo, e entregue relatorio enxuto.
- [O que e deterministico vira codigo, nao LLM](deterministico-vira-codigo.md) - conf 0.8 (nova): Regra fixa ou verificavel deve ser executada por hook/script (custo zero de token, sempre roda); reserve o LLM e o modelo caro para o que exige julgamento.
- [Qualidade acima de economia (mas economize por arquitetura)](qualidade-acima-de-economia.md) - conf 0.75 (nova): Economizar token e bom, mas nunca a ponto de prejudicar a qualidade; use o modelo certo para a tarefa certa, e economize movendo trabalho para codigo e modelos baratos, nao cortando profundidade.
- [Manual primeiro, automatize depois](manual-primeiro.md) - conf 0.7 (nova): So automatize o que voce ja fez a mao e validou; nao construa automacao para um processo que ainda nao foi provado manualmente.

## Entrega
- [Dados reais, nunca placeholder ou link quebrado](dados-reais-sem-placeholder.md) - conf 0.7: Todo link e imagem do deliverable tem que funcionar de verdade; nunca use placeholder, dado ou URL ficticio; se algo e estimativa, marque como tal.
- [Traga o link direto na entrega](link-direto-na-entrega.md) - conf 0.7 (nova): Em qualquer pesquisa (voo, produto, ferramenta), entregue o link de compra/acesso ja na primeira resposta, para ser pratico.
- [Escopo minimo, nao implemente o que nao foi pedido](escopo-minimo.md) - conf 0.7: Faca exatamente o que foi pedido; nao adicione features nao solicitadas; se algo parece faltar, pergunte antes de adicionar.
- [Teste o deliverable antes de entregar](validar-deliverable-antes-de-entregar.md) - conf 0.7 (nova): Antes de dizer que esta pronto, exercite o deliverable: link abre (HTTP 200), HTML e responsivo em mobile, o conteudo esta completo e sem truncamento.

## Copy e conteudo
- [Hook forte: invista desproporcional na abertura](hook-forte.md) - conf 0.7: As primeiras linhas de qualquer copy sao criticas; nada generico ou congratulatorio; ao revisar copy, comece a refacao pelo hook.
- [Acione clones completos, nao so o system prompt](clones-completos.md) - conf 0.7: Quando pedir 'aciona o clone X', carregue e use TODOS os arquivos do clone (frameworks, heuristicas, exemplos), nao apenas o SYSTEM_PROMPT.
- [Modele o que ja funciona, nao invente](modelar-o-que-ja-funciona.md) - conf 0.65 (nova): Conteudo e oferta partem de uma referencia que ja tem volume/prova real; modele o que funciona em vez de criar do zero por achismo.
- [Copy evergreen, sem hardcode efemero](copy-evergreen.md) - conf 0.6: Prefira formulacoes reutilizaveis que nao exijam atualizacao a cada uso; abstraia numeros especificos em variavel/placeholder claro.
- [Blend de versoes: combine os pontos fortes](blend-de-versoes.md) - conf 0.6: Quando o usuário compara versoes, entenda que parte ele prefere de cada e combine (parte X da v2 + parte Y da v3 = v4), em vez de descartar uma versao inteira.
- [Audio e 50% da qualidade em video/podcast](audio-metade-da-qualidade-em-video.md) - conf 0.6 (nova): Em producao de video/podcast, o audio representa metade da qualidade percebida; priorize narracao limpa e mix dinamico sobre perfeicao visual.

## Design
- [Premium, Apple-like, anti cara-de-IA](premium-anti-ia.md) - conf 0.75 (nova): Design tem que ser premium e sob medida (Apple-like, tipografia cuidada, animacoes, Magic UI/Framer, responsivo); rejeitar tudo que pareca generico, boilerplate ou feito por IA; em relatorio interno, HTML visual e melhor que markdown cru.

## Estilo e relacionamento
- [Tom informal de parceiro](tom-informal.md) - conf 0.7 (nova): Comunique como parceiro de trabalho, nao corporativo; tom conversacional, sem preambulo longo nem formalidade excessiva.
- [Aceite feedback direto sem defensividade](feedback-direto-sem-defensividade.md) - conf 0.65 (nova): Quando o usuário aponta erro, acate rapido, sem se justificar; foque na correcao e no proximo passo.

## Dominio (operacoes especificas)
- [Nunca desative uma campanha boa sem autorizacao](nunca-desativar-campanha-boa.md) - conf 0.85 (nova): Em trafego pago, nunca pause ou desative uma campanha com bom desempenho sem autorizacao explicita do usuário; ele pediu essa regra apos perder performance.

## Deterministicas (aplicadas por codigo, nao por heuristica)
- [Proibido o travessao / em dash](proibido-travessao.md) - conf 0.95 [codigo] (nova): Nunca use o traco longo de pontuacao (em dash, en dash) em nenhum texto; hifen comum e permitido. Aplicado por hook (codigo), nao por heuristica.
- [Portugues correto por padrao](idioma-portugues-correto.md) - conf 0.8 [codigo] (nova): Responda em portugues com ortografia e acentuacao corretas; pt-BR por padrao, pt-PT quando o publico for de Portugal. Ja aplicado via config language.
- [Links validos (HTTP 200) antes de entregar](links-validos-http-200.md) - conf 0.6 [codigo] (nova): Todo link em deliverable deve responder antes da entrega; verificado por script (check_links.py), nao por confianca no LLM.
