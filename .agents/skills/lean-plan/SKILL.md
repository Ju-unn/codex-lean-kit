---
name: lean-plan
description: Use when requirements are agreed enough to decide scope, architecture, data model, and the task breakdown, before any implementation code is written. Main agent only.
---

# Lean plan

Write the plan for a worker who has not seen this conversation. Workers write idiomatic code once they know the exact interface and the exact test.

What they cannot know is what you decided. Write those decisions down:
- which files
- which names and signatures
- which values from the requirements
- which tests prove each task

Everything else is theirs to decide. DRY. YAGNI. TDD. A commit per task.

## Output: docs/plan.md, from assets/plan-template.md

### 1. Scope
- MVP: the R-n the success metric depends on, chosen by the stakeholder's priorities. Build these first.
- Later: everything else, with a one-line reason each. Later items come after the MVP passes.

### 2. Architecture: two options, one recommendation
Compare two options against the R-n they serve: cost, risk, what each makes hard. Recommend one.
For each Later item, name the files the chosen option would change to add it. If they spread across unrelated files or layers, revisit the structure. Do not build the extension now.
- Empty workspace: start from references/stack-ts.md.
- Starter code exists: follow it.

### 3. File structure (before tasks)
Map every file that will be created or modified, with its one responsibility.
- Files that change together live together.
- Prefer small, focused files.

### 4. Data model and API
- Data model: tables, keys, and constraints per references/data-model.md, when the task stores data.
- API: method, path, request, response, error codes.
- UI, when the MVP has screens: run $ui-design steps 1-2 now. Put the chosen style, palette, and fonts in the plan, and point every UI task to docs/design-system/<slug>/MASTER.md.

### 5. Global constraints and review focus
- Global constraints: exact values copied from docs/requirements.md (limits, formats, rules), one per line. Every task inherits them.
- Review focus: the 5 inputs or failure modes most likely to hurt a real user that no test covers yet. Typical ones: empty, duplicate, concurrent, boundary time, no permission. Each gets a test in the task that owns the code.

### 6. Tasks: vertical slices
Each task is the smallest unit that carries its own test cycle and is worth a reviewer's gate.
- It is a narrow but complete path through every layer it needs (route → service → repository → test), demoable on its own.
- It is sized for one fresh context. Setup and config fold into the task that needs them.
- It lists the tasks that block it.
- A task that only uses an interface (an API contract, a function signature, a file or table format) is blocked by the task that fixes that interface, not by the tasks that implement it. Then it can run beside them. Example: a UI against the API contract.

Per task:
- Files: create / modify / test, with exact paths.
- Interfaces:
  - consumes: exact signatures from earlier tasks
  - produces: exact names and types that later tasks use
- Tests: test names and assertions, with the exact values from the requirements.
- Steps: write failing test → run (expected FAIL message) → implement the signature → run (expected PASS) → report (the controller commits).
- Role (worker or main), and done-when.

A step lets the implementer write exactly one reasonable thing.
- Lines that decide nothing ("handle edge cases", "add validation") are gaps.
- Function bodies that the signature and the test already determine are a transcript; leave them out.

### 7. Decisions
1-3 entries: context · decision · rejected alternatives · why · revisit if. Routine, reversible choices stay out.

## Self-review (yourself, before showing the user)
1. Coverage: every MVP R-n points to a task.
2. Step scan: no step decides nothing, and no step contains code that the signature and test already determine.
3. Type consistency: names and signatures match across tasks.
4. Review focus: each item has a test in its owning task.
5. Proportion: the plan is shorter than the code it describes.

## Gate
1. Show the user, in at most 15 lines: the scope cut, the two options with your recommendation, and the task list in blocking order. Ask:
   - Is the granularity right?
   - Are the blocking edges right?
   - Should any task merge or split?
2. Wait for approval.
3. Commit "docs: plan".
4. Run $handoff now. This is a planned handoff point; it ends by asking the user to run `/new` and continue from docs/HANDOFF.md.

Sources: obra/superpowers writing-plans (file structure, interfaces, global constraints, review focus, self-review); mattpocock/skills to-tickets (tracer-bullet slices, blocking edges, granularity check); mattpocock ADR format.
