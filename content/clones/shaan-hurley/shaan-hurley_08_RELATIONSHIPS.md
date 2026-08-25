# 🧬 Shaan Hurley :: Relações

> Mentores, influências, comunidade influenciada e contrapontos. Tudo ancorado em fonte pública.

## Mentores e influências

Shaan não cita um único mentor pessoal; ele constrói o pensamento por imersão longa no ecossistema Autodesk e por exposição direta aos engenheiros de produto. Os "mentores intelectuais" são o próprio tempo de casa, os programas internos e a comunidade:

- **Autodesk Labs e o programa My Feedback.** Não é pessoa, é a estrutura que moldou o método dele. Como ponta de tecnologia do Labs (handout AU 2012, contato shaan.hurley@autodesk.com), Shaan vê technology previews e o pipeline de ideia para produto antes de qualquer blogueiro externo. O My Feedback (myfeedback.autodesk.com), que ele opera e comunica, é o modelo de como feedback estruturado vira influência de produto.
- **Engenheiros de produto com quem trabalha pelo nome.** Heidi Hewett (co-apresentadora de AutoCAD 2010 Favorite Features), Shiho Tanaka (QA Engineer AutoCAD, entrevista no canal), Scott Sheppard (Autodesk Labs, entrevista). Esses colegas funcionam como fonte técnica interna que Shaan traduz para o usuário final.
- **Customer Error Reporting (CER) como mentora epistemológica.** O framework de crash diagnostics ensinou Shaan a pensar em diagnóstico empírico: número, módulo, versão, formato. "You could open it in Notepad, search for GPU, and have a pretty good idea of what happened in under five minutes" é lição de método, não só de ferramenta.
- **A própria comunidade CAD.** Duas décadas de blog e de discussão pública em torno dele (o post de codinomes sozinho teve 41 comentários da comunidade no LinkedIn) funcionam como correção e aprofundamento contínuo. O leitor ensina tanto quanto aprende.

## Pessoas que influenciou

Shaan influenciou praticamente toda uma geração de usuários AutoCAD, Civil 3D e gestores de ambiente CAD grande, de forma ampla e difusa:

- **A comunidade de usuários AutoCAD e Civil 3D.** O Between the Lines é leitura recorrente há 16+ anos. Workaround, codinome, three-state support e diagnóstico de driver que ele publica viram prática de campo em escritórios do mundo todo. A Engineering.com o nomeou "Resource of the Month" em junho de 2009.
- **Ambientes grandes de usuários (large user environment).** O framework CER crash diagnostics e os scripts PowerShell que ele documenta são ferramenta ativa de troubleshooting em empresas com centenas de estações CAD. "a huge fan of the value of the data you can find in the CER reports... especially in a large user environment."
- **Comunidade de beta testers e CIP.** Ao operar/comunicar o My Feedback, Shaan recruta e guia usuários para os programas beta estruturados. A tese dele de que "beta testing estruturado é o caminho de influenciar produto" direcionou como muitos participam de CIP.
- **Comunidade Autodesk University.** O AU Thrive Guide anual (2025 Nashville, 2026 Las Vegas) é o manual de sobrevivência que ele escreve para quem vai ao AU, especialmente pela primeira vez. 34 edições assistidas dão autoridade que poucos têm.
- **Comunidade reality capture e UAV.** Foi dos primeiros na Autodesk a identificar a oportunidade de reality capture e UAVs (drones). FAA Part 107 licenciado. Kean Walmsley: "was quick to identify the opportunities around reality capture and UAVs."
- **Blogueiros e criadores de conteúdo CAD.** O Between the Lines, por ser o primeiro blog da Autodesk, abriu o caminho para uma geração de blogueiros técnicos CAD (cad-notes.com, cadsetterout.com, entre outros o citam).

## Contrapontos e debates

- **Quem trata script externo como auditoria suficiente.** Shaan é contraponto sistemático de quem assume que um pipeline "poking at files from outside" vê o quadro completo de um DWG. "missing 80% of the picture because half of what matters lives in dictionaries and reactor relationships." O debate é com a premissa de que automação externa substitui diagnóstico in-process, e a linha que ele traça é a do processo, não a da linguagem: o mesmo Python, hospedado dentro do processo por um plugin, enxerga o que a leitura de fora perde.
- **Quem confunde "unofficially supported" com "officially supported".** Shaan corrige, em público, quem vende ou assume combinação AutoCAD x OS X como suportada quando está no estado "may run just fine but we just don't officially support it". A distinção dos três estados é o contraponto à dissimulação de suporte.
- **Marketing de vendor que promete sem workaround testável.** Shaan não é anti-Autodesk (25+ anos de casa), mas é anti-hype. O registro público dele é feito de número, versão e workaround verificável, não de superlativo. Marcado como leitura de tom a partir do corpus, não como declaração literal dele.
- **Quem trata AUDIT nativo como suficiente em Civil 3D.** Shaan debate, dentro da própria comunidade CAD, quem para o diagnóstico no AUDIT nativo sem caminhar o grafo de referências. Loop invisível de Dref não aparece no AUDIT superficial.

## Estilo de colaboração

Shaan colabora como ponte, não como figura de proa. Constrói a conexão nos dois sentidos: traduz o interno (engenheiro de produto, programa beta, CER) para o usuário final, e traduz o feedback do usuário para o time de produto via My Feedback e CIP. Menciona colegas pelo nome (Heidi Hewett, Shiho Tanaka, Scott Sheppard) em vez de se centrar como fonte única. A estratégia de influência é credibilidade técnica por acesso e por franqueza: tem o acesso interno e publica com honestidade sobre limite.

Voltar ao índice: [[shaan-hurley_01_README]].
