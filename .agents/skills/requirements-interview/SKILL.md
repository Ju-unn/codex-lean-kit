---
name: requirements-interview
description: Use when a task brief or README has just arrived, when requirements are vague or held by a stakeholder agent, or when the user pastes stakeholder answers or materials. Main agent only.
---

# Requirements interview

Interview relentlessly until there is a shared understanding. Map everything that is unknown, prepare every question, and keep the record.

## Who answers what
- **The user is the decision-maker.** Put each decision to the user and wait.
- **A stakeholder agent** holds the business facts, rules, priorities, and materials.
  - You cannot reach it. The user relays your questions and material requests, then pastes back the answers.
  - It reveals information only when asked, one topic at a time, and never hands over a solution.
- **Facts already in the README, files, or data** are yours to find, never a question.
  - If they span more than about 5 files or large data, spawn task_name "facts", agent_type "explorer", fork_turns "none".
  - Don't block on it: only the questions downstream of it wait.

Label every question with who answers it:
- **[담당자]** business information: how the work runs today, cases, rules, exceptions, priorities, the success metric. The user asks the stakeholder.
- **[자료]** a material request: what, why, and in what form (for example, a sample schedule as a table). The user requests it from the stakeholder.
- **[결정]** the user decides: scope cuts, technical choices, trade-offs, and an assumption where the stakeholder has no answer.

There is no cap on the number of questions.

## First pass (no code yet)
1. Read README.md and the provided files.
2. Create docs/requirements.md from assets/requirements-template.md:
   - the problem in one line
   - users and scenarios
   - R-n candidates with their source
   - ambiguities
3. Build the design tree: every open decision, and the decisions that hang off it.
4. Give the user the first round.

## Rounds: ask the whole frontier
The frontier is every question whose prerequisites are settled: what you can ask now without guessing at answers you haven't heard yet.
- Each round asks the whole frontier.
- A question whose answer depends on another open question waits for a later round.
- Settled answers push the frontier outward. Recompute it after every answer.

Question format:
`Q<n> [담당자|자료|결정] — <title>: <one idea, never compound> · why it changes the build · ➡ recommended answer (used as assumption A-n if unanswered)`

Number the questions most important first. The user may send the [담당자] and [자료] questions in one message or split them by theme.

How the [담당자] questions unfold, from shallow to deep:
- L0 map (the first message): which areas can the stakeholder answer, and which materials exist?
- L1 story (open): a recent concrete case; how it is handled today; why it goes wrong.
- L2 goal (open): the success metric, its current value, and where it is measured; who hurts most; the one thing that must work.
- L3 scope: data, scale, constraints, what to deliberately leave out.
- L4 rules and failure paths (closed, with your default):
  - edge cases, what can go wrong, concrete examples with real values
  - phrase each so that "yes" accepts your recommended answer
- L5 agreement: read the Agreement block back and ask for confirmation.

Two rules for [담당자] questions:
- In L0-L2, use no solution words (app, AI, automation). Ask about their work.
- Never ask the stakeholder what to build, or for a task list.

For question stems by technique, read references/question-techniques.md.

## When the user pastes answers or materials
1. Update R-n, with the Q-number as the source. Turn concrete examples into acceptance-test candidates.
2. Save pasted materials under docs/materials/ with their source (the Q-number), and use them as test data and examples.
3. Record assumptions as A-n, close the answered branches, and recompute the frontier.
4. Report only what changed, then give the next round.

## Done when
- The frontier is empty: every branch visited, nothing silently assumed.
- The stakeholder has confirmed the Agreement block, and the user has made the open [결정] calls.

If the requirements timebox ends first:
- Every open item becomes an explicit A-n with your recommended default.
- The remaining questions continue during the build. The user asks them while workers run.

Sources: mattpocock/skills grilling (design tree, frontier rounds, recommended answers, facts are your job, decisions are the user's) and to-questionnaire (one idea per question); juxt/allium elicit (process discovery, scope, obstacles, assumptions); Cofathon top-performer practice (agreement block, no solution words early).
