# Adversarial Audit — epistemic v3.1 → v3.2-DRAFT

**Session:** S-081626-AUDIT · **Role:** Z1 (proposes) · **Status:** ALL findings and code changes PENDING Z2 RATIFICATION
**Scope:** agent_view.py, ground.py, validate.py, experiment_decoupling.py, PRECOMMIT_MANIFEST.json (S-081526-NN)

## 0. Provenance note

The uploads directory was empty at audit time; all files were reconstructed to disk from in-context document content. Reconstruction was verified byte-exact: all three sha256 hashes match the committed manifest (`4beb713a…`, `91d2d86e…`, `b0a96d73…`), and both headline results reproduce exactly (52.2%, 100.0%). The audit therefore ran against the committed artifacts. Note that the committed agent_view.py itself contains a "RECONSTRUCTED TAIL" marker inside `run_ensemble` — meaning the manifest was minted *after* a truncation-and-rebuild event, which is itself an instance of finding RT-5 below.

## 1. Findings (severity order)

### RT-2 · IC-CAND-LEAD-TAUTOLOGY-01 — the 100.0% leading-indicator result is tautological — CRITICAL
v3.1 computes `t_collapse = argmin(mvar[3:t_sat]) + 3`, restricting the search window to indices strictly before `t_sat`. Therefore `t_collapse < t_sat` holds **by construction** whenever `t_sat > 4`. Empirical confirmation: pure iid-noise series fed through the identical logic score **1696/1696 = 100.0%** "lead hits." The committed "Leading indicator … 94/94 = 100.0%" carries zero evidential content as computed. If this number has been cited anywhere as evidence for the consensus-drift monitor's early-warning mechanism, a walk-back is required.

### RT-1 · IC-CAND-MASK-INERT-01 — sensor masks are functionally inert — CRITICAL
`absorb_projection` uses the mask only as a boolean gate (`mask > 0.0`), and `make_masks` clips all values to ≥ 0.05 in both modes — the gate can never fire and mask *magnitudes* are never used. Confirmed: complementary vs independent masks with the same seed produce **bit-identical trajectories**, as does a near-blind agent (mask = 1e-9). Consequences: (a) "partial observer" is not implemented; (b) the independent-mask null condition — the in-silico miniature of Segment 4 / multi-substrate independence — is a no-op; (c) any prior claim contrasting mask modes measured nothing.

### RT-5 · IC-CAND-SELF-RESEAL-MANIFEST-01 — the pre-commitment envelope reseals itself — CRITICAL
v3.1's T7 *writes* a fresh manifest on every run instead of *verifying* against the committed one. Demonstrated: after tampering with agent_view.py, validate.py exits 0 with "7/7 passed" and the manifest now pins the tampered hash. The temporal channel — the project's own third channel — is structurally absent from its flagship simulation: post-hoc code changes mint fresh "pre-commitments." Additionally, the analysis code (experiment_decoupling.py, where the tautology lives) was never pinned at all, and the manifest loop contains a duplicate `validate.py` entry.

### RT-4 · IC-CAND-T6-UNSEEDED-01 — the null-control test measures unseeded noise — HIGH
`run_ensemble` never seeds the global RNG used for private states and noise, so T6 is nondeterministic (observed Cohen's d across three back-to-back runs: +0.008, −0.212, −0.471). Combined with RT-1, T6 compares two *functionally identical* arms and reports noise as an effect size.

### RT-3 · Span-collapse objection to the 52.2% — TESTED, PARTIALLY EXONERATED
Hypothesis: `godview_residual` (lstsq of GROUND_TRUTH on span{h,m}) rises mechanically as agents converge (rank collapse), making "decoupling" a linear-algebra artifact. Test result: residual is nearly flat across pair angles 90°→1° (lstsq numerically rescues rank with large coefficients), and within the sweep corr(agreement slope, residual slope) = −0.120. The 52.2% is **not** primarily a span-collapse artifact. However, near-collinear pairs produce ill-conditioned fits (unbounded coefficients), so v3.2 adds conditioning diagnostics and an exclusion guard. The deeper objection stands and is quantified in §3.

### Minor
- T3 lacks try/finally: an assertion failure leaves GROUND_TRUTH scrambled for subsequent tests.
- `godview_residual` swallows all exceptions (bare `except Exception`).
- GROUND_TRUTH is a mutable module global.
- Mixed legacy global-RNG (`np.random.*`) and Generator usage throughout.

## 2. v3.2-DRAFT changes applied

| File | Change |
|---|---|
| agent_view.py | Mask is now a continuous per-dim absorption weight (eff. rate = lr × mask); zeros = truly blind dims. New `hard_partition` mask mode (disjoint support). Per-agent `np.random.Generator`; `run_ensemble` fully seeded via spawned streams. |
| ground.py | GROUND_TRUTH write-protected. `godview_residual_ex` returns (residual, condition number); only `LinAlgError` caught. |
| experiment_decoupling.py | Fair indicator: **full-window** mvar argmin, strict precedence. Circular-shift permutation null (200 perms); statistic is lift over null. Independence null for the joint decoupling rate. Conditioning exclusion (cond > 1e6). Three mask-mode arms. Sweep wrapped in `main()`. |
| validate.py | **T7 verify-by-default**: fails loudly on hash mismatch vs committed manifest; `--commit` mints a separate DRAFT and never overwrites the committed file. Analysis code now pinned. New **T8 mask-efficacy** regression guard (mask=0 absorbs nothing; monotone in magnitude). New **T9 anti-tautology** guard (indicator must score ≪100% on iid noise; measures 49.6%). T3 fail-safe restore. T6 seeded and reproducibility-asserted. 9/9 pass. |

Tamper test on v3.2: modifying agent_view.py now produces `T7 FAIL — PRE-COMMITMENT BROKEN`.

## 3. Substantive re-results under v3.2 (F-CAND material, pending Z2)

With active masks, a fair indicator, and proper nulls, the headline claims **invert**:

| mask mode | decoupled joint rate | independence null | joint/null | lead observed | shift null | lift |
|---|---|---|---|---|---|---|
| complementary | 48.3% | 52.5% | 0.92 | 23.0% | 72.9% | **−0.499** |
| independent | 51.1% | 56.6% | 0.90 | 23.9% | 68.8% | **−0.449** |
| hard_partition | 24.4% | 34.8% | 0.70 | 52.3% | 73.0% | **−0.207** |

Reading:
1. **The "decoupling regime" co-occurs at or below chance.** Joint rate ≤ P(conf up)·P(res flat) in every arm — confidence rise and residual non-decrease are independent-to-anticorrelated events in this world. The 52.2% was a *marginal co-occurrence rate*, not evidence of a coupled failure basin.
2. **The proposed internal early-warning signal LAGS.** mvar's global minimum falls *after* the confidence peak far more often than chance (negative lift in all arms). As implemented, mutual-agreement-variance collapse is a trailing symptom of convergence, not a leading indicator of it.
3. **True partial observation (hard_partition) *halves* the decoupling rate** — the first genuinely meaningful mask-mode contrast this instrument has produced, and directionally consistent with the S4 thesis (independence of observation channels reduces confident-but-ungrounded convergence). This deserves its own pre-registered follow-up before being cited.

**Walk-back implication:** the sentence "tonight's 52.2% is its base rate in a minimal world" and any use of the 100.0% leading-indicator figure should be withdrawn or re-scoped wherever they appear (strategy memo §1/S3, any registry candidate citing S-081526-NN sweep results). The market thesis does not depend on these numbers; the demo currently does.

## 4. Registry candidates proposed (Z1 → Z2)

- IC-CAND-LEAD-TAUTOLOGY-01 — leading-indicator statistic tautological by windowing (RT-2)
- IC-CAND-MASK-INERT-01 — sensor masks dynamically inert; S4 null-condition no-op (RT-1)
- IC-CAND-SELF-RESEAL-MANIFEST-01 — T7 re-mints rather than verifies pre-commitment; analysis code unpinned (RT-5)
- IC-CAND-T6-UNSEEDED-01 — null-control effect size is unseeded noise between identical arms (RT-4)
- F-CAND-DECOUPLING-AT-CHANCE-01 — under corrected instrument, confidence-rise and residual-non-decrease co-occur at ≤ independence-null rate; internal mvar signal lags rather than leads (v3.2 table above; falsification condition: a pre-registered v3.3 run in which joint/null ≥ 1.2 with positive lead lift would overturn)
- F-CAND-HARD-PARTITION-EFFECT-01 — disjoint observation support halves decoupling co-occurrence (24.4% vs ~50%); pre-register before citing

No REGISTERED.md fetch was performed this session; nothing above is registered. Per IC-030 discipline, run the findings-scan skill against the live registry before ratification if formal capture is desired.

## 5. Deliverables

```
epistemic_v3.2/
├── AUDIT_REPORT.md                      (this file)
├── redteam_probes.py                    (RT-1…RT-5, reproducible against v3.1)
├── experiment_decoupling.py             (v3.2-DRAFT)
└── epistemic/
    ├── agent_view.py                    (v3.2-DRAFT)
    ├── ground.py                        (v3.2-DRAFT)
    ├── validate.py                      (v3.2-DRAFT, 9 tests)
    └── PRECOMMIT_MANIFEST_DRAFT.json    (PENDING_Z2_RATIFICATION)
```

Verify-mode will correctly FAIL until Z2 promotes the draft to `PRECOMMIT_MANIFEST.json` and ledgers its hash — that failure is the feature working. The v3.1 committed manifest was not modified.

— Z1, S-081626-AUDIT
