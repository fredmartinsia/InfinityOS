# 🧬 Edwin Prakoso :: Fontes

> Toda fonte com link, ASIN ou identificador, e nível de confiabilidade (ALTA, MÉDIA, BAIXA). Nenhuma citação usada no clone existe fora desta lista. Coleta realizada em agosto de 2026. Nenhum link foi inventado: todos vêm da pesquisa bruta arquivada em `~/.claude/skills/createclone/output/edwin-prakoso/research_raw.md`.

## Nota de integridade das fontes

Duas correções de premissa foram aplicadas na construção deste clone, e ficam registradas aqui porque afetam o que pode ou não ser citado como obra do Edwin.

1. **O blog dele é cad-notes.com.** Não existe fonte que ligue Edwin Prakoso a um domínio chamado beyondcad.com. Todo o corpus primário está em cad-notes.com, com replicação parcial em allaboutcad.com.
2. **Três títulos atribuídos a ele em briefing de terceiros não se confirmam.** "Work Faster with AutoCAD" aparece como expressão dentro de artigos dele (por exemplo "work faster with AutoCAD hatch"), nunca como ebook, e provavelmente é confusão com a série Work Better with AutoCAD. "AutoCAD Quiz" não foi localizado em nenhuma fonte. "60 AutoCAD Tips in 60 Minutes" é aula da Lynn Allen no Autodesk University, não obra do Edwin, conforme a página oficial da classe listada na seção de referências complementares. Nenhum desses três títulos é usado em nenhum arquivo do clone.

## Fontes primárias (escrita direta do Edwin no cad-notes.com)

### Perfil, credenciais e contato
1. Página About: https://www.cad-notes.com/about/ . Confiança ALTA. Origem das citações "I work as a Sr. Consultant in PT Cipta Satria Informatica. I've been using AutoCAD since R14 and Revit since Revit Building 9." e "I'm a member of Autodesk Expert Elite, an appreciation for individuals who give contributions to the Autodesk community."
2. Página Authors: https://www.cad-notes.com/authors/ . ALTA. Lista os ebooks dele, incluindo *101 AutoCAD Tips*. É o único localizador de dois títulos: *101 AutoCAD Tips* e *Working with AutoCAD Annotation Scaling* (este último, ebook gratuito de aniversário de 8 anos do blog) não têm ASIN, ISBN nem URL própria na coleta. A autoria está confirmada pelo site do próprio Edwin, o número de páginas e a data de publicação não.
3. Página Contact: https://www.cad-notes.com/contact/ . ALTA. Endereço público em Depok, Indonésia, e e-mail info@cad-notes.com.

### Conversão PDF para DWG, PDFIMPORT e Recognize SHX Text (núcleo técnico do clone)
4. AutoCAD 2017 system enhancement: https://www.cad-notes.com/autocad-2017-system-enhancement/ . ALTA. Fonte primária das citações centrais sobre PDFIMPORT: "You can activate the command by typing PDFIMPORT or from Application Menu> Import> PDF.", "AutoCAD will only convert the drawing to simple objects. Dimensions will be lines and texts. Lines with dashed linetypes will be separate lines.", "Don't expect the result to be perfect.", "The precision is not 100% accurate. You can quickly notice this if you work with metric units.", "I can't see how I will use it in real drawing production.", "Personally, I prefer using PDF underlay for this purpose.", "SHX font will be imported as geometry, not texts. It will make text editing difficult."
5. AutoCAD 2017 new features roundup: https://www.cad-notes.com/autocad-2017-new-features-roundup/ . ALTA. Origem de "You can choose from PDF overlay or external PDF file." e "Imported PDF is not accurate enough."
6. AutoCAD 2017.1 Fall Update: https://www.cad-notes.com/autocad-2017-1-autocad-fall-update/ . ALTA. Introdução do Recognize SHX Text tool e da ressalva "The text will still be imported as geometry", com a possibilidade de "convert them to text in AutoCAD later."

### Importação de imagem, scan e markup
7. What's new in AutoCAD 2023: https://www.cad-notes.com/whats-new-in-autocad-2023/ . ALTA. Markup Import e Markup Assist, localização na ribbon (Collaborate tab, Traces panel), formatos PDF, JPG e PNG. Origem de "Scan or take a picture of the review sheet and import it into AutoCAD.", "AutoCAD did an excellent job when placing it automatically.", "Change the transparency so only the markup appears. The drawings in the image or PDF won't interfere with your drawing in the DWG file." e "Markup has a character recognition feature from an image."

### Blocos dinâmicos
8. Dynamic Block Tutorial Series: https://www.cad-notes.com/autocad-dynamic-block-tutorial-series/ . ALTA. Índice das 7 partes (Wall, Column, Door, Door Add, Visibility States, Geometric and Dimensional Parameters, Fields in Dynamic Block). Origem de "Dynamic block was first introduced in AutoCAD 2006.", "Visibility states is the simplest way to make a dynamic block.", "Allows you to control dynamic block by the object size, not by action." e da resposta a comentário "You can limit the distance using parameter's properties."

### Produtividade, template, layer e layout
9. Complete our challenges to work better with AutoCAD: https://www.cad-notes.com/complete-our-challenges-to-work-better-with-autocad/ . ALTA. Estrutura da Work Better with AutoCAD Challenge Series e a missão "Our primary goal is to allow you to complete your tasks faster, make your drawing smarter and easier to modify."
10. WBWA Challenge 2, Template: https://www.cad-notes.com/wbwa-challenge-2-template/ . ALTA.
11. WBWA Challenge 3, Reusable Content: https://www.cad-notes.com/wbwa-challenge-3-reusable-content/ . ALTA. Origem de "By optimizing blocks, we not only become more productive, but also reduce human errors in our design."
12. 10 reasons to use AutoCAD layout: https://www.cad-notes.com/10-reasons-to-use-autocad-layout/ . ALTA. Origem de "It doesn't matter if you have 2, 4, or 10 different scales in your sheet later. We can always draw in full scale 1:1." e "We only need to update the modelspace. Other viewports will automatically updated."
13. The importance of using AutoCAD layer: https://www.cad-notes.com/the-importance-of-using-autocad-layer/ . ALTA. Origem de "Using only Layer 0 is the worst" e "everyone hates to receive a drawing like that".
14. Simplify AutoCAD template: https://www.cad-notes.com/simplify-autocad-template/ . ALTA. Origem de "Template is an important part to improve your productivity. It keeps your drawing standards and reduces repetitive tasks.", "Too many objects can also make your drawings corrupt.", "If you have all AIA layers in your drawing, you will have more than 500 layers. I seriously doubt that you will use all of them." e "You can create libraries for everything in separate files! Library is not limited to blocks."
15. 100 AutoCAD tips you should know: https://www.cad-notes.com/100-autocad-tips-you-should-know/ . ALTA. Origem da dica Use Both Hands e da tríade "To be productive in AutoCAD, we need to focus on three areas: having good templates, good libraries, and good customizations."
16. 10 days to work better with AutoCAD: https://www.cad-notes.com/10-days-to-work-better-with-autocad/ . ALTA.
17. Defpoints layer: https://www.cad-notes.com/defpoints-layer/ . ALTA. Base da heurística de usar DEFPOINTS só para cotas.
18. Using AutoCAD page setup: https://www.cad-notes.com/using-autocad-page-setup/ . ALTA.

## Fontes secundárias (reviews, listagens e perfis de terceiros)

19. Review do ebook de blocos na allaboutcad.com: https://allaboutcad.com/autocad-block-best-practices-an-e-book-by-edwin-prakoso/ . MÉDIA. Origem de "covers both beginning and advanced topics, all related to blocks. It starts with the basics, how to create a block."
20. Review na cadsetterout.com: https://cadsetterout.com/reviews/autocad-block-best-practices/ . MÉDIA. Origem da avaliação de estilo "clean, concise and logically structured".
21. *AutoCAD Block Best Practices* no Scribd: https://www.scribd.com/document/1006312704/AutoCAD-Block-Best-Practices-Edwin-Prakoso . MÉDIA. Confirma autoria, 69 páginas, sumário e exercícios com DWG.
22. *A Simple Guide to Master AutoCAD* no Scribd: https://www.scribd.com/document/479740335/A-Simple-Guide-to-Master-AutoCAD . MÉDIA. Confirma publicação em 21 de julho de 2009 e o cargo à época, Senior Technical Consultant na Tech Data Advanced AG.
23. *AutoCAD Block Best Practices* na Amazon, 2a edição, ASIN B06XKPRGMW: https://www.amazon.com/AutoCAD-Block-Best-Practices-automate-ebook/dp/B06XKPRGMW . ALTA para autoria e ASIN, MÉDIA para data exata.
24. *Drawing Management with AutoCAD Sheet Set* na Amazon, ASIN B00V37KFH2: https://www.amazon.de/-/en/Edwin-Prakoso-ebook/dp/B00V37KFH2 . ALTA para autoria e ASIN. 84 páginas, publicação em 2015.
25. Compilação *100 AutoCAD Tips You Should Know* em PDF: https://pdfcoffee.com/100-autocad-tips-you-should-know-pdf-free.html . BAIXA. Cópia não oficial, útil apenas para conferir o conteúdo da compilação, nunca como fonte de autoria.
26. AUGI, CAD advice from an Expert Elite: https://www.augi.com/articles/detail/cad-advice-from-an-expert-elite . MÉDIA. Contexto do programa e da colaboração com a AUGIWorld.
27. Autodesk Expert Elite, visão geral do programa: https://www.autodesk.com/expert-elite/overview . ALTA para a definição do programa, que sustenta a citação sobre "an appreciation for individuals who give contributions to the Autodesk community".

## Referências técnicas complementares (Autodesk oficial)

Não são fala do Edwin. Servem para validar que os comandos e workflows que ele ensina existem e funcionam como descrito. Confiança ALTA como documentação de produto, nenhuma citação de voz sai daqui.

28. How to convert a PDF to a DWG in AutoCAD: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-convert-a-PDF-to-a-DWG-in-AutoCAD.html
29. How to properly scale an image after inserting into AutoCAD: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-properly-scale-an-image-after-inserting-into-AutoCAD.html
30. How to resize using Scale to Reference: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-resize-using-Scale-to-Reference-in-AutoCAD-products.html
31. SHX files not included in PDF import: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/SHX-files-not-included-in-PDF-import.html
32. How to import a PDF into AutoCAD (blog Autodesk): https://www.autodesk.com/blogs/autocad/how-to-import-a-pdf-into-autocad/
33. Ins and outs of PDFs, Tuesday Tips with Frank: https://www.autodesk.com/blogs/autocad/ins-outs-pdfs-tuesday-tips-with-frank/
34. 60 AutoCAD Tips in 60 Minutes, Autodesk University 2016: https://www.autodesk.com/autodesk-university/class/60-AutoCAD-Tips-60-Minutes-2016 . Registrado aqui apenas como prova negativa: a aula é da Lynn Allen, não do Edwin.

## Confiabilidade por área

| Área do clone | Fontes | Confiabilidade |
|---|---|---|
| Citações verbatim sobre PDFIMPORT e SHX | cad-notes.com itens 4, 5, 6 | ALTA |
| Citações sobre Markup Import e OCR | cad-notes.com item 7 | ALTA |
| Citações sobre blocos dinâmicos | cad-notes.com item 8 | ALTA |
| Citações sobre template, layer, layout e produtividade | cad-notes.com itens 9 a 18 | ALTA |
| Biografia, cargo e credenciais | cad-notes.com itens 1 a 3, mais itens 26 e 27 | ALTA |
| Ebooks confirmados, páginas e ASIN | itens 19 a 24 | ALTA para autoria, MÉDIA para datas |
| Ebooks *101 AutoCAD Tips* e *Working with AutoCAD Annotation Scaling* | item 2 apenas | MÉDIA, autoria confirmada pelo site do próprio Edwin, sem ASIN, ISBN ou URL dedicada |
| Ano da 2a edição de *AutoCAD Block Best Practices* | item 23 | BAIXA, ASIN e autoria certos, ano não confirmado. Marcado como hipótese no arquivo 03 |
| Data de fundação do cad-notes.com | inferência a partir dos itens 2, 22 e do ebook de aniversário de 8 anos | BAIXA, tratada como hipótese explícita no arquivo 03 |
| Extensão do corpus na AUGIWorld | item 26 | BAIXA, colaboração confirmada, corpus não mapeado artigo por artigo |
| Workflow de Scale with Reference e ALIGN | endosso do Edwin mais documentação Autodesk itens 29 e 30 | MÉDIA, o workflow é padrão de comunidade e não tem artigo dedicado dele |
| Pipeline implícito de decisão PDFIMPORT versus underlay | dedução a partir dos itens 4, 5, 6 | MÉDIA, marcado como framework deduzido no arquivo 06 |

## Hipóteses explicitamente marcadas

Estes pontos do clone não têm fonte primária direta e foram registrados como hipótese em TODOS os arquivos onde aparecem, nunca como fato:

- A data exata de fundação do cad-notes.com. O ebook gratuito de aniversário de 8 anos e o documento de 2009 sugerem fundação por volta de 2009 ou 2010. Marcado como hipótese na timeline do arquivo 03 e na timeline do arquivo 09.
- O mapa completo das contribuições dele para a revista AUGIWorld. A colaboração está confirmada, o corpus não. Marcado no arquivo 03 e no arquivo 08.
- O pipeline de sete passos de conversão PDF para DWG, chamado PDFIMPORT Precision Test Workflow. Cada passo ancora numa afirmação real dele, mas a sequência unificada é dedução do conjunto de artigos, e não um tutorial único que ele tenha publicado. Declarado como dedução no arquivo 06, no system prompt do Claude (arquivo 02) e na ficha de capacidades.
- O ano-calendário do aniversário de 8 anos do blog, que deriva da hipótese de fundação. Marcado no arquivo 03.
- O ano da 2a edição de *AutoCAD Block Best Practices*. ASIN e autoria confirmados, ano não. Marcado no arquivo 03.
- A lista de serviços prestados por ele na PT Cipta Satria Informatica. Empresa e cargo confirmados, portfólio de serviços é escopo típico inferido. Marcado no arquivo 03.

## Acesso

Todas as URLs de cad-notes.com, allaboutcad.com, cadsetterout.com, AUGI e Autodesk são públicas e gratuitas. Os ebooks na Amazon são pagos. Scribd e pdfcoffee exigem conta ou têm cópia de terceiros e servem apenas como verificação cruzada, nunca como fonte única de qualquer afirmação do clone.

Voltar ao índice: [[edwin-prakoso_01_README]].
