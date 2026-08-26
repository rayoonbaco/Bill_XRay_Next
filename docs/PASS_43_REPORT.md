# PASS 43 - Cold Generalization Trial

Goal: prove Bill X-Ray Next can apply its doctrine to a different major law without TCJA/ACA-specific prose rules.

Trial law: **Inflation Reduction Act (Public Law 117-169)**.

The pass imports only the legacy project's previously verified IRA evidence bundle: official source text, verified synthesis, external-evidence metadata, and release status. The new `generalization_trial.py` contains no IRA-specific prose templates; it normalizes direct-effect claims, discovers topic clusters, selects a minority of the available facts, and builds a cold column from that discovered structure.

This is a generalization bridge, not yet a fresh arbitrary-bill ingestion pass. A later pass must prove the same flow from a newly fetched law with no pre-existing verified legacy artifact.
