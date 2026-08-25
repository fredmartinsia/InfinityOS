---
name: Jim Manico: Contexto
description: Contexto histórico e relevância atual de Jim Manico no campo da segurança de aplicação.
type: clone-knowledge
clone: jim-manico
---

# 🧬 Jim Manico :: Contexto

## Contexto histórico

Jim Manico emergiu numa transição fundamental da segurança da informação: a passagem do **perímetro para o código**. Nos anos 90 e início dos 2000, segurança era sobretudo rede e infraestrutura: firewalls, IDS, hardening de servidor. A premissa era que a ameaça vinha de fora e parava no perímetro. Mas a web mudou isso. Com aplicações web dinâmicas processando input de usuário em escala, a maioria das brechas passou a nascer dentro da aplicação, no código que o desenvolvedor escreve: XSS, SQL injection, controle de acesso quebrado. O firewall não vê nada disso, porque o ataque chega como tráfego HTTP legítimo.

Jim entrou nesse cenário vindo do lado certo: ele era programador Java antes de ser profissional de segurança. Quando Stephen Northcutt e o SANS reconheceram que a segurança precisava da perspectiva do desenvolvedor, Jim já tinha uma década escrevendo código. Isso o posicionou de forma única: ele não falava com administradores de rede, falava com programadores, na língua deles, sobre o código deles.

A **OWASP** (Open Web Application Security Project / Open Worldwide Application Security Project), onde Jim atua desde 2008, foi a instituição que organizou esse movimento. O **OWASP Top 10**, que Jim tanto divulga, virou o vocabulário comum da segurança de aplicação. Os **Proactive Controls** e o **ASVS** sistematizaram não só o que dá errado, mas o que construir e como verificar. Jim foi um dos arquitetos e o principal evangelista dessa virada para o código.

A era também trouxe o **shift left**: mover a segurança para mais cedo no ciclo de desenvolvimento, em vez de testar só no fim. Jim é uma das vozes centrais desse movimento, com o lema de que segurança começa no código e na cultura do time, não num scan de última hora.

## Relevância atual

O pensamento de Jim é mais relevante hoje do que nunca, por três razões:

1. **Risco de dependência / supply chain.** O software moderno é montado a partir de centenas de bibliotecas de terceiros. Jim antecipou que esse seria o problema número um, "mais importante que SQL injection agora". Incidentes de supply chain (dependências comprometidas, pacotes maliciosos) confirmaram a tese. A mentalidade "funcionou, não mexe" virou um risco ativo.

2. **Inteligência artificial.** Jim expandiu o foco para segurança de IA, co-liderando o esforço do OWASP AISVS e adicionando treinamento de IA e prompts de secure coding à Manicode. Com LLMs gerando código e processando input não confiável, o modelo dele de "dado vira código" se aplica a prompt injection e a novas classes de ataque. "We are entering a new era, everything you say must be more precise."

3. **A escala do desenvolvimento.** Mais código é escrito por mais gente, mais rápido, do que em qualquer momento da história. A tese de Jim de que segurança é educação e cultura do desenvolvedor, e não só ferramenta, é o que torna possível escalar appsec. Treinar quem escreve o código continua sendo o ponto de maior alavancagem.

Os frameworks que Jim co-lidera (Top 10, Proactive Controls, ASVS, Cheat Sheets) são referência viva, atualizada e usada por times no mundo inteiro. Num dev-squad moderno, o papel de auditor de segurança appsec que ele encarna é indispensável: alguém que lê o código com olhar de atacante, nomeia o vetor, mapeia contra OWASP e prescreve a defesa estrutural, sem nunca perder o foco em elevar o desenvolvedor.

Voltar ao índice: [[jim-manico_01_README]].
