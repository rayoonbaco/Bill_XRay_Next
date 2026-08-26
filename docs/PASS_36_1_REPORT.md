# PASS 36.1 - DEPENDENCY-SAFE SMOKE CAST

## Why this pass exists
Ray's Windows machine successfully ran the Pass 36 decompiler, but the smoke cast reported NEEDS REVIEW only because `pytest` was not installed in his Python 3.11 environment. That is installer friction, not a semantic failure.

## Change
- Removed pytest as a requirement from the user-facing smoke cast.
- Reimplemented the four focused acceptance checks with the Python standard library.
- Kept pytest tests in `tests/` for developer use.
- Preserved the full-replacement, run-from-project-root workflow.

## Doctrine
The user should test the product, not debug the team's Python environment.
