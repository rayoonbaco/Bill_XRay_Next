# PASS 35 — Meaning Substrate Foundation

## Decision

Do **not** continue patching the legacy public translation layer. Preserve the legacy Bill_XRay project as the evidence spine and build a new doctrine-first interpretation layer beside it.

## Why

The legacy public-language path performs heading cleanup, phrase replacement, topic labeling, and assembly. Those operations can make legal text shorter without reconstructing the underlying legal event. That is the failure mode identified by the new doctrine.

## What Pass 35 built

A fresh `Bill_XRay_Next` project containing:

- the locked human-output doctrine;
- the finish-line pass roadmap;
- a first Legislative Decompiler;
- a structured `MeaningEvent` schema;
- explicit uncertainty and publishability gates;
- line-level source ranges and excerpts;
- TCJA proof artifacts;
- focused tests;
- a Windows one-click runner.

## Initial TCJA findings

The first decompiler run identifies statutory instructions that look like before/after changes, but it deliberately refuses to publish ambiguous compound changes.

Examples:

- **Estate and gift tax exemption:** a single explicit dollar substitution can be represented cleanly from the statute itself.
- **Child tax credit:** the same section changes more than one dollar threshold. Pass 35 now refuses to collapse those separate mechanics into one public statement.
- **Standard deduction:** multiple substitutions appear, but their filing-status categories require deeper context reconstruction.
- **Corporate rate:** the section states the new 21% rate, but not the prior rate; the system refuses to invent the “before” state.

## Release principle established

**Unknown is a valid result.**

If Bill X-Ray cannot reconstruct the semantic unit safely, it must send the item to the next context-resolution pass rather than manufacture fluent prose.

## Next pass

PASS 36 should split compound statutory sections into atomic semantic units and reconstruct external-code before/after context. That is the point where the child-credit and standard-deduction changes should become safe, human statements.
