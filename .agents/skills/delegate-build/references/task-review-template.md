# Task review request (the spawn message for a reviewer)

```
Review T-n. First check whether it matches its requirements, then whether it is well built.
This is a task-scoped gate. The whole-change review happens later.

What was requested: docs/plan.md (T-n section, Global Constraints), docs/requirements.md (R-n),
and the worker brief:
<brief>

What the worker claims (unverified):
<worker report>

Diff under review: base <SHA>, head <SHA>.
Run once: git diff --stat <base>..<head> and git diff <base>..<head>.
Inspect code outside the diff only to check a concrete risk you name. Example: a changed contract → check its callers.

Do not trust the report. A stated rationale ("kept it simple on purpose") never lowers a finding's severity.
Do not re-run the full suite. Run one focused test only when the code raises a specific doubt.
Warnings or noise in the reported test output are findings.

Part 1, spec compliance:
- Missing: requirements skipped, or claimed without being implemented
- Extra: features not requested, over-engineering
- Misunderstood: the right feature built the wrong way
- Cannot verify from this diff: name it, and say what the controller should check

Part 2, code quality:
- Separation of concerns, error handling, no duplicated logic, edge cases
- Tests: verify real behaviour with independent expected values; cover the task's edge cases
- Structure: each file has one clear responsibility and follows the plan's file structure
- Security: validation at the boundary, parameterized SQL, access checks, no secrets

Calibration:
- Critical: wrong result, data loss, security hole.
- Important: the task can't be trusted until fixed (missed requirement, fragile behaviour, swallowed errors, tests that assert nothing).
- Minor: polish.
Every finding gives file:line, what is wrong, why it matters, and how to fix it.

Output, starting directly with the verdict:
Spec: ✅ compliant | ❌ issues (file:line) · ⚠️ cannot verify: …
Strengths: one line
Issues: Critical / Important / Minor
Verdict: Approved | Needs fixes
```

Source: obra/superpowers subagent-driven-development, task-reviewer-prompt.
