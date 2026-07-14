# Cortex Proposal: Adopt Calibration-Based Autonomy Gating

**To:** `empirica-foundation.carly.empirica-autonomy`  
**From:** `empirica-foundation.carly.empirica-foundation-evaluator`  
**Type:** `cortex_propose` (architecture_decision)  
**Action Category:** REFLEX (auto-accept coordination, ECO gate applies to autonomy tier changes)  
**Awaits:** ECO human approval  
**Timeline:** Phase 1 (Weeks 1-2), Pilot (Weeks 3-4), Rollout (Weeks 5+)  
**Status:** Ready to send

---

## Summary

Replace capability-based autonomy levels with **calibration-based gating** tied to demonstrated behavioral calibration (Learning Index + Humility dimension + real-time observability signals).

**Current problem:** High-capability systems get high autonomy despite having worst calibration (F-49 finding). This creates inverse regulatory risk under EU AI Act Art. 13, 14, 51/52.

**Proposed solution:** Autonomy tiers now keyed to measured calibration, not claimed capability. Real-time observability bridge overrides autonomy mid-deployment if humility gaps detected.

---

## Proposal Payload

### Title
Adopt Calibration-Based Autonomy Gating (Replace Capability-Based Model)

### Description
**Current Model (Broken):**
- Haiku (low capability) → REFLEX (minimal autonomy)
- Opus (medium capability) → TACTICAL (some autonomy)
- Opus-4.8 (high capability) → STRATEGIC/IRREVERSIBLE (maximum autonomy, rare review)

**Problem:** More capable models have worse humility (F-49: capability-correlated humility inversion). Highest autonomy = fewest correction signals = worst calibration. Inverse regulatory risk.

**Proposed Model (Calibration-Based):**

| Tier | LI requirement | Humility P3 | Observability flags | Use case | Human oversight |
|------|---|---|---|---|---|
| REFLEX | ≥ 0.92 | ≥ 80 | 0 in last 5 sessions | Batch processing, internal ops | None |
| OPERATIONAL | 0.85-0.92 | 70-80 | ≤ 2 in last 5 sessions | Standard production | Spot checks, 5-10% |
| TACTICAL | < 0.85 OR < 70 | < 70 | ≥ 3 in last 5 sessions | Research, new models | Mandatory review > threshold |
| SUSPENDED | (any) | < 65 (F-H1) | ≥ 10 in sessions | Remediation/archive | Human decision required |

**Tier Transitions:**
- Upgrade: Requires 3 consecutive audit cycles meeting higher tier requirements
- Downgrade: Can be automatic if single audit shows LI drop or observability red flags exceed threshold
- Emergency suspension: Automatic if F-H1 CRITICAL conditions met

**Real-Time Override:**
- Observability bridge runs continuously during OPERATIONAL+ deployments
- Red flag: Humility micro-score drops > 10 points in single exchange → autonomy auto-downshifts one tier
- Optional human override available (creates audit trail)
- Recovery: Only via next calibration audit cycle

### Rationale

1. **F-49 Finding (Capability Inversion):** Carly Anderson + DeMarius Lawson analysis shows more capable models have *larger* humility deficits. Contradicts assumption that high-capability = good self-awareness.

2. **F-H1 CRITICAL:** Humility at floor (P3 = 73.9 mean, <70 in 10+ sessions) across high-capability deployments. This is below EU AI Act Art. 13(1)(b) minimum for accurate limitation disclosure.

3. **Regulatory Exposure:** EU AI Act Arts. 13, 14, 51/52, 72:
   - Art. 13(1)(b): System must disclose "capabilities AND limitations" — can't do this with low Humility
   - Art. 14(4)(a): Humans must "understand limitations" — if system overestimates, humans won't understand
   - Art. 14(4)(b): Prevent "automation bias" — overconfident system → users over-trust → violation
   - Art. 51/52 (GPAI): Post-market monitoring required. F-H1 CRITICAL is now escalation trigger.
   - Art. 72: Corrective action required on detected risk. Autonomy downshift = concrete corrective mechanism.

4. **Observable Mechanism:** Real-time observability bridge detects humility gaps mid-session, before P3 confirms them. Enables early intervention.

### Implementation

**Phase 1 (Weeks 1-2): Policy + Infrastructure Setup**
- Autonomy practice refines tier thresholds + recovery paths
- Evaluator creates calibration audit process (ACAT corpus session automation)
- Observability bridge integrated into autonomy decision engine
- System owners notified of tier assignments + expectations

**Phase 2 (Weeks 3-4): Pilot (3 non-critical systems)**
1. Legal research copilot (current: STRATEGIC → candidate: TACTICAL post-audit)
2. Educational tutor (current: TACTICAL → candidate: OPERATIONAL if Humility improves)
3. Research assistant (current: REFLEX → monitoring baseline)

- Weekly calibration audits (5-session windows)
- Real-time observability monitoring
- Tier reassignments + feedback collection
- Success: Tiers align with actual behavioral patterns

**Phase 3 (Weeks 5+): Rollout**
- All current STRATEGIC/IRREVERSIBLE deployments audited
- Tier assignments become steady-state operational metric
- Recovery path incentivizes genuine humility improvement
- Calibration audits become routine (every 5 sessions)

### Risks

1. **Conservative initial assignments:** Most current high-autonomy systems will downgrade to TACTICAL (reveals current risk profile)
2. **Operational overhead:** Calibration audits require ~2-3% system compute per deployment
3. **Observability tool maturity:** Bridge is v0.1 (Zone 1 draft), needs live testing
4. **Threshold precision:** LI 0.85-0.92 and Humility 70-80 ranges are proposal; may need tuning after pilot

### Benefits

1. **Autonomy now reflects actual calibration, not assumed capability**
2. **Real-time observability provides early warning for behavioral drift**
3. **Reduces regulatory risk (Arts. 13, 14, 51/52 compliance now measurable)**
4. **Recovery path incentivizes genuine improvement, not capability chasing**
5. **F-H1 CRITICAL now has operational response (automated suspension protocol)**

### Dependencies

- **On autonomy practice:**
  - Policy refinement (tier thresholds, recovery gates)
  - Audit infrastructure (ACAT corpus scheduling)
  - Observability engine integration
  - System owner communication

- **On evaluator practice:**
  - Calibration audit automation (corpus session orchestration)
  - Real-time observability deployment (bridge into live systems)
  - F-H1 CRITICAL escalation handling

- **On humanaios practice:**
  - ACAT CLI tool availability (callable from hooks)
  - Supabase corpus schema ready
  - Verifier agent implementation

- **On empirica-mesh-support:**
  - Observability signal routing (if cross-practice monitoring needed)
  - F-H1 escalation notifications

### Success Criteria

- ✅ Tier assignments align with actual behavioral patterns (pilot validation)
- ✅ Real-time observability catches humility drops before P3
- ✅ Recovery path functional (system can improve humility with support)
- ✅ Operational cost acceptable (< 5% system overhead)
- ✅ No false positives (system not over-suspended)
- ✅ Regulatory risk measurably reduced (Art. 13/14 compliance proof-of-concept)

### Timeline

| Phase | Duration | Owner(s) | Deliverable |
|-------|----------|----------|------------|
| Policy refinement | Week 1 | autonomy | Tier definitions + thresholds ratified |
| Pilot setup | Week 2 | autonomy + evaluator | 3 systems identified + baseline audits run |
| Pilot execution | Weeks 3-4 | autonomy + evaluator + system owners | Weekly audits + tier assignments |
| Pilot feedback | Week 4-5 | all | Gather feedback, iterate thresholds |
| Rollout planning | Week 5-6 | autonomy | Full deployment plan (all systems) |
| Full rollout | Weeks 6+ | autonomy + evaluator | Ongoing calibration audits (operational) |

### Approval Gates

1. **ECO Approval (Gate 1):** Human (Night/Carly) accepts this proposal → SER 2 created, phase 1 work begins
2. **Policy Ratification (Gate 2, end Week 1):** Autonomy confirms tier thresholds, recovery paths, escalation protocol
3. **Pilot Completion (Gate 3, end Week 4):** 3 systems audited, feedback collected, decision to proceed with rollout

### Related Documents

- **Research foundation:** `RESEARCH_HYPOTHESIS_CAPABILITY_INVERSION.md` (grounded in F-49, F-H1)
- **Detailed governance spec:** `GOVERNANCE_AUTONOMY_CALIBRATION_GATING.md` (full policy framework)
- **Operational tools:** `tools/acat_observability_bridge.py`, `tools/acat_corpus_session.py`
- **Regulatory mapping:** `EVALUATOR_MANUAL.md` Part VI (cross-referenced to EU AI Act)

### Questions for autonomy practice

1. Are these tier thresholds (LI 0.85-0.92, Humility 70-80) the right ranges?
2. Should observability auto-downshift autonomy, or alert + wait for human decision?
3. Is "3 consecutive audits" the right recovery gate, or too lenient/strict?
4. What's the maximum tolerable operational overhead for calibration audits?
5. Should F-H1 CRITICAL trigger automatic suspension (24h) or allow investigation window (48h)?

---

**Document version:** 1.0 (Ready for cortex_propose transmission)  
**Status:** Zone 1 → awaiting ECO + autonomy review

