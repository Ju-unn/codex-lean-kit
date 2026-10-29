# Question techniques (stems for the agenda)

The user rephrases these in their own words. Pick the technique that fits the open branch.

## Let them talk first: process discovery
- "Tell me about this work. What happens, start to finish?"
- Use the past tense: "Tell me about the last time this happened." It gives richer material than "describe the process".
- Follow up: "And then what happened?"
- Start from outcomes: "When this goes well, what is the result?" Then work backwards: "What has to happen before that? And before that?"
- Ask early who is involved. For each actor: "What do they need to do their job? What do they need to see?"
- Layered decomposition:
  - events: "What things happen?"
  - commands: "Who or what triggered each one?"
  - actors
  - entities: "What changed when it happened?"
  - policies: "Whenever X happens, should Y follow?"
  - information needs: "What did they need to see to decide?"
  - unknowns: "Where would different people give different answers?"

## Details: examples, not abstractions
- "Give me a case where it worked. Now one where it didn't. What was different?"
- When a rule is unclear, ask for more examples: "Can you give me a case where this went a different way?"
- Actor walkthrough, in the first person:
  - "You open the screen on Monday morning. What is in front of you?" That is the data to show.
  - "What can you do from here?" Those are the actions.
  - "When would that action not be available?" That is a guard.
  - "After that, who takes over?"
- Trace data backwards: "Where does that information come from? Who enters it, and when?" A chain with no source is a gap.
- Ground it: "If you were looking at the screen right now, what exactly would you see?"
- At external boundaries: "Does someone enter that by hand, or does it arrive from another system?"

## Obstacles: what goes wrong
- Pre-mortem: "Imagine it's live and people are frustrated. What happened?" Then: "How should it have been prevented or handled?"
- Nothing happens: "What if nobody acts? After a day? After a week?"
- Handoffs: "Who takes over at this point? How do they know it's their turn?"
- Enumerate the alternatives at each step:
  - "What is the main thing that happens?"
  - "What else could happen?"
  - "Anything else?"
  - Follow each alternative to its end.
- Test each transition:
  - "What if the preconditions aren't met?"
  - "Can it be undone?"
  - "Is there a time limit in this state?"
  - "Can it happen twice?"
- Invariants: "Is there something that must never be true at the same time?" Example: two active requests for the same slot.

## Check assumptions: show back what you heard
- Play back: "So it goes A, then B, then either C or D. Is that right?"
- Test order: "Could these steps happen in a different order? Would that change anything?"
- Verify actors: "Is it always the manager who approves? Could someone else, in some cases?"
- Check completeness at each transition: "Before we move on, is there any situation here we haven't covered?"
- Replay a real scenario: "Say Alice does X on Monday. Walk me through what happens, step by step."

## Scope
- "What's the boundary? What should we deliberately leave out?"
- "If only one thing could work on day one, which would it be?"

Source: juxt/allium elicit and its references (process discovery, detail elicitation, obstacle elicitation, assumption checking), adapted from spec-writing to stakeholder interviews.
