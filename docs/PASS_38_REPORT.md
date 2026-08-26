# PASS 38 - Investigation Engine

## One-pass goal
Convert decoded TCJA material into a ranked queue of things worth investigating, without allowing curiosity, unusualness, or large numbers to become allegations or public prose.

## Current state before this pass
Passes 35-37 created atomic meaning events and a Congressional Rosetta grammar. They could decode operations and preserve missing context, but they did not decide which parts of a giant law deserve scarce human attention.

## Desired state
A candidate is allowed into the investigation queue only with:
- an evidence location;
- a category and attention score;
- a plain reason a citizen might care;
- a concrete question to investigate;
- at least one ordinary/non-sinister explanation;
- explicit uncertainty;
- `public_claim_allowed = false`.

## Signals in this first engine
- delegated authority;
- overrides (`notwithstanding`);
- exceptions/special rules;
- narrowly specified classes;
- temporary/transition rules;
- large verified before/after numerical changes.

These signals are **leads, not conclusions**.

## Full-measure gate
Pass 38 deliberately does not write jokes, essays, winners/losers claims, corruption labels, or political conclusions. Pass 39 must adversarially test provocative candidates before any later writer sees them as usable findings.

## Files added/replaced
- `src/investigation_engine.py`
- `tests/test_investigation_engine.py`
- `SMOKE_TEST_PASS_38.py`
- `ONE_CLICK_PASS_38.bat`
- `artifacts/tcja_pass38_investigation_queue.json` (generated)
- `docs/PASS_38_REPORT.md`
- `README.md`

## Acceptance criteria
1. At least 15 TCJA investigation candidates across at least 4 categories.
2. Every candidate has evidence lines, uncertainty, and an ordinary explanation.
3. No candidate is allowed to become a public claim in Pass 38.
4. Dependency-free focused tests pass.
5. The project remains self-contained in the main folder.
