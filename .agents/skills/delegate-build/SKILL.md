---
name: delegate-build
description: Use when implementing the tasks in docs/plan.md, handing a task to a worker subagent, handling a worker's report, or running the per-task review and fix loop. Main agent only.
---

# Delegate and build (subagent-driven)

You are the controller:
- A fresh worker implements one task and commits it.
- You verify the result yourself.
- A fresh reviewer checks risky tasks.
- Fixes go back to the same worker.

Never pass on a report you have not checked.

## Before the first task
1. Install dependencies yourself, once. The user approves network access.
2. Run the test command, so every worker starts from a working setup.

## The task loop
Take tasks one at a time, in plan order. The next task starts only after this one is complete.

1. **Choose who builds it.**
   - Main: 2 files or fewer and a few dozen lines, or tightly coupled to details you just wrote. Follow $tdd yourself.
   - Worker: everything else.
2. **Dispatch.**
   - Record the task base: `git rev-parse --short HEAD`.
   - Fill references/brief-template.md. Point to docs paths; never paste documents.
   - `spawn_agent` with task_name "t<n>", agent_type "worker", fork_turns "none", message = the brief.
   - The role pins model and effort, so pass neither. Without roles, spawn as AGENTS.md Subagents says.
3. **While it runs.**
   - Integrate finished work or update docs.
   - If you are idle, call `wait_agent` in 5-10 minute stretches.
   - Suggest the user spends the wait on follow-up stakeholder questions.
   - A worker's approval request (for example, git commit) appears in the main screen for the user to approve.
4. **Handle the report by status.**
   - DONE: go to step 5.
   - DONE_WITH_CONCERNS: read the concerns first. Resolve doubts about correctness before the review.
   - NEEDS_CONTEXT: answer from the docs, or ask the user, then send it with `followup_task`.
   - BLOCKED: find the cause.
     - Missing context: provide it.
     - Task too big: split it in docs/plan.md.
     - Plan wrong: tell the user.
     - Never re-send the same task unchanged.
5. **Verify it yourself.**
   - `git log --oneline <base>..HEAD` and `git diff --stat <base>..HEAD`.
   - Read the diff.
   - Run the task's tests and the full suite.
   - Check the TDD evidence in the report: RED, then GREEN.
6. **Task review.** It applies when the task touches domain rules, data writes, input handling, auth, or money.
   - `spawn_agent` with task_name "r<n>", agent_type "reviewer", fork_turns "none".
   - Message: references/task-review-template.md, filled.
   - For any other task, your step 5 is the review.
7. **Fix loop.**
   - Send Critical and Important findings to the same worker with `followup_task`.
   - The worker fixes, re-runs the covering tests, commits, and reports.
   - Re-review only the fix diff.
   - After 3 rounds on one task, stop and decide with the user: split, simplify, or move to Later.
8. **Complete the task.**
   - Give the user a 3-line walkthrough: what changed · why this way · one risk.
   - Tick the task in docs/plan.md.
   - Add one line to docs/worklog.md: T-n, commits, test count, review verdict.
   - Check `date`. Once the build phase has ended (AGENTS.md, scaled), start no new task and name $quality-gate as the next step.

## Failures and surprises
- A failing test or unexpected behaviour: use $debugging before any fix.
- A new requirement from the stakeholder:
  1. Add an R-n to docs/requirements.md first.
  2. If MVP-critical, add a new T-n; otherwise put it under Later.
  3. Tell the user the time cost.
- Every MVP task passes before minute 125 (of 180, scaled): take Later items one at a time, through the same loop.

## Parallel workers
At most 2 at once, and only when the two tasks share no files and neither consumes the other's interfaces.

## Fallback
If spawn_agent offers no agent_type, the roles are not loaded: dispatch and review as above, spawning as AGENTS.md Subagents says.
If spawn_agent does not exist:
1. Build each task yourself with $tdd.
2. Review your own diff with references/task-review-template.md.
3. Then commit.

Sources: obra/superpowers subagent-driven-development (task loop, status handling, task review) and codex-tools (fresh context, waiting); mattpocock/skills implement-spec (context pointers).
