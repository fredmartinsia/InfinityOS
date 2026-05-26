# Task: build-interactive-form

> Construir formulário multi-step ou pesquisa com transições, validação animada e a11y. Estilo Typeform mas com a alma do design system.

## Quando usar

- Pesquisa / quiz / questionário (3+ perguntas)
- Onboarding multi-step
- Formulário de captação rico (não só email + nome)
- Configurador de produto (escolha A → B → C → resultado)

## Quando NÃO usar

- Form de 1-2 campos → embute na LP direto
- Tabela de edição (mais de 1 ao mesmo tempo) → use `*build-saas-interface`

## Pré-requisitos

1. Design system com componentes de input, button, error states.
2. Lista de perguntas / steps com tipos (texto, single-choice, multi-choice, slider, date, file upload, etc.).
3. Lógica condicional (se houver ramificação).
4. Backend / endpoint de submissão.

## Workflow (3 etapas)

### Etapa 1 — Emil Kowalski: Animação entre steps + estados de input

**Input:** lista de perguntas + tokens.
**O que faz:**
- Transição entre steps (slide horizontal? fade? layout id?)
- Animação de entrada de cada input (stagger sutil)
- Validação inline animada (erro aparece com motion, não com layout shift)
- Success state animado quando submete
- Progress indicator com animação
**Saída:** `components/StepTransition.tsx` + `components/AnimatedInput.tsx`

### Etapa 2 — Sam Selikoff: Implementação React/Next.js

**Input:** etapa 1.
**O que faz:**
- Estrutura de form com React Hook Form (ou Zod + estado simples)
- Server action para submit
- Optimistic update no progress bar
- Persistência local (localStorage) para evitar perda em refresh
- Lógica condicional (next step depende de answer)
- Validação Zod compartilhada client + server
**Saída:** form rodando com lógica completa

### Etapa 3 — Josh Comeau: A11y crítico em formulários

**Input:** form rodando.
**O que faz:**
- Labels associados corretamente (htmlFor)
- Error messages anunciados em ARIA live
- Focus management entre steps (foco vai pro primeiro input do step novo)
- Keyboard nav: Enter avança, Esc volta, Tab funciona em ordem visual
- prefers-reduced-motion para usuários sensíveis
- Contraste em todos os estados
- Mensagens de erro descritivas (não só "Erro")
**Saída:** form final + `report-a11y.md`

## Entrega

```
squads/frontend-squad/output/{slug}/
├── README.md
├── app/
│   └── form/page.tsx
├── components/
│   ├── Form.tsx (orquestrador de steps)
│   ├── Step.tsx (wrapper com transition)
│   ├── inputs/ (Text, Choice, Slider, Date, File...)
│   ├── ProgressIndicator.tsx
│   └── SuccessState.tsx
├── lib/
│   ├── schema.ts (Zod)
│   ├── steps-config.ts (lista de perguntas)
│   └── submit.ts (server action)
└── report.md
```

## Checkpoints

- **Após etapa 1** — usuário aprova animação entre steps
- **Antes da entrega** — checklists passam

## Critérios de aceite

- Cada step transita em < 400ms
- Validação inline: erro aparece em < 100ms após blur ou submit attempt
- Persistência funciona (recarregue a página, dados estão lá)
- A11y: keyboard completo + screen reader friendly
- Mobile: input não causa zoom (font-size ≥ 16px)
- Submit final com feedback claro (loading → success ou error)

## Anti-padrões

- Botão "Próximo" sem estado disabled antes de validar
- Step que desaparece sem feedback visual
- Erro que desloca conteúdo (CLS)
- Auto-advance no single-choice sem confirmação (causa miss-clicks)
- localStorage sem expiração (form de 6 meses atrás aparece sozinho)
- Input sem label (placeholder ≠ label)
