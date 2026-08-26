# PASS 42 - CLAIM VS LAW MAPPER

## Goal
Teach Bill X-Ray to compare a public political claim with the statutory machinery without collapsing the result into a partisan TRUE/FALSE stamp.

## Architecture move
Pass 42 creates a separate rhetoric lane and law lane.

The mapper:
1. records the public claim and its source;
2. decomposes the claim into legal promises that would have to exist for the statement to be literally guaranteed by statute;
3. maps those promises to verified statutory mechanisms;
4. separates supporting language from limiting conditions;
5. states what the reviewed law does not establish;
6. preserves questions that require implementation or later real-world evidence;
7. forbids motive or deception claims from a law/rhetoric mismatch alone.

## ACA demonstration
Public claim: **If you like your doctor, you can keep your doctor.**

The reviewed ACA provisions do support:
- preservation of certain existing coverage from termination merely because the Act requires it;
- choice among participating primary-care providers who are available to accept the enrollee;
- a sufficient choice of providers in qualified plans.

They do not establish an unconditional statutory right to one specific physician regardless of network participation or availability.

Machine classification: **CLAIM_BROADER_THAN_STATUTORY_GUARANTEE**.

That classification is intentionally not TRUE or FALSE. It says the political sentence is broader and simpler than the guarantee visible in the statutory machinery reviewed here.

## Control case
The TCJA headline claim **The child tax credit is $2,000** is classified **SUPPORTED_BUT_INCOMPLETE** because the headline amount is real while refundability and identification conditions remain part of the law.

This proves the mapper is not designed merely to attack political claims. It can also say that a claim is substantially supported while still restoring the conditions that public shorthand leaves out.

## Release gate
- Every claim clause must have evidence IDs.
- Every statutory evidence item must retain exact source excerpts and limits.
- No TRUE/FALSE classification when the evidence supports a qualified answer.
- No claim about later outcomes from statutory text alone.
- No inference of lying, fraud, motive, corruption, or intent.

## Human gate
**Did this make the gap between the public sentence and the legal mechanism understandable without telling the citizen what political opinion to hold?**
