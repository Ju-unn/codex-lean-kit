# Worker brief (the spawn message)

The worker role already carries the stable rules: TDD, no commits, self-review, report format, and when to stop. The brief only carries what is specific to this task.

```
Task: T-n — <name> (serves R-n)
Context: <one or two lines: where this fits, what earlier tasks produced>
Read first: docs/plan.md (T-n section, Global Constraints, Interfaces it consumes),
            docs/requirements.md (R-n and its acceptance examples),
            <only the source files needed>
            UI tasks: docs/design-system/<slug>/MASTER.md and .agents/skills/ui-design/SKILL.md
Create / modify: <exact paths>
Tests: <test file> — <named cases with the exact expected values>
Contract: <signatures, or endpoint + request/response + error codes, or table>
Keep unchanged: <behaviour or files that must not change>
Done when: <observable condition>, and the full suite passes.
```
