# Bill X-Ray

**Understanding first. Argument afterward.**

Bill X-Ray is an AI-assisted legislative reasoning demonstration designed to turn cryptic Congressional language into ordinary human meaning without severing claims from their evidence.

The public experience is deliberately simple: read the human story first, then open **Check My Homework** to inspect the supporting statutory receipts and limits, or **How This Became Human** to see the transformation from raw legal language to defensible prose.

## Launch build

Pass 45.3 — **Four Laws, Four Synthesis Signatures**

The launch build contains four worked examples:

- Tax Cuts and Jobs Act (TCJA)
- Inflation Reduction Act (IRA)
- Affordable Care Act (ACA)
- CHIPS and Science Act

The same doctrine is applied across all four, while each law produces a different synthesis signature because its evidence and structure are different.

## The doctrine

Bill X-Ray separates several jobs that ordinary summaries often collapse:

1. Decode recurring Congressional grammar.
2. Break provisions into atomic meaning events.
3. Restore missing context and legal nouns.
4. Investigate interesting patterns without treating suspicion as proof.
5. Challenge conclusions against evidence and uncertainty.
6. Separate enacted text from rhetoric, implementation, official review, and observed outcomes when needed.
7. Select only the facts that earn space in the human story.
8. Keep every material public claim attached to a receipt.

The goal is not to tell citizens what to think. It is to make difficult public documents understandable enough that they can think about them themselves.

## Public product

Open `public/index.html` or run `START_BILL_XRAY_PUBLIC.bat` on Windows.

The public interface contains:

- a 30-second version
- a long-form explanatory essay
- **Check My Homework** evidence receipts
- **How This Became Human** transformation ladder
- four distinct whole-law synthesis signatures

## Deploy

This repository includes `render.yaml` for a Render static-site deployment. See `DEPLOY.md`.

## Development validation

The project includes the complete staged smoke-test history used to protect semantic fidelity, public-language cleanliness, evidence traceability, and the launch experience.

The final Pass 45.3 package cleared the complete inherited regression suite before launch packaging.
