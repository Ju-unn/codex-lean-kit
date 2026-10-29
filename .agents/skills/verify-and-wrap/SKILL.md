---
name: verify-and-wrap
description: Use when about 25 minutes remain, when the work is feature-complete, before claiming anything is done, fixed, or passing, or when preparing submission. Main agent only.
---

# Verify and wrap

Evidence before claims, always.

## The iron law
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```
If you haven't run the verification command in this turn, you cannot claim it passes.

## The gate function (before any status claim)
1. IDENTIFY the command that proves the claim.
2. RUN the full command, fresh.
3. READ the full output: exit code, failure count.
4. VERIFY: does the output confirm the claim?
   - No: state the actual status, with the evidence.
   - Yes: state the claim, with the evidence.

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | test output: 0 failures | an earlier run, "should pass" |
| Type check clean | tsc output: 0 errors | tests passing |
| Server works | started on 0.0.0.0, curl returns the expected body | "it compiled" |
| Bug fixed | the original symptom re-tested and gone | code changed |
| Worker finished | git diff shows the change | the worker said so |
| Requirements met | line-by-line R-n checklist | tests passing |

Red flags:
- "should", "probably", "seems to"
- satisfaction before verification ("Done!")
- trusting a report
- partial checks

## 1. Evidence
Run these now, and record the result lines in docs/worklog.md.
- Type check, full test suite, smoke: start the server on 0.0.0.0, curl the main endpoints, stop it.
- Mark each check PASS, FAIL, or NOT_RUN, with its command. A check that never ran is NOT_RUN, never PASS.
- Requirements: re-read docs/requirements.md. Map every MVP R-n to done, partial, or not done, with its evidence (test, file, or commit).

## 2. Report
Write docs/REPORT.md in Korean, from assets/report-template.md.
- Fill every section. Every claim points to a test, file, or commit that exists.
- Consistency check: each statement matches the code and the git log. Remove stale text and TODOs.
- The task README's required files and format come first.

## 3. Submission check
1. Commit "docs: report".
2. Run $handoff for the final handoff to the next person.
3. Check that the required files from the task README exist and are saved, and that `git status` is clean.
4. Remind the user:
   - Start submitting 10 minutes before the end.
   - The Browser preview check is theirs to do.

## 4. Weak-spot brief
The user reads this; it is not for memorizing.
1. For each core part, write 3 lines: weakness → impact → what to verify next.
2. Ask the user 5 likely follow-up questions, one at a time:
   - Why this structure?
   - What happens when X fails?
   - What was left out, and why?
3. Let them answer in their own words. Correct factual errors only.
4. Include one question with a false premise, and check that they spot it.

Sources: obra/superpowers verification-before-completion (iron law, gate function, claims table); affaan-m/ECC verification-loop; ponytail-debt (shortcuts become stated limits).
