---
name: handoff
description: Use when the plan has just been approved, when wrapping up, before /compact or /new, or when the conversation is getting long. Main agent only.
---

# Handoff

Another session or another person must be able to continue from files alone, without this conversation.

## Planned points
- After plan approval:
  1. Write the handoff.
  2. The user runs `/new` and starts the build with "docs/HANDOFF.md를 읽고 이어서 진행해." AGENTS.md also makes a new session read the handoff first.
  3. The build then runs on a clean context.
- At wrap: write the final handoff for the person who maintains this next.
- Any other time: before `/compact`, or when the conversation is getting long.

## Write docs/HANDOFF.md
Replace the file each time. Korean, 30 lines at most.

For the next session:
- Read first: the files the next step needs, in order. Usually docs/requirements.md (Agreement, R-n), docs/plan.md (next T-n, Global constraints), and the docs/qna.md entries those R-n cite, for exact values.
- Phase and the time from `date`
- Done: the latest commits (short hash + subject)
- In progress: T-n, who is on it, its state
- Next 3 steps, and the skill to use next
- Open questions for the stakeholder or the user
- Server: the start command, and whether it is running now

For the next person:
- How to run and test: the exact commands
- Code map: the 3-5 files that matter and what each does
- Known risks and limits; point to docs/REPORT.md once it exists
- Where decisions live: docs/plan.md Decisions

Point to requirements.md, plan.md, and commits instead of copying them.

## Before writing
- If a subagent is still running, wait for it and verify its result. Never hand off in the middle of a task.
- Drift check: re-read the Agreement block in docs/requirements.md. If the work has drifted from it, tell the user in one line and record the decision.

## Then
1. Commit "docs: handoff".
2. Tell the user in one line that docs/HANDOFF.md was written.
3. After plan approval, end the turn with: "/new를 입력한 뒤 `이어서 할게`라고 보내 주세요." Start no build work in this session, even if the user says 진행해. Only "/new 없이 계속" overrides this.
4. Any other point: name the next command, `/new` or `/compact`.
