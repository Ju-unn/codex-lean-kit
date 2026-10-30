---
name: tdd
description: Use when implementing any feature or bugfix, before writing implementation code, or when writing or changing tests. For the main agent and for workers.
---

# Test-driven development

Write the test first. Watch it fail. Write minimal code to pass.
If you didn't watch the test fail, you don't know if it tests the right thing.
Violating the letter of these rules is violating their spirit.

## When
- Always: new behaviour, bug fixes, behaviour changes, refactoring of tested code.
- Exceptions (no test first):
  - configuration
  - scaffolding
  - generated code
  - visual-only UI (layout, styling); the user checks visuals in the browser

## Where tests go: seams
- A seam is a public boundary where behaviour is observable from outside: HTTP routes (supertest against createApp) and service functions.
- Tests live at seams, never against private helpers or internals.
- The seams under test are the tests listed in docs/plan.md, agreed at plan approval. A test at an unlisted seam needs a reason in your report.
- A good test reads like a specification ("accepts only the first of two identical submissions") and survives refactors because it does not care about internal structure.

## The iron law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
Production logic written before its test: delete it and redo it test-first. Don't keep it as a reference or adapt it while writing the test.

## The loop: one vertical slice at a time
1. RED: write ONE minimal test for one behaviour.
   - Clear name, one thing.
   - Real code; mocks only at system boundaries.
2. Verify RED (mandatory): run it.
   - It must fail, not error, with the expected message, because the feature is missing.
   - It passes: you are testing existing behaviour, so fix the test.
   - It errors: fix the error and re-run until it fails correctly.
3. GREEN: write the simplest code that passes. No extra features, options, or improvements to other code.
4. Verify GREEN (mandatory):
   - Run the test, then the project's full test command.
   - All green, output pristine (no errors or warnings).
   - A failure you did not cause still goes in your report by name.
5. REFACTOR, only when green: remove duplication, improve names, extract helpers. Stay green. Add no behaviour.
6. Next behaviour: back to 1.

Never write all the tests first and then all the code (horizontal slicing):
- Bulk tests verify imagined behaviour.
- They test the shape of things rather than what users see.
- They stay green when the real behaviour changes.
Each test is a tracer bullet that responds to what the last cycle taught you.

## Good tests
- Expected values come from an independent source: a literal, a worked example, the requirement. Never recompute them the way the code does (tautological).
  - Bad: `expect(total(items)).toBe(items.reduce((s, i) => s + i.price, 0))`
  - Good: `expect(total([{ price: 10 }, { price: 5 }])).toBe(15)`
- Verify through the interface, not a side channel. Create through the API and read back through the API; don't run a raw SELECT.
- One behaviour per test. "and" in the name → split it.
- Mock only system boundaries (time, randomness, external HTTP). Never mock your own modules. The database is real: a fresh ':memory:' database per test file.
- Before writing a test, name the production change that would make it fail.

## Bug fixes
First write a failing test that reproduces the bug, then fix it. Never fix a bug without a test.

## Evidence to report
- RED: the command, the relevant failing line, and why that failure was expected.
- GREEN: the command and the passing counts.

## Red flags: stop and restart the cycle
Code before test · test passes immediately · can't explain why the test failed · "I'll add tests later" · "too simple to test" · "I already checked it manually" · "tests after achieve the same thing" · "this case is different".

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll test after" | Tests written after pass immediately, which proves nothing. |
| "Already manually tested" | Manual checks leave no record and can't be re-run. |
| "TDD is too slow under the time limit" | Rework from untested code costs more than the test. |
| "Need to explore first" | Fine. Throw the exploration away, then start with a test. |

## When stuck
| Problem | Solution |
|---|---|
| Don't know how to test it | Write the wished-for call and its assertion first. |
| Test too complicated | The design is too complicated; simplify the interface. |
| Must mock everything | Too coupled; pass dependencies in, e.g. createApp(db). |
| Setup is huge | Extract a test helper. Still huge? Simplify the design. |

## Before reporting
- [ ] Every new behaviour has a test that was seen failing for the expected reason
- [ ] Minimal code per test; full suite green; output pristine
- [ ] Real code in tests; mocks only at system boundaries
- [ ] The plan's edge cases and error paths are covered

Sources: obra/superpowers test-driven-development; mattpocock/skills tdd (seams, vertical slices, anti-patterns).
