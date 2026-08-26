# PASS 37 — Congressional Rosetta Grammar

## Goal
Teach Bill X-Ray Next to recognize recurring legislative grammar as legal operations before any editorial writer sees the material.

## What changed
- Added `src/congressional_rosetta.py`.
- Added a reusable grammar catalog for amendments, overrides, conditions, exceptions, legal classifications, scoped definitions, effective dates, delegated rulemaking/determinations, authorizations, appropriations, and redesignations.
- Every grammar construct carries both a plain human operation and explicit context requirements.
- Hard gate: **grammar recognition alone can never become a public factual claim.**
- Added a TCJA-wide Rosetta artifact and dependency-free smoke cast.

## Why this is not a glossary
A glossary says `notwithstanding = despite`.

The Rosetta layer says:
1. this is an override operation;
2. identify the rule being overridden;
3. determine the override's scope and duration;
4. only then may a later semantic layer explain the consequence to a human.

Likewise, `treated as` is not translated as a phrase. It is recognized as a legal classification operation whose practical consequence still has to be reconstructed.

## Release gate
Pass 37 is CLEAR only when:
- core grammar examples are recognized;
- the live TCJA contains expected construct types;
- every live hit records context requirements; and
- zero grammar hits are publishable as factual claims by themselves.
