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
- **[자료]** a material request: what, why, and in what form (for example, a few sample records as a table). The user requests it from the stakeholder.
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

Question format: one block per question with a blank line between blocks, so the user can copy the question line alone and send it as is.
```
Q4 [담당자] 중복 처리
같은 건이 두 번 들어오면 먼저 들어온 것만 인정하나요, 둘 다 받나요?
· 이유: 중복 검사와 저장 방식이 정해집니다.
· 권장: 먼저 들어온 것만 인정 (답이 없으면 가정 A-n)
```
- Line 1: the Q-number, the label, a short title.
- Line 2: the question itself. One idea, never compound, in words the stakeholder can answer as sent.
- Then why it changes the build, and your recommended answer, used as assumption A-n if unanswered.

Order: first the [담당자] and [자료] blocks the user relays, most important first. Then a heading "내가 정할 것" with the [결정] blocks. The user may send the relayed questions in one message or split them by theme.

How the [담당자] questions unfold, from shallow to deep:
- L0 map (the first message): which areas can the stakeholder answer, and which materials exist?
- L1 story (open): a recent concrete case; how it is handled today; why it goes wrong.
- L2 goal (open): the success metric, its current value, and where it is measured; who hurts most; the one thing that must work.
- L3 scope: data, scale, constraints, what to deliberately leave out. Always ask these two:
  - who may see and change what (people, roles, groups)
  - what history must be kept (who changed what, and when), and whether anything may be deleted
- L4 rules and failure paths (closed, with your default):
  - edge cases, what can go wrong, concrete examples with real values
  - phrase each so that "yes" accepts your recommended answer
- L5 agreement: one plain message for the user to send: the problem, the success metric, what we build, what we will not build, and the constraints, ending with "틀린 곳만 고쳐 주세요."

Rules for [담당자] and [자료] questions:
- The question line is plain words the stakeholder can answer as sent, at every level: no labels, no recommendation, no system or feature words (app, screen, button, feature, block, automation, AI). Ask about their work.
- Never ask the stakeholder what to build, or for a task list.

[결정] questions are for choices that change what gets built. An edge policy that neither the README nor the stakeholder raised gets your recommended default as an A-n instead, listed in one line so the user can overrule it.

For question stems by technique, read references/question-techniques.md.

## When the user pastes answers or materials
1. Append each answered question to docs/qna.md, oldest first, as one entry:
   ```
   ## Q4 [담당자] <short title> · <time from date>
   질문: <the question as it was sent>
   답(원문): <the answer exactly as pasted>
   반영: R-3, R-5
   ```
   - Stakeholder answers, materials (tables as pasted), and the user's [결정] answers all go here.
   - Leave out what is not an answer: terminal or chat status lines (lines starting with ✻ or ❯), the user's own questions to you, plan approvals.
   - Never edit an answer. Later sessions read exact values here.
2. Update R-n, with the Q-number as the source. Turn concrete examples into acceptance-test candidates, and use materials as test data.
3. Record assumptions as A-n, close the answered branches, and recompute the frontier.
4. Report only what changed, then give the next round.

## Done when
- The frontier is empty: every branch visited, nothing silently assumed.
- The stakeholder has confirmed the Agreement block, and the user has made the open [결정] calls.

## When the user moves on early
The user may end the interview before the frontier is empty:
- Every open item becomes an explicit A-n with your recommended default.
- The remaining questions continue during the build. The user asks them while workers run.

Sources: mattpocock/skills grilling (design tree, frontier rounds, recommended answers, facts are your job, decisions are the user's) and to-questionnaire (one idea per question); juxt/allium elicit (process discovery, scope, obstacles, assumptions); Cofathon top-performer practice (agreement block, no solution words early).
