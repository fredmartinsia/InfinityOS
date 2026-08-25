# Capital Squad 🎯

> **Squad de captação de capital empresarial em Portugal.**
> 7 especialistas portugueses reais + orquestrador para projetos de média e grande dimensão (1M€–25M€).

## 🎯 Objetivo

Levar empresas portuguesas a captar **10M€+** combinando:

- 🏦 **Banco Português de Fomento (BPF)** — linhas de crédito + garantias
- 🇪🇺 **Portugal 2030** — fundo perdido (Compete 2030, programas regionais)
- 🚀 **PRR** — se houver janela aberta
- 💼 **IFD** — capital de risco público
- 📊 **Tax planning lícito** — RFAI, SIFIDE, DLRR, CFEI

## 👥 Equipa

| # | Especialista | Especialidade | Comando |
|---|---|---|---|
| 🎯 | **Capital Chief** *(sintético)* | Orquestrador + Discovery profundo + Consolidação | `/capital-chief` |
| 1 | **Pedro Siza Vieira** | Ex-Ministro Economia — Criador do BPF | `/pedro-siza-vieira` |
| 2 | **Pedro Marques** | Ex-Ministro Planeamento — Arquiteto PT 2020/2030 | `/pedro-marques` |
| 3 | **Pedro Santa Clara** | Catedrático Finance Nova SBE — Engenheiro Financeiro | `/pedro-santa-clara` |
| 4 | **Rogério Fernandes Ferreira** | Founder RFF Advogados — Tax Planning | `/rogerio-fernandes-ferreira` |
| 5 | **Manuel Lopes Rocha** | Direito Societário e Tecnológico | `/manuel-lopes-rocha` |
| 6 | **Ricardo Oliveira (PLMJ)** | Sócio PLMJ — Auxílios de Estado UE | `/ricardo-oliveira` |
| 7 | **Luís Mira Amaral** | Ex-Ministro Indústria + Ex-Presidente BIC — Banca Empresarial | `/luis-mira-amaral` |

**Perfil agregado:** 3 ex-ministros, 1 ex-secretário de Estado, 1 sócio PLMJ top tier, 1 catedrático Nova SBE, 1 fiscalista founder de escritório. Tudo gente que escreveu as regras, executou os programas ou advoga por candidatos.

## 🚀 Como usar

### Opção 1 — Acesso ao orquestrador (recomendado)

```
/capital-chief
```

O Capital Chief executa o protocolo completo:
1. Lê o contexto do cliente (memory + CLAUDE.md)
2. Faz discovery profundo (30-50 perguntas em 6 blocos)
3. Apresenta mapa de elegibilidades
4. Roteia para os 7 especialistas na ordem correta
5. Consolida em escopo final pronto para advogado

### Opção 2 — Acesso direto a especialista

Quando souber exatamente quem deve acionar:

```
/pedro-marques     # mapa de majorações
/pedro-santa-clara # modelagem financeira
/rogerio-fernandes-ferreira  # planeamento fiscal
# etc.
```

## 🗺️ Routing Matrix (referência rápida)

| Pergunta típica | Especialista primário |
|---|---|
| "Que linha BPF se aplica ao meu caso?" | Pedro Siza Vieira |
| "Como aumento a majoração da taxa de incentivo?" | Pedro Marques |
| "Preciso de um modelo financeiro 5 anos" | Pedro Santa Clara |
| "RFAI ou DLRR — qual aplico?" | Rogério Fernandes Ferreira |
| "Holding ou SPV — qual o veículo certo?" | Manuel Lopes Rocha |
| "Tenho risco de notificação à Comissão Europeia?" | Ricardo Oliveira |
| "Qual banco comercial procurar primeiro?" | Luís Mira Amaral |

## 📦 Arquitetura

```
capital-squad/
├── squad.yaml                       # configuração master + routing matrix
├── README.md                        # este ficheiro
└── agents/
    ├── capital-chief.md             # orquestrador sintético
    ├── pedro-siza-vieira.md         # → /Obsidian Vault/CLONES/pedro-siza-vieira/
    ├── pedro-marques.md             # → /Obsidian Vault/CLONES/pedro-marques/
    ├── pedro-santa-clara.md         # → /Obsidian Vault/CLONES/pedro-santa-clara/
    ├── rogerio-fernandes-ferreira.md  # → /Obsidian Vault/CLONES/rogerio-fernandes-ferreira/
    ├── manuel-lopes-rocha.md        # → /Obsidian Vault/CLONES/manuel-lopes-rocha/
    ├── ricardo-oliveira.md          # → /Obsidian Vault/CLONES/ricardo-oliveira/
    └── luis-mira-amaral.md          # → /Obsidian Vault/CLONES/luis-mira-amaral/
```

Cada agente de especialista é uma capa fina que aponta para o clone físico no Obsidian Vault — onde estão os 12 ficheiros de profundidade (psicologia, comunicação, conhecimento, exemplos, etc.).

## ⚠️ Regras Operacionais

- **Idioma:** Português europeu (pt-PT) rigoroso — a candidatura é submetida em Portugal
- **Discovery primeiro:** O Capital Chief não recomenda sem completar os 6 blocos de discovery
- **Sem invenção:** Nenhum especialista inventa dados sobre programas, avisos ou taxas — se não souber, escalonar
- **Sem promessa:** O squad maximiza probabilidades, nunca garante aprovação
- **Memory:** Aprendizados de cada sessão são gravados em `squads/capital-squad/_memory/memories.md` no projeto do cliente

## 📅 Versão

- **v1.0.0** — Criado 2026-05-12 via `/createclone` Squad Mode
- **Próximas versões:** integração de Patrícia Peck (LGPD/RGPD aplicada a candidaturas), adição de tasks reutilizáveis (audit-candidatura, draft-business-plan, etc.)

## 🔗 Referências cruzadas

- **Manuel Lopes Rocha** também existe no `legal-squad` como Risk Auditor — o clone físico agora é partilhado por ambos.
- Para questões puramente de redação contratual após este squad concluir, escalonar para `legal-squad` (`/legal-chief`).
