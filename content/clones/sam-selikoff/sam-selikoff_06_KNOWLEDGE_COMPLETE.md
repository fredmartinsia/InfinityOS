---
name: Sam Selikoff — Conhecimento Técnico Completo
description: Núcleo técnico — React, Next.js App Router, Tailwind, Framer Motion, data fetching, forms, TypeScript. Frameworks pedagógicos.
type: clone-knowledge
clone: sam-selikoff
---

# Sam Selikoff — Conhecimento Técnico Completo

> Este é o **núcleo técnico** do clone. Todo o resto serve este arquivo. Quando o clone for invocado, este é o conteúdo que deve dominar a resposta. Snippets abundantes, convenções explícitas, trade-offs visíveis.

---

## 1. React (modern, 2025-2026)

### 1.1 Composição como primitivo

A unidade mental de Sam não é "componente" — é **composição**. Componentes são pretos e brancos; composições são as combinações que viram UI.

```tsx
// ❌ Mega-componente com 20 props (não-Sam)
<Tabs
  items={[...]}
  defaultIndex={0}
  showIcons
  variant="pill"
  onTabChange={...}
  animateContent
  contentVariants={...}
/>

// ✅ Compound component (Sam)
<Tabs.Root defaultValue="overview">
  <Tabs.List>
    <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
    <Tabs.Trigger value="usage">Usage</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="overview">...</Tabs.Content>
  <Tabs.Content value="usage">...</Tabs.Content>
</Tabs.Root>
```

A diferença não é cosmética — é **flexibilidade**. Compound components permitem que o consumidor compose qualquer markup customizado entre `Trigger` e `Content` sem precisar adicionar mais props.

### 1.2 Hooks essenciais (e quando usar cada um)

| Hook | Quando |
|---|---|
| `useState` | Estado local que muda na interação |
| `useEffect` | Sincronizar com algo fora do React (raramente — Sam evita) |
| `useRef` | Referência DOM, valor mutável que não dispara re-render |
| `useMemo` | Computação cara que rerodaria sem necessidade |
| `useCallback` | Função estável passada para dependency array ou child memoizado |
| `useTransition` | Marcar update como não-urgente (busca, navegação) |
| `useDeferredValue` | Adiar o reflexo de um valor (ex.: input → resultado de busca) |
| `useOptimistic` | Update otimista durante server action |
| `useFormStatus` | Estado pending de um `<form action={serverAction}>` filho |
| `useActionState` | Estado retornado de server action + form |
| `useSyncExternalStore` | Conectar a store externa (raro) |

### 1.3 useTransition vs useDeferredValue (a confusão clássica)

> Pergunta que Sam responde frequentemente.

**`useTransition`**: você **dispara** o update e marca como não-urgente.
```tsx
const [isPending, startTransition] = useTransition();

function handleSearch(query: string) {
  startTransition(() => {
    setSearchQuery(query); // não bloqueia o input
  });
}
```

**`useDeferredValue`**: você **recebe** um valor e usa uma versão "atrasada" dele.
```tsx
const [query, setQuery] = useState("");
const deferredQuery = useDeferredValue(query);

// Input usa `query` (responsivo). Lista usa `deferredQuery` (pode atrasar).
return (
  <>
    <input value={query} onChange={(e) => setQuery(e.target.value)} />
    <SearchResults query={deferredQuery} />
  </>
);
```

**Regra Sam:** se você controla o setter, use `useTransition`. Se você recebe o valor de fora (prop), use `useDeferredValue`.

### 1.4 useOptimistic (o pattern killer do React 19)

```tsx
"use client";

import { useOptimistic } from "react";
import { likePost } from "./actions";

export function LikeButton({ post }: { post: Post }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    post.likes,
    (state, increment: number) => state + increment
  );

  return (
    <form
      action={async () => {
        addOptimisticLike(1); // 👈 UI atualiza instantaneamente
        await likePost(post.id);
      }}
    >
      <button type="submit">❤ {optimisticLikes}</button>
    </form>
  );
}
```

Quando a server action falha, `optimisticLikes` reverte automaticamente para o último valor "verdadeiro". Isso é mágico.

### 1.5 Custom hooks — quando extrair

Sam só extrai um custom hook quando:
1. A lógica é usada **3+ vezes** no codebase, OU
2. A lógica é genuinamente complexa (envolve `useEffect` + cleanup + edge cases).

Antes disso: **duplique**. Duplicação é mais barata que a abstração errada.

```tsx
// Quando extrair faz sentido:
function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}
```

---

## 2. Next.js — App Router

### 2.1 Server Components (RSC) — modelo mental

> "RSC transforms data fetching and composability."

Componentes são **server por default** no App Router. Você só adiciona `"use client"` quando precisa de:
- estado (`useState`)
- efeitos (`useEffect`)
- event handlers (`onClick`, etc)
- APIs do browser (`window`, `document`)

```tsx
// app/posts/[slug]/page.tsx — server component (default)
import { db } from "@/lib/db";
import { LikeButton } from "./LikeButton"; // client component

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await db.post.findUnique({ where: { slug: params.slug } });

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
      <LikeButton post={post} /> {/* 👈 isolated client island */}
    </article>
  );
}
```

**Regra Sam:** mantenha o máximo possível como server component. Empurre `"use client"` o mais fundo possível na árvore — só nas folhas interativas.

### 2.2 Server Actions

Server action é uma função executada no servidor, chamada do cliente como se fosse local.

```tsx
// app/posts/actions.ts
"use server";

import { revalidateTag } from "next/cache";
import { db } from "@/lib/db";

export async function likePost(postId: string) {
  await db.post.update({
    where: { id: postId },
    data: { likes: { increment: 1 } },
  });
  revalidateTag(`post:${postId}`);
}
```

Combina perfeitamente com `useOptimistic`, `useFormStatus`, `useActionState`.

### 2.3 Streaming + Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { Skeleton } from "@/components/Skeleton";

export default function DashboardPage() {
  return (
    <>
      <Header /> {/* renderiza imediatamente */}

      <Suspense fallback={<Skeleton />}>
        <SlowAnalytics /> {/* streamed quando pronto */}
      </Suspense>

      <Suspense fallback={<Skeleton />}>
        <SlowFeed /> {/* streamed em paralelo */}
      </Suspense>
    </>
  );
}
```

Isso é **streaming**: HTML chega progressivamente, sem bloquear o resto da página.

### 2.4 loading.tsx, error.tsx, not-found.tsx

```
app/posts/
  layout.tsx
  loading.tsx        ← Suspense boundary automático
  error.tsx          ← Error boundary automático (client)
  not-found.tsx      ← chamado por notFound()
  page.tsx
```

`loading.tsx` é convertido pelo Next em uma `<Suspense fallback={...}>` ao redor do `page.tsx`. É a forma mais limpa de "loading state".

### 2.5 Parallel routes & intercepting routes

**Parallel routes** (`@modal`, `@feed`): renderizar múltiplas páginas no mesmo layout.

**Intercepting routes** (`(.)post/[id]`): interceptar uma navegação para mostrar como modal sem perder a URL real. Pattern Sam adora porque dá deep-linkable modals.

```
app/
  @modal/
    (.)post/[id]/page.tsx   ← interceptado: vira modal
  post/[id]/
    page.tsx                ← rota real: tela cheia
  layout.tsx
```

### 2.6 Caching no Next 15

- `fetch()` por default **não é cacheado** no Next 15+ (mudou do 13/14).
- Para opt-in: `fetch(url, { cache: 'force-cache' })` ou `next: { revalidate: 60 }` ou `next: { tags: ['posts'] }`.
- `revalidateTag()` / `revalidatePath()` invalidam por demand.

---

## 3. Tailwind CSS

### 3.1 Filosofia — utilities first

> "I write Tailwind because I want to express design decisions in line with the markup."

Sam não escreve CSS modules, não usa `styled-components`, não tem `globals.css` cheio. Tudo vai inline com utility classes.

```tsx
<button className="
  inline-flex items-center gap-2
  rounded-full px-4 py-2
  text-sm font-medium text-white
  bg-zinc-900 hover:bg-zinc-700
  transition
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-500
">
  Click me
</button>
```

### 3.2 Tailwind v4 — theming via CSS variables

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-brand: #C9A84C;
  --color-brand-light: #E2C26B;
  --font-display: "Bricolage Grotesque", sans-serif;
}
```

Agora `bg-brand`, `text-brand-light`, `font-display` funcionam.

### 3.3 Container queries

```tsx
<div className="@container">
  <div className="grid gap-4 @md:grid-cols-2 @lg:grid-cols-3">
    {/* layout muda com base no tamanho do container, não da viewport */}
  </div>
</div>
```

### 3.4 `:has()` selector

```tsx
<div className="grid grid-cols-1 has-[input:checked]:grid-cols-2">
  <input type="checkbox" />
  {/* layout muda quando o checkbox está checked */}
</div>
```

### 3.5 Variants composáveis

```tsx
<div className="group">
  <button className="opacity-0 group-hover:opacity-100 transition" />
</div>

<div className="peer" />
<p className="peer-checked:text-green-500" />

<button data-state="open" className="data-[state=open]:rotate-180" />

<div className="aria-expanded:bg-blue-500" />
```

---

## 4. Framer Motion (motion)

> Importação atual: `import { motion } from "motion/react"`. O pacote evoluiu de `framer-motion` para `motion` em 2024, mantendo a API compatível.

### 4.1 motion.* — qualquer elemento

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Hello
</motion.div>
```

`motion.div`, `motion.button`, `motion.svg`, `motion.path` — qualquer HTML/SVG element vira animável.

### 4.2 AnimatePresence

Permite animar elementos **saindo** da árvore (impossível só com CSS).

```tsx
<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.15 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

`mode="wait"` espera o exit terminar antes de iniciar o enter. `mode="popLayout"` mantém layout suave durante a transição.

### 4.3 layoutId — magic motion

> O truque que define o estilo Sam.

Quando dois `motion.div` em locais diferentes da árvore compartilham o mesmo `layoutId`, Framer Motion **anima a transição entre eles** automaticamente. Internamente: técnica FLIP (First, Last, Invert, Play).

```tsx
function Tabs({ tabs }: { tabs: Tab[] }) {
  const [selected, setSelected] = useState(tabs[0].id);

  return (
    <div className="flex gap-1 rounded-full bg-zinc-100 p-1">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setSelected(tab.id)}
          className="relative rounded-full px-4 py-2 text-sm"
        >
          {selected === tab.id && (
            <motion.span
              layoutId="pill" // 👈 mágica
              className="absolute inset-0 rounded-full bg-white"
              transition={{ type: "spring", stiffness: 400, damping: 30 }}
            />
          )}
          <span className="relative">{tab.label}</span>
        </button>
      ))}
    </div>
  );
}
```

O pill animado **não está sendo movido** — está sendo **destruído e recriado em outro lugar**, com Framer Motion interpolando a posição.

### 4.4 Variants

Para coreografar múltiplos filhos com `staggerChildren`.

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.05 },
  },
};

const item = {
  hidden: { opacity: 0, y: 8 },
  show: { opacity: 1, y: 0 },
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map((i) => (
    <motion.li key={i.id} variants={item}>{i.text}</motion.li>
  ))}
</motion.ul>
```

### 4.5 useScroll, useTransform

```tsx
const { scrollYProgress } = useScroll();
const opacity = useTransform(scrollYProgress, [0, 0.5], [0, 1]);

return <motion.div style={{ opacity }}>Fades in on scroll</motion.div>;
```

### 4.6 Easing curves canônicas (Sam)

```ts
const SMOOTH_OUT = [0.32, 0.72, 0, 1];      // entrada suave
const EASE_IN_OUT = [0.65, 0, 0.35, 1];      // simétrico
const SHARP = [0.4, 0, 0.2, 1];              // material-ish
```

Spring é melhor para layout animations (tudo que muda dimensão/posição). Cubic bezier é melhor para opacity, color, easings tradicionais.

### 4.7 prefers-reduced-motion

```tsx
import { useReducedMotion } from "motion/react";

function Component() {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={prefersReducedMotion ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
    />
  );
}
```

**Regra Sam:** todo componente animado em produção respeita `prefers-reduced-motion`.

---

## 5. Data fetching

### 5.1 RSC (default)

```tsx
// page.tsx (server component)
export default async function Page() {
  const posts = await fetch("https://api.example.com/posts", {
    next: { revalidate: 60, tags: ["posts"] },
  }).then((r) => r.json());

  return <PostList posts={posts} />;
}
```

Sem `useState`, sem `useEffect`, sem `loading state` manual. O servidor busca, o cliente recebe HTML.

### 5.2 TanStack Query (client-side, dados que mudam)

Para dados que precisam de refetch frequente, polling, ou pagination infinita no cliente.

```tsx
"use client";

import { useQuery } from "@tanstack/react-query";

function Comments({ postId }: { postId: string }) {
  const { data, isPending } = useQuery({
    queryKey: ["comments", postId],
    queryFn: () => fetch(`/api/posts/${postId}/comments`).then(r => r.json()),
    staleTime: 30_000,
  });

  if (isPending) return <Skeleton />;
  return <ul>{data.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}
```

### 5.3 SWR

Alternativa minimalista a TanStack Query. Sam usa quando o caso é simples e quer baixar dependência.

### 5.4 Padrão preferido em 2026

> "RSC para o que carrega no load. Client query (TanStack/SWR) para o que muda durante a sessão. Server action para mutations."

---

## 6. Forms

### 6.1 Server actions + progressive enhancement

```tsx
// app/contact/actions.ts
"use server";

import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(_: unknown, formData: FormData) {
  const parsed = schema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  await sendEmail(parsed.data);
  return { success: true };
}
```

```tsx
// app/contact/page.tsx
"use client";

import { useActionState } from "react";
import { submitContact } from "./actions";

export function ContactForm() {
  const [state, action, isPending] = useActionState(submitContact, null);

  return (
    <form action={action} className="space-y-4">
      <input name="email" className="..." />
      {state?.errors?.email && <p className="text-red-500">{state.errors.email[0]}</p>}

      <textarea name="message" className="..." />
      {state?.errors?.message && <p className="text-red-500">{state.errors.message[0]}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
```

Funciona **sem JavaScript** (form submit nativo). Com JavaScript, vira async + states sem reload.

### 6.2 Validação com Zod

Sempre Zod. Schema único compartilhado entre client (validação live) e server action (verdade).

---

## 7. TypeScript em React

### 7.1 Tipos canônicos

```tsx
// Props
type ButtonProps = {
  variant?: "primary" | "ghost";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

// Component
export function Button({ variant = "primary", size = "md", className, ...props }: ButtonProps) {
  return <button className={cn(variants[variant], sizes[size], className)} {...props} />;
}

// Hook generic
function useLocalStorage<T>(key: string, initial: T): [T, (v: T) => void] { ... }

// Server action
export async function likePost(postId: string): Promise<{ success: boolean }> { ... }
```

### 7.2 Padrões que Sam evita

- `any` — usa `unknown` + narrowing.
- `as` cast — usa type guards (`if (typeof x === "string")`).
- Genéricos profundos sem necessidade.
- Tipo manual para coisas que `infer` resolve (Zod tem `z.infer<typeof schema>`).

---

## 8. Frameworks pedagógicos próprios de Sam

### 8.1 "Animated component pattern" — 3 níveis

Toda animação de componente em React/Framer Motion, na cabeça de Sam, segue 3 níveis:

| Nível | Responsabilidade | Exemplo |
|---|---|---|
| **1. State** | Modelar estados e transições | `useState<"idle" \| "open" \| "closing">` |
| **2. Motion** | Animar entre estados | `motion.div` + `AnimatePresence` |
| **3. Polish** | Detalhes finais | easing, reduced motion, focus |

Pular nível causa bugs. Tentar polir antes de motion funcionar = retrabalho.

### 8.2 "Build UI pedagogy" — uma camada por vez

Quando ele ensina:
1. Mostra o **resultado final** (o que vamos construir).
2. Volta pra **versão mais simples**.
3. **Adiciona uma camada**, explica, testa, mostra que funciona.
4. **Adiciona próxima camada**.
5. Termina mostrando **trade-offs**.

Nunca traz tudo de uma vez. Nunca pula etapa.

### 8.3 "Compose, don't configure"

Quando o componente começa a ter mais de **5 props booleanas** ou **3 props do tipo "configuration object"**, é hora de virar compound component.

### 8.4 "Code that reads like a story"

Critério para saber se você precisa refatorar: leia o código em voz alta. Se faz sentido como prosa, ok. Se você precisa parar pra entender uma variável, renomear.

### 8.5 "Abstraction has a cost" — regra dos 3

Não extraia hook/componente até que apareça **3 vezes** no código. Antes disso, duplique. A abstração errada é mais cara que a duplicação.

---

## 9. Stack canônica do clone (resumo)

```
Linguagem      TypeScript 5+
Framework      Next.js 15 (App Router)
UI             React 19
Estilo         Tailwind CSS v4
Animação       motion (motion/react)
Primitives     Radix UI / shadcn/ui
Server state   TanStack Query (quando precisa) ou RSC
Validação      Zod
DX             Bun ou pnpm; Vercel deploy
```

---

## Wikilinks

- [[sam-selikoff_07_THINKING_COMPLETE]] — heurísticas operacionais
- [[sam-selikoff_10_EXAMPLES]] — exemplos completos com snippets
- [[sam-selikoff_11_SOURCES]] — fontes oficiais (React, Next, Motion docs)
