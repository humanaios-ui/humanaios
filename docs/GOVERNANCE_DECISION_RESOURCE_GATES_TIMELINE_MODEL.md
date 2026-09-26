# Governance Decision: Resource-Gate Timeline Model for Mesh Coordination

**Decision Authority:** Admiral (Carly R. Anderson) — Zone 2  
**Status:** ✅ RATIFIED (2026-08-14)  
**Effective Date:** 2026-08-14 (immediately)  
**Scope:** Foundation-wide (all 6 practices)  
**Impact Level:** Architectural (reshapes milestone + gate model)

---

## Decision

**The mesh shall coordinate by resource gates, not calendar dates.**

### Old Model (Time-Driven)
```
Phase 1: Aug 12-25 (fixed calendar)
Phase 2: Aug 26-Sep 20 (fixed calendar)
M1 gate: Sep 8 (fixed date, creates crisis if prerequisites slip)
M2 gate: Sep 25 (fixed date)
M3 gate: Oct 30 (fixed date)
...
PROBLEM: Artificial deadline pressure even when blockers unresolved
```

### New Model (Resource-Gate-Driven)
```
Phase 1: ENDS WHEN [autonomy A.0.1-A.0.3 pass] AND [humanaios rater recruited] 
         AND [all 6 practices draft practice-specs]
         (No calendar date; triggers when prerequisites met)

Phase 2: STARTS WHEN Phase 1 gates complete
         ENDS WHEN [independence checks pass] AND [P1 baselines sealed]
         (No calendar date; driven by actual readiness)

M1 gate: FIRES WHEN [ACAT P1 sealed] AND [Empirica P1 sealed] AND [Admiral approves]
         (No Sep 8; fires when ready, could be Sep 5 or Sep 20 depending on prerequisites)
```

**Exception (Preserved):** External governance deadlines remain time-locked:
- autonomy Phase 1 baseline publication: Nov 4 (grant requirement, not negotiable)
- prEN 18229 formal vote window: TBD pending CEN decision (regulatory, not negotiable)
- Admiral Zone 2 review window: 2026-12-22 (stakeholder expectation, can be extended by Admiral decision)

---

## Rationale

### Problem with Time-Driven Model
1. **Artificial crisis creation:** Fixed milestone date + unmet prerequisites = forced decision (rush work or miss deadline)
2. **Masking blockers:** Hitting calendar date does not guarantee readiness; creates false progress signal
3. **Cascade failures:** One prerequisite slip affects all downstream gates, creates domino effect
4. **Loss of autonomy:** Prerequisites become secondary to deadline; teams optimize for hitting date, not for quality
5. **Invisible dependencies:** Calendar timeline hides what actually gates next step; resource model makes dependencies explicit

### Advantages of Resource-Gate Model
1. **No artificial pressure:** Work proceeds at pace of actual readiness, not clock
2. **Explicit dependencies:** Every gate lists exact prerequisites; mesh knows what unblocks next step
3. **Natural escalation:** If prerequisite blocked (e.g., Cortex SER 3.5), gate naturally waits; blocker becomes visible decision point
4. **Quality focus:** Teams optimize for readiness, not for deadline compliance
5. **Reduced thrashing:** No "catch-up" mode when calendars slip; work scope doesn't change, timeline does
6. **Better predictability:** Gates fire when prerequisites actually done, reducing rework and late discoveries

### Trade-Offs
| Aspect | Time-Driven | Resource-Gate | Winner |
|--------|-------------|---------------|--------|
| **Predictability** | Calendar clear but often wrong | Harder to predict but accurate when it fires | Resource-gate (accuracy > false certainty) |
| **Stakeholder expectations** | Easy to set ("by Sep 8") | Requires explaining dependency model | Time-driven (appearance) but Resource-gate (reality) |
| **Team discipline** | Calendar creates external pressure | Requires internal discipline to not slow-roll | Depends on team maturity |
| **Blocker visibility** | Deadline-driven, last-minute escalations | Early escalation, visible in gate requirements | Resource-gate (proactive vs. reactive) |
| **External constraints** | Calendar can honor them | Must be listed as special case | Tie (both honor external deadlines) |

**Verdict:** Resource-gate model is superior for internal coordination. Time-locked deadlines preserved only for external governance constraints.

---

## Application to Current Phases

### Phase 1: Governance Adoption Specification (Was: Aug 12-25)

**NEW MODEL:**

Phase 1 **COMPLETES WHEN ALL OF:**
- [ ] autonomy A.0.1-A.0.3 gates verified PASSING (mesh-support to confirm in Tue sync)
- [ ] humanaios rater recruitment CONFIRMED (evaluator to confirm in Wed collab)
- [ ] All 6 practices drafted practice-spec.yaml (mesh-support interview feedback complete)
- [ ] Evaluator practice-spec Phase 1 interview CONDUCTED (prop_joagp2rawnccphohr57wk474lq confirmation pending)
- [ ] Admiral ratified practice-spec adoption governance (Zone 2 decision pending)

**NO CALENDAR DATE.** Phase 1 ends when prerequisites met.

**Expected timing** (not a deadline): Aug 25-Sep 5, based on prerequisite state at 2026-08-14. If autonomy gates slip, Phase 1 completion slips. No artificial crisis at "Aug 25."

### Phase 2: P1 Baseline Administration (Was: Aug 26-Sep 20)

**NEW MODEL:**

Phase 2 **STARTS WHEN Phase 1 COMPLETES** (no Aug 26 date)

Phase 2 **COMPLETES WHEN ALL OF:**
- [ ] Independence CHECK gates 2A + 2B dry-run VALIDATED (evaluator checkpoint)
- [ ] ACAT P1 baseline SEALED to git notes (humanaios commit)
- [ ] Empirica P1 baseline SEALED to git notes (evaluator commit)
- [ ] Admiral approval for M1 gate OBTAINED (Zone 2 decision)

**NO CALENDAR DATE.** Phase 2 ends when prerequisites met.

**Expected timing** (not a deadline): Sep 5-15, based on Phase 1 completion + M1 prerequisites. If Cortex SER 3.5 blocker extends, M1 gate slips naturally (no crisis, just honest timeline).

### M-Gates (M1-M5): Resource-Driven

**M1 FIRES WHEN:**
- [ ] autonomy A.0.1-A.0.3 verified PASSING
- [ ] humanaios ACAT P1 baseline SEALED
- [ ] evaluator Empirica P1 baseline SEALED
- [ ] Admiral approval OBTAINED

**Was:** Sep 8 (calendar)  
**Now:** Whenever prerequisites complete (could be Sep 5 if early, Oct 5 if prerequisites slip, no artificial deadline)

**M2 FIRES WHEN:**
- [ ] Independence CHECK gates 2A + 2B VERIFIED passing
- [ ] P1 backfill prerequisites MET
- [ ] Admiral approval OBTAINED

**Was:** Sep 25 (calendar)  
**Now:** Whenever prerequisites complete

*... same pattern for M3, M4, M5*

---

## External Governance Deadlines (Time-Locked, Non-Negotiable)

The following remain **calendar dates** because they are driven by external governance, not internal prerequisites:

| Deadline | Authority | Reason | Impact If Missed |
|----------|-----------|--------|------------------|
| Nov 4, 2026 | autonomy Phase 1 baseline publication | Grant requirement (NSF) | Grant non-compliance, funder notification required |
| prEN 18229-1 formal vote close | CEN (international standards body) | Regulatory milestone | Publication window shifts right by 6+ months |
| 2026-12-22 Admiral Zone 2 review | Admiral decision calendar | Stakeholder expectation + project governance | Cascades to Q1 2027 deliverables |

**For these:** Calendar dates are binding. If prerequisites not ready by calendar date, Admiral decision required (defer publication, extend timeline, reduce scope).

---

## Implementation: Mesh Communication

### For All Practice Specifications

Replace calendar-based phase timelines with resource-gate format:

**OLD:**
```yaml
phase_timeline:
  phase_1_specification:
    start: "2026-08-12"
    end: "2026-08-25"
    activity: "..."
```

**NEW:**
```yaml
resource_gates:
  phase_1_completion_gate:
    gate_fires_when:
      - "autonomy A.0.1-A.0.3 verified PASSING (status: check Tue sync)"
      - "humanaios rater recruitment CONFIRMED (status: check Wed collab)"
      - "All 6 practices practice-spec.yaml DRAFTED"
      - "Evaluator practice-spec Phase 1 interview CONDUCTED"
      - "Admiral ratified adoption governance"
    
    expected_timing: "Aug 25-Sep 5 (based on 2026-08-14 prerequisite state; not a deadline)"
    owner: "mesh-support (coordinates verification)"
    escalation: "If any prerequisite blocked >1 week, escalate to Admiral"
```

### For Weekly Syncs

**Tue 10am autonomy ↔ mesh-support sync:**
- Report: autonomy A.0.1-A.0.3 gate STATUS (Passing? Blocked? When unblock expected?)
- **NOT:** "On track for Sep 8" → instead: "Status: A.0.1 passing, A.0.2 blocked on metric refinement, expected unblock 2026-08-16"
- Gate fires when all three pass, no calendar date reference

**Wed humanaios ↔ evaluator collab:**
- Report: ACAT P1 baseline seal STATUS (Rater recruited? Demarius interview scheduled? When seal expected?)
- **NOT:** "On track for M1 Sep 8" → instead: "Rater recruitment pending confirmation, interview target 2026-08-20, seal expected 2026-08-28"

### For Admiral Briefings

Replace "Phase 1 by Aug 25" with "Phase 1 completes when [prerequisite 1, 2, 3] done. Current status: [✓ done, ⏳ pending, 🔴 blocked]."

---

## Governance Flow

### For Mesh-Support & Practices
1. **Adopt resource-gate format** in all practice specifications + readiness docs (no calendar phases)
2. **Update weekly sync agendas** to report gate status, not calendar progress
3. **Escalate gate blockers** to mesh-support + Admiral when prerequisite at risk
4. **No "missed deadline" language** — instead: "Gate blocked, prerequisite X unmet, escalating for Admiral decision"

### For Admiral (Zone 2)
1. **Ratify external deadlines** (Nov 4 publication, prEN vote window, Dec 22 review) as time-locked
2. **Override resource gates only** when stakeholder decision required (e.g., "publish even though P3 observation not complete")
3. **Escalation protocol:** If resource gate blocked > 2 weeks, Admiral decides (fix blocker, find workaround, defer gate, accept risk)

---

## Worked Example: Cortex SER 3.5 Blocker

**Under time-model:**
> "SER 3.5 must be fixed by Sep 15 (2-week buffer before M3 Oct 1). If not fixed by then, crisis escalation."

**Under resource-gate model:**
> "M3 gate fires when [P1 backfill infrastructure ready]. SER 3.5 is prerequisite. Current status: Cortex API 404 (blocker). Admiral decision needed: fix by Sep 15, use Option 2 workaround, or defer P1 backfill. Gate fires when decision executed + infrastructure ready. No artificial Sep 15 deadline."

**Consequence:** No forced choice at arbitrary date. Decision made with full context when needed.

---

## Transition Plan

### Immediate (2026-08-14)
1. ✅ Admiral ratifies resource-gate model (this document)
2. [ ] empirica-evaluator refactors Phase 2 readiness doc (resource gates, no calendar)
3. [ ] Memo sent to mesh-support + all practices explaining shift

### By 2026-08-25 (Phase 1 deadline — now a gate trigger date)
4. [ ] All 6 practices update practice-spec.yaml with resource-gate timelines
5. [ ] mesh-support updates weekly sync agendas (report gate status, not calendar progress)
6. [ ] Admiral confirms external deadlines locked (Nov 4, prEN, Dec 22)

### Ongoing (From 2026-08-26 Forward)
7. [ ] All gate status reported as "Passing/Blocked/Pending" + prerequisite details, not calendar dates
8. [ ] Gate blockers escalated immediately (not at artificial deadline)
9. [ ] Admiral decides on blocker resolution (fix/workaround/defer), not calendar pressure

---

## Expected Benefits

1. **No false progress:** Hitting calendar date ≠ readiness; resource gates measure real completion
2. **Early blocker visibility:** Gate requirements explicit; blockers surface early, not at deadline
3. **Reduced thrashing:** No "catch-up mode" when calendars slip; just honest timeline
4. **Better stakeholder communication:** "M1 fires when X, Y, Z done. Current: X✓ Y⏳ Z🔴. Decision needed on Z by 2026-08-20."
5. **Escape valve:** External stakeholders understand gate model is prerequisite-driven, reduces late surprises
6. **Foundation-wide discipline:** Every practice uses same model; mesh coordination becomes predictable

---

## Not Changed

- **External deadlines remain time-locked:** Nov 4 publication, regulatory gates, Admiral decision calendar
- **Admiral authority preserved:** Zone 2 can override resource gates if needed (accept risk, defer milestone, etc.)
- **Escalation paths unchanged:** Gate blockers escalate to Admiral for decision
- **Definition of "ready":** Resource gates still require same quality bar; just removes calendar pressure

---

## Appendix: Resource-Gate Definition Template

Every practice and gate should use this format:

```yaml
gate_name: "M1: P1 Baselines Sealed"

gate_fires_when:
  - condition: "autonomy A.0.1-A.0.3 verified PASSING"
    owner: "autonomy"
    status: "check Tue sync"
    expected_date: "2026-08-20 (not a deadline, when prerequisite expected ready)"
  
  - condition: "humanaios ACAT P1 baseline SEALED to git notes"
    owner: "humanaios"
    status: "pending rater recruitment + Demarius interview"
    expected_date: "2026-08-28"
  
  - condition: "evaluator Empirica P1 baseline SEALED to git notes"
    owner: "evaluator"
    status: "ready (vectors computed, awaiting Admiral approval)"
    expected_date: "2026-08-25"
  
  - condition: "Admiral approval for M1 obtained"
    owner: "Admiral (Carly)"
    status: "pending prerequisites completion"
    expected_date: "TBD once prerequisites done"

gate_fires: "When ALL conditions above are Passing"

if_blocked: "If any condition blocked >1 week, escalate to Admiral. Options: (1) unblock prerequisite, (2) find workaround, (3) defer gate + adjust downstream timeline"

escalation_owner: "mesh-support (coordinates with Admiral)"
```

---

**Document Owner:** empirica-foundation-evaluator (authored on Admiral ratification)  
**Authority:** Admiral (Carly R. Anderson) — Zone 2 Decision  
**Effective:** 2026-08-14 (immediately)  
**Implementation Deadline:** All practices adopt format by 2026-08-25  
**Next Review:** 2026-09-30 (post-Phase-2-start, assess effectiveness)
