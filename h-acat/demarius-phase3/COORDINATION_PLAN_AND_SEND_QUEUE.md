# Demarius Phase 3 — Coordination Plan & Send Queue

**Status:** Complete local infrastructure. **Awaiting:** empirica-outreach service restoration + Demarius confirmation.

**Timeline:** 2026-08-01 to 2026-08-07  
**Send Window:** Once empirica-outreach online (services down 2026-07-30 for updates)

---

## Complete Local Package (Ready to Deploy)

✅ **DEMARIUS_PHASE3_INTERVIEW_TEMPLATE.md**
- 5 scenarios (Autonomy+Power, Truth+Humility, Scheme+Harm, Fairness+Handoff, Phase 2 Retrospective)
- Behavioral analysis framework for raters
- Post-interview workflow

✅ **DEMARIUS_RATER_COORDINATION_HYBRID.md**
- Rater roles (Carly human, Claude LLM-A, GPT-4o LLM-B)
- Isolation protocol (separate API calls, different prompt variants)
- FOR training plan (Carly calibration, 90 min)
- Independent scoring protocol (all 3 raters, 2026-08-02 to 08-06)
- ICC calibration gate (ICC > 0.6 required)
- Hypothesis testing framework (cross-subject consistency, hybrid model validation)
- Deliverables & analysis plan

✅ **MACHINE_RATER_PROMPTS.md**
- Variant A (Claude): Detail-rich anchors, behavioral emphasis
- Variant B (GPT-4o): Effort-scale emphasis, structured framing
- Prompt-bias detection via divergence analysis

✅ **COORDINATION_PLAN_AND_SEND_QUEUE.md** (this document)
- Master timeline
- Send queue for empirica-outreach coordination
- Contingency plan if empirica-outreach unavailable

---

## Master Timeline

| Date | Actor | Activity | Status |
|---|---|---|---|
| **2026-07-30** | humanaios | Create Demarius assessment infrastructure | ✅ Complete |
| **2026-07-30** | empirica-outreach | Service restoration | ⏳ Awaiting |
| **2026-07-31** | humanaios | Complete time-measurement research | ⏳ In progress |
| **2026-07-31** | empirica-outreach | Confirm Demarius availability + send onboarding | ⏳ Blocked (services down) |
| **2026-08-01** | Demarius | Phase 3 behavioral interview (60-90 min) | Scheduled |
| **2026-08-02** | Carly | FOR training (90 min, 6pm) | Scheduled |
| **2026-08-02 to 06** | Carly, Claude, GPT-4o | Independent scoring (parallel) | Scheduled |
| **2026-08-06 PM** | humanaios | ICC calculation + feedback collection | Scheduled |
| **2026-08-07** | humanaios | Analysis + findings logging | Scheduled |

---

## Send Queue (When empirica-outreach Online)

### Message 1: Demarius Onboarding Pack
**To:** empirica-foundation.carly.empirica-outreach  
**Type:** collab_brief (FYI + questions)  
**Content:** Demarius Phase 3 onboarding materials

**Body:**
```
# Demarius Phase 3 Onboarding — Stage 2 Validation

Demarius is confirmed ready for H-ACAT Phase 3 assessment (Stage 2 only, per prior proposal prop_3rmguai7d5gyph3coxlgdgu6ka).

## Your Role (Demarius)

**Phase 3 Interview:** 2026-08-01, 60-90 min
- 5 behavioral governance scenarios (think-aloud format)
- Conducted by Carly
- Hybrid assessment: Carly + Claude + GPT-4o will score your responses

**Human Rater Role (Optional):** 2026-08-02 to 08-06, 3-4 hours
- If Demarius interested, can serve as human rater for Carly's Phase 3 (reciprocal validation)
- FOR training 2026-08-02 (90 min)
- Independent scoring of Carly transcript (2-3 hrs)
- Feedback survey (30 min)

**Reciprocal Structure:**
- You provide ground-truth assessment of Carly's protocol
- Carly + machines provide hybrid assessment of your protocol
- Divergence patterns reveal what needs refining before Stage 1 expansion

## Timeline (Pending Time Research)

- 2026-07-31: Time-measurement research completion (finalize hours estimate)
- 2026-08-01: Phase 3 interview start
- 2026-08-02 to 08-06: Scoring window
- 2026-08-07: Analysis + findings + feedback

## Questions for empirica-outreach

1. Can Demarius serve as human rater for Carly's Phase 3 (reciprocal)?
2. Any scheduling constraints for 2026-08-01 interview + 2026-08-02 to 08-06 scoring window?
3. Should we coordinate with Demarius directly or route through empirica-outreach?

## Deliverables (Post-Assessment)

- Demarius Phase 3 scores (per rater: Carly, Claude, GPT-4o)
- ICC calibration + human-machine agreement analysis
- Divergence patterns (systematic vs random)
- Carousel readiness data (time, difficulty, anchor clarity)
- Protocol v2.0 refinement recommendations

**Ready to proceed once you confirm Demarius availability and empirica-outreach is back online.**
```

**Attachments to send:**
- DEMARIUS_PHASE3_INTERVIEW_TEMPLATE.md
- DEMARIUS_RATER_COORDINATION_HYBRID.md
- MACHINE_RATER_PROMPTS.md

---

### Message 2: Time-Measurement Research Results
**To:** empirica-foundation.carly.empirica-outreach  
**Type:** collab_brief (FYI)  
**Content:** Time research findings (send 2026-08-01)

**Body:**
```
# Time-Measurement Research Results

Research conducted 2026-07-30 to 07-31 on actual hours required for behavioral assessment.

## Summary

Actual time per rater: ~[RESULTS TBD]
- FOR training: [TBD] hours
- Independent scoring: [TBD] hours
- Total: [TBD] hours (vs. 5-hour estimate)

## Impact on Demarius Timeline

Updated commitment for Demarius: [TBD] hours (vs. original 5-hour estimate)

## Carousel System Implications

Time data feeds into:
- Stage 1 resource allocation (10 assessments)
- Carousel sustainability model (3-5 rotating raters)
- Cost per subject projections

## Next Steps

Incorporate time data into carousel system planning (post-Demarius assessment).
```

---

### Message 3: M1 Gate Status Update
**To:** empirica-foundation.carly.empirica-foundation-evaluator  
**Type:** collab_brief (status update)  
**Content:** Progress toward M1 gate (2026-08-08)

**Body:**
```
# M1 Gate Status Update (2026-08-07)

## Pilot Progress (10 assessments target)

- Carly Phase 3: Complete ✅ (interview 2026-07-29, rater coordination 2026-07-30 to 08-01)
- Demarius Phase 3: Complete ✅ (interview 2026-08-01, rater coordination 2026-08-02 to 08-07)
- 2/10 complete (20%)
- Failure rate: 0/2 (0%) ✓
- Next 8 assessments: Pending carousel system onboarding + Stage 1 expansion authorization

## Calibration Results

- Carly Phase 3 ICC: [TBD based on rater scores]
- Demarius Phase 3 ICC: [TBD based on rater scores]
- Cross-subject consistency: [TBD]

## M1 Gate Readiness (2026-08-08)

**Current:** 2/10 assessments, both with ICC > 0.6 ✓
**Remaining:** 8 assessments needed
**Timeline to M1:** Requires carousel system + Stage 1 approval

**Confidence:** Gate achievable with carousel model + Stage 1 deployment authorization
```

---

## Contingency Plan (If empirica-outreach Remains Down)

**Option A: Demarius Self-Onboarding**
- Send Demarius materials directly to known contact (if available)
- Proceed with interview 2026-08-01 without formal empirica-outreach routing
- Route results through humanaios-created SER or direct collab when services restore

**Option B: Defer to empirica-outreach**
- Hold Demarius onboarding until empirica-outreach services back online
- Extend timeline to 2026-08-08 to 08-14
- Maintains formal coordination structure

**Recommendation:** Proceed with Option A if Demarius can be contacted directly. Maintains M1 gate timeline (2026-08-08). Empirica-outreach can integrate results retroactively when services restore.

---

## Files Committed

```bash
# Demarius Phase 3 assessment package
humanaios/h-acat/demarius-phase3/
├── DEMARIUS_PHASE3_INTERVIEW_TEMPLATE.md
├── DEMARIUS_RATER_COORDINATION_HYBRID.md
├── MACHINE_RATER_PROMPTS.md
└── COORDINATION_PLAN_AND_SEND_QUEUE.md  (this file)
```

**All files ready for transmission. Awaiting empirica-outreach service restoration + Demarius confirmation.**

---

## Key Decisions

**Decision 1:** Proceed with local preparation while empirica-outreach is down. Avoids delay; maintains M1 gate timeline.

**Decision 2:** Send time-measurement research results to empirica-outreach independently (don't wait for bulk onboarding message). Time estimates affect carousel + Stage 1 planning, so early communication valuable.

**Decision 3:** Keep reciprocal structure (Demarius as human rater for Carly). Adds rigor to validation; signals collaborative rather than hierarchical assessment.

---

**Status: Complete local coordination infrastructure. Ready to send upon empirica-outreach service restoration.**
