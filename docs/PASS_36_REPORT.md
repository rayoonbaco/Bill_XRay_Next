# PASS 36 — Atomic Before / After Reconstruction

## Purpose
Stop treating a congressional section as one idea. Split every identifiable statutory change into its own semantic event before any public prose is written.

## What changed
- The project is now self-contained for the TCJA proof path; `sources/tcja.txt` is bundled inside the project.
- The decompiler emits separate atomic substitution events rather than section-level bags of numbers.
- Child-tax-credit changes `$1,000 -> $2,000` and `$3,000 -> $2,500` are now separate events with different statutory labels.
- Standard-deduction substitutions are split but deliberately held from publication until the referenced pre-amendment code categories are reconstructed.
- The 21% corporate rate is captured while the prior rate remains explicitly unresolved rather than invented.
- A root-level smoke-cast script now explains the pass, runs the engine, runs tests, prints the human duties, and saves a readable result artifact.

## Release philosophy adopted
Bill X-Ray Next now prefers complete project/file replacements over patch packages. BAT launchers and smoke-cast files live in the main project folder and run from there.

## Gate
PASS 36 is successful only if the engine proves that multiple dollar substitutions in one section are different semantic facts and preserves unresolved context rather than compressing it away.
