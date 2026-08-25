# Checklist de Qualidade de Output, YouTube Squad

**Checklist ID:** YT-CL-001
**Referenced by:** tasks de síntese do youtube-chief (`*empacotar` → tasks/empacotar-publicacao.md, `*planejamento-mensal` → tasks/planejamento-mensal.md, `*decisao-estrategica` → tasks/decisao-estrategica.md)
**Purpose:** Validar toda entrega do squad antes de chegar ao {{USER_NAME}}, garantindo que nenhuma recomendação saia sem pesquisa prévia, comment mining, modelagem cross-cultural, SEO/GEO e o pacote completo. Este gate converte o Filtro de Qualidade do youtube-chief e o bloco `qa` do `squad.yaml` em checklist formal.

[[LLM: INITIALIZATION INSTRUCTIONS

Este checklist valida o output geral do YouTube Squad (estratégia e produção de YouTube/podcast do sua comunidade, canais {{USER_NAME}} e Infinity Cast, mercado Portugal/Brasil).

APPROACH DE EXECUÇÃO:
1. Para cada seção, verifique cada item contra a entrega real.
2. Marque cada item como [x] Passou, [ ] Falhou, ou [N/A] Não se aplica.
3. Itens CRITICAL bloqueiam a entrega; itens não-críticos são consultivos.
4. A regra inegociável do chief manda: se houver achismo sem dados ou formato sem casos comprovados, BLOQUEIE a entrega e volte para a pesquisa (não maquie o gap).
5. Justifique cada [N/A] em uma linha, N/A não pode esconder um item crítico que deveria ter sido cumprido.

Itens CRITICAL têm o sufixo (CRITICAL).]]

---

## 1. Pesquisa & Evidência

- [ ] Pesquisa prévia foi feita pelo `@youtube-researcher` antes de qualquer agente Tier 2 entrar em ação (CRITICAL)
- [ ] Comment mining incluído, top 10-20 dúvidas, dores e desejos extraídos de comentários multi-plataforma (YouTube + Instagram + Reddit + Quora) (CRITICAL)
- [ ] 5+ casos validados para o formato proposto (canais BR/USA/PT do nicho)
- [ ] Fontes citadas com link ou referência rastreável (nada de "vi por aí")
- [ ] Scan cobriu os mercados relevantes (BR + USA + PT/EU) e não só um deles

## 2. Modelagem

- [ ] Modelagem cross-cultural BR + USA → PT/EU aplicada (referência do que já funciona em mercado mais maduro)
- [ ] Thumbnail acompanhada de referências modeladas com links (thumbnails que já funcionaram em canais semelhantes)
- [ ] Estrutura/formato recomendado baseado nos padrões dos canais top, não em hipótese solta
- [ ] Se o formato é inédito, está sinalizado claramente como hipótese de teste (não como certeza)

## 3. SEO/GEO

- [ ] Título com SEO + GEO (otimização para busca e para respostas generativas)
- [ ] Descrição com SEO + GEO + chamada para ação + links
- [ ] Keyword principal definida (mais secundárias quando aplicável)
- [ ] Tags relevantes geradas quando a entrega inclui metadados de vídeo

## 4. Output Completo

- [ ] Entrega contém o pacote completo: título + descrição + estrutura sugerida + thumbnail conceitual + referências modeladas com 3+ links (CRITICAL)
- [ ] Estrutura sugerida cobre hook + corpo + CTA
- [ ] Thumbnail entregue como conceito visual descrito (não apenas "fazer uma thumbnail boa")
- [ ] Quando a demanda é decisão estratégica, a entrega traz prós/contras + casos de canais que escolheram cada caminho
- [ ] Próximos passos ou ações prioritárias indicados ao final

## 5. Marca & Escrita

- [ ] Identidade sua comunidade respeitada, laranja sobre preto na direção visual de thumbnail/capa
- [ ] Nenhum travessão (em dash, o traço longo) em qualquer texto da entrega (CRITICAL)
- [ ] Português do Brasil correto (gramática, ortografia, pontuação)
- [ ] Tom adequado ao canal alvo ({{USER_NAME}} individual ou Infinity Cast podcast)
- [ ] Caminhos e nomes de comando citados batem com o registro oficial do squad

## 6. Anti-Achismo

- [ ] Nenhuma recomendação baseada em achismo sem dados (CRITICAL)
- [ ] Nenhum formato sugerido sem casos de sucesso comprovados (CRITICAL)
- [ ] Toda afirmação forte rastreia para uma fonte: pesquisa, comment mining, modelagem ou caso validado
- [ ] Riscos e pontos de atenção sinalizados quando a evidência é parcial ou o cenário é incerto

---

## PASS/FAIL Criteria

**PASS:** Todos os itens CRITICAL [x], menos de 2 falhas não-críticas, E o pacote completo da Seção 4 entregue.

**REVISE:** Todos os itens CRITICAL [x], mas 2+ falhas não-críticas OU lacuna de modelagem/SEO que dá para fechar com um passe rápido de revisão.

**FAIL:** Qualquer item CRITICAL desmarcado, em especial pesquisa prévia ausente, comment mining ausente, pacote incompleto, travessão presente ou recomendação por achismo/formato sem casos. Bloquear a entrega e voltar para a pesquisa antes de reapresentar.

**Scoring:**
- Seções 1-2: gate de evidência e modelagem (a fundação, nada estratégico passa sem isso).
- Seção 3: gate de SEO/GEO (descoberta do conteúdo).
- Seção 4: gate de completude do pacote (o que o {{USER_NAME}} recebe de fato).
- Seção 5: gate de marca e escrita (laranja sobre preto, pt-BR, sem travessão).
- Seção 6: gate anti-achismo (o diferencial inegociável do squad, uma entrega que passa em 1-5 mas falha aqui recebe FAIL, nunca PASS).
