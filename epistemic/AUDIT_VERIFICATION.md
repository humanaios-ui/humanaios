# Audit-of-Audit — v3.2-DRAFT verification (S-081626, Claude Opus 4.8 pass)

## Provenance
Uploads dir empty (same condition auditor reported); files reconstructed from
in-context content. Byte-hash match vs uploaded draft manifest NOT meaningful
for this reconstruction (docstrings condensed); verification is BEHAVIORAL.
Behavioral reproduction: EXACT (see below), so dynamics are faithful.

## RT findings independently re-verified against v3.1 (own probe implementations)
- RT-1 mask inertness: CONFIRMED (comp-vs-ind and near-blind runs bit-identical)
- RT-2 lead tautology: CONFIRMED (1696/1696 = 100.0% on iid noise — exact match)
- RT-4 T6 nondeterminism: CONFIRMED (d = +0.316, -0.113, +0.130 across identical calls)
- RT-5 self-resealing envelope: CONFIRMED (tampered v3.1 passes 7/7; manifest repins tampered hash)
- RT-3 span-collapse: partially exonerated per audit; conditioning guard adopted in v3.2 — accepted

## v3.2 suite verification
- 8/9 with T7 correctly FAILING vs v3.1 manifest (verify-by-default works)
- Tamper test: v3.2 fails LOUDLY on modified agent_view (fix confirmed)
- T9 anti-tautology: 49.6% on iid noise (matches audit exactly)
- T8 mask efficacy: monotone, zero-mask blind (matches)
- Experiment table: ALL 12 headline numbers reproduced exactly
  (48.3/52.5/0.92 | 51.1/56.6/0.90 | 24.4/34.8/0.70; lifts -0.499/-0.449/-0.207)

## NEW finding this pass (RT-6, Z1-proposed)
IC-CAND-PARAMS-UNVERIFIED-01: T7 verify-mode compares only *.py hashes.
Demonstrated: editing the committed manifest's params block (cond_limit
1e6 -> 999.0) still yields "T7 PASS", exit 0. The params entry is decorative
in both directions. Partial mitigation exists (params are hardcoded in
pinned analysis files), full fix: (a) verify params equality committed-vs-
computed, (b) ledger the manifest's own hash in REGISTERED.md so the
committed file is itself tamper-evident.

## Minor notes on v3.2
- T6 arms use seeds 42/43/44: mode contrast confounded with seed; label as
  descriptive or use paired seeds per arm.
- EpistemicAgent fallback rng uses legacy global randint: no-rng callers get
  nondeterministic runs; deprecate the fallback or seed it explicitly.

## Walk-backs required (IC-031 discipline) — from MY v3.1 outputs
1. "94/94 = 100.0%" leading-indicator figure (VALIDATION_REPORT.txt, S-081526):
   tautological; already flagged OPEN in-session, now formally withdrawn.
2. "52.2% is its base rate in a minimal world" (strategy memo, S3 mapping):
   withdrawn; corrected statement: confidence-rise and residual-non-decrease
   co-occur at/below independence-null rates; confidence is UNINFORMATIVE
   about ground error, and mvar-collapse LAGS convergence (lift < 0, all arms).
3. Corrected S3/S4 demo claim (stronger, honest version): internal confidence
   carries ~zero information about ground error, and true observation-channel
   partition (hard_partition) reduces confident-ungrounded convergence — the
   only arm-level effect that survives, pre-register before citing (F-CAND-
   HARD-PARTITION-EFFECT-01).

## RECOMMENDATION
RATIFY v3.2 with conditions: fix RT-6 (params verification + ledger manifest
hash), adopt T6 seed-pairing note, ratify the auditor's 4 IC-CANDs + 2 F-CANDs
+ this pass's IC-CAND-PARAMS-UNVERIFIED-01, and execute the two walk-backs.
Registry-touching items require live REGISTERED.md fetch at ratification
session per IC-030.
