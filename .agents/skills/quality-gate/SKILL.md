---
name: quality-gate
description: Use when the MVP works end to end and the whole change needs a final review for spec coverage, code quality, security, data model, and over-engineering before wrap-up, or when the user asks for a review. Main agent only.
---

# Quality gate (final review)

Two fresh reviewers check the whole change along separate axes, so one axis cannot mask the other:
- Code that follows good standards can still implement the wrong thing.
- Code that does exactly what was asked can still be unsafe.

## Run
1. Pin the fixed point.
   - Commit everything.
   - The fixed point is `baseline`.
   - `git diff --stat baseline...HEAD` must be non-empty. A bad ref or an empty diff fails here, not inside the reviewers.
2. Spawn both reviewers in parallel, each with agent_type "reviewer" and fork_turns "none":
   - task_name "spec", message: the request in references/review-spec.md
   - task_name "quality", message: the request in references/review-quality.md
3. Present both reports, verbatim and lightly cleaned, under "Spec" and "Quality" headings.
   - Don't merge or re-rank findings across the two axes.
   - End with one line per axis: number of findings and the worst one.
4. Triage with the user, in 10 lines at most:
   - Must: fix now through $delegate-build (test first).
   - Should and Nice: list under Limits in docs/REPORT.md. A trivial fix may be done now.
5. Re-run the full suite and commit "fix: gate findings".

## Fallback
If spawn_agent offers no agent_type, spawn both reviewers as AGENTS.md Subagents says (reviewer: gpt-6.1-sol, high).
If spawn_agent does not exist, apply both requests yourself, one after the other, with the same output formats.

Sources: mattpocock/skills code-review (two axes, fixed point, smell baseline); ponytail-review (priorities, concrete cases, output); obra/superpowers final whole-branch review; cloudflare security-audit (checker separate from author); affaan-m/ECC reviewer checklists.
