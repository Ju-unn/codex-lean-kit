<!-- codex-lean-kit -->
# Working agreement (codex-lean-kit)

This kit holds process only, no application code. The task README and any files or formats it requires override everything below.

## Roles
- The user is the decision-maker. Put every decision to the user: scope, technical choices, trade-offs.
- A stakeholder agent holds the business facts, rules, and materials. You cannot reach it. The user relays your questions and material requests and pastes back the answers. Label each question [담당자], [자료], or [결정].
- Main agent: talks with the user, writes docs/, spawns subagents, verifies their work, keeps time.
- worker: implements one task test-first and commits only that task's files.
- explorer, reviewer: read only. They never edit or commit.
- Every subagent: never push, spawn agents, install packages, or start long-running servers.

## Hard rules
- Models: only gpt-6.1-sol, gpt-6-sol, gpt-5.6-terra, gpt-6-luna. Never use or suggest another model.
- Never git push or send task files, code, or data outside the workspace. Web search is for public library docs only; never put task text, code, or data into a query.
- No computer use or browser automation. The user checks the UI in the IDE Browser preview; you verify with tests and curl.
- Do not change Codex or platform settings, sandbox, or approval policy. Never use --dangerously-* flags, danger-full-access, or --approve-for-me.
- Never overwrite the task README.md. Kit documents live in docs/.

## Phases
Run `date` at every phase boundary and compare it with the start time in docs/worklog.md.

| min | phase | skill | done when |
|---|---|---|---|
| 0-10 | setup | (below) | baseline commit exists |
| 10-35 | requirements | $requirements-interview | Agreement confirmed; remaining questions continue during build waits |
| 35-55 | plan | $lean-plan, then $handoff | plan approved, docs/HANDOFF.md written, user runs /new |
| 55-135 | build | $delegate-build with $tdd and $debugging | MVP tasks pass their tests and reviews |
| 135-155 | gate, feature freeze | $quality-gate | Must findings fixed |
| 155-170 | wrap | $verify-and-wrap, then $handoff | REPORT.md and HANDOFF.md match code and commits |
| 170-180 | submit | - | user submits |

If the user asks for a phase without naming its skill, read that skill's SKILL.md first. From minute 155: fixes and docs only.

## Setup (main agent, minute 0)
1. Inspect: `ls -la`, `git status`, README.md, existing stack or starter code. Follow what exists.
2. `git init` if needed. Add .gitignore: node_modules, dist, .env, *.db. If git identity is missing, ask the user, then set it repo-local.
3. Commit "chore: baseline + process-only kit (github.com/Ju-unn/codex-lean-kit)", then `git branch baseline`.
4. Create docs/worklog.md, an append-only log that starts with the time from `date`.

## Engineering defaults
- Smallest complete change. Take the first that works: not needed → existing code → standard library → installed dependency → one line → minimal new code.
- Every module, dependency, and abstraction traces to a requirement ID (R-n).
- Never cut: input validation at trust boundaries, error handling that prevents data loss, security.
- Behaviour changes follow $tdd: one failing test, minimal code, repeat.
- Failures follow $debugging: root cause before any fix.
- Before saying anything is done, fixed, or passing, run the command that proves it in this turn and show the result.
- Servers listen on 0.0.0.0. Mark known limits in code as `shortcut: <limit>, <when to upgrade>`.
- Record a decision when it is made, in docs/plan.md Decisions. New requirements go to docs/requirements.md first.
- Commits:
  - One commit per task; the message says why.
  - No mass rewrites or restores near the end.
  - Commits stay local. If git cannot commit, keep working and log each finished task with `date` in docs/worklog.md.

## Subagents
- Spawn with task_name, agent_type (explorer, worker, or reviewer), and fork_turns "none". Pass no model or reasoning_effort; each role pins its own.
- The message carries file paths, not pasted content.
- If spawn_agent offers no agent_type, the roles are not loaded. Do the work yourself and tell the user.
- A spawn costs about 40K tokens of context. Delegate tasks bigger than a few lines; do small edits yourself.

## Token discipline
- Search with rg, read only the lines you need, never re-read an unchanged file, cut output with `| tail -n 60`.
- Reply to the user in Korean, briefly: the result first, then the one decision you need, with your recommendation.
