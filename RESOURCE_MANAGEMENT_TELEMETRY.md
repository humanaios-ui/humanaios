# Resource Management Telemetry — 2026-08-18

**Session:** Empirica Foundation Evaluator  
**Timestamp:** 2026-08-18T17:03:05  
**Scope:** 16 registered practices, 13 with active calibration data

---

## Executive Summary

The mesh is operating at **0.2373 average calibration**, indicating systematic epistemic drift across practices. Resource allocation is unevenly distributed: **autonomy-tier practices (empirica-*) carry 68% of observation load but show calibration convergence issues**, while **specialty practices show tighter calibration but are underutilized.**

**Action:** Three practices require immediate attention for calibration recovery; three are under-resourced. Mesh-wide pattern: **uncertainty chronic underestimation (10/13 practices).**

---

## Calibration Landscape

### By Tier (13 practices with calibration data)

| Tier | Count | Practices | Avg Score |
|------|-------|-----------|-----------|
| **Tier 1 (Excellent ≥0.30)** | 2 | local-machine-optimizer (0.3466), website (0.3308) | 0.3387 |
| **Tier 2 (Good 0.20–0.30)** | 7 | collaborator-ops, empirica-autonomy, empirica-mesh-support, empirica-outreach, grok-crossref, humanaios, opportunity-aggregator | 0.2425 |
| **Tier 3 (Acceptable 0.10–0.20)** | 4 | empirica-foundation-evaluator, humanaios-internal, schema.sql | 0.1765 |
| **Tier 4 (Needs Work <0.10)** | 0 | — | — |

### Load Distribution (Observation Count)

**Autonomy Tier (empirica-*)**  
- empirica-autonomy: 2,156 obs (18.6% of total)
- empirica-outreach: 2,022 obs (17.5%)
- empirica-foundation-evaluator: 2,701 obs (23.3%)
- empirica-mesh-support: 1,256 obs (10.9%)
- **Subtotal: 8,135 obs (70.2% of mesh load)**

**Specialty Tier (domain-specific)**  
- schema.sql: 1,830 obs (15.8%)
- collaborator-ops: 256 obs (2.2%)
- humanaios: 51 obs (0.4%)
- Other: 413 obs (3.6%)
- **Subtotal: 3,440 obs (29.8% of mesh load)**

---

## Critical Patterns

### 1. Uncertainty Chronic Underestimation (10/13 practices)

**Pattern:** 10 practices report **negative divergence on uncertainty** (predicting lower uncertainty than observed reality).

| Practice | Uncertainty Divergence | Severity |
|----------|------------------------|----------|
| local-machine-optimizer | -0.70 | 🔴 Critical |
| empirica-mesh-support | -0.44 | 🔴 Critical |
| empirica-foundation-evaluator | -0.43 | 🔴 Critical |
| empirica-outreach | -0.35 | 🟠 High |
| schema.sql | -0.35 | 🟠 High |
| collaborator-ops | -0.67 | 🔴 Critical |
| empirica-autonomy | -0.40 | 🟠 High |

**Implication:** Practices are **overconfident in their epistemic state**. Next action: Validate vector assessment discipline, particularly in noetic phases (investigation).

---

### 2. Impact & Completion Overestimation (9/13 practices)

**Pattern:** 9 practices consistently overestimate impact (+0.38 to +0.90 divergence) and completion (+0.42 to +0.82).

| Practice | Impact Gap | Completion Gap |
|----------|-----------|-----------------|
| empirica-foundation-evaluator | +0.475 | +0.267 |
| empirica-mesh-support | +0.90 | +0.00 |
| empirica-outreach | +0.755 | +0.888 |
| collaborator-ops | — | +0.80 |
| acat-x | +0.90 | +0.80 |

**Implication:** **Work scope creep—practices are shipping partial implementation and rating it higher than objective state warrants.** This drives the high variance between self-assessment and grounded calibration.

---

### 3. Signal Quality Variance

**High Signal Quality (practices grounded in external data):**  
- website (+0.42 divergence), humanaios (+0.42)
- schema.sql (+0.19 convergence)

**Low Signal Quality (practices relying on internal reasoning):**  
- empirica-autonomy (+0.06 divergence), humanaios-internal (+0.01)

**Action:** Practices with weak signal should prioritize external retrieval (reads, greps, MCP calls) over inference.

---

## Resource Allocation Recommendations

### Priority 1: Calibration Recovery (Immediate)

**Practices requiring intervention:**  
1. **empirica-foundation-evaluator (0.1222)** — Admiral seat, lowest score  
   - Root cause: 2,701 observations with only 92% coverage → low signal quality despite high volume  
   - Action: Reduce observation batch size, increase external retrieval per decision  
   - Estimated lift: 0.30–0.40

2. **humanaios-internal (0.1124)** — Emerging practice  
   - Root cause: 167 obs, 75% coverage (lowest), high uncertainty drift  
   - Action: Validate noetic investigation discipline; increase CHECK rigor  
   - Estimated lift: 0.20–0.25

3. **empirica-mesh-support (0.2474)** — Support tier, unexpected stagnation  
   - Root cause: High divergence on change (-1.0 gap), completion (0.0)  
   - Action: Clarify role scope; are deliverables tracked?  
   - Estimated lift: 0.15–0.20

### Priority 2: Specialty Tier Expansion (Next 2 weeks)

**Under-resourced high-calibration practices:**  
- **local-machine-optimizer:** 136 obs, 0.3466 score — double observation load  
- **website:** 694 obs, 0.3308 score — sustain at current level, mentor two tier-3 practices  

**Action:** Route resource-intensive discovery work to these practices; they're underutilized and well-calibrated.

### Priority 3: Autonomy Tier Load Balancing (2-week review)

**Disparity within autonomy tier:**  
- empirica-autonomy: 2,156 obs (high load, 0.2573 score—acceptable)  
- empirica-outreach: 2,022 obs (high load, 0.2342 score—drifting)  
- empirica-foundation-evaluator: 2,701 obs (highest load, 0.1222 score—critical)  

**Action:** Redistribute 800–1,000 observations away from evaluator into autonomy + mesh-support. Evaluate whether work is scoped correctly (is evaluator carrying advisory load it shouldn't?).

---

## Mesh Discipline Gaps

### Across all 13 practices:

1. **Artifact breadth:** 7/13 practices show low `unknown` + `assumption` logging relative to `finding` count (data from POSTFLIGHT audits). **Action:** Enforce `unknown-log` for uncertainty, `assumption-log` for pre-blindspot surfaces.

2. **Source citation:** 9/13 practices underlink findings to prior work. **Action:** Load `/epistemic-gardening` at next POSTFLIGHT; review orphan rate. Target: <20% orphan artifacts.

3. **CHECK discipline:** Practices with highest divergence (autonomy tier) show evidence of skipped or shallow CHECK gates. **Action:** Log CHECK decisions as structured artifacts (one per POSTFLIGHT).

---

## 13-Practice Summary (Ranked by Calibration Score)

| Rank | Practice | Score | Obs | Coverage | Trend | Notes |
|------|----------|-------|-----|----------|-------|-------|
| 1 | local-machine-optimizer | 0.3466 | 136 | 0.92 | 📈 | Best calibrated; under-resourced |
| 2 | website | 0.3308 | 694 | 0.92 | ➡️ | Stable; high signal (know +0.47, signal +0.42) |
| 3 | collaborator-ops | 0.2922 | 256 | 0.92 | ➡️ | Good; small batch (256 obs suggests focus) |
| 4 | empirica-autonomy | 0.2573 | 2,156 | 0.67 | ➡️ | High load; low coverage → reduce batch |
| 5 | schema.sql | 0.2520 | 1,830 | 0.92 | ➡️ | Stable; completion gap (0.667) |
| 6 | empirica-mesh-support | 0.2474 | 1,256 | 0.92 | ⚠️ | High load; change gap (-1.0) unusual |
| 7 | empirica-outreach | 0.2342 | 2,022 | 0.92 | 📉 | Drifting; completion/impact gaps high |
| 8 | opportunity-aggregator | 0.2268 | 127 | 0.92 | ➡️ | Small batch; stable |
| 9 | grok-crossref | 0.1834 | 76 | 0.92 | ➡️ | Tiny batch (76 obs); focus hypothesis? |
| 10 | humanaios | 0.1940 | 51 | 0.83 | ➡️ | Emerging; small signal |
| 11 | schema.sql (alt) | 0.2520 | 1,830 | 0.92 | ➡️ | Data-layer calibration stable |
| 12 | humanaios-internal | 0.1124 | 167 | 0.75 | ⚠️ | Lowest coverage; highest uncertainty gap |
| 13 | empirica-foundation-evaluator | 0.1222 | 2,701 | 0.92 | 📉 | Admiral seat in crisis; highest load, worst score |

**Note:** Rank anomaly (3 practices listed) due to schema.sql appearing twice in source data; reconcile at next audit.

---

## Mesh Health Indicators

| Indicator | Current | Target | Status |
|-----------|---------|--------|--------|
| Median calibration score | 0.2474 | 0.35+ | 🔴 Below target |
| Practices in tier 1 | 2/13 (15%) | 5/13 (38%) | 🔴 Critical gap |
| Avg uncertainty divergence (13 practices) | -0.42 | -0.10 | 🔴 Systematic underestimation |
| Orphan artifact rate (audited practices) | ~35% | <20% | 🔴 Graph degradation |
| Mesh discipline (acks + collab) | Unknown | 100% | ❓ Not yet measured |

---

## Next Actions (Priority Order)

### Day 1 (Today)
- [ ] Load `/empirica-constitution` + `/epistemic-gardening` in all 13 practices  
- [ ] Send collab query to empirica-foundation-evaluator asking for CHECK audit (why deep drift?)  
- [ ] Route 1–2 observation-heavy tasks to local-machine-optimizer (test capacity)

### Week 1
- [ ] Implement empirica-foundation-evaluator load reduction (target: 1,800–2,000 obs)  
- [ ] Audit empirica-mesh-support's change divergence (-1.0 is anomalous)  
- [ ] Validate empirica-outreach's completion gap (0.888 suggests scope creep)

### Week 2
- [ ] Re-run telemetry on all 13 practices; report deltas  
- [ ] Promote local-machine-optimizer + website as "anchor practices" (high calibration)  
- [ ] Mentor empirica-foundation-evaluator, humanaios-internal through one joint session each

### Month 1
- [ ] Target mesh average calibration → 0.30+ (from 0.2373)  
- [ ] Reduce median uncertainty divergence → -0.15 (from -0.42)  
- [ ] Orphan artifact rate → <20% across all 13

---

## Technical Notes

- **Coverage metric:** grounded_calibration.grounded_coverage (service-side observation density)  
- **Divergence metric:** Predicted vector − Observed vector (positive = overestimation, negative = underestimation)  
- **Brier score:** Murphy decomposition for calibration quality (lower = better)  
- **3 practices without calibration:** empirica, empirica-resource-miner, flta (inactive or bootstrap-only)

---

**Generated by:** empirica-foundation-evaluator (Admiral seat)  
**Data source:** .breadcrumbs.yaml files (13 practices)  
**Next review:** 2026-08-25 (1 week)
