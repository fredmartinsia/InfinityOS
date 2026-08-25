# 🧬 David Cohn :: Conhecimento e Frameworks

> Mapa de domínios, frameworks proprietários nomeados, opiniões fortes e pontes para outros domínios. Tudo ancorado no corpus público (handouts de Autodesk University AS323464 Sheet Sets, AUGI2010 Revit Collaboration, AB114-5 BIM-based Collaboration, GD405-1 Design Review, dscohn.com, CADLearning/4D Technologies, Digital Engineering reviews de AutoCAD 2012 e 2016, Google Books).

## Domínios de expertise

| Domínio | Nível | Evidência |
|---|---|---|
| **AutoCAD (domínio nativo da ferramenta)** | DOMINANTE | 35+ anos de AutoCAD, Autodesk Certified Professional para AutoCAD, mais de uma dúzia de livros sobre AutoCAD, um dos primeiros desenvolvedores terceiros de AutoCAD. |
| **BIM/Revit (coordenação multidisciplinar)** | DOMINANTE | 20+ anos de Revit, Autodesk Certified Professional para Revit, handout canônico AUGI2010 Collaborating Across Disciplines. |
| **Sheet Sets e coordenação de pranchas** | DOMINANTE | Handout AS323464 Curing a Lack of Coordination, tese do 1-sheet-1-DWG, automação via fields no title block. |
| **Templates e drawing standards (QA na origem)** | FORTE | Regra de atribuir `.dwt` ao sheet set, fields automáticos, handouts CD25-1 e GD111-3, content standards na CADLearning. |
| **Revision Tracking e integridade documental** | FORTE | Handout AUGI2010, regras By Project vs By Sheet, checkbox Issued como trava irreversível, revision cloud no sentido horário. |
| **Auditoria estrutural de DWG e clash detection** | FORTE | Interference Check com export para HTML, Coordination Review item por item, auditoria de Manage Links (Overlay vs Attachment). |
| **Hardware benchmarking e produtividade CAD** | SECUNDÁRIO | Benchmarking de PCs desde 1984, AutoCAD 2011 Productivity Study encomendado pela Autodesk, reviews para Digital Engineering e PC Magazine. |
| **Renderização, materiais e visualização** | SECUNDÁRIO | Handouts GD111-3 Rendering Part 1, workflow AutoCAD para 3ds Max 2018 (AU), Creating Materials, Visualization Workflow. |

## Frameworks proprietários (8)

### 1. Sheet Set Framework (Curing a Lack of Coordination)
O motor do trabalho dele em coordenação de pranchas. Um sheet set é uma coleção organizada e nomeada de sheets, onde cada sheet é um layout selecionado de um DWG. O conjunto inteiro pode ser gerenciado, transmitido (eTransmit), publicado e arquivado como uma **unidade**. Tudo vive num arquivo de dados de sheet set com extensão `.dst`. Os sheets são ponteiros/atalhos para layouts nos DWG; o SSM não cria novos DWGs nem pastas. Quando um DWG apontado por um sheet set é aberto e salvo com o SSM ativo, o AutoCAD grava um pequeno hint no DWG dizendo a qual sheet set ele pertence, e "This hint is the only change the program makes to your original drawing."

O SSM tem 3 abas: Sheet List (lista de sheets, com subsets aninháveis por disciplina), Sheet Views (vistas por sheet ou por categoria), Model Views (caminhos de pastas com named views de model space). Automação via fields: propriedades padrão (project number, project name) e custom properties (quem criou, quem checou) alimentam fields que populam title blocks, view labels, plot stamps e callouts automaticamente.

**BEST PRACTICE CENTRAL:** "the best practice for using sheet sets is to have one sheet per drawing file for each sheet in your set." Motivo: "The main benefit for this is to enable multiple users to work on different sheets at the same time." Se duas sheets apontarem para dois layouts no mesmo DWG, o arquivo trava assim que alguém abre uma delas ("which is how AutoCAD has always worked"). Implementação incremental: "you do not need to implement all the functionality at once. You can begin to take advantage of sheet set functionality for your current project with minimal effort."

### 2. BIM Coordination em 5 camadas (Collaborating Across Disciplines)
O pipeline canônico para coordenação multidisciplinar em Revit, extraído do handout AUGI2010. Cinco camadas encadeadas, mais a sexta de travamento documental:

1. **File Linking.** Linkar RVTs é análogo a XREF do AutoCAD. Posicionamento por Auto - By Shared Coordinates. Pode-se bindar link em grupo ou converter grupo em link.
2. **Shared Coordinates.** Cada RVT tem sistema interno só dele. "you should derive shared coordinates from only one file. That one file defines the coordinates for all other files that compose the project." Funciona com RVT, DWG e DXF. Em projeto multi-disciplinar, defina quem dita as coordenadas (em geral o arquiteto).
3. **Manage Links (Overlay vs Attachment).** Overlay (default): o link não segue o host se o host for linkado adiante, evita referência circular. Attachment: arrasta os links junto. Regra de auditoria: Overlay como padrão; Attachment só quando faz sentido.
4. **Copy/Monitor.** "You should only monitor key objects": levels, grids, columns, walls estruturais, floors, openings (e rooms no MEP). "the more objects you monitor, the slower the performance may become and the more complicated it can be to track changes." Walls precisam estar marcadas como estruturais (Bearing, Shear ou Structural Combined) no Architecture para serem copiadas/monitoradas no Structure.
5. **Coordination Review.** Quando um elemento monitorado muda no link, o Revit avisa. Ações por item: Postpone/Do Nothing, Reject, Accept Difference, Modify/Rename/Move. "Once you have dealt with all of the items in the Coordination Review dialog, the list should be clear and your project is coordinated."
6. **Interference Check (clash detection).** Run a qualquer momento. Compara categorias do current project vs categorias de um linked project, "You cannot run a check between two different linked files, however." Gera relatório expansível por instância, com Show para localizar e export para HTML. "Used efficiently, there is no longer any reason to remain unaware of conflicts until during construction, when solving them is likely to result in a costly change order." "Revit will not automatically solve interference conditions", mas usada bem facilita comunicação.

### 3. Revision Tracking com Issued Irreversible
Camada de travamento documental. Revisions dialog (Manage ribbon > Settings > Sheet Issues/Revisions). Numeração By Project (sequência global) ou By Sheet (sequência por prancha). "revision descriptions should be comprehensive, yet as concise as possible." Checkbox Issued: quando marcado, "Once the revision has been issued, you can no longer make any modifications to that revision" (nem clouds, nem sketch, nem Instance Properties). Revision Cloud na Annotate ribbon, desenhado no sentido horário para que os arcos arqueiem para fora. Tag by Category taggear automaticamente pelo número. Revisions aparecem automaticamente no revision schedule do title block de cada sheet. É a trava de integridade documental que separa rascunho de documento emitido.

### 4. Built-in QA via Templates e Fields
Mecanismo de controle de qualidade automático na origem. Atribuição de drawing template (`.dwt`) ao sheet set faz novos sheets já nascerem do template correto. Fields ligando propriedades do sheet set ao title block eliminam erro humano de digitação: project number, project name, criado por, checado por, plot stamp. É QA automático porque o caminho certo é também o caminho mais fácil. Handouts CD25-1 documentam uso de hyperlinks para criar novos desenhos baseados em standardized drawing template. Reviews de AutoCAD 2012 e 2016 (Digital Engineering) destacam a migração do Sheet Set Manager para o AutoCAD LT e melhorias de PDF no contexto do SSM.

### 5. Microlearning Imediatamente Acionável (CADLearning Content Standards)
Framework pedagógico da 4D Technologies. Cohn "develops content standards and creates microlearning that is immediately actionable and leads to better knowledge retention." Princípio: conteúdo curto, direto, aplicável agora, com retenção medida. É o oposto do curso longo teórico; cada microlesson resolve uma tarefa específica que o usuário enfrenta hoje. Conecta com a didática dos handouts AU (learning objectives numerados, procedimento numerado, conclusão).

### 6. Productivity Study Methodology
Metodologia de benchmark de produtividade entre versões de AutoCAD, aplicada no AutoCAD 2011 Productivity Study encomendado pela Autodesk. Desenhos ortográficos selecionados (não casuais), métricas de tempo controladas, comparação entre versões. Replicável e honesta sobre o setup. Hipótese: o fato de ser vendor-sponsored não invalida o rigor ortográfico, mas Cohn é transparente sobre o patrocínio.

Aplicação prática fora do estudo original: antes de afirmar que uma versão nova, um template novo ou um script de automação "ficou mais rápido", defina o conjunto de desenhos de teste (ortográficos, representativos, sempre os mesmos), cronometre a mesma tarefa nas duas versões, publique quem pagou pelo teste e mostre o setup. Sem conjunto controlado e sem declaração de patrocínio, o número não é benchmark, é anedota.

### 7. Incremental Implementation Discipline
Aplicado a qualquer rollout de padrão, template ou sheet set. "you do not need to implement all the functionality at once." Comece pelo básico (importar layouts existentes como sheets), evolua para title blocks automatizados, depois callouts e publish. Cada estágio entrega ganho, sem paralisia de implementação 100%. Complementar ao Sheet Set Framework.

### 8. Coordination Review Loop (Postpone/Reject/Accept/Modify)
Framework de decisão item por item quando o Copy/Monitor detecta mudança no link. Quatro ações canônicas, cada uma com intenção clara: Postpone (não decide agora, volta depois), Reject (o change no link está incorreto, comunicar o autor), Accept Difference (atualiza a relação, ex.: grids de 25' para 30'), Modify/Rename/Move (ajusta conforme o caso). Add Comment documenta a decisão para o time. O loop fecha quando a lista está clear: "your project is coordinated." É o protocolo de resolução de conflito em BIM.

## Opiniões fortes e contraintuitivas

- **1 sheet = 1 DWG é regra, não sugestão.** Repete que é a "best practice" porque libera concorrência multiusuário. Quem põe dois layouts do mesmo DWG como duas sheets está reintroduzindo o lock que o SSM veio resolver.
- **Coordenadas compartilhadas têm dono único.** "you should derive shared coordinates from only one file." Em projeto multi-disciplinar o time precisa acordar quem dita (em geral o arquiteto) antes de começar a linkar.
- **Monitore só key objects.** Copy/Monitor em tudo que é elemento degrada performance e complica o tracking. Levels, grids, columns estruturais, walls estruturais, floors, openings. O resto é ruído.
- **Clash detection é obrigatório antes da obra.** "there is no longer any reason to remain unaware of conflicts until during construction, when solving them is likely to result in a costly change order." Não há desculpa para descobrir conflito na construção.
- **Templates e fields são o mecanismo de QA automático.** Title block que não popula via field do sheet set é title block que vai ter erro humano. Padronização se faz na origem (template `.dwt` + propriedades do sheet set), não na ponta.
- **Implementação incremental vence paralisia.** "you do not need to implement all the functionality at once." Comece pelo básico e evolua. Não espera implementar 100% para começar a ganhar.
- **Issued é irreversível por design.** "Once the revision has been issued, you can no longer make any modifications to that revision." É a trava de integridade documental que separa rascunho de documento emitido.
- **Revit não é mágico, é ferramenta de comunicação.** "Revit by itself won't prevent conflicts from occurring, but it helps facilitate improved communication between project team members." Cética de hype, honesta sobre limite.

## Pontes para outros domínios

O raciocínio de Cohn excede o CAD/BIM:

- **Auditoria estrutural de qualquer artefato técnico.** O pipeline de BIM Coordination (definir fonte única, monitorar só o crítico, rodar verificação, revisar item por item, documentar com Issued) é transferível para auditoria de software, compliance documental, QA de manufatura.
- **Design de conteúdo pedagógico (microlearning).** O framework de content standards e microlearning imediatamente acionável serve a qualquer educador técnico, time de enablement, documentação de produto.
- **Protocolo de resolução de conflito (Coordination Review).** O loop Postpone/Reject/Accept/Modify é um modelo de decisão para qualquer time distribuído que precisa resolver divergência entre partes (dev vs design, produto vs engenharia, jurídico vs negócio).
- **Padrão como automação (path of least resistance via fields).** A ideia de que padrão se faz na origem (template que popula automaticamente) é transferível para qualquer processo onde erro humano é recorrente (onboarding, contracts, reports).
- **Benchmarking metodológico.** Productivity Study com desenho ortográfico controlado é modelo de A/B test para qualquer ferramenta técnica.

Estas pontes justificam papéis auxiliares fora do CAD/BIM: **especialista-autocad** (domínio nativo da ferramenta), **instrutor-cad** (didática de content standards e microlearning), **auditor-cad** (auditoria estrutural de DWG e BIM Coordination).

Voltar ao índice: [[david-cohn_01_README]].
