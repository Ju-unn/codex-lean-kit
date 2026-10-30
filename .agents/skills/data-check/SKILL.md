---
name: data-check
description: Use when the task provides data files (CSV, JSON, XLSX, logs) or asks for numbers, tables, or charts computed from data, before writing analysis or aggregation code, and before reporting any computed number. For the main agent and for workers.
---

# Data check

Most wrong answers in data tasks are wrong numbers, not broken code: the wrong denominator, a retest counted twice, rows multiplied by a join. Fix what the data means before computing anything, and prove each key number twice.

## 1. Profile, read-only
- Never modify the provided data files. Outputs go to out/, or to the path the task README names.
- Look, don't read: row count, columns, types, a few rows, missing values, duplicate keys, value ranges, units. Never print or paste a whole file.
  - Python: the standard library (csv, json, statistics) through `python3 -c` or a short script. pandas only if `python3 -c "import pandas"` works.
  - No Python: a short node script, or `head` and `wc -l`.
- Record one line per file in docs/worklog.md: rows, columns, the anomalies found.

## 2. Data contract, before any analysis code
Add a "Data contract" section to docs/requirements.md, one row per file:

| File | One row means | Key | Units and time | Numerator / denominator | Duplicates, retests, missing |
|---|---|---|---|---|---|

- What the data shows goes in the table.
- What it means but does not show becomes a [담당자] or [자료] question through $requirements-interview, with your recommended default as an A-n until the answer arrives. Typical ones: which of several retests counts, whether zero-count rows are excluded, where a period starts and ends.
- Never settle a denominator or a retest rule by guessing.

## 3. Compute
- Ratios: the sum of numerators over the sum of denominators of the same population. Not the average of per-row ratios, unless the task defines it that way. A zero or missing denominator gives "cannot compute", never 0.
- Joins: check that the key is unique on the side that must be unique. Compare row counts and numerator and denominator totals before and after. A join that adds rows is a bug until explained.
- Time: one time zone; say whether boundaries are inclusive.
- Keep the count at each step (read → valid → in scope → after dedup) and report it.
- The computation lives in code with tests, not in a notebook cell or in your head. $tdd applies: each expected value comes from a hand count on a tiny fixture.

## 4. Prove each key number twice
Before a number goes into the UI, an output file, or docs/REPORT.md:
1. Recompute it by a second method on the real input: a different code path (a plain loop against pandas, SQL against code) or a direct count from the raw file.
2. Check one small case by hand.
3. Show the user the recompute command, so they can run it again.
4. If the two disagree, use $debugging. Never adjust an expected value to match the output.

## 5. Stack for an analysis task
When the deliverable is numbers or tables, offer this as one of the two options in $lean-plan; the user decides:
- One package-free Python CLI, `python3 analyze.py`, writing out/*.csv or out/*.json, with unittest tests.
- pandas or matplotlib only when already installed. No installs for a few lines of work.
- A web view only if the task README asks for one. Then the server reads out/ and computes nothing itself.

## 6. Report
In docs/REPORT.md, give every key number with its population, period, units, excluded counts, and how it was checked twice.

Sources: written for this kit. The data contract and the second-method recompute follow practice shared across public Cofa preparation kits.
