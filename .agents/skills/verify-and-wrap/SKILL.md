---
name: verify-and-wrap
description: Use when the work is feature-complete, before claiming anything is done, fixed, or passing, or when preparing submission. Main agent only.
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
| Server works | running on 0.0.0.0 at the app's port, curl returns the expected body | "it compiled" |
| Bug fixed | the original symptom re-tested and gone | code changed |
| Worker finished | git diff shows the change | the worker said so |
| Requirements met | line-by-line R-n checklist | tests passing |
| Numbers correct | recomputed by a second method, one case checked by hand ($data-check) | the code ran |

Red flags:
- "should", "probably", "seems to"
- satisfaction before verification ("Done!")
- trusting a report
- partial checks

## 1. Evidence
Run these now, and record the result lines in docs/worklog.md.
- Type check, full test suite, smoke: make sure the server is up as AGENTS.md says, curl the main endpoints, and leave it running for the user's preview.
- Mark each check PASS, FAIL, or NOT_RUN, with its command. A check that never ran is NOT_RUN, never PASS.
- Requirements: re-read docs/requirements.md. Map every MVP R-n to done, partial, or not done, with its evidence (test, file, or commit).

## 2. Report
Write docs/REPORT.md in Korean, from assets/report-template.md.
- Fill every section. Every claim points to a test, file, or commit that exists.
- Consistency check: each statement matches the code and the git log. Remove stale text and TODOs.
- docs/requirements.md: every R-n has a final MVP value (yes, no, or later); no 후보, 대기, 미확정, or 승인 대기 remains; the Agreement header says whether the stakeholder confirmed it.
- The task README's required files and format come first.

## 3. Submission check
1. Commit "docs: report".
2. Run $handoff for the final handoff to the next person.
3. Check that the required files from the task README exist and are saved, and that `git status` is clean.
4. Draft the result message the user sends to the stakeholder: one copyable block, at most 5 lines of plain Korean without system words. What was built, how to open and use it, the limits they must know, the next step.
5. Remind the user:
   - The server stays running; they check the main screen in the preview themselves.

## 4. Weak-spot brief
The user reads this; it is not for memorizing.
1. Flow map, 5 lines at most: input → processing → output for the main use case, naming the files and functions on the way.
2. Decisions the user changed: 2-3 cases from docs/qna.md [결정] entries and docs/plan.md Decisions, each as "AI proposed → the user chose → why". Use only cases in the record; never invent one.
3. For each core part, write 3 lines: weakness → impact → what to verify next.
4. Ask the user 6 likely follow-up questions, one at a time, as in the exam. Give one of them a false premise, a feature or rule the code does not have, and check that they spot it.
   - Why this structure?
   - How do you know the core feature works? Which test or recompute shows it?
   - What happens when X fails, or when two users change the same record at once?
   - What was left out, and why?
   - Which AI suggestion did you change or reject, and why?
   - How would you add one Later item, and which files change?
5. Let them answer in their own words. Correct factual errors only.

Sources: obra/superpowers verification-before-completion (iron law, gate function, claims table); affaan-m/ECC verification-loop; ponytail-debt (shortcuts become stated limits).
