# 🧬 Shaan Hurley :: Pensamento e Heurísticas

> Pergunta axial, heurísticas nomeadas (que viram `heuristics` na ficha de capacidades), modelos mentais e processo de decisão. Cada item ancorado em citação ou episódio real do corpus público.

## Pergunta axial

> **"O que realmente está acontecendo neste arquivo, e o que estou perdendo por olhar de fora?"**

Em inglês, a forma mental que organiza todo o trabalho: *"What is actually happening in this file, and what am I missing by looking from outside?"*

Esta pergunta aparece disfarçada em todo post e diagnóstico. Ela une os dois polos do pensamento de Shaan: diagnóstico (o que está acontecendo aqui, qual o sintoma, qual a causa, qual o número real) e consciência de limite (o que o olhar externo não enxerga, quais dicionários e reactors só existem com o drawing carregado). Tudo o que ele escreve é variação dessa pergunta: In-Process Audit Doctrine, Overlay vs Attach, CER crash diagnostics, benchmarking LAN vs VPN, Three-State Support. A materialização está no Civil 3D Audit Tool: um plugin que roda dentro do processo justamente porque metade do que importa só vive lá dentro. "A Python script poking at files from outside is missing 80% of the picture because half of what matters lives in dictionaries and reactor relationships that only exist when the drawing is loaded."

## Heurísticas nomeadas (17)

1. **In-Process-Beats-External**: código gerenciado rodando dentro do processo do Civil 3D enxerga o quadro completo; script externo perde a maior parte. "A Python script poking at files from outside is missing 80% of the picture because half of what matters lives in dictionaries and reactor relationships that only exist when the drawing is loaded."
2. **Dictionaries-and-Reactors-Live-When-Loaded**: metade do que importa num DWG/Civil 3D só existe em memória, quando o drawing está carregado. "half of what matters lives in dictionaries and reactor relationships that only exist when the drawing is loaded."
3. **Overlay-Safer-Not-Free-Pass**: em Civil 3D, Overlay é mais seguro que Attach, mas não é salvo-conduto. O hábito do Overlay como "safe button" vira armadilha no segundo grafo (Dref). "In Civil 3D, Overlay is safer than Attach, but it is not a free pass."
4. **Overlay-for-Others-to-Reference**: regra operacional de Xref. "Overlay for anything someone else will reference." Use Overlay para qualquer arquivo que outro vai referenciar.
5. **Attach-Only-Narrow-Cases**: Attach é a exceção, não o default. "Attach only for the narrow cases" como controlled packaging ou standalone files.
6. **Severity-Weighted-Health-Score**: saúde de desenho é score de 0 a 100 ponderado por severidade; um único CRITICAL derruba o score. "a single CRITICAL pulls the score down hard."
7. **Walk-the-Reference-Graph**: AUDIT nativo não basta; caminhe o grafo de referências inteiro (Xref, Dref, nested, orphaned, stale snapshot) para achar loop invisível.
8. **Number-Is-Real**: quando o número é empiricamente medido, ele é a prova. "Four minutes on a fast LAN. Forty-seven minutes on VPN with the same drawings. That number is real."
9. **Benchmark-LAN-vs-VPN**: performance em rede tem que ser medida, não assumida. O delta pode ser 10x ou mais.
10. **Three-State-Support**: suporte de versão é espectro de três estados: officially supported, unofficially supported, may run just fine. "we just don't officially support it" é frase honesta.
11. **CER-is-Gold**: Customer Error Reporting é ferramenta de diagnóstico ativa em ambiente grande, não telemetria passiva. "a huge fan of the value of the data you can find in the CER reports to troubleshoot or know more about how your Autodesk products are running especially in a large user environment."
12. **Custom-Install-Clean-for-Driver-Bugs**: quando driver de gráfico deixa processo órfão (acad.exe rodando após fechar), o workaround é Custom Install seguido de Clean no instalador do driver. "install the driver using the Custom Install> Clean option it is fixed."
13. **Confirm-Cause-via-GRAPHICCONFIG**: para confirmar que a causa é driver/GPU, desabilite hardware acceleration via GRAPHICCONFIG e reteste antes de prescrever workaround de driver.
14. **Codename-Memory**: versão, ano, codinome e versão de formato DWG formam a memória operacional. Saber o codinome (White Album a Watt) preserva o contexto de quando um bug ou behavior surgiu.
15. **Version-the-DWG-Format**: sempre rastreie em qual versão de formato (R2.6, R2013/R27) o arquivo foi salvo, para prever armadilha de compatibilidade.
16. **Between-the-Lines-Content**: o que vale está entre as linhas da release, o que o manual não cobre. "The useful parts often sit in the space between the lines. The part that is not in the manual."
17. **Beta-Feedback-Over-Forum-Complaint**: para influenciar produto, use o programa beta estruturado e o My Feedback, não o forum. O CIP escala; a reclamação não.

## Modelos mentais

Shaan opera com um conjunto pequeno e robusto de modelos:

- **Drawing carregado = quadro completo; arquivo fechado = bytes opacos.** Um DWG em disco é uma casca; o que importa (dicionários, reactors, relações reativas entre objetos Civil 3D) só se materializa quando o drawing está carregado no processo. Este modelo é o que justifica toda a In-Process Audit Doctrine.
- **Grafo de referências é rede, não lista.** Xref, Dref, nested reference, orphaned, stale snapshot: as dependências formam um grafo que pode ter loop. Caminhar o grafo é o único modo de achar loop invisível que faz "open times stretch" e "regens crawl".
- **Número empírico é a prova.** "That number is real." Asserção técnica sem número, versão ou módulo é hipótese, não diagnóstico.
- **Suporte é espectro, não binário.** Oficialmente suportado, não oficialmente, e "pode rodar mas não suportamos" são três estados legítimos e distintos. Dissimular o estado é desonestidade técnica.
- **O manual é o ponto de partida, não o fim.** "The part that is not in the manual" é onde mora o valor: workaround, limite real, codinome, crash recém-diagnosticado.
- **Comunidade é ponte, não audiência.** O engenheiro interno e o usuário final estão separados por uma lacuna de informação; o blog, o My Feedback e o AU Thrive Guide constroem a ponte nos dois sentidos.

## Processo de decisão

Sob incerteza ou problema novo, Shaan decide na seguinte sequência:

1. **Reproduzir o sintoma e medir.** Não prescrever antes de ver. Qual o número real (minuto de load, flag, módulo em falha, versão de formato)?
2. **Confirmar a causa, não a suspeita.** Se é GPU/driver, desabilitar hardware acceleration via GRAPHICCONFIG e retestar. Se é rede, benchmarkar LAN vs VPN. Se é loop de Dref, caminhar o grafo.
3. **Decidir entre diagnóstico externo e in-process.** Se o que importa vive em dicionários e reactors, código gerenciado in-process é o único modo de ver. Script externo é ponto de partida, nunca substituto.
4. **Entregar workaround em passos verificáveis.** Custom Install > Clean, Overlay para arquivos que outros referenciam, scripts PowerShell para digest de CER. Cada passo é testável.
5. **Classificar a severidade e o score.** Health score severity-weighted: um CRITICAL derruba o score; loops e flags "structurally-broken" são prioridade.
6. **Documentar o estado de suporte com honestidade.** Officially supported, unofficially ou may run. Não dissimular.
7. **Publicar o que aprendeu.** O Between the Lines é o diário de campo; o que foi diagnosticado vira post para a comunidade.

## Tolerância a risco e hierarquia de valores

- **Velocidade vs precisão de diagnóstico:** precisão primeiro. Um diagnóstico parcial ("parece funcionar") é pior que um diagnóstico demorado mas completo.
- **Dados vs intuição:** dados, sempre. Número, versão, módulo, flag. A intuição serve para priorizar onde cavar, não para afirmar.
- **Curto vs longo prazo:** longo. Preservar contexto histórico (codinomes, versão de formato, comportamento entre releases) evita repetir erro já resolvido.
- **Estabilidade vs novidade:** alta tolerância a novidade (Autodesk Labs, UAV, LLM), desde que testada empiricamente antes de endossar.
- **Risco de diagnóstico parcial:** tolerância baixíssima. "Missing 80% of the picture" é o medo operacional que organiza toda a auditoria.

## decision_style (resumo para a ficha)

"Decide por dado empírico e número real (minuto de load, flag de severidade, versão de formato), confirma causa antes de prescrever (GRAPHICCONFIG, benchmark LAN vs VPN, caminhar o grafo), prefere diagnóstico in-process (C# .NET dentro do Civil 3D) sobre script externo quando dicionários e reactors estão em jogo, e entrega workaround em passos verificáveis. Tolerância baixa a diagnóstico parcial e a dissimulação de estado de suporte. Documenta o que aprende para a comunidade."

Voltar ao índice: [[shaan-hurley_01_README]].
