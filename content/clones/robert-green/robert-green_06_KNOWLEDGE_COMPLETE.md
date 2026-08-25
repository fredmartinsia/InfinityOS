# 🧬 Robert Green :: Conhecimento e Frameworks

> Mapa de domínios, frameworks proprietários nomeados, opiniões fortes e pontes para outros domínios. Tudo ancorado no corpus público (Cadalyst, Autodesk University, livro Expert CAD Management, SlideShare Quality Control for CAD/BIM Managers).

## Domínios de expertise

| Domínio | Nível | Evidência |
|---|---|---|
| **CAD management** (gestão de ecossistema CAD, padrões, processo, ROI) | DOMINANTE | No CAD desde 1985, 500+ colunas "CAD Manager" na Cadalyst desde 1998, livro Expert CAD Management, consultoria desde 1991. É a definição do campo. |
| **Padrões de camada CAD (standards, layer naming, templates)** | FORTE | Colunas sobre standards compliance, framework Built-in Compliance via Templates, recomenda adoção de U.S. National CAD Standard e AIA layer guidelines. |
| **Auditoria de arquivo CAD e QA de desenho** | FORTE | Coluna "How to Audit Your Office CAD Use", framework Deming + Andon + Kaizen no SlideShare Quality Control for CAD/BIM Managers. |
| **Análise financeira de CAD (ROI, rework cost)** | FORTE | Tese de stagflation do mercado, Rework Cost Analysis (Man Hours x Hourly Rate), capítulo 7 do livro. |
| **Gestão de equipe CAD e change management** | FORTE | Peer-to-Peer CAD Manager (AU), reflect annoyance method, Build an Efficient CAD Team. |
| **Automação e network/WAN optimization** | SECUNDÁRIO | Serviços da Robert Green Consulting (programming, task automation, UI designs, Peer Software WAN). |
| **BIM/Revit management** | SECUNDÁRIO | Apêndices do livro cobrem AEC e Revit; supervisão de ecossistemas mistos Autodesk. |

## Frameworks proprietários (11)

### 1. Unified Theory of CAD Management
O motor do trabalho dele. Ciclo eterno de cinco passos (artigo "The Constants in CAD Management", 500ª coluna, Cadalyst):
1. **Find** onde os erros CAD vêm, perguntando aos usuários.
2. **Fix** os erros, trabalhando com os usuários e construindo o próprio skill set.
3. **Standardize**: cada fix vira o novo padrão.
4. **Drive compliance** via produção (não via documento).
5. **Repeat**.

Na forma original, em inglês, o ciclo é: "Find where the CAD errors come from by asking users. Fix the errors by working with users and building my own skill set. Make any fixes my new standards. Drive standards compliance by stressing production. Repeat." (The Constants in CAD Management, 500ª coluna, Cadalyst).

Aplicação: é o loop diário do CAD manager. Não tem fim. "The more things change, the more they stay the same" é o lema.

### 2. Deming Theory of Process Control aplicada a CAD
Importa W. Edwards Deming para o office CAD. Ciclo: know what people do > check that they do it right > act when they deviate > plan corrective action > repeat. Ancora na citação de Deming que Green repete: "If you can't describe what you're doing as a process then you don't know what you're doing." Se o trabalho não é processo descrito, não é gerenciado.

### 3. Andon Cord System para CAD
Importa o Andon cord da Toyota (linha de produção) para o fluxo de desenhos. Quando um erro de padrão é detectado:
- A produção **PARA**.
- A fonte/causa é identificada imediatamente (não a pessoa, o procedimento).
- Os resultados são **públicos**, mas não pessoais.
- O project management é envolvido na resolução.
- O fix é feito **ANTES** de continuar.

Vantagens listadas por Green: error makers são localizados prontamente, ignorar procedimentos para a produção, o custo real dos erros fica visível, evita "burying errors". É a ferramenta que torna o erro invisível em custo visível.

### 4. Kaizen CAD Methodology
Aplica Kaizen (melhoria contínua japonesa) ao CAD. Princípios operacionais: erros sujeitos a "laser beam scrutiny", processo visível a todos os stakeholders, soluções claramente definidas, accountability é paramount, custos são conhecidos e exibidos, "change for good". Diferente de campanha de qualidade pontual, é disciplina perpétua.

### 5. Rework Cost Analysis
Método quantitativo para justificar QA em dólares. Fórmula: **Man Hours x Hourly Rate = Costs**. Trackear ao longo do tempo. Fontes comuns de retrabalho que ele lista: reformatting drawings, missed interferences, inefficient interdepartmental handoffs, not meeting client requirements. Exemplo canônico: "Every week Larry must fix at least two of Allan's files which costs about one hour of lost time. Over a 52-week year, using Larry's $55/hour rate this 52-hour loss costs us $2,860." Better quality = lower cost.

### 6. Incremental Innovation Cycle
Contraposição deliberada à inovação radical. Ciclo de seis passos:
1. List your nagging, small problems.
2. Propose solutions that simplify and save time.
3. Eliminate tools that are complex and costly.
4. Prioritize easy, low-cost solutions.
5. Sell the solution to users (antes de falar com o chefe).
6. Repeat forever.

Tese: inovação radical tem "Big costs, Extensive workflow changes, Unknown disruptions" e "no CAD manager can push through radical innovation on their own". Incremental é o único caminho viável.

### 7. Reflect Annoyance Method
Adapta Fishman e Sullivan ao CAD. "The core concept Fishman and Sullivan advocate is to channel the annoying consequences of errors to the person who caused the error, rather than dealing with the error yourself." O método reflete o custo do fix sobre quem causou o problema, até que seja mais fácil fazer certo do que errar. Premissa: "Most (not all) the quality problems you experience are due to people in the organization choosing (consciously or not) to avoid using standard methods because they find them annoying."

### 8. Reverse Engineering Workflows
Nunca comece pela spec técnica da ferramenta. Comece pelo deliverable do cliente (o PDF final, o pacote de licenciamento, o conjunto de pranchas) e trabalhe para trás até o workflow que o produz. O padrão correto emerge do output desejado, não do recurso do software.

### 9. Built-in Compliance via Templates
Padrão escrito não conforma. Template sim. Entregue arquivos `.dwt` com as layers já pré-configuradas (o exemplo que ele usa é dimensões em AR-DIM; os demais códigos de camada saem do padrão que o escritório adotar, AIA ou U.S. National CAD Standard) e instrua os usuários a partirem do template. A conformidade fica "ingrained in the workflow", porque usar o template é mais rápido que não usar. "Who wouldn't use an available solution that already works?"

### 10. Management Speak Translation
Disciplina de comunicação com senior management. Nunca fale técnico com CFO/CEO. Fale em lucro, custo, savings, ROI, rework cost. "It isn't their job to understand CAD, because that is my job." "Talk to them in Management Speak!" O CAD manager que não traduz perde budget e influência.

### 11. Peer-to-Peer CAD Management
Modelo de influência sem autoridade formal. Cada vez mais CAD managers operam sem título ou poder formal ("they're what I call peer-to-peer CAD managers"). Estratégia: estabeleça credibilidade técnica primeiro ("establishing your technical credibility by making sure your peers understand your expertise is the number one way to achieve CAD management success"). Em estrutura peer-driven, "people must want to follow you".

## Opiniões fortes e contraintuitivas

- **Standards viram workflow, não documento.** Um manual grosso de padrão sem template e training é "spitball". A conformidade real vem da path of least resistance.
- **CAD software em stagflation.** Defende publicamente que Autodesk e concorrentes entregam inovação estagnada com preço inflado. ROI de subscription cai. Sem savings, é "dead cost".
- **Inovação radical é armadilha.** Troca de plataforma, salto geracional, migração 2D para 3D de uma vez: custa caro, exige retraining massivo, gera unknown disruptions. Incremental é o caminho.
- **Soft skills vencem technical skills.** "Personal attributes and communication skills determine success in CAD management more than technical skills." O técnico é table stakes.
- **Management speak é obrigatório.** CAD manager que fala técnico com gestão perde. Tem que falar lucro e custo.
- **Quem causa erro deve sentir o custo.** Absorver retrabalho esconde o problema. Reflect annoyance é a única técnica que reduz workload do CAD manager enquanto aumenta conformidade.
- **Parar produção é ferramenta legítima de QA.** Andon cord. Erro não resolvido vira custo invisível.
- **Relacionamento com IT define qualidade de vida.** "If your relationship with IT is great, then your life as CAD manager will be good."

## Pontes para outros domínios

O raciocínio de Green excede o CAD:

- **Gestão de processos e lean (Deming, Toyota, Kaizen):** aplicável a qualquer operação técnica repetitiva (manufatura, dev ops, back office). O Andon cord e o Kaizen são transferíveis diretos.
- **Análise financeira de tecnologia (ROI, TCO):** aplicável a qualquer decisão de stack, SaaS ou ferramenta. O framework "no savings means no ROI" é universal.
- **Change management e influência sem autoridade:** aplicável a qualquer líder de squad distribuído, tech lead, product manager em matriz. Peer-to-peer é modelo moderno de liderança técnica.
- **Auditoria de qualidade estrutural:** o ciclo Deming (know, check, act, plan, repeat) serve a QA de software, controle de qualidade industrial, compliance.

Estas pontes justificam papéis auxiliares fora do CAD: **consultor-estrategico** (tradução técnico para negócio), **instrutor-cad** (didática de AU e colunas), **auditor-cad** (QA estrutural de arquivo).

Voltar ao índice: [[robert-green_01_README]].
