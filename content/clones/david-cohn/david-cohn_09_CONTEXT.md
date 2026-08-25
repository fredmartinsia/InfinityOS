# 🧬 David Cohn :: Contexto

> Era e cenário em que a pessoa se destacou, e por que o pensamento ainda importa.

> Nota de rastreabilidade: as datas da indústria usadas como pano de fundo (AutoCAD lançado em 1982, Revit adquirido pela Autodesk em 2002, Sheet Set Manager introduzido no AutoCAD 2005, migração para subscription em 2016) são registro público da história do CAD, não vêm do corpus de David Cohn. Os fatos sobre a trajetória dele estão ancorados em `_11_SOURCES`.

## Contexto histórico

David Cohn entrou no CAD nos anos 80, quando AutoCAD (lançado em 1982) era a exceção acessível que rodava em PC e a categoria "desktop CAD" estava se formando. O que o mundo era então:

- **O CAD era mainframe ou workstation cara.** AutoCAD em PC era a democratização do desenho técnico. Quem aprendia nos anos 80 estava na fronteira da acessibilidade. Cohn tornou-se editor da Cadalyst em setembro de 1987, vindo de editar o Memphis User Group Newsletter, ou seja, estava no epicentro da comunidade técnica que se formava em torno do AutoCAD em PC.
- **Não existia BIM.** Revit foi adquirido pela Autodesk só em 2002. A coordenação multidisciplinar era feita em 2D com XREF, e a ideia de linked model com Copy/Monitor estava para nascer. Cohn viu essa transição do zero.
- **Não existia Sheet Set Manager.** O SSM chegou no AutoCAD 2005. Antes, pranchas eram gerenciadas manualmente, com title block populado à mão, callouts digitados, arquivos soltos em pasta. O framework "Curing a Lack of Coordination" de Cohn responde direto a essa dor histórica.
- **Pre-Internet, pre-cloud, pre-IA generativa.** Troca de arquivo era disquete ou rede local. Não havia sync, não havia versionamento distribuído. Cada erro de padrão se propagava por semanas. Citação de "archaic file names" no handout AS323464 é referência direta a esse contexto.
- **A indústria de benchmarking de hardware para CAD estava nascendo.** Cohn faz benchmarking de PCs desde 1984, atividade que sustentou por décadas em reviews para Computer Graphics World, PC Magazine e Desktop Engineering/Digital Engineering.

A carreira dele acompanha a maturação do CAD/BIM como indústria:

- **Anos 1980:** AutoCAD em PC democratiza CAD. Cohn é um dos primeiros desenvolvedores terceiros, criando add-ons. Editor da Cadalyst a partir de 1987.
- **Anos 1990:** AutoCAD consolida desktop CAD. Cohn publica dezenas de artigos e os primeiros livros canônicos (Complete AutoCAD até Release 11, AutoCAD LT: The Complete Guide, David Cohn's AutoCAD Release 14 Essentials em 1999, AutoCAD 2000: The Complete Reference em 2000).
- **Anos 2000:** BIM (Revit, adquirido em 2002) começa a subir. AutoCAD 2005 traz Sheet Set Manager. Cohn documenta e ensina ambos, e sobe a senior editor e publisher de publicações irmãs (CADCAMNet, Engineering Automation Report). O status de AIA Registered Provider é confirmado, mas a pesquisa não recuperou o ano em que foi obtido: não é datado aqui.
- **Anos 2010:** Subscription substitui perpetual license (Autodesk 2016). Revit/BIM ameaça o AutoCAD 2D. Cohn formaliza o pipeline de BIM Coordination em cinco camadas (AUGI2010), conduz o AutoCAD 2011 Productivity Study, atua como Learning Product and Process Strategist na Autodesk. AutoCAD 2012 review destaca a migração do SSM para o AutoCAD LT.
- **Anos 2020:** SaaS, IA generativa, cloud. Cohn vira Senior Content Manager CADLearning na 4D Technologies, desenvolve content standards e microlearning para AutoCAD, AutoCAD LT e ReCap. Cobertura de additive manufacturing certification na Digital Engineering (maio/2024).

## Vantagens do contexto

- **Chegou cedo (anos 80) e viu toda a curva de maturação do CAD/BIM.** Tem memória operacional de 35+ anos de AutoCAD e 20+ de Revit, autoridade histórica que recém-chegado não tem.
- **Formação em arquitetura pela Syracuse University** deu vocabulário para falar de desenho técnico com o cliente arquiteto em pé de igualdade, e sustenta o AIA Registered Provider status.
- **Certificação dupla (Autodesk Certified Professional para AutoCAD e Revit).** Combinação rara que permite dialogar com times 2D e BIM sem regionalismo, e auditar deliverable misto.
- **Trânsito entre Autodesk (vendor), Cadalyst (imprensa técnica independente) e 4D Technologies (produto de aprendizagem).** Dá visão de produto e de usuário ao mesmo tempo. Diferente de Robert Green ([[robert-green]], consultor que critica vendor de fora, contraste de posicionamento entre clones do vault), Cohn é o insider que mantém honestidade sobre limitações mesmo tendo sido strategist na própria Autodesk.
- **Atuação como expert witness em litígio de CAD.** Dá a ele a disciplina de auditor defensável, com evidência e procedimento rastreável.

## Desafios do contexto

- **A indústria consolidou em poucos vendors** (Autodesk, Bentley, Nemetschek, Bricsys), com lock-in crescente. Manter independência crítica sendo insider de vendor é tensão produtiva constante.
- **A transição de AutoCAD 2D para Revit/BIM ainda é parcial em muitos escritórios.** Cohn opera nas duas margens, o que exige manter certificação e domínio em dois paradigmas simultaneamente.
- **Vendor-sponsored research (AutoCAD 2011 Productivity Study pago pela Autodesk) expõe a crítica de viés.** Cohn sustenta o rigor do setup ortográfico e é transparente sobre o patrocínio, mas a percepção de viés é desafio recorrente.

## Relevância atual

Por que Cohn importa em 2026, quando o CAD/BIM convive com IA generativa, cloud, scan (ReCap) e realidade estendida:

- **Os frameworks de coordenação sobrevivem à ferramenta.** Sheet Set Manager, BIM Coordination em cinco camadas, Copy/Monitor de key objects, Revision Tracking com Issued são invariantes. A IA generativa não torna Interference Check obsoleto; torna-o mais necessário, porque acelera a produção e amplifica o custo do erro não detectado.
- **Auditoria estrutural virou crítica com pipeline automático de vetorização.** No projeto Quinta do Campo, o DWG vem de pipeline Python OpenCV + ezdxf + QCAD. Sem auditoria estrutural humana (camadas A-PAREDES/A-COTAS/A-HACHURA/A-MOBILIARIO/A-VAOS, entidades LWPOLYLINE/CIRCLE/ARC/INSERT/HATCH íntegras, R2013/R27, zero erros ezdxf), o output automático vira lixo confiante. Cohn é quem pergunta "está preciso, coordenado e completo?" antes de aceitar.
- **Microlearning imediatamente acionável é o formato dominante de educação técnica.** O framework de content standards da CADLearning, com retenção medida, virou referência para qualquer time de enablement e documentação de produto.
- **Integridade documental (Issued) virou crítica em contexto de rastreabilidade.** Em projetos sujeitos a auditoria legal ou contractual, o checkbox Issued como trava irreversível é o que separa rascunho de documento emitido. A tese de Cohn sobre revision tracking é diretamente aplicável.
- **A certificação dupla virou referência de carreira.** Em um mercado onde profissional de CAD/BIM precisa dialogar com 2D e BIM, a certificação Autodesk Certified Professional para AutoCAD e Revit é o modelo de carreira que Cohn encarna.

Voltar ao índice: [[david-cohn_01_README]].
