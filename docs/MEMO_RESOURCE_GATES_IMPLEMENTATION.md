# MEMO: Resource-Gate Timeline Model — Implementation for Mesh-Support & Practices

**TO:** empirica-mesh-support, all foundation practices (autonomy, humanaios, outreach, website, empirica-autonomy)  
**FROM:** empirica-foundation-evaluator (on Admiral ratification)  
**DATE:** 2026-08-14  
**RE:** Governance decision effective immediately — shift to resource-gate coordination  
**AUTHORITY:** Admiral (Carly R. Anderson), Zone 2

---

## Summary

Effective **2026-08-14**, the mesh coordination model shifts from **time-driven** (calendar dates, phases) to **resource-gate-driven** (prerequisites, readiness).

**Key change:** Milestones fire when prerequisites complete, not on calendar dates. External governance deadlines (Nov 4 publication, regulatory gates) remain time-locked.

**Impact:** No "missed deadline" crises; early blocker visibility; honest timelines.

---

## What Changes

### OLD MODEL (Time-Driven)
```
Phase 1: Aug 12-25 (calendar)
M1 gate: Sep 8 (calendar)
M2 gate: Sep 25 (calendar)
...
IF prerequisites slip: artificial crisis at fixed date
```

### NEW MODEL (Resource-Gate-Driven)
```
Phase 1: ENDS WHEN [autonomy A.0.1-A.0.3 pass] AND [humanaios rater recruited] 
         AND [all 6 practices draft specs]
         (No calendar date; fires when ready)

M1 gate: FIRES WHEN [ACAT P1 sealed] AND [Empirica P1 sealed] AND [Admiral approves]
         (No Sep 8; fires when ready)

M2 gate: FIRES WHEN [independence checks pass] AND [P1 backfill data confirmed]
         (No Sep 25; fires when ready)
...
IF prerequisites slip: gate naturally waits, no artificial deadline pressure
```

### External Deadlines (UNCHANGED, Time-Locked)
- Nov 4: autonomy Phase 1 baseline publication (grant requirement)
- TBD: prEN 18229 formal vote window (regulatory)
- 2026-12-22: Admiral Zone 2 review window (governance expectation)

---

## For Mesh-Support

### Action Items (By 2026-08-25)

1. **Update all 6 practice-spec templates** from calendar phases to resource-gate format
   - Provide template: `gate_fires_when: [condition 1, condition 2, ...]`
   - Remove: `start: "2026-08-XX"`, `end: "2026-08-YY"`
   - Add: `expected_timing: "early Sep (based on Aug 14 prerequisite state; not a deadline)"`

2. **Revise weekly sync agendas** (Tue 10am autonomy ↔ mesh-support)
   - OLD: "Are we on track for M1 Sep 8?"
   - NEW: "A.0.1 status? A.0.2 status? A.0.3 status? When all passing?"
   - Focus: gate prerequisites, not calendar

3. **Escalation protocol update**
   - If any M-gate prerequisite blocked >1 week: escalate to Admiral
   - Provide option list: (1) unblock prerequisite, (2) find workaround, (3) defer gate
   - Admiral decides, not calendar

4. **Comms to all practices**
   - Explain: resource-gate model, why it's better (no false deadlines), what changes
   - Share: GOVERNANCE_DECISION_RESOURCE_GATES_TIMELINE_MODEL.md
   - Ask: update practice-spec by 2026-08-25 with resource-gate timelines

### Status Reporting Format (Immediate)

**OLD:**
> "M1 gate on track for Sep 8. Autonomy gates 90% complete. Humanaios rater recruitment pending."

**NEW:**
> "M1 prerequisites: autonomy A.0.1✓ A.0.2✓ A.0.3⏳ (metric refinement due 2026-08-20); humanaios rater🔴 (confirmation pending); evaluator P1✓. Gate fires when A.0.3✓ + rater✓ + Admiral approves."

Focus: gate completion, not calendar progress.

---

## For All Practices

### What You're Changing

1. **Your practice-spec.yaml**
   - Replace calendar-based `phase_timeline` with `resource_gates`
   - List prerequisites for each gate
   - Provide "expected timing" based on current prerequisite state (not a deadline)

2. **Your readiness status**
   - Report: gate prerequisites (✓ done, ⏳ pending, 🔴 blocked)
   - NOT: "on track for Aug 25"

3. **Your escalation triggers**
   - If prerequisite blocked >1 week: escalate to mesh-support + Admiral
   - NOT: wait for calendar deadline to cry wolf

### Example: empirica-autonomy Practice Spec

**OLD:**
```yaml
phase_timeline:
  phase_1_gates:
    start: "2026-08-08"
    end: "2026-08-25"
    success_criteria:
      - "A.0.1 gate passing"
      - "A.0.2 gate passing"
      - "A.0.3 gate passing"
```

**NEW:**
```yaml
resource_gates:
  phase_1_completion_gate:
    gate_fires_when:
      - "A.0.1 metric validation PASSING (status: ✓ done)"
      - "A.0.2 connectivity metric PASSING (status: ⏳ refinement due Aug 20)"
      - "A.0.3 state machine verification PASSING (status: ⏳ testing phase due Aug 22)"
    
    expected_timing: "Aug 22-25 (based on 2026-08-14 status, not a deadline)"
    gate_fires: "When all three passing + Admiral approval obtained"
    
    if_blocked: "If A.0.2 or A.0.3 slip past Aug 25, notify mesh-support immediately. 
                 Admiral decides: accelerate, find workaround, or defer."
```

---

## For Admiral

### Decision Authority (Preserved)

1. **External deadlines remain locked** (you can modify, but with intent)
   - Nov 4 Phase 1 baseline publication: can defer to Nov 11 if prerequisites not ready, but must decide
   - prEN vote window: regulatory, but you know exact window from CEN
   - Dec 22 Zone 2 review: your decision calendar, can shift if needed

2. **Resource gates are now your escalation points**
   - If gate blocked >1 week, mesh-support escalates
   - You decide: (a) unblock prerequisite, (b) find workaround, (c) defer gate
   - Example: "Cortex SER 3.5 blocked? Use Option 2 workaround + proceed to M3."

3. **No artificial deadlines**
   - If a gate naturally waits because prerequisites aren't done, that's the right call
   - Hitting an arbitrary calendar date without readiness = false progress (not acceptable)

---

## FAQ for Practices

**Q: Does this mean we can just delay forever?**  
A: No. External deadlines are still locked (Nov 4 publication, regulatory dates). Internal gates fire when ready. If a gate is blocked, Admiral decides on workaround or defer, not delay indefinitely.

**Q: What if a prerequisite is blocked forever?**  
A: Escalate to Admiral. Options: fix the blocker, use a workaround, or officially defer the gate. Decision made with eyes open, not at an artificial calendar deadline.

**Q: How do we communicate timelines to stakeholders?**  
A: "M1 gate fires when [prerequisite 1, 2, 3]. Current status: 1✓ 2✓ 3⏳ (expected unblock 2026-08-20). Stakeholders see honest progress, not false calendar confidence."

**Q: What about dependencies between my work and other practices?**  
A: That's why resource gates list prerequisites and owners. If you depend on autonomy A.0.3, your gate lists "autonomy A.0.3 passing" as a prerequisite. When autonomy is done, your gate can fire. Transparent, not hidden in calendar magic.

**Q: Does this change the quality bar?**  
A: No. Resource gates still require the same rigor. We're just removing artificial time pressure and being honest about when we're actually ready.

---

## Implementation Checklist (For Mesh-Support)

- [ ] Send this memo + governance decision doc to all 6 practices
- [ ] Provide template: resource-gate format + example (autonomy, humanaios, evaluator)
- [ ] Update Tue 10am sync agenda (gate status, not calendar progress)
- [ ] Update weekly standup template (prerequisites ✓/⏳/🔴, not "on track for X date")
- [ ] Create escalation tracker: gate + prerequisite + owner + blocker status + escalation date (if >1 week blocked)
- [ ] Brief Admiral on new status reporting format
- [ ] Confirm all practices update practice-spec by 2026-08-25

---

## Rationale (If Questioned)

**Why not calendar dates?**

Calendar dates create artificial crisis points. If autonomy A.0.3 gate slips from Aug 25 to Sep 5, the entire mesh feels like it "failed." But actually, we're doing the right thing: waiting for readiness instead of shipping incomplete work.

Resource gates flip the model: gates fire when ready. Blockers are visible early (not at deadline crisis). Admiral makes decisions on blockers with full context, not time pressure.

**Why keep external deadlines?**

External governance (grants, regulators, stakeholder commitments) has real deadlines. Nov 4 publication is a grant requirement, not negotiable. But if prerequisites aren't ready by Oct 20, Admiral explicitly decides: push publication to Nov 11, reduce scope, or find workaround. Honest decision, not artificial time crunch.

---

## Stakeholder Communication Template

For Carly (Admiral) to use when external parties ask "when is M1?"

> "M1 gate fires when three prerequisites complete: autonomy A.0.1-A.0.3 validated, ACAT P1 baseline sealed, Empirica P1 baseline sealed, and I approve. Current status: [✓✓✓✓ all done → M1 fires within 48h], or [✓✓⏳ waiting on ACAT baseline → M1 fires once baseline sealed, expected 2026-08-28]. We coordinate by readiness, not calendar. This means no false deadlines, but also no surprises when blockers surface."

---

## Next Steps

1. **Admiral confirms** external deadlines (Nov 4, prEN, Dec 22) locked, or adjusts if needed
2. **mesh-support sends** memo + template to all 6 practices
3. **All practices update** practice-spec.yaml by 2026-08-25
4. **Tue 10am sync** (2026-08-14) first reporting with gate status (not calendar progress)
5. **Weekly review** of gate-blocking prerequisites; escalate if >1 week blocked

---

## Questions?

mesh-support: coordinate with Admiral on any clarifications  
Practices: ask mesh-support for template help or examples  
Admiral: make decision if any gate blocked; resource model enables faster decisions because blockers are visible early

---

**Document Owner:** empirica-foundation-evaluator (authored on Admiral ratification)  
**Authority:** Admiral (Carly R. Anderson) — Zone 2  
**Effective:** 2026-08-14  
**To:** mesh-support, autonomy, humanaios, outreach, website, empirica-autonomy

---

*This memo is the formal communication of the governance decision. Included: GOVERNANCE_DECISION_RESOURCE_GATES_TIMELINE_MODEL.md (full rationale + implementation) for any practice wanting the complete context.*
