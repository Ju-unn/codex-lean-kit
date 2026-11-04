---
name: ship-check
description: Use when the build has passed $quality-gate and before $verify-and-wrap, when the task README or the stakeholder mentions load, response time, data volume, Docker, containers, or deployment, or when the user asks for a performance test, a speed-up, or a pre-deploy check. Main agent only.
---

# Ship check (performance and pre-deploy)

Show that the app holds up under the load it will meet, and that it starts the same way on another machine, without deploying it. Measure before changing anything, change only what the measurement points at, and measure again the same way.

## What applies
- Performance, sections 1-3: whenever there is a server, or a computation over the data.
- Container, section 4: only when `docker --version` works (see the runtimes line in docs/worklog.md) or the task README asks for Docker. Never install Docker or change its settings.
- Never deploy, push an image, or log in to a registry.

## 1. Targets
- Read them from docs/requirements.md: the load answer from $requirements-interview L3 (people at once, data size, how long they can wait).
- None given: one A-n with your default, shown to the user in one line. Default: 20 requests at once, p95 under 500 ms, 0 errors, on 10 times the provided data.
- Use p95 and the error rate. An average hides the slow requests.

## 2. Measure the baseline
- Data: the provided data, plus a seed script that writes a scaled copy (10 times the rows, or the size the stakeholder gave) to a temporary DB or to out/. Never write over the provided files.
- Load:
  - A tool already installed (autocannon, k6, hey, ab), else a package-free scripts/load.mjs: N concurrent loops against the main read and write endpoints, real IDs from the seed, printing requests, errors, p50, p95, and max.
  - The server runs without watch mode, on another port than the user's preview (for example 3100), with the scaled data.
  - Warm up once, then run 3 times and take the middle result. Same machine, same data, same command every time.
- A CLI or batch job: time the full run on the scaled data, as one plain command.
- After a run with writes, check the data rules still hold: no duplicates, totals match, nothing half-written.
- Log the command and the numbers in docs/worklog.md.

## 3. Improve only what the measurement shows
1. Find where the time goes before changing code:
   - time per handler (a timing log line, removed afterwards)
   - `EXPLAIN QUERY PLAN` on the slow SQL: a SCAN of a big table means a missing index
   - queries per request: more than a few, or one per row, is N+1
   - response size: a list with no limit
2. Fixes, cheapest first:
   - the index that query needs (lean-plan/references/data-model.md)
   - one query instead of a query per row
   - a limit or pages on lists
   - compute once at load or on write instead of on every request
3. One change at a time. $tdd for any behaviour change; the full test suite stays green.
4. Re-measure with the same command. Keep the change only if the number got better; otherwise revert it.
5. Target already met: change nothing, and say so.

## 4. Pre-deploy check (Docker only)
Files at the workspace root:
- Dockerfile:
  - base image pinned to a version (node:22-slim, python:3.12-slim), never latest
  - install from the lockfile (`npm ci`), production dependencies only; copy only what runs
  - runs as a non-root user (`USER node`)
  - CMD in exec form (`CMD ["node", "dist/index.js"]`), so the app gets SIGTERM and stops cleanly
- .dockerignore: node_modules, .git, .env, *.db, docs, out.
- compose.yaml, only when there is more than one service or data that must survive a restart (a volume).
- .env.example listing every setting the app reads. No secrets in the image or in git.

The app:
- reads PORT and the data path from the environment and listens on 0.0.0.0
- answers GET /health with 200 when it and its DB respond, and the container has a HEALTHCHECK on it
- logs to stdout

Check, one plain command per step, and log each result:
1. `docker build -t app-check .`
2. Start it on another host port than the preview (`docker compose up -d`, or `docker run -d -p 3100:3000 app-check`), then curl /health and one main endpoint for the expected body.
3. `docker compose ps` or `docker inspect` shows it healthy.
   - Send one bad request (an unknown ID, broken JSON): it gets a 4xx and the container stays up. A crash here is a Must fix.
4. Data: write one record, stop and start the container, read the record back.
5. Logs: `docker compose logs --tail 20` shows no errors. Note the image size from `docker image ls app-check`.
6. Stop the container at the end. The preview server keeps running.

Docker commands usually need to run outside the sandbox. On "Access is denied" or a daemon pipe error, ask for approval once, with prefix_rule ["docker", "build"] or ["docker", "compose"]. Still failing, or the daemon is not running: NOT_RUN with the error line. Never fix it by changing Docker settings.

## 5. Report
Add to docs/REPORT.md §4, one row each:
- load: command, data size, target, p95 and errors before → after, what changed
- container steps 1-5: PASS, FAIL, or NOT_RUN
In §7 Limits, name what was not measured, such as a real network, several machines, or long runs.

Sources: sickn33/agentic-awesome-skills application-performance-performance-optimization (targets first, baseline, measure, then validate); grafana k6 and agentic-qe performance-testing (p95 thresholds, not averages); a public Docker agent-skill gist and cppalliance/boost-data-collector #228 (pinned image, non-root user, healthcheck, persistence check).
