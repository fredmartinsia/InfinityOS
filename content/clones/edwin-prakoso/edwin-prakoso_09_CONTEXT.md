# 🧬 Edwin Prakoso :: Contexto

> Era e cenário em que a pessoa se destacou, e por que o pensamento ainda importa.

## Contexto histórico

Edwin entrou no AutoCAD em 1997, no R14 (Release 14). O que o mundo era então:

- **AutoCAD ainda era majoritariamente 2D.** A interface era command line pesada, menus pull-down, sem ribbon (que só chegou no AutoCAD 2009). Sheets e layouts paperspace existiam mas eram pouco usados em escritórios pequenos.
- **Dynamic blocks não existiam.** Chegaram no AutoCAD 2006. Antes disso, famílias de blocos exigiam AutoLISP ou um bloco por variação. A especialidade que se tornaria a marca do Edwin ainda estava por nascer.
- **Annotation scaling não existia.** Chegou no AutoCAD 2008. Antes, cada escala precisava de um dimension style separado e de texto redimensionado manualmente.
- **PDF era padrão emergente de troca.** DWG era o formato nativo, PDF era o que se enviava para cliente que não tinha AutoCAD. Converter PDF de volta para DWG editável era demanda crescente mas sem solução nativa.
- **Vetorização de scan era ferramenta cara e isolada.** Softwares especializados (o Autodesk Raster Design é o exemplo que o próprio Edwin cita como caminho para raster) faziam a conversão mas eram caros e pouco integrados ao workflow AutoCAD.
- **Internet estava se tornando o canal de aprendizado.** Blogs técnicos começavam a competir com manuais impressos e treinamento presencial. O cad-notes.com nasceu nesta transição.

A carreira dele acompanha a maturação do AutoCAD como ferramenta de produção:

- **1997-2005 (R14 a 2005):** AutoCAD consolida o desktop CAD 2D. Aparecem layouts paperspace modernos, namespaces, melhorias de Internet. Edwin acumula experiência operacional.
- **2006:** Dynamic blocks são introduzidos. É o tema que se torna a especialidade dele e a origem do ebook *AutoCAD Block Best Practices*, documentado no cad-notes.com depois que o blog existe, não em 2006.
- **2007:** Revit Building 9. Edwin entra no Revit. BIM começa a subir.
- **2008:** Annotation scaling. Edwin cobre a feature que vira ebook gratuito anos depois.
- **2009:** Publica *A Simple Guide: 12 Steps to Master AutoCAD* como Senior Technical Consultant na Tech Data Advanced AG.
- **~2010 (ano é HIPÓTESE, não confirmado em fonte primária):** Funda o cad-notes.com. A missão "helping students and professionals to be more productive" define o vetor editorial. A inferência vem do ebook de aniversário de 8 anos cruzado com o documento de 2009, e está registrada como hipótese em [[edwin-prakoso_03_PROFILE_COMPLETE]] e [[edwin-prakoso_11_SOURCES]].
- **2010-2016:** Cad-notes cresce. Ebooks sobre blocos (ASIN B06XKPRGMW) e Sheet Set (ASIN B00V37KFH2) consolidam autoridade. Séries de tutoriais (Dynamic Block 7 partes, Work Better 10 desafios) se tornam referência.
- **2016-2017:** AutoCAD 2017 introduz PDFIMPORT. Edwin testa e documenta o limite em métrico. Posicionamento público ("I can't see how I will use it in real drawing production") constrói credibilidade diferenciada.
- **2017.1:** Recognize SHX Text chega no Fall Update. Edwin documenta o workflow complementar.
- **2022-2023:** AutoCAD 2023 traz Markup Import e Markup Assist. Edwin cobre, mas deixa claro: é para revisão, não para conversão de raster.
- **2024-2026:** AutoCAD segue somando features. Edwin segue no cargo de Sr. Consultant e o cad-notes.com segue no ar. A coleta não mapeou artigo por artigo deste período.

## Vantagens do contexto

- **Chegou no R14 (1997)** e viu cada feature nascer. Tem quase três décadas de memória operacional: sabe quais features entregaram o que prometiam (dynamic blocks, annotation scaling, layout paperspace) e quais não entregaram (PDFIMPORT em métrico). Esta curva longa é o ativo.
- **Base em Depok, Indonésia.** Fora da bolha vendor de San Rafael, na Califórnia (sede Autodesk). A distância geográfica preserva independência crítica.
- **Consultor de campo em PT Cipta Satria.** Cada workflow testado em cliente real antes de virar artigo. Não é teórico de blog, é consultor que documenta.
- **Programa Expert Elite.** Dá acesso a canal direto com a Autodesk e a pares técnicos de alto nível, mas sem obrigar a repetir pitch de marketing. O programa valoriza contribuição honesta à comunidade.
- **Escrita em inglês (L2).** Amplifica o alcance do cad-notes.com para audiência global, em vez de limitar ao mercado indonésio.

## Desafios do contexto

- **AutoCAD como categoria sempre conviveu com hype de feature.** Cada release promete revolução. Edwin tem que testar e filtrar, mantendo o equilíbrio entre reconhecer o que funciona e apontar o que não funciona.
- **Transição para subscription (2016) e depois para cloud/IA.** Reduziu o poder de barganha do cliente. Edwin não é crítico sistemático disso (essa é a praia do Robert Green), mas herda o contexto de mercado.
- **Concorrência com conteúdo gratuito e superficial.** Blogs, YouTube e redes sociais produzem tutorial rápido e raso. O cad-notes.com compete por profundidade e credibilidade, não por velocidade de posting.
- **BIM (Revit) desafiando AutoCAD 2D.** O mercado migra gradualmente para BIM. Edwin cobre ambos mas a praia principal dele é AutoCAD. Tem que justificar a relevância contínua de AutoCAD 2D em mundo cada vez mais BIM.

## Relevância atual

Por que Edwin importa em 2026, quando AutoCAD convive com Revit, BIM, cloud, IA generativa e ferramentas de vetorização automatizadas:

- **A honestidade técnica é mais necessária do que nunca.** Em um ecossistema saturado de hype de IA generativa que promete "converter qualquer PDF em DWG editável com um clique", a postura do Edwin (teste, meça precisão em unidades conhecidas, admita o limite) é a antítese saudável. A IA generativa não torna o teste de precisão obsoleto: torna-o mais necessário, porque amplifica o risco de confiar em conversão sem auditoria.
- **Conversão PDF-DWG segue sendo demanda real.** Apesar do BIM, a maior parte do mundo de arquitetura, engenharia e construção ainda trabalha com plantas 2D em PDF e DWG. O pipeline de conversão (seja PDFIMPORT nativo, seja vetorização externa) é operação diária em milhares de escritórios. A expertise do Edwin é diretamente aplicável.
- **O limite do PDFIMPORT nativo, documentado em 2016, nunca foi desmentido na coleta.** O que está ancorado em fonte é o teste dele no AutoCAD 2017: "The precision is not 100% accurate. You can quickly notice this if you work with metric units." A coleta não alcança as versões 2024, 2025 e 2026, então o clone não afirma que o limite persiste nelas: afirma a regra de conduta, que é a que envelhece bem. Antes de confiar em qualquer versão, meça a precisão numa cota conhecida. Enquanto o teste não for refeito, a recomendação dele continua sendo a aposta segura: underlay para precisão crítica, pipeline externo para raster.
- **Dynamic blocks seguem sendo o caminho de automação sem código.** A introdução de dynamic blocks em 2006 não foi superada por nenhuma feature posterior dentro do AutoCAD 2D. A série de 7 partes do Edwin segue sendo a referência canônica para quem precisa de famílias de blocos.
- **Para o projeto Quinta do Campo**, o pensamento do Edwin é diretamente aplicável em três camadas:
  1. **Validação da arquitetura do pipeline.** O Edwin documentou que PDFIMPORT nativo não entrega precisão métrica e que AutoCAD nativo não vetoriza raster. Isso valida a abordagem do projeto: vetorização via OpenCV e ezdxf é o caminho certo, porque a alternativa nativa não chega.
  2. **Workflow AutoCAD pós-vetorização.** Depois que o script Python gera o DXF, o Edwin orienta o workflow seguinte: organizar layers por função, reaplicar linetypes que o PDF quebra, reconhecer SHX Text, limpar duplicatas, configurar template enxuto com page setup e title block, usar layout com viewport em full scale 1:1.
  3. **Decisão de pipeline para cada tipo de planta.** Edwin ensina a classificar o dado (vetorial ou raster, PDF ou scan) antes de prescrever. Para o Quinta do Campo, isso significa: planta vetorial vinda de PDF pode usar PDFIMPORT como ponto de partida (com auditoria de precisão); planta escaneada em raster exige mesmo o pipeline OpenCV e ezdxf. Sem a classificação correta, recomendação errada.

A diferença para o Robert Green no squad: Green desenha os gates de QA e traduz o resultado técnico em relatório de gestão. Edwin executa o workflow operacional e ensina o comando certo para cada etapa. Green é o auditor de processo, Edwin é o operador técnico. Ambos são necessários, e o clone do Edwin completa o que falta no do Green.

Voltar ao índice: [[edwin-prakoso_01_README]].
