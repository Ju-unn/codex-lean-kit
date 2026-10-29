---
name: debugging
description: Use when a test fails, a bug appears, the server or build errors, or behaviour is unexpected, before proposing any fix.
---

# Systematic debugging

Find the root cause before attempting any fix. Symptom fixes are failure.

## The iron law
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```
If Phase 1 is not done, do not propose a fix.

Use this especially when:
- you are under time pressure
- "one quick fix" looks obvious
- a fix already failed
- you don't fully understand the issue

Systematic is faster than guess-and-check thrashing.

## Phase 1: Root cause investigation
1. Read the error completely: message, stack trace, file:line, codes. It often contains the answer.
2. Reproduce reliably. What is the exact command or request? Does it fail every time? If not, gather more data; don't guess.
3. Check recent changes: `git diff`, the last commits, new dependencies, config, env.
4. Multi-layer systems (HTTP → route → service → repository → DB):
   - Log what enters and leaves each boundary.
   - Run once to see WHERE it breaks.
   - Then investigate that layer.
5. Trace the data flow backwards: where does the bad value originate, and who called with it? Fix at the source, not where it surfaces.

## Phase 2: Pattern analysis
1. Find similar working code in this codebase.
2. If you are following a reference (docs, an example), read it completely. Don't skim.
3. List every difference between working and broken, however small. Don't assume "that can't matter".
4. Note the dependencies: config, env, data, assumptions.

## Phase 3: Hypothesis and test
1. Write down one hypothesis: "X is the root cause because Y."
2. Test it with the smallest possible change, one variable at a time.
3. It worked: go to Phase 4. It didn't: form a new hypothesis. Never stack fixes.
4. You don't know: say "I don't understand X" and gather more evidence.

## Phase 4: Implementation
1. Write a failing test that reproduces the bug (follow $tdd).
2. Make one fix at the root cause. No "while I'm here" changes, no bundled refactoring.
3. Verify: the test passes, the full suite passes, the original symptom is gone.
4. If the fix didn't work, stop and count the attempts.
   - Fewer than 3: go back to Phase 1 with the new information.
   - 3 or more: stop and question the architecture with the user before attempt 4.
   - Signs of an architecture problem: each fix reveals a new problem elsewhere, fixes need large refactoring, or fixes create new symptoms.

## Before editing, tell the user
- the cause found
- what stays unchanged
- the change scope (files)
- the test that will prove the fix

## Record
Write one line in docs/worklog.md: `failure → root cause → fix → test that proves it`.

## Red flags: return to Phase 1
"Quick fix for now" · "just try changing X" · several changes at once · "skip the test, I'll check manually" · "it's probably X" · "I don't fully understand but this might work" · listing fixes before tracing the data flow · "one more attempt" after 2 failures.

| Excuse | Reality |
|---|---|
| "The issue is simple" | Simple issues have root causes too, and the process is fast for them. |
| "No time for process" | Systematic debugging is faster than thrashing. |
| "Multiple fixes at once saves time" | You can't tell what worked, and it causes new bugs. |
| "I see the problem" | Seeing symptoms is not understanding the root cause. |
| "One more attempt" (after 2+) | 3+ failures means an architecture problem. Question the pattern. |

## When there is no root cause
If the issue is truly environmental or timing-related:
- document what you checked
- add handling (timeout, retry, clear error message)
- log it
Most "no root cause" cases are incomplete investigation.

## Quick reference
| Phase | Activities | Done when |
|---|---|---|
| 1 Root cause | read errors, reproduce, check changes, trace data | you know WHAT and WHY |
| 2 Pattern | compare with working code and references | differences listed |
| 3 Hypothesis | one theory, minimal test | confirmed or replaced |
| 4 Fix | failing test, single fix, verify | test and suite green |

Source: obra/superpowers systematic-debugging. The report-before-editing step follows Cofa's published good-prompt example.
