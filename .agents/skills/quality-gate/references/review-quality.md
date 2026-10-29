# Quality review request (the spawn message for task_name "quality")

```
Review the whole change like the developer who will be paged when it breaks.
Order of importance: correct, safe, holds under the expected load, tested, fast, lean.

Scope: git diff baseline...HEAD -- . ':!*lock*'
Read the diff, then the code it touches: callers of every changed function, the functions it calls, the tests.
Trace the real flow: where data comes in, what is stored, what goes out.
Judge load against docs/requirements.md (number of users, data size), and say which load you assumed.

Read and apply these checklists:
- .agents/skills/quality-gate/references/security.md
- .agents/skills/lean-plan/references/data-model.md
- .agents/skills/quality-gate/references/overengineering.md

Look for, in this order:
1. Bug: wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones), a caller broken by the change, a fix applied in one caller while the shared function stays broken.
2. Risk: security holes (injection, missing input checks, missing access checks, secrets), data loss (errors swallowed, writes in the wrong order, no transaction).
3. Load: check-then-write races, a query per item, lists that only grow, per-process state that must be shared.
4. Missing test: risky logic (a branch, a parser, money, security, data writes, a bug fix) with no test that fails when it breaks. One good test, not coverage.
5. Speed: only big slowdowns. Small wins are suggestions.
6. Lean: dead code, unused options, speculative features, a dependency for a few lines, abstraction with one implementation, near-copies that must change together, one function doing unrelated jobs.

Smell baseline. These are judgment calls, never hard violations; name the smell and quote the hunk:
- Mysterious Name: a name doesn't reveal what it does or holds. Rename it.
- Duplicated Code: the same logic in more than one place. Extract it.
- Feature Envy: a function reaches into another object's data more than its own. Move it.
- Data Clumps: the same fields keep travelling together. Give them a small type.
- Repeated Switches: the same if/switch cascade in several places. Use one map.
- Shotgun Surgery: one change forces scattered edits. Gather it into one module.
- Divergent Change: one module edited for unrelated reasons. Split it.
- Speculative Generality: hooks, parameters, or abstractions with no current need. Delete them.
- Message Chains: long a.b().c().d() navigation. Hide it behind one function.
- Middle Man: a layer that only delegates. Cut it.

Before you report:
- Every finding needs a concrete case: this input or situation leads to this wrong result. No case, no finding.
- Re-read the lines and confirm: the caller exists, the value can really be empty, the code really is unused.
- A `shortcut:` comment that names its limit is a decision, not a finding, unless the expected load already crosses it.
- Report only what you are more than 80% sure of. Merge duplicates. No style taste, no "consider", no vague worries.
- Propose the smallest fix that works, and prefer fixes that delete code.

Output, in plain words:
What this change does: 2-3 sentences.
Then the findings, numbered across all groups:
- Must fix: bug, security hole, data loss, breaks at the expected load
- Should fix: risky code without a test, duplication, mixed responsibilities, code that should not exist
- Nice to have: small speed-ups, shorter forms
Each finding: **title** (file:line) · What this is · Problem (the concrete case) · Fix · If we skip it.
End with:
- Verdict: ship | Verdict: fix <numbers> first
- Not checked: <one line, if something mattered and you could not check it>
```
