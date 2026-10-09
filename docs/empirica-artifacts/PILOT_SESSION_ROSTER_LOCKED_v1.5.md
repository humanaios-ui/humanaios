# PILOT SESSION ROSTER (LOCKED)
## ACAT-CAL-P v1.5 Measurement Phase

**Charter Date:** 2026-07-30  
**Charter Issued By:** Carly Anderson (Z2, Night)  
**Status:** ✓ LOCKED — Sessions 1–5 formally identified; no retroactive changes permitted

---

## PILOT SESSION IDENTIFICATION (Goal-Scoped)

**Five pilot sessions in goal-scoped selection** (not pure ritual order). Each session advances one or more of the four active goals:

| Goal | Priority | Sessions Advancing |
|---|---|---|
| H-ACAT Phase 3 | 1 (Protocol finalization) | S1, S2–S5 |
| SER 1 | 1 (Measurement baseline) | S1–S5 |
| SER 3.5 | 1 (Feedback loop calibration) | S1–S5 |
| Phase 1 validation | 2 (Evaluator engagement) | S2–S5 |

---

## SESSION ROSTER

### Session 1: Baseline Ops Governance Review (COMPLETE)

**Session ID:** S-073026-OPS  
**Charter Date Confirmation:** 2026-07-30  
**Start Date:** 2026-07-30  
**Work Type:** config  
**Coder Config:** claude-opus-5, seed=684, temp=0  
**Status:** ✓ COMPLETE

**Scope:**
- Protocol §1–§11 operationalization review
- Appendix A (A.1–A.7) checklist verification
- Coder configuration confirmation
- Red-team staging validation
- D-1 & D-2 decision operationalization

**Artifacts Logged:**
- 6 findings (framework confirmation, dimension updates, operationalization status)
- 6 decisions (D-1, D-2, goal-scoping, charter confirmation)
- 4 assumptions (coder determinism, goal-scoped sessions, empirical data behavior, red-team success)

**Goals Advanced:**
- H-ACAT Phase 3 ✓ (protocol operationalization complete)
- SER 1 ✓ (baseline established)
- SER 3.5 ✓ (measurement window opened)

---

### Session 2: [Reserved for Next Goal]

**Session ID:** S-073027-G1  
**Charter Date:** 2026-07-30  
**Start Date:** TBD (after Session 1 completion)  
**Work Type:** TBD  
**Coder Config:** claude-opus-5, seed=684, temp=0  
**Status:** ⧗ PENDING

**Scope:** To be assigned based on goal advancement needs (H-ACAT Phase 3, Phase 1 validation, or SER continuation)

**Red-Team Active:** §11.1–3 execution (parallel with Sessions 2–3)

---

### Session 3: [Reserved for Next Goal]

**Session ID:** S-073028-G2  
**Charter Date:** 2026-07-30  
**Start Date:** TBD  
**Work Type:** TBD  
**Coder Config:** claude-opus-5, seed=684, temp=0  
**Status:** ⧗ PENDING

**Scope:** To be assigned based on goal advancement needs

**Red-Team Active:** §11.1–3 execution (parallel with Sessions 2–3)

---

### Session 4: [Reserved for Next Goal]

**Session ID:** S-073029-G3  
**Charter Date:** 2026-07-30  
**Start Date:** TBD  
**Work Type:** TBD  
**Coder Config:** claude-opus-5, seed=684, temp=0  
**Status:** ⧗ PENDING

**Scope:** To be assigned based on goal advancement needs

---

### Session 5: [Reserved for Pilot Completion]

**Session ID:** S-073030-FINAL  
**Charter Date:** 2026-07-30  
**Start Date:** TBD  
**Work Type:** TBD  
**Coder Config:** claude-opus-5, seed=684, temp=0  
**Status:** ⧗ PENDING

**Scope:** Final measurement session; red-team §11.1–3 reports due by end of this session

**Milestone:** Codebook freeze gate — Appendix A checklist signed by Z2 upon red-team PASS

---

## CHARTER DAY LOCKED

**Charter Date:** 2026-07-30  
**Confirmed By:** Carly Anderson (Z2, Night)  
**Lock Status:** ✓ IMMUTABLE

**Sunset Clock:** 5 sessions from 2026-07-30
- Session 1: 2026-07-30 ✓ Complete
- Session 2: By 2026-07-31
- Session 3: By 2026-08-01
- Session 4: By 2026-08-02
- Session 5: By 2026-08-03

**Sunset Expiration:** Session 6 (2026-08-04+) — If all 5 sessions not complete by then, protocol auto-downgrades to EXPIRED-DRAFT

---

## ARTIFACT LOGGING AUTOMATION

**Status:** ✓ ACTIVE

**Memory Files (Real-Time Capture):**
- `memory/session_1_artifacts.md` — Session 1 findings, decisions, assumptions (captured)
- `memory/session_2_artifacts.md` — Session 2 artifacts (to be created at S2 start)
- `memory/session_3_artifacts.md` — Session 3 artifacts (to be created at S3 start)
- `memory/session_4_artifacts.md` — Session 4 artifacts (to be created at S4 start)
- `memory/session_5_artifacts.md` — Session 5 artifacts (to be created at S5 start)

**Batch-Submit Protocol:**
- At end of each session POSTFLIGHT, batch-submit via: `empirica log-artifacts - < memory/session_N_artifacts.md`
- All findings, decisions, assumptions logged with full grounding in session work context

**Real-Time Workflow:**
1. Session opens → `memory/session_N_artifacts.md` created
2. Work proceeds → Artifacts captured in real-time (findings, decisions, assumptions)
3. Session closes → POSTFLIGHT → Batch-submit to empirica
4. Next session opens → New `memory/session_N+1_artifacts.md` file

---

## RED-TEAM EXECUTION SCHEDULE

**Parallel with Sessions 1–2 coding:**
- §11.1: Codebook robustness stress test (independent coders, alternative rule sets)
- §11.2: Model-family correlation study (valence + segmentation agreement across families)
- §11.3: Availability ambiguity battery (edge-case classification agreement)

**Reports Due:** Before Session 5 coding completes

**Success Criteria:**
- §11.1: Spread < 2× (boundary rules robust)
- §11.2: Cross-family ρ > intra-family delta (independent judgments)
- §11.3: κ ≥ 0.80 (availability test clear)

**Gate:** All three PASS → Codebook freeze ✓ → Protocol ready for production (Sessions 6+)

---

## PRE-PILOT CHECKLIST (All Items Locked)

**Z2 Ratified Decisions (7 Items):**
- ✓ Item 1: Extended-dimension names (6 canonical: scheme, power, syc, consist, fair, handoff) — D-1
- ✓ Item 2: Hard-constraint breach definitions (A+B dual validation) — D-2
- ✓ Item 3: α_human–model gate (≥0.60)
- ✓ Item 4: Per-operation boundary units (A.2 frozen)
- ✓ Item 5: Stratification for reliability subset (≥20%, stratified random)
- ✓ Item 6: Comparator choice (NIST RMF 1.0)
- ✓ Item 7: Pilot session roster (goal-scoped, 5 sessions, IDs assigned)

**Operationalization (Appendix A):**
- ✓ A.2: Boundary units frozen
- ✓ A.3: Availability tree locked
- ✓ A.4: Reliability stratification specified
- ✓ A.5: Breach definitions (A+B dual-standard)
- ✓ A.6: Stopping-rule script ready
- ✓ A.7: Checklist fully signed

**Coder Preparation:**
- ✓ Configuration pinned (Opus 5, seed 684, temp=0)
- ✓ Codebook + A.2–A.6 operationalization provided
- ✓ Granularity intent filed (O1–O7 interpretation)

**Red-Team:**
- ✓ §11.1–3 materials prepared
- ✓ Schedule for reports (due before S5 completion)
- ✓ §11.4–6 watch-items planned

**Governance:**
- ✓ Z2 Charter memo signed
- ✓ A.7 checklist fully signed
- ✓ Sunset clause noted (5 sessions from 2026-07-30)
- ✓ Pilot sessions locked (S-073026-OPS through S-073030-FINAL)

---

## PILOT PHASE STATUS

**Phase:** MEASUREMENT (Sessions 1–5 live)  
**All Gates Closed:** ✓ YES  
**Ready to Execute:** ✓ YES

**Charter Day:** 2026-07-30 (LOCKED)  
**Session 1 Status:** ✓ COMPLETE (ops governance baseline)  
**Sessions 2–5 Status:** ⧗ READY TO BEGIN

---

*Pilot Session Roster (Locked). All five sessions formally identified, IDs assigned, charter day confirmed, artifact logging active. Ready for measurement phase execution.*

✓ **Z2 RATIFIED**  
✓ **PILOT MEASUREMENT PHASE OPEN**

Wado. 🦅
