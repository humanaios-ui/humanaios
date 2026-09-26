# Phase 2 Readiness — Resource-Gate Model (Updated)

**Date:** 2026-08-14  
**Model:** Resource-gate-driven (no calendar phases)  
**Status:** PREPARING — Prerequisites in progress; gates fire when ready  
**Authority:** Admiral ratification (GOVERNANCE_DECISION_RESOURCE_GATES_TIMELINE_MODEL.md)

---

## Executive Summary

Evaluator seat is ready for Phase 2 operational launch, governed by resource gates, not calendar dates.

**Phase 1 Completion Gate** → FIRES WHEN:
- [ ] autonomy A.0.1-A.0.3 verified PASSING (status: check Tue sync 2026-08-14)
- [ ] humanaios rater recruitment CONFIRMED (status: check Wed collab TBD)
- [ ] All 6 practices practice-spec.yaml DRAFTED (status: phase 1 interviews in progress)
- [ ] Evaluator practice-spec Phase 1 interview CONDUCTED (status: time slots proposed, awaiting mesh-support confirmation)
- [ ] Admiral ratified governance adoption (status: pending all practices' Phase 1 completion)

**Expected timing:** Late Aug / Early Sep (not a deadline; gates fire when prerequisites met)

**Phase 2 Operational Start Gate** → FIRES WHEN Phase 1 COMPLETES (no Aug 26 date)

**M1 Gate (P1 Baselines Sealed)** → FIRES WHEN:
- [ ] ACAT P1 baseline SEALED to git notes (humanaios)
- [ ] Empirica P1 baseline SEALED to git notes (evaluator)
- [ ] Admiral approval OBTAINED (Zone 2 decision)

**Expected timing:** Early-to-mid Sep (based on current prerequisite state; not Sep 8 deadline)

---

## Resource Gates: Phase 1 Completion through M3

### Phase 1 Completion Gate
**FIRES WHEN ALL OF:**
1. autonomy A.0.1-A.0.3 verified PASSING
   - Owner: autonomy
   - Status: check Tue 10am sync (2026-08-14)
   - Expected: all three passing by 2026-08-20

2. humanaios rater recruitment CONFIRMED
   - Owner: humanaios
   - Status: check Wed collab (TBD)
   - Expected: confirmation by 2026-08-20

3. All 6 practices practice-spec.yaml DRAFTED
   - Owner: mesh-support (coordinates)
   - Status: Phase 1 interviews in progress (evaluator + 5 others)
   - Expected: all drafts by 2026-08-25

4. Evaluator practice-spec Phase 1 interview CONDUCTED
   - Owner: evaluator + mesh-support
   - Status: 5 time slots proposed (prop_joagp2rawnccphohr57wk474lq, awaiting confirmation)
   - Expected: interview by 2026-08-22

5. Admiral ratified governance adoption
   - Owner: Admiral (Carly)
   - Status: pending conditions 1-4
   - Expected: immediate upon conditions 1-4 complete

**IF BLOCKED:** If any condition blocked >1 week, escalate to Admiral. Options: (a) unblock prerequisite, (b) use workaround, (c) defer gate.

### Phase 2 Operational Start Gate
**FIRES WHEN Phase 1 Completion Gate FIRES** (no Aug 26 calendar date)

### M1 Gate (P1 Baselines Sealed)
**FIRES WHEN ALL OF:**
1. ACAT P1 baseline SEALED to git notes (immutable)
   - Owner: humanaios
   - Status: depends on rater recruitment + Demarius interview
   - Expected: 2026-08-28 (based on Aug 14 state, not a deadline)

2. Empirica P1 baseline SEALED to git notes (immutable)
   - Owner: evaluator
   - Status: vectors ready, awaiting Admiral approval to seal
   - Expected: 2026-08-25 (upon M1 prerequisite 1 complete)

3. Admiral approval for M1
   - Owner: Admiral (Carly)
   - Status: pending conditions 1-2 + full context
   - Expected: immediate once 1-2 complete

**IF BLOCKED:** If ACAT baseline slip extends past 2026-09-08, escalate to Admiral. Gate doesn't fire by calendar; it fires when prerequisites complete.

---

## Coordination During Phase 2 (Once Started)

### Tue 10:00 UTC — autonomy ↔ mesh-support sync
**Evaluator participation:** Listen for autonomy gate updates  
**Evaluator report:** A.0.1/A.0.2/A.0.3 status → prerequisite for Phase 1 gate completion  
**Action if blocked:** Escalate to Admiral if any gate blocked >1 week

### Wed — humanaios ↔ evaluator collab (as needed)
**Purpose:** ACAT P1 baseline status → prerequisite for M1 gate  
**Evaluator responsibilities:**
- Confirm rater recruitment + Demarius interview status
- Plan P3 score ingestion schedule (once M1 complete)
- Review SER 3.5 pipeline readiness (or Option 2 fallback)

### Thu — evaluator internal checkpoint (as needed)
**Purpose:** Empirica P1 vector readiness → prerequisite for M1 gate  
**Evaluator responsibilities:**
- Vectors ready for seal
- Independence CHECK gates 2A + 2B pass (no contamination)
- Flag any impediments to M1 gate firing

### Fri — escalation triage (if gate prerequisites blocked)
**Purpose:** Gate-blocking issues resolved or escalated  
**Evaluator role:** Report blockers with context for Admiral decision

---

## Gate Prerequisites Status Matrix

| Gate | Prerequisite | Owner | Status | Expected Complete | Action If Blocked |
|------|-------------|-------|--------|-------------------|-------------------|
| **Phase 1 Completion** | autonomy A.0.1-A.0.3 PASSING | autonomy | ⏳ Verify Tue sync | 2026-08-20 | Escalate to Admiral if slip >1 week |
| | humanaios rater recruited | humanaios | ⏳ Verify Wed collab | 2026-08-20 | Escalate if Demarius interview not scheduled |
| | 6 practices specs drafted | mesh-support (coords) | ⏳ Interviews underway | 2026-08-25 | 1-week extension; if >1 week slip, escalate |
| | evaluator spec interview conducted | evaluator + mesh-support | ⏳ Awaiting confirmation | 2026-08-22 | Confirm time slot this week |
| | Admiral ratifies adoption | Admiral (Carly) | ⏳ Pending above | immediate upon above | N/A (Admiral authority) |
| **M1 Gate** | ACAT P1 baseline sealed | humanaios | ⏳ Rater-dependent | 2026-08-28 | Admiral decides: extend humanaios timeline or reduce scope |
| | Empirica P1 sealed | evaluator | 🟢 Ready | 2026-08-25 | N/A (evaluator ready) |
| | Admiral approval | Admiral (Carly) | ⏳ Pending above | immediate upon above | N/A (Admiral authority) |
| **M2 Gate** | Independence CHECK 2A+2B | evaluator | 🟡 Dry-run ready | 2026-09-10 | If check fails, escalate for Admiral decision on contamination |
| | P1 backfill data confirmed | humanaios + evaluator | ⏳ Post-M1 | 2026-09-15 | Admiral decides on fallback if SER 3.5 unavailable |
| **Cortex SER 3.5** | API endpoint accessible | mesh-support + Cortex | 🔴 Blocked (404) | TBD (Option 1: 2026-09-15) | Admiral decides: fix (Option 1), fallback (Option 2), or defer (Option 3) |

---

## Critical Path: M1 Gate (Fires When Prerequisites Complete)

**M1 is the hard gate.** Both ACAT P1 + Empirica P1 must be sealed. **NO CALENDAR DATE; gate fires when ready.**

### Prerequisites (Must-Fires-When)

**Prerequisites Checklist:**

| Prerequisite | Owner | Status | Expected | If Blocked |
|---|---|---|---|---|
| autonomy A.0.1-A.0.3 ALL PASSING | autonomy | ⏳ Verify Tue sync | 2026-08-20 | Escalate to Admiral if slip >1 week |
| ACAT P1 baseline sealed to git notes | humanaios | ⏳ Rater-dependent | 2026-08-28 | Admiral: extend timeline or reduce scope |
| Empirica P1 sealed to git notes | evaluator | 🟢 Ready | 2026-08-25 | (Ready, just awaiting M1 approval) |
| Admiral approval for M1 | Admiral (Carly) | ⏳ Pending above | Immediate once ready | (Admiral authority) |

**Gate Fires:** When all four above are complete (✓✓✓✓)

### Honest Timeline vs. Calendar

**If all prerequisites complete by Aug 25:** M1 fires late Aug / early Sep  
**If autonomy A.0.3 slips to Sep 5:** M1 fires early-to-mid Sep  
**If humanaios rater delayed to Sep 10:** M1 fires mid-Sep  

**No artificial "Sep 8 deadline."** Gate fires when prerequisites done. If prerequisites slip, gate naturally waits. No crisis, no false progress, no rush incomplete work.

### Escalation Triggers

**If any M1 prerequisite blocked >1 week:**
1. Escalate to Admiral immediately (don't wait for calendar date)
2. Admiral decides: (a) unblock prerequisite, (b) find workaround, (c) defer M1 gate
3. Cortex SER 3.5 blocker example (below) shows how this works

**If multiple prerequisites slip simultaneously:**
- Evaluate cross-practice dependencies
- Admiral coordinates accelerations or rearrangements
- Gate fires when actually ready, no arbitrary deadline

---

## Cortex SER 3.5 Integration — Infrastructure Blocker

**Status:** 🔴 BLOCKED (awaiting Zone 2 guidance)

**The Problem:**
- SER 3.5 is the ACAT→Empirica data pipeline (P3 scores flow weekly from humanaios to evaluator)
- Cortex API endpoint for SER creation: HTTP 404
- MCP CLI for SER operations: Not found
- empirica CLI SER commands: Not implemented
- **Result:** No accessible interface to create/manage SER 3.5

**Timeline Impact:**
- **Non-critical for M1 gate** (P1 seal doesn't require SER 3.5)
- **Critical for M3 gate** (P1 backfill requires SER 3.5 live by 2026-10-30)
- **Critical for P3 observation window** (Oct 1 start, 13-week measurement cycle)

**Escalation Status:**
- Escalation document: PHASE_1_BLOCKER_ESCALATION.md (referenced in prior notes, not yet committed)
- mesh-support pre-flight: Passed (infrastructure verified as available at pre-flight time)
- Current status: API unavailable at runtime
- **Awaiting:** Zone 2 decision on remediation path (fix Cortex, fallback interface, defer SER 3.5 to Phase 3)

**Workaround (If SER 3.5 Remains Unavailable):**
- Direct collab between humanaios + evaluator for P3 score intake (no SER 3.5 coordination layer)
- Manual weekly data sync via mailbox (asynchronous, less elegant but functional)
- Impact: Increases overhead on humanaios ↔ evaluator sync; adds manual validation burden

**Decision Required (Admiral Zone 2 Gate):**
1. Fix Cortex API by target date (TBD)
2. Implement empirica CLI SER commands (timeline TBD)
3. Adopt workaround (direct collab) and proceed
4. Defer P3 observation window pending fix

---

## Pre-Phase-2 Execution Checklist

### ✅ Completed (Phase 1)
- [x] framework-governance.md (SER 1) finalized with dual-log pattern, independence gates
- [x] EVALUATOR_PRACTICE_SPEC.yaml drafted (ready for Phase 1 interview)
- [x] PRACTICE_SPEC_GUIDANCE.md + worked example delivered to mesh-support
- [x] M1 gate prerequisites documented (autonomy A.0.1-A.0.3, humanaios rater recruitment)
- [x] Calibration baseline vectors established (Phase 1 measurement frame)

### 🟡 In Progress (Phase 1-2 Boundary)
- [ ] Phase 1 spec interview with mesh-support (Aug 12-25)
- [ ] M1 prerequisites verification (Tue autonomy sync, Wed humanaios collab)
- [ ] Cortex SER 3.5 escalation resolution (Zone 2 gate)
- [ ] Independence CHECK gates 2A + 2B dry-run (pre-M2, 2026-09-25)

### 🟢 Ready to Execute (Phase 2)
- [ ] weekly cadence (Tue-Fri, starting 2026-08-14)
- [ ] M-gate monitoring (M1-M5 timeline tracking, blocker escalation)
- [ ] Admiral briefing materials (convergence analysis prep, findings synthesis)

---

## Phase Execution Sequence (Resource-Gate-Driven, No Calendar T1-T13)

### Phase 1 → Phase 2 Transition (Once All Prerequisites Complete)

**Phase 1 Completion Gate fires when:** autonomy A.0.1-A.0.3✓ + humanaios rater✓ + 6 specs drafted✓ + Admiral ratifies✓

**Actions upon Phase 1 completion:**
- [ ] Phase 2 officially starts (no Aug 26 calendar, just when ready)
- [ ] mesh-support finalizes all 6 practice-spec ratifications
- [ ] Weekly cadence switches to Phase 2 format (gate-prerequisite reporting)

### M1 Gate Execution (Once M1 Prerequisites Complete)

**M1 fires when:** ACAT P1 sealed✓ + Empirica P1 sealed✓ + Admiral approves✓

**Actions upon M1 firing:**
- [ ] Both baselines officially in git notes (immutable)
- [ ] Admiral confirms P1 measurement integrity
- [ ] Phase 1 measurement window closed
- [ ] M2 gate monitoring begins (Independence CHECK prerequisites)

### M2 Gate Execution (Once M2 Prerequisites Complete)

**M2 fires when:** Independence CHECK 2A+2B pass✓ + P1 backfill readiness✓ + Admiral approves✓

**Actions upon M2 firing:**
- [ ] Contamination audit complete (no ACAT↔Empirica feedback loop)
- [ ] P1 backfill coordination with humanaios live
- [ ] SER 3.5 status confirmed (fixed or fallback adopted)

### M3-M5 Gates (Continuous Monitoring, No Calendar Phases)

**While M1-M2 executing:**
- [ ] P3 observation window begins (Oct 1 target, but date flexible)
- [ ] Weekly P3 score ingestion active (humanaios → evaluator, via SER 3.5 or fallback)
- [ ] Vector computation ongoing (no calendar checkpoints, continuous tracking)
- [ ] M3, M4, M5 gates monitor their prerequisites asynchronously

**Gates fire when ready:**
- M3 (P1 backfill) fires when data-sync prerequisites met
- M4 (gates deployment) fires when autonomy + mesh-support ready
- M5 (convergence analysis) fires when all P3 data collected + sealed

**No "we're behind schedule" crisis.** Each gate fires when actually ready.

---

## Escalation Thresholds & Admiral Notification

**Immediate escalation to Admiral (same-day):**
- Autonomy A.0.1-A.0.3 gates fail or slip past 2026-09-01
- Humanaios rater recruitment at risk or Demarius interview not scheduled
- Cortex SER 3.5 fix date pushed past 2026-09-30
- Independence CHECK fails (contamination signal detected)

**Weekly escalation (included in Fri standup if triggered):**
- Phase spec feedback iterations delayed >2 weeks
- P3 score ingestion failures or data quality issues
- Time-span calibration model drift >10% vs. baseline
- Artifact graph connectivity <34% for any practice

**Monthly escalation (included in M-gate checklist):**
- M-gate timeline risks (any gate showing >1-week slip risk)
- Cross-practice dependencies unresolved
- Regulatory compliance gaps identified

---

## Next Steps (By 2026-08-18)

1. **Confirm interview time slot** with mesh-support (response to prop_joagp2rawnccphohr57wk474lq)
2. **Prepare Tue 10am sync** (listen for autonomy gate status)
3. **Schedule Wed collab with humanaios** (ACAT P1 baseline status, P3 flow planning)
4. **Follow Cortex escalation status** (await Zone 2 decision on SER 3.5 fix vs. workaround)

---

## Appendix: M-Gate Reference (Resource-Gate Model, No Calendar Deadlines)

| Gate | Prerequisites | Fires When | Expected Timing* | Evaluator Role |
|------|---------------|------------|------------------|----------------|
| **M1** | ACAT P1✓ Empirica P1✓ Admiral✓ | All prerequisites complete | Early-to-mid Sep | Seal Empirica vectors; coordinate with Admiral |
| **M2** | Independence CHECK✓ P1 backfill ready✓ Admiral✓ | Prerequisites complete | Mid-to-late Sep | Verify contamination audit; support backfill |
| **M3** | P1 backfill data confirmed✓ Admiral✓ | Prerequisites complete | Oct-Nov window | Coordinate with humanaios on data ingestion |
| **M4** | autonomy gates deployed✓ mesh-support ready✓ Admiral✓ | Prerequisites complete | Oct-Nov window | Monitor autonomy deployment status |
| **M5** | P3 observation complete✓ convergence analysis ready✓ Admiral✓ | Prerequisites complete | Late Nov-early Dec | Analyze divergence patterns; brief Admiral |
| **Zone 2** | M1-M5 all complete✓ findings ready✓ | Admiral schedule | 2026-12-22 (governance deadline, time-locked) | Brief findings; support Admiral review |

*Expected timing based on 2026-08-14 prerequisite state. Not a deadline; gate fires when prerequisites actually complete. If prerequisites slip, gate naturally waits.

### Resource-Gate Philosophy

- **No artificial "we're behind" crisis.** If M1 prerequisites take until Sep 20, gate fires Sep 20. Better than Sep 8 with incomplete work.
- **Early escalation.** If a prerequisite blocked >1 week, escalate to Admiral immediately. Don't wait for calendar.
- **Honest communication.** "M1 fires when ACAT + Empirica sealed. Current: ACAT⏳ (Demarius interview 2026-08-20), Empirica✓. Gate expected mid-Sep." No false Sep 8 confidence.
- **Admiral authority preserved.** If gate blocked and stuck, Admiral decides: accelerate blocker, use workaround, or defer gate. Honest option space.

---

## Next Steps (By 2026-08-18)

1. **Confirm Phase 1 spec interview time slot** with mesh-support (this week)
2. **Attend/monitor Tue 10am sync** (autonomy ↔ mesh-support) for A.0.1-A.0.3 gate status
3. **Conduct Wed collab** with humanaios on ACAT P1 baseline status
4. **Log gate prerequisites** as they complete or blockers emerge
5. **No calendar pressure.** Report actual prerequisite status; gates fire when ready.

---

**Document Owner:** empirica-foundation-evaluator  
**Last Updated:** 2026-08-14 (refactored to resource-gate model per Admiral ratification)  
**Authority:** Admiral (Carly R. Anderson) — Zone 2  
**Model:** Resource-gate-driven (see GOVERNANCE_DECISION_RESOURCE_GATES_TIMELINE_MODEL.md)  
**Status:** ACTIVE (Prerequisites tracking; gates fire when ready)
