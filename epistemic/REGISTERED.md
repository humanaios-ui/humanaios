# Epistemic Suite — Registry Ledger (IC-030 Discipline)

**Status:** Z2 RATIFIED (2026-08-17, ALL TESTS PASS)  
**Registry Entry:** v3.2 LIVE ✅

---

## Manifest Ledger (Tamper-Evidence Record)

| Artifact | Hash (SHA256) | Ratification Date | Tests | Status |
|---|---|---|---|---|
| **PRECOMMIT_MANIFEST.json** | `62061b97…7302684` | 2026-08-17 | **9/9 PASS** | **LIVE** |

**Manifest Contents:**
- `agent_view.py`: c4d0b61b… (continuous masks, per-agent RNG, seeded runs)
- `ground.py`: 4c112a4c… (write-protected GROUND_TRUTH, condition reporting)
- `validate.py`: a59abfb8… (9 tests: T7 verify-by-default, T8 mask-efficacy, T9 anti-tautology)
- `params`: cycles=16, warmup=3, cond_limit=1e6, n_perm=200, etc.

---

## Z2 Ratification Record

**Decision:** RATIFY v3.2 (all conditions met)  
**Authority:** Z2 (2026-08-17)  
**Transition:** PRECOMMIT_MANIFEST_DRAFT.json → PRECOMMIT_MANIFEST.json  

**Test Results (Canonical):**
```
T1: AST import audit ...................... PASS
T2: Zero ground module coupling ........... PASS
T3: Bit-identical under scrambled ground . PASS
T4: Seeded reproducibility ............... PASS
T5: Valid trajectory ranges .............. PASS
T6: Mask contrast effects (REPORT) ....... PASS (comp vs ind: d=+0.028; vs hard_partition: d=-0.649)
T8: Mask efficacy regression guard ....... PASS (0.0 blind, monotone 0 < 4.910 < 9.819)
T9: Anti-tautology guard (iid-noise) .... PASS (49.6%, not 100%)
T7: Pre-commitment verify (manifest) .... PASS (pinned files match ledger)

RESULT: 9/9 PASSED
```

**Conditions Met:**
- ✅ RT-1 (Sensor masks) — Fixed with continuous absorption weights
- ✅ RT-2 (Leading indicator tautology) — Fixed with full-window mvar + strict precedence
- ✅ RT-3 (Span-collapse) — Tested, exonerated; conditioning guard added
- ✅ RT-4 (T6 unseeded) — Fixed with spawned RNG streams
- ✅ RT-5 (Self-resealing manifest) — Fixed with T7 verify-by-default
- ✅ RT-6 (Params verification) — Partial mitigation in place (full fix deferred)
- ✅ Manifest ledger established (IC-030 discipline)
- ✅ All critical findings documented + walk-backs identified

---

## Candidate Issues (Ratified Registry)

**Integrity Candidates (IC-CAND):**
- IC-CAND-MASK-INERT-01 ........................ Fixed (RT-1)
- IC-CAND-LEAD-TAUTOLOGY-01 ................... Fixed (RT-2)  
- IC-CAND-T6-UNSEEDED-01 ...................... Fixed (RT-4)
- IC-CAND-SELF-RESEAL-MANIFEST-01 ............ Fixed (RT-5)
- IC-CAND-PARAMS-UNVERIFIED-01 ............... Partial mitigation (RT-6, full fix deferred)

**Falsification Candidates (F-CAND):**
- F-CAND-DECOUPLING-AT-CHANCE-01 ............ Confirmed (joint/null ≤ 1.0; pre-register before citing)
- F-CAND-HARD-PARTITION-EFFECT-01 ........... Confirmed (24.4% vs ~50%; pre-register before citing)

---

## Walk-Backs (Enforced at Ratification)

Effective 2026-08-17, the following published claims are officially withdrawn:

1. **"94/94 = 100.0% leading indicator (mvar collapse precedes confidence peak)"**  
   - Source: VALIDATION_REPORT.txt, S-081526  
   - Reason: Tautological by windowing (RT-2); zero evidential content  
   - Action: Withdraw from all publications, strategy memos, registry entries

2. **"52.2% is its base rate in a minimal world"**  
   - Source: Strategy memo, S3 mapping  
   - Reason: v3.2 testing shows joint/null ≤ 1.0; confidence uninformative  
   - Action: Withdraw or re-scope to "co-occurs at or below chance"

3. **S3/S4 Demo Claim (original formulation)**  
   - Source: Prior S3/S4 thesis statement  
   - Reason: Only hard_partition effect survives; other arms at or below null  
   - Action: Re-scope to hard_partition contrast only; pre-register before citing

---

## Mesh Coordination

**Proposal Status:** v3.2-LIVE coordination ready  
**Targets:** 
- humanaios (Phase 1 verification suite execution)
- outreach (audit readiness)  
- autonomy (calibration gating framework)

**Next Step:** Emit cortex proposal with test results + ratification confirmation

---

**This document constitutes the tamper-evidence ledger (IC-030 discipline).** The manifest hash above, committed to git with this record, prevents undetected post-hoc modifications. Verify integrity: `shasum -a 256 PRECOMMIT_MANIFEST.json` should always return `62061b97…7302684`.
