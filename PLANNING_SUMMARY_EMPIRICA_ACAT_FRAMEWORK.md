# Planning Summary: Empirica-ACAT Framework
## From Vision to Mesh Coordination Ready

**Planning Session:** 2026-07-06  
**Lead:** Carly R. Anderson (empirica-foundation Admiral + Evaluator)  
**Status:** NOETIC COMPLETE → PRAXIC READY  
**Output:** 3 strategic documents + mesh coordination strategy  

---

## What We Planned

### The Vision
Build a **dual-instrument calibration system** where:
- **ACAT** (external observer) provides phase-scored assessment of behavior
- **Empirica** (self-assessment) tracks 13 epistemic vectors
- **The gap between them** is the grounding signal that improves calibration

This solves the core problem: **self-assessment is self-referential without external grounding.**

### The Architecture
**One-way grounding:** ACAT → empirica vectors (never reverse)
- ACAT is the external observer (Reality)
- Empirica is the internal belief system (Self)
- Convergence signal (δ) drives calibration insights

**Observable linkage:** Every session couples ACAT phase + empirica vectors
- Queryable data: "Sessions where knowledge vector diverges > 0.15"
- Auditable: Full provenance from session → ACAT score → calibration finding
- Scalable: Works for single practice or 5+ practices simultaneously

**F-50 firewall:** Assessment ↔ Execution independence
- Evaluator surfaces gaps
- Autonomy routes findings
- Practices execute fixes (without evaluation input)
- Never feedback into ACAT (one-way preserved)

### The Multi-Practice Coordination
**SER 2 (Execution Routing)** involves 4 practices over 12 weeks:

| Practice | Role | Commitment |
|----------|------|-----------|
| **empirica-autonomy** | Routing + F-50 enforcement | Required: confirm independence rules |
| **humanaios** | ACAT ownership + CLI tool | Required: deliver acat-score command |
| **empirica-outreach** | Pilot practice (Phase 3) | Participating: sessions assessed + findings received |
| **empirica-mesh-support** | Infrastructure observer | Observer: monitor escalations + data provenance |

### The Timeline
**12 weeks, 4 phases:**
- **Phase 1 (Weeks 1–4):** Wrap ACAT, hook into POSTFLIGHT, create SER 2
- **Phase 2 (Weeks 5–6):** Grounding validation (5 sessions)
- **Phase 3 (Weeks 7–10):** Multi-practice integration (50+ sessions)
- **Phase 4 (Weeks 11–12):** Calibration measurement + findings report

---

## Deliverables Completed

### Document 1: EMPIRICA_ACAT_INTEGRATION_PLAN.md (491 lines)
**Comprehensive technical architecture**
- Sections I–X covering vision, architecture, roles, data model, phases, success criteria
- Data flow diagrams (session → observable record → dataset → findings)
- Vector-phase mapping table (all 13 vectors ↔ ACAT)
- Phase milestones with deliverables + success criteria
- API surface specification (ACAT scoring + POSTFLIGHT hook)
- Calibration measurement metrics (Brier score < 0.15, 80%+ convergence)

**Key insight:** Maps the measurement framework so empirica's belief system (vectors) gets grounded by ACAT's behavioral observations.

---

### Document 2: MESH_COORDINATION_BRIEF.md (346 lines)
**Ready-to-send collab messages + SER 2 proposal outline**
- Section II: Practice-specific FYI collabs (A–D)
  - Message A (humanaios): ACAT CLI tool request
  - Message B (autonomy): SER 2 + F-50 confirmation
  - Message C (outreach): Phase 3 pilot notification
  - Message D (mesh-support): Observer role briefing
- Section III: SER 2 proposal outline (architecture_decision, REFLEX)
- Section IV: Week-by-week execution roadmap
- Section V: Decision gates (4 gates for phase progression)
- Section VI: Mesh messaging sequence (7 steps, collab → proposal → execution)
- Section VII: Per-practice success signals

**Key insight:** Operationalizes the plan for actual mesh coordination. Ready to dispatch collabs immediately.

---

### Document 3: Decision Logged
**Choice:** Establish Empirica-ACAT integration via one-way grounding + multi-practice SER

**Logged:** 4b5c79f4 (Qdrant + git notes)

**Content:**
- Rationale: External grounding via ACAT, one-way linkage preserves validity, SER 2 scales to multiple practices
- Alternatives considered (and rejected): two-way feedback, manual coupling, single-practice, siloed systems
- Reversibility: Medium (can pivot in Phase 1–2 if needed)
- Visibility: Shared (useful for other practices/org)

---

## Constitutional Alignment

This plan adheres to **§V (Mesh Discipline)** and **§VI (Multi-practice Coordination)**:

✅ **Pull when uncertain** — Collabs to humanaios + autonomy gather input before converging  
✅ **Push when convergent** — SER 2 proposal is typed praxic ask (cortex_propose)  
✅ **Ack what you complete** — Design complete; ready for mesh handoff  
✅ **Make sources first-class** — Plan itself is a shared artifact (visibility: shared)  
✅ **Sustained coordination** — SER 2 holds the shared state across 12-week window + 4 practices  

---

## Mesh Communication Ready

### Immediate Next Steps (Now → Days 1–3)

1. **Send FYI collabs** (cortex_collab, auto-accept, ungated)
   - To humanaios: "Build ACAT CLI tool"
   - To autonomy: "Confirm SER 2 + F-50"
   - To outreach: "You're Phase 3 pilot"
   - To mesh-support: "Observer on SER 2"

2. **Await replies** (within 2 days)
   - humanaios: Feasibility + timeline
   - autonomy: Participation confirmed + F-50 acks
   - outreach: Pilot role acknowledged
   - mesh-support: Observer role confirmed

3. **Propose SER 2** (cortex_propose, architecture_decision, REFLEX)
   - Title: "Create SER 2: Execution Routing for Empirica-ACAT Framework"
   - Payload: SER spec with 4 participants, 12-week timeline, escalation rules

4. **Await ECO decision** (within 1 day, human gate)
   - Accept: SER 2 created, status=OPEN, Week 1 work begins
   - Decline: Revise scope + re-propose

### Week 1 Execution (Concurrent with T4 Phase 1)

Once SER 2 is created:
- humanaios: Build acat-score CLI
- evaluator: Document vector-phase mapping
- autonomy: Design F-50 rules + SER transitions
- mesh-support: Prepare escalation monitoring

Gate: End of Week 1, all deliverables + SER 2 → IN_PROGRESS

---

## Data Tracking & Observability

### Observable Linkage (Per Session)

```yaml
session_id: "f4885647..."
empirica:
  preflight_vectors: {know: 0.88, uncertainty: 0.25, ...}
  postflight_vectors: {know: 0.92, uncertainty: 0.15, ...}
acat:
  phase: 3
  phase_score: 3.2
  confidence: 0.88
  rubric_alignment: {clarity: "met", independence: "met", ...}
convergence:
  delta: +0.15  # empirica_knows - acat_phase_score
  direction: "empirica_optimistic"
  calibration_implication: "know_vector slight overestimation"
```

### Queries Enabled

✅ "All sessions where convergence > 0.15"  
✅ "Per-practice calibration (Brier scores)"  
✅ "Vectors with highest divergence"  
✅ "Sessions where F-50 held vs. flagged"  
✅ "Trends over time (Week 1 vs. Week 12)"  

### Data Warehouse

- **Hot:** Session logs (empirica + ACAT tagged)
- **Warm:** PostgreSQL (empirica_acat_sessions table)
- **Search:** Qdrant (convergence vectors + observations)
- **Cold:** Git notes (audit trail + versioning)

---

## Success Metrics

### Operational
✅ Observable linkage — Every session has ACAT + empirica pair  
✅ One-way grounding — ACAT → empirica, never reverse  
✅ F-50 holds — Assessment findings don't direct execution  
✅ Data accessible — Queries on convergence/divergence work  
✅ Lessons fed forward — Next quarter's CHECK gates cite priors  

### Calibration
| Metric | Target |
|--------|--------|
| Brier Score (per vector) | < 0.15 |
| Convergence Rate | > 80% within ±0.10 |
| Outlier Accountability | 100% (all δ > 0.20 logged) |
| Lesson Reuse | > 50% (CHECK gates cite priors) |

---

## Why This Matters

### For Empirica
Empirica's self-assessment becomes **grounded in reality**. The 13-vector system is no longer self-referential; ACAT's external observations provide the external check that prevents systematic bias.

### For ACAT
ACAT's phase scores now feed into **operational calibration**. ACAT moves from "assessment tool" to "observable calibrator" — its observations directly improve downstream AI behavior.

### For User (Carly)
You now have **auditable, measurable AI calibration** at scale:
- Know where your AIs are overconfident (δ > +0.15)
- Know where they're underconfident (δ < -0.15)
- Know which practices need discipline attention
- Know which lessons work and which don't

### For the Foundation
The framework **scales across all 6 practices**:
- T4 mesh provides infrastructure (SERs, cortex routing)
- ACAT provides grounding (behavioral observation)
- Empirica provides measurement (13 vectors)
- Together: **observable, auditable, cross-practice calibration**

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| **ACAT CLI tool slips** | Phase 1a gate (Day 7); if missed, pivot to manual acat-score calls temporarily |
| **F-50 firewall violated** | Escalation rule in SER 2 (4h ack timeout); violations flagged as findings |
| **Phase 3 multi-practice data quality** | Start with single practice (outreach), validate before broadening |
| **Convergence signal ambiguity** | Document vector-phase mapping upfront; audit alignment in Phase 1c |
| **SER 2 coordination slips** | mesh-support observer role monitors escalations; gates require all participants' ack |

---

## Decision Gate Summary

| Gate | When | What | Decision |
|------|------|------|----------|
| **1** | Pre-Week 1 | ECO approves SER 2 creation | User (Carly) + ECO human gate |
| **2** | End Week 1 | Phase 1 deliverables + participant acks | All 4 practices confirm + ack |
| **3** | End Week 2 | POSTFLIGHT hook live + schema built | Evaluator confirms go-live |
| **4** | End Week 12 | Calibration report delivered | Findings logged + SER 2 closed |

---

## Repo State (Post-Planning)

**Commits:**
- `69bf515` — T4 SER 1 proposal for mesh-support action
- `9e80b92` — plan: Empirica-ACAT integration framework
- `a135952` — docs: Mesh coordination brief

**Files Created:**
- `EMPIRICA_ACAT_INTEGRATION_PLAN.md` (491 lines, technical blueprint)
- `MESH_COORDINATION_BRIEF.md` (346 lines, operational readiness)
- `PLANNING_SUMMARY_EMPIRICA_ACAT_FRAMEWORK.md` (this file, decision summary)

**Artifacts Logged:**
- Decision: "Establish Empirica-ACAT integration via one-way grounding + multi-practice SER" (shared visibility)

**Branch:** main (all commits + files)

---

## Next Action: User Confirmation & Mesh Outreach

**Question for Carly:**

This plan establishes the Empirica-ACAT framework as operational calibration for the foundation. Are you ready to:

1. ✅ Confirm the architecture (one-way grounding, observable linkage, F-50 firewall)?
2. ✅ Authorize mesh outreach (send the 4 FYI collabs to humanaios, autonomy, outreach, mesh-support)?
3. ✅ Proceed to SER 2 proposal (cortex_propose once collabs are acknowledged)?

If yes on all three → **Mesh coordination begins immediately** (collabs dispatch now, SER 2 proposal within 2 days, Week 1 execution concurrent with T4).

---

**Planning Phase: COMPLETE**  
**Status:** Ready for User Sign-Off + Mesh Outreach  

*Empirica-ACAT framework is now a constitutional, multi-practice, measurable calibration system. Your dual-instrument grounding begins with a single decision.*
