# TypeScript default stack (empty workspace only)

Use this when the workspace has no package.json or starter code. Otherwise follow what exists.

## Layout
```
server/
  src/app.ts         createApp(db) returns the express app; no listen, so tests import it
  src/index.ts       opens the DB, runs schema.sql, app.listen(Number(process.env.PORT ?? 3000), '0.0.0.0')
  src/routes/*.ts    HTTP only: validate input, call a service, map errors
  src/services/*.ts  domain rules (unit-tested)
  src/repos/*.ts     SQL only, parameterized
  src/schema.sql     idempotent CREATE TABLE IF NOT EXISTS
  test/*.test.ts     vitest + supertest against createApp(new DatabaseSync(':memory:'))
public/ or web/      UI, chosen below
```

## UI
- One simple page:
  - plain HTML/JS in public/, served by express.static.
  - One process on port 3000.
- Several screens or client state:
  - Vite + React in web/.
  - The user still opens port 3000, so Vite takes it and the API moves to 3001 (`PORT=3001`).
  - In vite.config: `server: { host: '0.0.0.0', port: 3000, strictPort: true, allowedHosts: ['.e2b.app', '.e2b.dev'], proxy: { '/api': 'http://localhost:3001' } }`
  - Without allowedHosts, Vite 6+ rejects the preview hostname with "Blocked request. This host is not allowed."
- Every screen:
  - shows empty, loading, and error states
  - labels things in the user's language
  - makes the one primary action obvious
  - follows docs/design-system/<slug>/MASTER.md from $ui-design
  - Graders take screenshots.

## Packages
The main agent installs them once.
- server: express, zod
- dev: typescript, tsx, vitest, supertest, @types/node, @types/express, @types/supertest
- DB:
  - `node:sqlite` DatabaseSync when `node --version` is 22.13 or later (no dependency; verified under vitest 5).
  - Otherwise better-sqlite3.

## Scripts
`"dev": "tsx watch src/index.ts"`, `"test": "vitest run"`, `"typecheck": "tsc --noEmit"`

## Code rules
- Strict TypeScript; no `any`.
- Validate once at the route boundary with zod; trust the types after that.
- One error shape `{ error: { code, message } }` and one error middleware. Responses never include stack traces or SQL.
- Names use the domain nouns from docs/requirements.md.
- Comments: one Korean line above every function saying what it does; any other comment says why.
- Formatting: one statement per line, lines under 120 characters. Never minify or squash HTML, CSS, or JS onto long lines.
- UI checks (node --test) live in test/, never in public/ or any folder the server serves.
- Tests:
  - Each test file creates its own in-memory DB.
  - Test behaviour at the route or service seam.
  - No test re-computes its expected value the way the code does.
