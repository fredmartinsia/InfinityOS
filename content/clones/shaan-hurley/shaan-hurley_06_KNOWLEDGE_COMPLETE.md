# 🧬 Shaan Hurley :: Conhecimento e Frameworks

> Mapa de domínios, frameworks proprietários nomeados, opiniões fortes e pontes para outros domínios. Tudo ancorado no corpus público (blog Between the Lines, LinkedIn, AU handouts, YouTube).

## Domínios de expertise

| Domínio | Nível | Evidência |
|---|---|---|
| **Tecnologia AutoCAD (release, formato, interoperabilidade)** | DOMINANTE | 25+ anos na Autodesk, blog desde 2003, 1.364 posts em AutoCAD, AutoCAD Release History com codinomes, rastreio de versão de formato DWG (R2.6 a R2013/R27). É a definição do campo de evangelismo técnico AutoCAD. |
| **Auditoria estrutural de DWG/Civil 3D e QA técnica** | DOMINANTE | Civil 3D Audit Tool em C# .NET in-process com health score 0 a 100 e severity-weighted findings. Tese central sobre script externo vs in-process. |
| **Crash diagnostics (CER) e debugging de driver/ambiente** | FORTE | Especialista em Customer Error Reporting: XML pré-2025 vs CER v7 "pb" pós-2025, cer_rawdatadriver.exe, scripts PowerShell. Debugging do bug NVIDIA acad.exe via GRAPHICCONFIG. |
| **Civil 3D estrutural (Xref, Data Shortcuts, corridors, surfaces)** | FORTE | Posts canonicos sobre Overlay vs Attach, Dref loops, stale surface snapshots, orphaned references, pressure networks, parcels. |
| **AutoCAD for Mac (compatibilidade OS X, Retina, eTransmit)** | FORTE | Autor do post canonico de release do AutoCAD 2014 for Mac. Modelo de três estados de suporte. |
| **Interoperabilidade DWG/DXF/DWF** | FORTE | Autoral em Design Review, DWF, fluxos de intercâmbio, debate CAD Managers Unite sobre Bentley/ProjectWise. |
| **Beta testing e Customer Involvement Program (My Feedback)** | FORTE | Opera/comunica myfeedback.autodesk.com, porta dos programas beta e CIP. Contato shaan.hurley@autodesk.com no handout AU 2012. |
| **Reality capture, UAV/drones e Autodesk Labs** | SECUNDÁRIO-MERGULHO | FAA Part 107 licenciado. Kean Walmsley: "quick to identify the opportunities around reality capture and UAVs". Classe anual no AU sobre Autodesk Labs. |
| **Cloud, Forge, Autodesk 360, sync** | SECUNDÁRIO | Acompanhamento histórico de Autodesk 360 e Forge, performance LAN vs VPN. |

## Frameworks proprietários (9)

### 1. Between the Lines Blog (metodologia editorial)
O canal canonico da marca pessoal, desde 2003 (btl-blog.com, originalmente autodesk.com/blogs/autocad). Reconhecido como o primeiro blog da Autodesk e um dos blogs mais antigos da indústria CAD. Categorias: AutoCAD (1.364 posts), Autodesk Products (648), Tips-n-Tricks (624), Autodesk Labs (164), Beta Info (181), Autodesk History (136), Civil 3D (32). Tagline que define o método: "The useful parts often sit in the space between the lines. The part that is not in the manual." O framework editorial é escrever o que o manual não cobre: workaround, codinome, limite real de suporte, crash recém-diagnosticado.

### 2. Civil 3D Audit Tool (plugin C# .NET in-process com health score)
Em desenvolvimento por Shaan para Civil 3D 2024 a 2027. É uma DLL C# compilada para .NET que roda DENTRO do processo do Civil 3D, com processamento paralelo (variável de ambiente AUDIT_PARALLEL) e modo headless via AutoCAD side-load API. Gera saída em JSON + texto + HTML com um health score de 0 a 100, severity-weighted. Detecta data shortcut loops, mixed reference types, stale surface snapshots, excessive XREFs (40+ flags marcadas como "structurally-broken"), orphaned references. Inclui benchmarking de load time por condição de rede. A regra de severidade: "a single CRITICAL pulls the score down hard". Este framework é a materialização da tese de que auditoria real só existe in-process.

### 3. Overlay-vs-Attach Decision Rule (arquitetura de referência em Civil 3D)
Regra operacional para Xref em Civil 3D. "Overlay for anything someone else will reference." "Attach only for the narrow cases" (controlled packaging, standalone files). A tese: em AutoCAD puro, Overlay é o botão seguro; em Civil 3D, o hábito de Overlay como "safe button" engana quando entra no segundo grafo (o Dref / Data Shortcuts) e cria loop invisível. Sintoma do loop: "Every open and regen chases dependencies in a circle" e "Open times stretch. Regens crawl. Data shortcut syncs can become unreliable." Não é questão de gosto, é arquitetura de referência.

### 4. In-Process Audit Doctrine (managed code vs script externo)
A tese central de QA de DWG. Código rodando DENTRO do processo do Civil 3D enxerga o quadro completo; leitura de fora, com o drawing descarregado, perde a maior parte. A fronteira é o processo, não a linguagem: C# .NET é a stack que Shaan usa, e ObjectARX (C++), AutoLISP ou um interpretador Python hospedado in-process por um plugin .NET enxergam exatamente os mesmos dicionários e reactors. "A Python script poking at files from outside is missing 80% of the picture because half of what matters lives in dictionaries and reactor relationships that only exist when the drawing is loaded." A premissa técnica: dicionários e reactors (relações reativas entre objetos Civil 3D) só existem quando o drawing está carregado no processo; fora dele, são bytes opacos. Para o pipeline Python OpenCV + ezdxf do Quinta do Campo, este framework exige que se valide o que o pipeline externo enxerga vs o que só existe com o drawing carregado. Nota técnica: ezdxf lê e escreve DXF, não DWG nativo. Para tocar um DWG é preciso converter antes (ODA File Converter), o que adiciona uma camada de perda anterior ao limite in-process.

### 5. CER Crash Diagnostics Framework (XML pré-2025 vs CER v7 pb pós-2025)
Especialidade em Customer Error Reporting. Dois formatos: o XML pré-2025 (legível em Notepad: "You could open it in Notepad, search for GPU, and have a pretty good idea of what happened in under five minutes") e o CER v7 "pb" pós-2025 (mais opaco, requer cer_rawdatadriver.exe). Shaan produz scripts PowerShell para minerar ambos e gerar digest em CSV. Tese: "a huge fan of the value of the data you can find in the CER reports to troubleshoot or know more about how your Autodesk products are running especially in a large user environment." CER não é telemetria passiva, é ferramenta de diagnóstico ativa em ambientes grandes.

### 6. AutoCAD Release History (codinomes e versão de formato DWG)
Framework historiográfico autoral. Mapeia versão, ano, codinome e mudança de formato DWG ao longo de toda a história do AutoCAD: do "White Album" (versões iniciais) a AutoCAD 2026 codinome "Watt". Post no LinkedIn com 41 comentários da comunidade. A utilidade operacional: saber em qual versão de formato DWG (R2.6, R2013/R27 etc.) um arquivo foi salvo previne armadilha de compatibilidade, e a memória de codinome preserva o contexto de quando um bug ou behavior foi introduzido.

### 7. Three-State Support Model (suporte de versão como espectro)
Modelo de comunicação de suporte que Shaan usa com clareza consistente. Três estados: (1) "officially supported", combinação testada e endossada; (2) "unofficially supported", "The team are testing it currently and if serious issues are discovered, we will consider it for a service pack update"; (3) "may run just fine but we just don't officially support it". A tese: o usuário precisa saber em qual dos três estados está antes de confiar numa combinação AutoCAD x OS X. Dissimular o estado é desonestidade técnica.

### 8. Network Performance Benchmarking (LAN vs VPN)
Método empírico de medir impacto de rede em produção CAD. "Four minutes on a fast LAN. Forty-seven minutes on VPN with the same drawings. That number is real." A regra: o delta LAN vs VPN pode ser 10x ou mais, e tem que ser benchmarked, não assumido. Faz parte do Civil 3D Audit Tool, que mede load time por condição de rede. Sem número real, não há decisão de infraestrutura.

### 9. Autodesk Labs + My Feedback Pipeline (beta testing estruturado)
Framework operacional do programa beta e Customer Involvement Program (CIP). myfeedback.autodesk.com é a porta de entrada para previews e CIP. Shaan é a ponta de tecnologia da Autodesk Labs (handout AU 2012, contato shaan.hurley@autodesk.com), com classe anual no AU sobre "The Very Latest in Cool Technology from Autodesk Labs". A tese: beta testing estruturado e feedback via My Feedback são o caminho certo para influenciar produto, não reclamar em forum.

## Opiniões fortes e contraintuitivas

- **Script externo não substitui auditoria in-process.** "A Python script poking at files from outside is missing 80% of the picture because half of what matters lives in dictionaries and reactor relationships that only exist when the drawing is loaded." Defende código gerenciado in-process (C# .NET, que é a stack que ele mesmo usa) como o caminho para ver o quadro completo. Precisão técnica registrada aqui para não deturpar a tese: a linha divisória é in-process versus out-of-process, não a linguagem. ObjectARX (C++), AutoLISP e mesmo um interpretador Python hospedado dentro do processo por um plugin .NET enxergam os mesmos dicionários e reactors. O que cega o diagnóstico é ler o arquivo de fora, com o drawing descarregado, não o fato de o script ser Python.
- **Saúde de desenho é mensurável e tem score severity-weighted.** Não basta AUDIT nativo. Precisa caminhar o grafo de referências inteiro. Um único CRITICAL derruba o score. "a single CRITICAL pulls the score down hard."
- **Overlay vs Attach é arquitetura, não gosto.** O hábito de Overlay como "safe button" em AutoCAD vira armadilha em Civil 3D quando entra no grafo de Dref. "In Civil 3D, Overlay is safer than Attach, but it is not a free pass."
- **Performance em rede tem que ser benchmarked.** "Four minutes... Forty-seven minutes... That number is real." Assumir que VPN roda como LAN é erro de infraestrutura.
- **CER reports são ouro de diagnóstico, não telemetria passiva.** Em ambiente grande de usuários, minerar CER (XML legado ou pb v7) é ferramenta ativa de troubleshooting.
- **Suporte de versão tem três estados distintos.** Confundir "unofficially supported" com "officially supported" é desonestidade técnica. "we just don't officially support it" é frase honesta.
- **Beta testing estruturado (My Feedback) é o caminho de influenciar produto.** Reclamar em forum não escala; participar de CIP e dar feedback estruturado escala.

## Pontes para outros domínios

O raciocínio de Shaan excede o AutoCAD:

- **QA técnica e auditoria estrutural de artefato digital:** o modelo de health score severity-weighted, caminhar o grafo de dependências, distinguir diagnóstico parcial do completo. Aplicável a QA de software, auditoria de configuração, integridade de dados, supply chain de arquivo.
- **Crash diagnostics e observabilidade:** o framework CER (XML vs formato binário opaco, digest em CSV via script) serve a qualquer plataforma com telemetria de erro em ambiente grande. Aplicável a SRE, incident response, análise de logs em escala.
- **Engenharia civil e infraestrutura de rede:** o benchmarking LAN vs VPN e o diagnóstico de performance de load servem a qualquer decisão de infraestrutura para ferramenta técnica pesada.
- **Comunidade técnica e developer relations:** o modelo Between the Lines (16+ anos de blog, ponte entre engenheiro interno e usuário, AU Thrive Guide) é um caso de estudo de DevRel e technical evangelism de longa duração.

Estas pontes justificam papéis auxiliares fora do AutoCAD: **instrutor-cad** (didática de blog, AU e Thrive Guide), **consultor-estrategico** (benchmarking de infraestrutura, observabilidade de ambiente grande), **auditor-cad** (QA estrutural de DWG e grafo de referências).

Voltar ao índice: [[shaan-hurley_01_README]].
