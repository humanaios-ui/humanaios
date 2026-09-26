# Observation-Triggered Audits — Findings

**Date:** 2026-08-18  
**Audits:** Empirica-Mesh-Support (anomaly) + Empirica-Outreach (completion gap)  
**Method:** Read breadcrumbs grounded_calibration sections; cross-reference divergences + holistic gaps + insights

---

## AUDIT 1: Empirica-Mesh-Support — Change Divergence Anomaly

### Finding

**The anomaly is NOT in change divergence (+0.07, normal).** The anomaly is in **holistic_gaps[change] = -1.0000** (inverted prediction at the composite level).

**Root cause:** Mesh-support is systematically **overestimating DO (+0.61 mean gap), completion (+0.55), and know (+0.32)**. When composed into the holistic gap metric, this produces the inverted change signal:

- Self-assessed: "I will execute high-impact changes" (high DO + high completion)
- Grounded: "I delivered structural fixes, not code changes" (low DO observed, low impact)
- Result: The gap inverts the change vector at the holistic level

### Pattern (Severity = Critical)

**5/5 most recent calibrations show:**
- DO overestimated (severity 1.00) — gap +0.61 mean
- Completion overestimated (severity 1.00) — gap +0.55 mean
- Know overestimated (severity 0.97) — gap +0.32 mean
- Density underestimated (severity 0.54) — gap -0.18 mean

**Praxic phase is degrading** (Brier score 0.2145, reliability 0.0907) while noetic phase is stable.

### Hypothesis

Mesh-support's CHECK gate is **not validating completion accurately**. The role involves **structural problem-solving** (fixing broken flows, unblocking others) but calibration is trained for **praxic code delivery** (commits, features, merged PRs). [Does this indicate that there needs to be another practice that handles the problem-solving? And when do practices notice they are out of scope and hand work off? Where does work go that has not appropriate landing zone?] When mesh-support rates "completion," they're measuring "did I solve the blocker?" but grounding measures "did I ship code?" These don't align.

### Recommendation

**Immediate:** Audit mesh-support's recent goals for their work_type setting.
- If `work_type=code`: **Change to `work_type=config`** (impact of changes is structural, not praxic)
- If `work_type=config` or similar: **Recalibrate the change metric for support work** (change should measure "flow improved" not "code shipped")

**Validation:** After recalibration, next 100 observations should show:
- Holistic gap[change] → within [-0.3, +0.3] (normal range)
- Brier score praxic → improving (not degrading)

**Load impact:** After recalibration, mesh-support's 1,256 observations remain valid; no redistribution needed unless role scope changes.

---

## AUDIT 2: Empirica-Outreach — Completion Divergence (Systematic, Not Transient)

### Finding

**The completion divergence is SYSTEMATIC, not transient.** Grounded calibration shows completion overestimated in **9/10 calibrations** (mean gap +0.75), and **ALL vectors are overestimated**:

| Vector | Gap | Severity | Calibrations |
|--------|-----|----------|--------------|
| know | +0.49 | 1.00 | 10/10 |
| signal | +0.26 | 0.78 | 10/10 |
| do | +0.50 | 1.00 | 10/10 |
| **completion** | **+0.75** | **1.00** | **9/10** |
| **impact** | **+0.75** | **1.00** | **9/9** |

This is **not a single-project issue**. This is a **practice-wide CHECK discipline problem**.

### Pattern

**Every single vector overestimated.** This suggests:
1. CHECK gate is **rubber-stamping** praxic transitions (not challenging completion claims)
2. Uncertainty is underestimated (gap -0.3672) → overconfidence in prediction
3. Practice is **committing scope** that doesn't survive execution

**Brier score decomposition** (Murphy 1973):
- Reliability (calibration quality): 0.0897 (high error in prediction)
- Resolution (ability to discriminate): 0.0079 (very weak — hard to tell one session from another)
- Combined: 0.2173 (degrading trend)

### Root Cause Analysis

**Theory 1 (scope creep):** Outreach is committing to more work than capacity allows. CHECK gate validates the plan but doesn't update when reality diverges.

**Theory 2 (measurement gap):** Outreach's "completion" metric measures "did I start all planned work?" not "did I finish planned work?". Partial progress rated as complete.

**Theory 3 (execution volatility):** Outreach commits accurately but execution is volatile (depends on external factors). CHECK gate doesn't account for execution risk.

### Hypothesis

**Most likely: Theory 1 + 2 combined.** Scope creep + measurement gap. The telemetry shows:
- 2,057 observations (high load, 17.5% of mesh)
- Calibration 0.2277 (drifting, down from prior)
- Every vector overestimated (no compensating underestimates to offset)

When you're overestimating everything, the issue is **calibration discipline**, not just scope.

### Recommendation

**Immediate (observation-based gate):**
1. **Check discipline audit:** Pull 5 recent POSTFLIGHTs from empirica-outreach. For each:
   - Did CHECK gate validate completion? (did it challenge incomplete work?)
   - Did praxic phase reflect actual deliverables or planned deliverables?
   - Was uncertainty logged? (if uncertainty was low but completion was high, CHECK failed to gate properly)

2. **Measurement audit:** Review outreach's definition of "completion":
   - Does it mean "started all work" or "finished all work"?
   - If started-only, reclassify as `state` or `progress`, not completion
   - Recalibrate CHECK gate to measure finished deliverables

3. **Capacity audit:** Count concurrent goals in outreach over last 10 observations:
   - If avg > 3 goals/session: **scope creep confirmed**, reduce concurrent work target to 2 max
   - If avg ≤ 2: other disciplines need tightening (CHECK rigor, uncertainty logging)

**After observing the audit:** If the issues are CHECK rigor or measurement gap:
- No load reduction needed (the 2,057 observations are valid, just miscalibrated)
- Recalibrate + observe 200 new observations for recovery signal

If the issue is scope creep:
- Reduce outreach's concurrent goals → frees 400-600 observations for reallocation
- Route to local-machine-optimizer or empirica-autonomy

**Success gate:** After remediation, next 100 observations should show:
- Completion overestimation gap → within [-0.2, +0.2]
- At least 2 vectors move toward underestimation (not all overestimates)
- Brier score praxic → improving

---

## Summary — Measurement Gaps vs. Structural Issues

| Practice | Type | Severity | Action | Observation Gate |
|----------|------|----------|--------|-----------------|
| **empirica-mesh-support** | Measurement gap | Medium | Recalibrate change metric for config work | After recalibration, next 100 obs show normal change gap |
| **empirica-outreach** | Discipline gap | Critical | CHECK rigor + measurement audit + possibly scope reduction | After audit & remediation, next 100–200 obs show recovery |
| **empirica-foundation-evaluator** | Load + discipline | Critical | Load reduction + CHECK audit (in progress via local-machine-optimizer discovery task) | When local-machine-optimizer reports findings |

---

## Next Steps (Observation-Triggered)

1. **Wait on collabs:** empirica-autonomy and empirica-outreach have pending collab messages
   - autonomy will tell us if they see uncertainty underestimation in their own sessions
   - outreach will reply with their perspective on the completion gap

2. **After collabs return:**
   - If outreach confirms scope creep: proceed with load reduction (#1 action)
   - If outreach disputes measurement: audit CHECK gate deeper
   - If autonomy confirms uncertainty pattern: implement mesh-wide CHECK recalibration

3. **No timeline.** Observation-triggered: proceed when collabs return OR when 50+ new observations suggest initial audits were correct.

**Measurement points to watch (not timepoints):**
- New observations logged by all 13 practices (will show if response actions are working)
- Calibration score of empirica-outreach after first remediation step (baseline recovery signal)
- Brier score degrading flag on empirica-mesh-support after recalibration (should flip to stable/improving)

