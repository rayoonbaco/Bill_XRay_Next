# PASS 40.1 - Semantic Coverage Expansion

## Goal
Give the Human Story Engine enough court-cleared meaning to tell a real TCJA story without relaxing the doctrine.

## Architectural move
Pass 40 exposed a two-fact bottleneck. Pass 40.1 adds a second safe semantic lane: **direct statutory facts**. A direct fact is allowed only when the enacted text itself is sufficient to say what Congress sets, creates, requires, permits, limits, or schedules. Each fact carries exact source lines, an evidence excerpt, confidence, and explicit limits on what it does not prove.

This lane does **not** infer motive, fairness, winners/losers, distributional effects, budget effects, corruption, or real-world outcomes.

## Result
- 33 direct statutory facts cleared.
- 8 human categories represented.
- 0 source-anchor holds.
- 31 facts used by the Human Story Engine.
- First expanded story is approximately 1,170 words.
- Machine readiness: `STORY_READY_FOR_HUMAN_GATE`.

## Why this matters
The writer is no longer forced to pad two before/after facts. It has enough verified material to select a story. Pass 40.1 still bans humor and satire. The next gate is human comprehension, not style.
