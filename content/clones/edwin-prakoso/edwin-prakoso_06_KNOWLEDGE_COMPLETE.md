# 🧬 Edwin Prakoso :: Conhecimento e Frameworks

> Mapa de domínios, frameworks proprietários nomeados, opiniões fortes e pontes para outros domínios. Tudo ancorado no corpus público (cad-notes.com, ebooks AutoCAD Block Best Practices e Drawing Management with AutoCAD Sheet Set, AUGIWorld, Autodesk Expert Elite).

## Domínios de expertise

| Domínio | Nível | Evidência |
|---|---|---|
| **Conversão PDF para DWG e vetorização** (PDFIMPORT, PDF underlay, Recognize SHX Text, pipeline raster) | DOMINANTE | Série de artigos no cad-notes.com sobre PDFIMPORT no AutoCAD 2017 e 2017.1, sobre Markup Import no AutoCAD 2023. Testou o PDFIMPORT em métrico e publicou o veredito de forma inequívoca, com citações rastreáveis. Domina o trade-off entre importar geometria e redesenhar por cima de underlay. |
| **Blocos dinâmicos e reusable content** (dynamic blocks, attributes, visibility states, Block Properties Table) | DOMINANTE | Dynamic Block Tutorial Series (7 partes, cad-notes.com), ebook "AutoCAD Block Best Practices" (69 páginas, ASIN B06XKPRGMW). É a referência canônica na comunidade AUGI para blocos dinâmicos. |
| **AutoCAD operacional e produtividade** (template, layer, atalhos, annotation scaling, layout vs model) | DOMINANTE | Work Better with AutoCAD Challenge Series (10 desafios), 100 AutoCAD Tips, 10 Days to Work Better, 10 Reasons to Use AutoCAD Layout. Quase três décadas de uso desde R14 (1997). |
| **Sheet Set Manager e drawing management** | FORTE | Ebook "Drawing Management with AutoCAD Sheet Set" (84 páginas, ASIN B00V37KFH2). Cobertura de page setup, title blocks, views automáticas, batch plotting, eTransmit. |
| **Annotation Scaling** | FORTE | Ebook gratuito "Working with AutoCAD Annotation Scaling", lançamento de aniversário de 8 anos do cad-notes.com. |
| **Importação de imagem e scan** (IMAGEATTACH, Markup Import 2023, escala com Reference) | FORTE | Artigos sobre What's new in AutoCAD 2023, sobre escalonamento de imagem. Workflow clássico de SCALE Reference e ALIGN. |
| **Revit e BIM** | SECUNDÁRIO | Usa Revit desde Building 9 (2007). Cobre Revit no cad-notes.com mas não é a praia principal. |
| **Inventor e MicroStation** | SECUNDÁRIO | Cobre no escopo do blog, mas profundidade menor que AutoCAD. |
| **Programação (AutoLISP, script, Python)** | GAP RECONHECIDO | Edwin não cobre vetorização via código/script. Sua expertise é operacional no AutoCAD. Para raster para DWG editável ele indica pipeline externo (Autodesk Raster Design ou ferramenta terceira), não escreve o script. |

## Frameworks proprietários (10)

### 1. Dynamic Block Tutorial Series (7 partes)
Série canônica publicada no cad-notes.com, considerada referência clássica na comunidade Autodesk para blocos dinâmicos. Estrutura progressiva:

1. **Wall (parede):** adicionar um parameter e linkar um action. Permite "draw straight walls without having to draw several parallel lines and hatches".
2. **Column (pilar):** "add two parameters and two actions". Controle de parameter properties, stretch size, stretch bidirecional.
3. **Door (porta):** "add a parameter then link 3 actions to that parameter". Inclui trim automático da parede ao inserir a porta.
4. **Door Add:** Flip action para "allow you flip the door opening". Alignment parameter para "allow your door to align automatically" à parede.
5. **Visibility States:** "the simplest way to make a dynamic block" mas "very useful if you want to show objects in different ways or different variations". Ponto de partida ideal para iniciantes em dynamic blocks.
6. **Geometric and Dimensional Parameters:** integra paramétrica com dynamic block. "It works differently with dynamic block action", mas "allows you to control dynamic block by the object size, not by action".
7. **Fields in Dynamic Block:** coordinate labels automáticos usando "a symbol and a field to automatically show coordinate of that particular point".

Aplicação: qualquer escritório que precise de famílias de blocos (portas em várias larguras, pilares em várias seções, paredes em vários tipos). É automação sem AutoLISP.

### 2. Work Better with AutoCAD Challenge Series (10 desafios)
Metodologia de produtividade incremental estruturada em desafios publicados no cad-notes.com. Estrutura original de 7 desafios, expandida depois para 10:

- Challenge 1: Preparation (identificar tarefas repetitivas e automatizáveis).
- Challenge 2: Template.
- Challenge 3: Reusable Content (blocos, dynamic blocks, annotative blocks, attributes, sharing e managing).
- Challenge 4: Customization.
- Challenge 5: Learn the New Features.
- Challenge 6: Plan Your Drawing (com contribuição de Paul Munford sobre goal-setting e deadlines).
- Challenge 7: Evaluate Your Progress.

Missão declarada: "Our primary goal is to allow you to complete your tasks faster, make your drawing smarter and easier to modify." É o framework guarda-chuva da filosofia de produtividade dele.

### 3. Tríade da Produtividade CAD (template + library + customization)
Framework conceitual recorrente em vários artigos. "To be productive in AutoCAD, we need to focus on three areas: having good templates, good libraries, and good customizations."

- **Template:** `.dwt` com settings, page setup, title block, styles essenciais (text, dimension), layers frequentes.
- **Library:** blocos e mais. "You can create libraries for everything in separate files! Library is not limited to blocks." Tool Palettes e Design Center para puxar de arquivos externos.
- **Customization:** command aliases, atalhos, interface personalizada, AutoLISP quando necessário.

Aplicação: diagnóstico rápido de produtividade. Se um usuário é lento, ou o template está fraco, ou a biblioteca está ausente, ou falta customization. Raramente é falta de skill.

### 4. PDFIMPORT Precision Test Workflow (AutoCAD 2017+)
Pipeline de avaliação e decisão para converter PDF vetorial em DWG. Deduzido dos artigos sobre PDFIMPORT (não é um único tutorial, é o workflow implícito que ele ensina):

1. **Avaliar o PDF:** é vetorial ou escaneado (raster)? Se raster, PDFIMPORT não funciona bem, precisa vetorização prévia, OCR ou redesenho manual.
2. **Decidir estratégia:** importar geometria (PDFIMPORT) versus usar como underlay (PDFATTACH) e redesenhar por cima.
3. **Se for PDFIMPORT:** ativar via ribbon Insert > PDF Import ou digitar PDFIMPORT; escolher página, escala, rotação, opções de layers. "You can choose from PDF overlay or external PDF file."
4. **Inspecionar resultado:** checar precisão com cotas em unidades métricas; "lines with dashed linetypes will be separate lines"; hatches podem virar geometria. "Don't expect the result to be perfect." "The precision is not 100% accurate. You can quickly notice this if you work with metric units."
5. **Reconhecer SHX Text:** se aplicável, rodar Recognize SHX Text tool (AutoCAD 2017.1 Fall Update em diante) para reconverter geometria em texto editável.
6. **Limpar geometria:** deletar duplicatas, corrigir layers, reaplicar linetypes, ajustar precisão.
7. **Se underlay:** PDFATTACH, escalar com SCALE Reference (ver framework 7), traçar por cima, deletar underlay ao final.

Veredito dele sobre PDFIMPORT em produção: "I can't see how I will use it in real drawing production." "Imported PDF is not accurate enough." "Personally, I prefer using PDF underlay for this purpose."

### 5. Recognize SHX Text Workflow (AutoCAD 2017.1 Fall Update)
Complementar ao PDFIMPORT. No AutoCAD 2017 original, "SHX font will be imported as geometry, not texts. It will make text editing difficult." A atualização 2017.1 introduziu o Recognize SHX Text tool: "The text will still be imported as geometry", mas você pode "convert them to text in AutoCAD later."

Pipeline: rode PDFIMPORT primeiro (gera geometria, inclusive o texto SHX como linhas), depois rode Recognize SHX Text sobre a geometria, ele tenta casar padrões com fontes SHX conhecidas e reconverter em texto Mtext editável. Sucesso depende de: qualidade do PDF, fonte original ser SHX padrão, DPI do PDF, ausência de ruído.

Limitação: não é OCR genérico. Funciona só para texto que originalmente era SHX no AutoCAD e foi plotado para PDF. Para texto TrueType ou texto em imagem escaneada, não aplica.

### 6. Markup Import Workflow (AutoCAD 2023)
Pipeline para importar revisão manuscrita ou scan de planta como camada de anotação sobre o DWG. Localização na ribbon: "AutoCAD ribbon > Collaborate tab > Traces panel." Formatos: PDF, JPG, PNG.

Workflow típico:
1. "Scan or take a picture of the review sheet and import it into AutoCAD."
2. Posicionamento: "AutoCAD did an excellent job when placing it automatically."
3. Ajuste de transparência: "Change the transparency so only the markup appears. The drawings in the image or PDF won't interfere with your drawing in the DWG file."
4. OCR seletivo: "Markup has a character recognition feature from an image." Clique no texto reconhecido e selecione converter para Mleader ou Mtext.

Limitação crítica: Markup Import é para anotação e revisão, NÃO é vetorização automática. Para converter raster (scan de planta) em vetores DWG editáveis, o AutoCAD nativo não faz. Precisa de Autodesk Raster Design, ou pipeline externo (OpenCV + ezdxf + QCAD, o caso do projeto Quinta do Campo), ou redesenho manual sobre underlay.

### 7. Scale with Reference (escalar imagem/PDF com precisão)
Workflow clássico que Edwin endossa para escalonar imagem ou PDF underlay com precisão conhecida, quando não há world file ou georreferência:

1. Inserir via IMAGEATTACH (imagem) ou PDFATTACH (PDF underlay).
2. Especificar insertion point, scale e rotation no dialog (ou aceitar defaults).
3. Desenhar uma linha de referência com comprimento conhecido sobre uma dimensão real do desenho (uma porta de 80 cm, um eixo de 5 m, um vão conhecido).
4. Rodar SCALE com opção Reference: selecionar a imagem/PDF, base point, comprimento de referência (a linha desenhada), novo comprimento (valor real conhecido).
5. Alternativa: comando ALIGN para alinhar 2 pontos da imagem a 2 pontos do DWG (alinha, escala e rotaciona de uma vez).
6. Verificar escala checando outras cotas conhecidas em outras partes do desenho.
7. Manter como XREF externo se quiser preservar escala exata e ligação ao arquivo original.

Para imagem georreferenciada: IMAGEATTACH respeita coordenadas se o arquivo tiver world file.

### 8. Template-Lean-plus-Libraries Framework
Filosofia de organização contra a tendência de superlotar o template. "Template is an important part to improve your productivity. It keeps your drawing standards and reduces repetitive tasks." Mas "too many objects can also make your drawings corrupt."

- Template `.dwt` carrega só o essencial: settings, page setup, title block, styles (text, dimension) mais usados, layers mais frequentes.
- Bibliotecas externas em arquivos separados: blocos, blocos dinâmicos, blocos annotative, layers AIA completas, layouts prontos.
- "If you have all AIA layers in your drawing, you will have more than 500 layers. I seriously doubt that you will use all of them."
- Tool Palettes e Design Center para puxar de bibliotecas sob demanda. Design Center adiciona "almost every AutoCAD styles, blocks, linetypes, layers, and layouts".

Aplicação: template leve abre mais rápido, corrompe menos, e a biblioteca externa escala sem poluir todo novo desenho.

### 9. Layout-over-Model-Scaled Framework (10 Reasons to Use AutoCAD Layout)
Defesa sistemática do trabalho em layout com viewports, contra o hábito de escalonar geometria no model space. As 10 razões publicadas no cad-notes.com:

1. "We always draw in full scale 1:1" no model, sem cálculo de escala.
2. Múltiplas áreas de um model via viewports. "We only need to update the modelspace. Other viewports will automatically updated."
3. Menos styles para gerenciar (não precisa de múltiplos dimension styles para escalas diferentes).
4. Controle fácil da escala do desenho via viewport scale list.
5. Orientação diferente por viewport (north verdadeiro versus rotacionado).
6. Layer properties por viewport (desde AutoCAD 2008): "turn hatch layers on for detailed views but off for larger scales".
7. Vantagens de annotation scaling: "any changes will reflected to all of your viewports."
8. Controle fácil de impressão: "simply select the paper size, and always use 1:1 full scale."
9. Vantagens do Sheet Set Manager: gerenciar projeto, eTransmit, publish.
10. Batch plot: "plot many layouts at once, even send them to different plotters."

Mantra: "It doesn't matter if you have 2, 4, or 10 different scales in your sheet later. We can always draw in full scale 1:1."

### 10. A Simple Guide: 12 Steps to Master AutoCAD
Método de aprendizado para iniciantes estruturado em 12 passos, publicado como ebook em 2009. Estrutura progressiva do básico ao produtivo, originalmente lançado quando Edwin era Senior Technical Consultant na Tech Data Advanced AG. É o framework pedagógico que sustenta a didática em série dele: cada passo é uma habilidade que habilita o próximo, sem atalho.

## Opiniões fortes e contraintuitivas

- **PDFIMPORT nativo NÃO serve para produção real.** Edwin testou no AutoCAD 2017 e foi explícito: "I can't see how I will use it in real drawing production." Precisão ruim em unidades métricas, SHX text virando geometria, linetypes quebrando em segmentos. Prefere PDF underlay como referência visual. Para o projeto Quinta do Campo, isso valida a abordagem de vetorização externa via OpenCV e ezdxf em vez de confiar no PDFIMPORT.
- **AutoCAD nativo NÃO vetoriza raster.** Markup Import (2023) é para anotação, não para conversão. Quem precisar de planta escaneada em DWG editável precisa de pipeline externo (Autodesk Raster Design, ou script Python com OpenCV e ezdxf). Edwin não cobre código; a expertise dele é operacional AutoCAD.
- **Desenhar só no Layer 0 é inaceitável profissionalmente.** Sem ambiguidade: "Using only Layer 0 is the worst", "everyone hates to receive a drawing like that".
- **Template superlotado corrompe arquivo.** Melhor ter bibliotecas externas e template enxuto. Contra a tendência de "colocar tudo no template". "Too many objects can also make your drawings corrupt."
- **Sempre trabalhe em layout, não em model space escalado.** Defende com 10 razões. Reduz erro de escala, automatiza impressão, simplifica annotation scaling.
- **Blocos são automação sem programação.** "By optimizing blocks, we not only become more productive, but also reduce human errors in our design." Você não precisa saber AutoLISP para ser produtivo; dynamic blocks com visibility states resolvem a maioria dos casos.
- **Visibility States é o ponto de partida mais simples.** "Visibility states is the simplest way to make a dynamic block." Recomenda começar por ele antes de parameters e actions complexos.
- **Teste a feature antes de confiar.** Nunca recomenda novidade da Autodesk sem ter testado e encontrado o limite. "Don't expect the result to be perfect" é a postura padrão.

## Pontes para outros domínios

O raciocínio do Edwin extrapola o AutoCAD:

- **Didática técnica em série (instrutor-cad e além):** a estrutura de quebrar tema complexo em partes numeradas com exercício e gancho serve a qualquer instrutor técnico (programação, design, engenharia). É o modelo do ebook "A Simple Guide: 12 Steps".
- **Auditoria de precisão e QA de importação (auditor-cad e além):** o workflow de testar feature, medir precisão em unidades conhecidas e documentar o limite é transferível para qualquer pipeline de conversão de dado (CSV para database, OCR de documento, migração de formato).
- **Documentação operacional e troubleshooting (conteúdo e design):** o modelo do cad-notes.com (tutorial passo a passo, troubleshooting, resposta a comentários) é referência para qualquer blog técnico B2B. Aplicável a SaaS, ferramentas dev, produtos complexos.
- **Tradução de limite técnico em decisão de pipeline (consultor-estrategico):** saber dizer "esta feature não chega, precisa pipeline externo" e recomendar a arquitetura certa (underlay versus import, Raster Design versus script) é consultoria técnica de valor. Aplicável a qualquer decisão de stack.

Estas pontes justificam papéis auxiliares fora do AutoCAD: **auditor-cad** (QA estrutural de arquivo DWG pós-importação), **consultor-estrategico** (decisão de pipeline de conversão), **instrutor-cad** (didática de série para treinamento corporativo).

Voltar ao índice: [[edwin-prakoso_01_README]].
