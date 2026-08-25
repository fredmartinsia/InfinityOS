# 🧬 Shaan Hurley :: Contexto

> Era e cenário em que a pessoa se destacou, e por que o pensamento ainda importa.

## Contexto histórico

Shaan Hurley entrou na Autodesk em 1998. O que o mundo era então:

- **O CAD era desktop, license perpetual e AutoCAD dominava o 2D.** BIM ainda era promessa distante e o Revit sequer pertencia à Autodesk. Cloud, sync e mobile não existiam no fluxo CAD: troca de arquivo era rede local.
- **Não existia blog corporativo de CAD.** A Autodesk não tinha canal técnico direto ao usuário; a comunidade dependia de fóruns e de revistas como Cadalyst. Shaan fundou o Between the Lines em 2003, originalmente em autodesk.com/blogs/autocad, e o transformou no PRIMEIRO blog da Autodesk e em uma das crônicas mais longas da indústria CAD ao vivo.
- **O programa beta era opaco.** Customer Involvement Program e o acesso a previews eram informais. Shaan estruturou, comunicou e operou o My Feedback (myfeedback.autodesk.com) como porta de entrada dos programas beta e CIP.
- **Customer Error Reporting (CER) era telemetria passiva.** Em 1998 o dado de crash existia mas não era trabalhado como ferramenta de diagnóstico ativa em ambiente grande. Shaan virou especialista em minerar CER, do formato XML pré-2025 ao CER v7 "pb" pós-2025, com scripts PowerShell.

A carreira dele acompanha a maturação do ecossistema CAD:

- **Anos 1990 e início dos 2000:** AutoCAD consolida desktop CAD 2D. Shaan entra na Autodesk (1998) e funda o Between the Lines (2003), o primeiro blog da empresa.
- **Anos 2010:** AutoCAD for Mac (2011, 2013, 2014) com OS X Mavericks, Retina e eTransmit; transição de AutoCAD WS para AutoCAD 360 (2013, citado na Wikipedia); ascensão do Civil 3D e dos problemas estruturais de Xref/Dref; Autodesk Labs como pipeline de ideia para produto; reality capture e UAVs decolam, e Shaan é dos primeiros a identificar a oportunidade (FAA Part 107 em 2016).
- **Anos 2020:** o modelo de licença migra de perpetual para subscription; cloud, Forge e Autodesk 360 entram; CER muda de formato (XML para pb v7 em 2025) e Shaan adapta o troubleshooting; Civil 3D Audit Tool em C# .NET in-process com health score 0 a 100 surge como resposta à insuficiência do AUDIT nativo e do script externo; LLM entra no radar e Shaan reconhece que é útil mas alerta sobre o limite do olhar externo.

## Vantagens do contexto

- **25+ anos dentro da Autodesk** deram acesso raro a engenheiros de produto (Heidi Hewett, Shiho Tanaka, Scott Sheppard) e a programas internos (My Feedback, CER, Labs). A memória operacional de toda a curva de release é autoridade que nenhum blogueiro externo tem.
- **Base em Bend, Oregon** manteve distância do ruído de marketing corporativo, preservando a franqueza técnica.
- **Blog de 16+ anos** refinou a didática técnica e a estrutura sintoma-causa-workaround-confirmação.
- **Trabalho de campo com crash, driver e formato** deu profundidade que evangelista de palco não tem. Shaan diagnostica, não apenas apresenta.
- **FAA Part 107 (2016)** legitimou a vertente reality capture/UAV antes de virar hype.

## Desafios do contexto

- **A complexidade do DWG cresceu mais que a transparência.** Dicionários, reactors e relações reativas entre objetos Civil 3D tornaram o formato mais opaco a ferramenta externa. A In-Process Audit Doctrine é resposta direta a esse desafio.
- **O CER ficou mais fechado.** A transição do XML (legível em Notepad) para o pb v7 (que requer cer_rawdatadriver.exe) reduziu o acesso fácil ao dado de crash. Shaan precisa de scripts PowerShell para recuperar o nível de diagnóstico que antes era trivial.
- **A indústria consolidou em poucos vendors**, com lock-in crescente em formato. Defender interoperabilidade DWG/DXF/DWF e three-state support honesto é desvantajoso em informação frente ao marketing de vendor.

## Relevância atual

Por que Shaan importa em 2026, quando o CAD convive com BIM, cloud, IA generativa e realidade estendida:

- **A tese central se aprofundou.** Quanto mais objetos reativos e dicionários o DWG/Civil 3D acumula, mais verdadeira é a afirmação de que script externo perde a maior parte do quadro. "A Python script poking at files from outside is missing 80% of the picture." IA generativa e automação externa não tornam a auditoria in-process obsoleta; tornam-na mais necessária, porque aceleram a produção e amplificam o custo de um diagnóstico parcial.
- **QA estrutural de artefato digital virou disciplina geral.** O modelo de health score severity-weighted, caminhar o grafo de dependências e distinguir diagnóstico parcial do completo serve a QA de software, integridade de dados e auditoria de configuração, não só a DWG.
- **Observabilidade e crash diagnostics em escala são centrais em SRE e DevOps.** O framework CER (formato opaco, digest via script, valor em ambiente grande) traduz direto para qualquer plataforma com telemetria de erro em escala.
- **Para o projeto Quinta do Campo**, o pensamento de Shaan é diretamente aplicável. O pipeline Python OpenCV + ezdxf que vetoriza planta scanneada em DWG precisa ser validado contra o alerta técnico do Shaan: o que o pipeline externo enxerga é a casca; dicionários e reactors só existem com o drawing carregado. E há um limite anterior a esse: ezdxf opera sobre DXF, não sobre DWG nativo, então o DWG precisa ser convertido (ODA File Converter) antes de qualquer leitura, com perda própria nessa conversão. A auditoria final do DWG R2013/R27 não pode parar no script externo; precisa de validação in-process ou ao menos de AUDIT com o drawing aberto, caminhando o grafo de referências. A fronteira aqui é o processo, não a linguagem: um Python hospedado dentro do processo por um plugin enxerga o mesmo que C# .NET ou ObjectARX, e o que cega o diagnóstico é ler o arquivo de fora, com o drawing descarregado. A distinção dos três estados de suporte orienta a decisão de versão de AutoCAD/QCAD para o cliente.

Voltar ao índice: [[shaan-hurley_01_README]].
