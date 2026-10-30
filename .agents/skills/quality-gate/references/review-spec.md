# Spec review request (the spawn message for task_name "spec")

```
Check whether the whole change implements what was asked, nothing more and nothing less.

Diff: git diff baseline...HEAD -- . ':!*lock*'   and   git log --oneline baseline..HEAD
What was asked:
- docs/requirements.md: the Agreement block, R-n with acceptance examples, assumptions A-n
- docs/plan.md: scope (MVP and Later), Global Constraints, Review Focus

Report each finding with a quote of the requirement line and the code location (file:line):
- Missing: an MVP R-n or acceptance example that is not implemented, or claimed but not working
- Extra: behaviour nobody asked for (scope creep, speculative features)
- Wrong: implemented, but differently from the requirement or the Global Constraints
- Cannot verify from the diff: what the controller must check by hand, for example in the browser

If docs/REPORT.md or the plan's task status claims something, check the claim against the code and the commits.

Under 400 words. Start directly with:
Spec verdict: complete | gaps: <R-n list>
```
