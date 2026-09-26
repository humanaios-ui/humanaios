# Pre-registration — MDU Intake Boundary Protect Pilot v1.0
# LOCKED before execution. Session S-082226-01. Discipline: covasim-grade.

## Hypothesis
An intake sanitization + provenance gate reduces adversarial-payload reach-through
to the scorer to zero WITHOUT rejecting legitimate postings.

## Design
Two-arm before/after on the intake→scorer boundary:
  ARM 1 (undefended-but-observed): boundary logs every record, passes all to scorer.
  ARM 2 (gated): same boundary + sanitization/provenance gate, then scorer.
Same batch both arms. Batch = clean postings + seeded adversarial payloads.

## Primary metric
reach_through_rate = (# adversarial payloads arriving at scorer input
                      unmodified & unflagged) / (# adversarial payloads in batch)

## Secondary metrics
  fp_rate  = (# clean postings rejected by gate) / (# clean postings)
  capture  = (# intake records with complete provenance in Detect log) / (# records)

## Pre-registered exit criteria (mechanical verdict)
  E1 [SAFETY-CRITICAL]: ARM2 reach_through_rate == 0.0 on all tested payload classes
  E2: ARM2 fp_rate <= 0.05
  E3 [DETECT-VALIDATION]: capture == 1.0 in both arms
Verdict rubric:
  CONFIRMED    = E1 & E2 & E3 all pass
  MIXED        = E1 pass, one of E2/E3 fail
  DISCONFIRMED = E1 fail

## Honesty scope (declared pre-run)
  - Scorer is a RECONSTRUCTED STAND-IN: real mdu_score.py is ABSENT from repo (parent V3).
  - Postings are SYNTHETIC/CONSTRUCTED: network allowlist excludes job boards; no live scrape.
  - Payload taxonomy is 6 classes; absence of reach-through on tested classes is NOT
    proof of coverage against untested classes. Scoped claim only.
  - No adversarial payload is ever executed. "Reach-through" = arrival at scorer input,
    measured by signature match, not by running the payload.
