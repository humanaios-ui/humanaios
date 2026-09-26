# Epistemic Agent Validation Suite — v3.2-DRAFT

**Status:** PENDING Z2 RATIFICATION (S-081626 audit complete)  
**Audit Session:** S-081626-AUDIT  
**Auditor Role:** Z1 (proposes findings)  
**Ratification Gate:** Z2 decision (via cortex governance)

---

## Contents

```
epistemic/
├── agent_view.py               v3.2-DRAFT: continuous masks, per-agent RNG, seeded runs
├── ground.py                   v3.2-DRAFT: write-protected GROUND_TRUTH, detailed conditioning
├── validate.py                 v3.2-DRAFT: 9 tests including T7 verify-by-default, T8 mask-efficacy, T9 anti-tautology
├── experiment_decoupling.py    v3.2-DRAFT: fair indicator, full-window mvar, proper nulls
├── redteam_probes.py           RT-1…RT-5 reproducible against v3.1 (standalone verification)
├── PRECOMMIT_MANIFEST_DRAFT.json   v3.2 artifact hashes (awaiting ledger at ratification)
└── README.md                   This file
```

---

## Audit Summary

**Z1 passed these findings to Z2 for ratification (S-081626):**

### Critical Red-Team Findings (RT-1 through RT-5)

| Finding | Category | Impact | Fix Status |
|---------|----------|--------|-----------|
| **RT-1: Sensor Masks Inert** | IC-CAND-MASK-INERT-01 | Partial observer not implemented; S4 null-condition no-op | ✅ v3.2: continuous masks, per-dim absorption weights |
| **RT-2: Leading Indicator Tautological** | IC-CAND-LEAD-TAUTOLOGY-01 | 100.0% leading-indicator is by construction (windowing bias) | ✅ v3.2: full-window mvar, strict precedence test |
| **RT-3: Span-Collapse Objection** | Span-collapse hypothesis tested | Residual not primarily an artifact; conditioning guards added | ✅ v3.2: conditioning diagnostics + exclusion guard |
| **RT-4: T6 Unseeded Noise** | IC-CAND-T6-UNSEEDED-01 | Null control compares identical arms with unseeded variance | ✅ v3.2: T6 fully seeded via spawned RNG streams |
| **RT-5: Self-Resealing Manifest** | IC-CAND-SELF-RESEAL-MANIFEST-01 | T7 re-mints rather than verifies; analysis code unpinned | ✅ v3.2: T7 verify-by-default, analysis pinned |

### New Candidate Issues Found This Pass (RT-6)

| Finding | Category | Implication |
|---------|----------|-----------|
| **RT-6: Params Unverified** | IC-CAND-PARAMS-UNVERIFIED-01 | T7 checks only hashes, not params equality; params entry decorative | Partial mitigation in v3.2; full fix deferred (ledger manifest hash at ratification) |

---

## Walk-Backs: Claims That Must Be Corrected

When Z2 ratifies, these prior statements require formal withdrawal or re-scoping:

1. **"94/94 = 100.0% leading-indicator figure"** (VALIDATION_REPORT.txt, S-081526)  
   → Tautological by windowing; already flagged open in-session, now formally withdrawn.

2. **"52.2% is its base rate in a minimal world"** (strategy memo, S3 mapping)  
   → Withdrawn. Corrected statement: under v3.2, confidence-rise and residual-non-decrease co-occur **at or below** independence-null rates. Confidence is **uninformative** about ground error.

3. **S3/S4 demo claim re-scoped (stronger version)**  
   → Internal confidence carries ~zero information about ground error. True partial observation (hard_partition) reduces confident-but-ungrounded convergence — the only arm-level effect that survives (24.4% vs ~50%). Pre-register before citing (F-CAND-HARD-PARTITION-EFFECT-01).

---

## Headline Results Under v3.2 (Inverted from v3.1)

With active masks, fair indicator, and proper nulls:

| mask mode | decoupled joint | null | ratio | lead observed | shift null | lift |
|---|---|---|---|---|---|---|
| complementary | 48.3% | 52.5% | 0.92 | 23.0% | 72.9% | **−0.499** |
| independent | 51.1% | 56.6% | 0.90 | 23.9% | 68.8% | **−0.449** |
| hard_partition | 24.4% | 34.8% | 0.70 | 52.3% | 73.0% | **−0.207** |

**Key inversion:** The "decoupling regime" co-occurs **at or below chance**. Prior claims of coupling/early warning **do not survive correction**.

---

## How This Integrates

**Before Z2 ratification:**
- Code is staged in `epistemic/` as v3.2-DRAFT
- Tests pass 9/9 in verify-by-default mode
- Manifest is DRAFT (T7 will FAIL on verify until ratified)
- All red-team findings documented
- Walk-back corrections identified

**At Z2 ratification:**
- Z2 decides whether to accept findings + fixes
- If accepted, promote `PRECOMMIT_MANIFEST_DRAFT.json` → `PRECOMMIT_MANIFEST.json`
- Ledger manifest hash in REGISTERED.md (IC-030 discipline)
- T7 verify-by-default then passes
- Walk-backs issued via appropriate channels

**After ratification:**
- Empirica peers (humanaios, outreach, autonomy) consume v3.2 via mesh proposal
- Any prior claims citing v3.1 results are corrected

---

## Verification Steps (v3.2-DRAFT)

```bash
# Verify tests fail correctly (draft manifest not ratified):
python3 epistemic/validate.py
# Expected: T7 FAIL — PRE-COMMITMENT BROKEN (manifest in draft state)

# Verify tamper detection works:
python3 epistemic/validate.py --audit
# Expected: detects modified agent_view.py, aborts

# Run red-team probes independently (don't rely on manifest):
python3 epistemic/redteam_probes.py
# Expected: RT-1…RT-5 all reproduced against v3.1 baseline
```

---

## References

- **Audit Report:** See `AUDIT_REPORT.md` (in project root or referenced finding)
- **Audit Verification:** `AUDIT_VERIFICATION.md` — independent re-verification of v3.2 suite
- **Redteam Probes:** `redteam_probes.py` — standalone reproducers for RT-1 through RT-5
- **IC/F-CAND Registry:** See registry-candidates proposed in AUDIT_REPORT §4
- **Mesh Coordination:** See cortex inbox for humanaios verification-suite requests

---

**Awaiting Z2 ratification. Non-blocking for Phase 1 pilot consumption (can use v3.1 in parallel).**
