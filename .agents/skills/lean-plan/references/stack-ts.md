# TypeScript default stack (empty workspace only)

Use this when the workspace has no package.json or starter code. Otherwise follow what exists.

## Layout: feature modules on a pure domain
Folders follow features, so one slice of the plan lives in one place; a small shared domain holds the rules.
```
server/
  src/index.ts                       entry: opens the DB, runs schema.sql, app.listen(Number(process.env.PORT ?? 3000), '0.0.0.0')
  src/app.ts                         composition root: createApp(db, clock) mounts each feature's router; no listen
  src/schema.sql                     idempotent CREATE TABLE IF NOT EXISTS
  src/shared/db.ts                   connection and a transaction helper; no business rules
  src/shared/errors.ts               the one error shape and the error middleware
  src/domain/<topic>.ts              pure business rules: types, rule lists, status transitions
  src/features/<feature>/route.ts    HTTP only: validate with zod, call the service, map errors
  src/features/<feature>/service.ts  one function per use case; owns the transaction; calls domain and repo
  src/features/<feature>/repo.ts     SQL only, parameterized
  test/domain.test.ts                domain rules, no DB
  test/<feature>.test.ts             vitest + supertest against createApp(new DatabaseSync(':memory:'), fakeClock)
public/                              UI, chosen below
test/ui/*.check.mjs                  UI logic checks, run with node --test test/ui/
```

## Dependency direction
- route → service → domain and repo. Nothing imports a route.
- domain/ imports nothing outside domain/: no express, no node:sqlite, no features.
- A feature never imports another feature's route or repo. Logic two features share moves to domain/ (rules) or shared/ (tools).
- The UI reaches the server only through /api.

## Patterns, used where the requirements need them
- Composition root with parameter injection: `createApp(db, clock)`, so tests pass an in-memory DB and a fake clock.
- Repository: repo.ts holds every SQL statement of its feature.
- Service layer: one exported function per use case; the transaction boundary.
- Strategy as a rule list, when there are several business rules: an array of rule functions, each returning a violation code or null. Adding a rule adds one entry.
- State transition table, when an entity has statuses: each status maps to its allowed next statuses, and every change goes through one function.
- One error shape for every failure.

## Principles (SOLID, applied to functions)
- S: one responsibility per file, one feature per folder.
- O: extend through the rule list and the transition table, not by editing their callers.
- L: whatever is passed in (db, clock) can be swapped for the in-memory or fake one; the tests prove it.
- I: a service imports only the repo functions it uses.
- D: dependencies arrive as parameters. No interface file with one implementation, no DI container.

## UI
- One simple page:
  - plain HTML/JS in public/, served by express.static.
  - One process on port 3000.
- Split the UI by feature too: public/app.js (entry), public/api.js (the one fetch helper), public/<feature>.js per screen area, loaded as ES modules.
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
- UI checks live in test/ui/, never in public/ or any folder the server serves.
- Shape (from Object Calisthenics, the parts that help reading):
  - Guard clauses first; at most one level of nesting after them. No else after a return.
  - Don't reach through other modules (a.b().c().d()); call the function that owns the data. Builder chains such as zod and express are fine.
  - No abbreviations (request, count, assignment), except Express's req, res, next.
  - Functions up to 30 lines, files up to 150. Past that, split by responsibility.
- Tests:
  - Each test file creates its own in-memory DB.
  - Test behaviour at the route or service seam.
  - No test re-computes its expected value the way the code does.
