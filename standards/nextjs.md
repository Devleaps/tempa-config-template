---
description: How to build Next.js and TypeScript front ends and Node services
---

# Next.js and TypeScript

Follow the patterns of the repo you are in, and of the team's reference app if it has one, before inventing
new ones.

## Stack

- Next.js 15 (App Router), React 19, TypeScript strict, Tailwind 4, Zod, TanStack Query 5.
- **pnpm** workspaces (with Turborepo in monorepos). Never npm or yarn.
- ESLint flat config (no `any`, `consistent-type-imports`), Prettier, vitest. ESM with `.js` import
  specifiers in Node services.
- Verify with `pnpm lint && pnpm typecheck && pnpm test && pnpm build`.

## Architecture

- **The browser never talks to a backend or third party directly.** It calls a same-origin proxy route that
  injects the user's token server-side; the browser never sees the backend origin or a token. The backend
  (BFF) holds the business rules and authorization.
- **Every capability in the UI is also available through the API** (and the MCP where there is one), and
  the UI only ever calls that API, so the rules live in one place.
- Typed API client: one `request<T>(schema, path)` that Zod-parses every response. A schema mismatch is a
  bug, not something to cast away.
- Modules are framework-agnostic (nothing in a module imports Next) and never import each other; they
  talk through the API and events. Enforce it with ESLint `no-restricted-imports`.
- Detail views are dialogs, not dynamic routes. A second view of one subject is a sub-page.
- Server state lives in TanStack Query: invalidate after mutations; optimistic updates snapshot in
  `onMutate`, roll back in `onError`, invalidate in `onSettled`.
- An action with side effects beyond a status change (a drag that creates a record) asks for confirmation;
  something that cannot be undone is not draggable at all.

## Node services (BFF, MCP)

- Fastify; Zod `safeParse` on body and query (400 on failure); a unique violation (`23505`) is a 409.
- All dependencies injected through one `ServerDeps` object; wiring in `main.ts`, not in modules.
- Every store has an in-memory twin for unit tests, kept in genuine parity, plus real-Postgres tests for
  what the twin cannot model (see `postgres`).
- MCP tools are thin wrappers over the typed client, never Postgres; mirror the API's validation in the
  input schema so a bad argument fails with a useful error.

## UI

- Use the design system components and tokens; never hardcode a colour. Theming is token overrides only,
  painted server-side from a cookie so the first response has the right theme.
- Self-host fonts with `next/font/local`; never `next/font/google` (it downloads on every build and breaks
  releases).
- Layouts work at phone width (navigation becomes a drawer below `md`); side-by-side boards stack.
- Accessible by default: labels on inputs, keyboard navigation, visible focus.

## Security

- Session cookies are HMAC-signed and verified; the app refuses to start in production without the
  session secret.
- Secrets only in server code and environment variables, never in `NEXT_PUBLIC_*`.
- Validate all input on the server with Zod, even when the client already did.
