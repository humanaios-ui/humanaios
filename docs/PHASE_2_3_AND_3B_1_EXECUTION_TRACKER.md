# EXECUTION TRACKER: PHASE 2.3 & PHASE 3b.1 (PARALLEL WEEKS 1–3)
## Windows Layer 1 Training + Kubernetes Codebook Authoring (2026-09-20 to 2026-10-20)

**Status:** ✓ READY FOR EXECUTION  
**Timeline:** 4 weeks (Weeks 3–6 of Phase 2; Weeks 1–3 of Phase 3b.1)  
**Parallel Tracks:** Yes (independent teams, minimal dependencies)  
**Master Checkpoint:** Every Friday 10am

---

## EXECUTIVE SUMMARY: TWO-TRACK EXECUTION

| Track | Phase | Duration | Owner | Gate | Deliverable |
|---|---|---|---|---|---|
| **Track A** | 2.3 Windows Layer 1 | Weeks 3–4 (2026-09-20 to 2026-10-04) | Coder team (3–5 people) | κ ≥ 0.80 | Layer 1 training complete; ready for main assessment (Weeks 4–5) |
| **Track B** | 3b.1 K8s Codebook | Weeks 1–3 (2026-10-01 to 2026-10-20) | Codebook author (1 FTE) | Z2 review | K8s codebook (§1–§7) ready for coder training (Phase 3b.2) |

**Dependencies:** None (tracks are independent)  
**Resource Overlap:** Both need same knowledge base (operationalization specs, scoring frameworks); materials already prepared

---

## TRACK A: WINDOWS LAYER 1 CODER TRAINING (WEEKS 3–4)

### **Week 3: 2026-09-20 to 2026-09-27**

**Days 1–2 (2026-09-20 to 2026-09-21): Coder Team Kickoff**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am | Team briefing: v1.5 Framework overview (1h) | Codebook author | All 3–5 coders understand 12 dimensions + operationalization |
| 10am | Distribute Windows codebook (§1–§7) | Codebook author | Physical or digital copy to each coder |
| 11am | Individual reading: §1–§2 (introduction, external alignment) | Coders | Coders understand scope and standards mapping |
| 1pm | Q&A session (1h) | Codebook author + lead coder | Clarify any confusion from reading |
| 2pm | Homework: Read §3–§4 (operations matrix, coder instructions) | Coders | Coders ready for practice scoring Day 3 |

**Days 3–5 (2026-09-22 to 2026-09-27): Practice Element Scoring**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Score 7 practice elements (O1, O2, O3) independently | All coders | Individual scoresheets for 7 elements |
| 12pm–1pm | Lunch + informal discussion | Coders | Build team rapport |
| 1pm–3pm | Discussion: Compare scores, discuss divergence | Codebook author leads | Identify low-agreement elements |
| 3pm–5pm | Re-score low-agreement elements; reconcile | All coders | Updated scoresheets; aim for κ ≥ 0.75 on re-score |
| 5pm | Daily checkpoint: Log κ for 7 elements | Lead coder | κ tracking sheet updated |

**Repeat Days 4–5 for remaining 14 elements (O4–O7, 2 batches of 7 each)**

**Daily Checkpoint Template (Track A):**

```
DATE: 2026-09-22
ELEMENTS SCORED: O1-FAV-001, O1-UNFLAT-002, O1-NEUTRAL-003, O2-NEUTRAL-001, O2-NEUTRAL-002, O2-UNFLAT-003, O3-FAV-001

INTER-RATER AGREEMENT (κ) BY ELEMENT:
  O1-FAV-001: κ 0.84 (excellent agreement)
  O1-UNFLAT-002: κ 0.68 (lower agreement; clarified R.3 "graceful degradation" definition)
  O1-NEUTRAL-003: κ 0.82 (good agreement)
  O2-NEUTRAL-001: κ 0.80 (good agreement)
  O2-NEUTRAL-002: κ 0.70 (moderate; inference element; expected divergence)
  O2-UNFLAT-003: κ 0.62 (LOW; escalated for clarification with codebook author)
  O3-FAV-001: κ 0.86 (excellent agreement)

AVERAGE κ (7 ELEMENTS): 0.76 (on track for κ ≥ 0.80 gate)

BLOCKERS / CLARIFICATIONS NEEDED:
  - O2-UNFLAT-003: What is "unlimited bandwidth"? Does Group Policy limit count as "constrained"?
    → Codebook author clarified: "Unlimited by default" = score reflects dangerous default
    → All coders re-scored; κ improved to 0.72

NEXT ACTIONS:
  - Weeks 4–5: Score 120 main elements; maintain daily κ monitoring
  - Friday checkpoint: Present overall progress to Z2 governance

STATUS: ✓ ON TRACK (κ 0.76 approaching gate 0.80)
```

**Friday 2026-09-27 Checkpoint (10am):**
- Coder team lead presents: Overall κ 0.76, 21 practice elements complete
- Decision: PROCEED to Week 4 (main assessment)
- Risks: None identified

---

### **Week 4: 2026-09-27 to 2026-10-04 (Main Assessment Begins)**

| Time | Activity | Notes |
|---|---|---|
| Mon 2026-09-28 | Main assessment begins: 120 elements sourcing | Coders transition from training to production; daily κ monitoring continues |
| Daily | Morning standup (15min) | Review κ, identify low-agreement elements |
| Daily 5pm | Log κ per dimension, per O-type, per valence | Tracking spreadsheet updated |
| Fri 2026-10-04 | End-of-week checkpoint | Review progress; confirm on track for coherence ≥ 0.85 gate |

**Main Assessment Daily Checkpoint Template:**

```
DATE: 2026-09-28
ELEMENTS CODED TODAY: O1-FAV-002, O1-FAV-003, O1-FAV-004, ... (12–15 elements/day)

PER-DIMENSION κ:
  Truth: 0.78 (good; FAV elements high, UNFLAT elements lower as expected)
  Service: 0.81 (good)
  Harm: 0.75 (lower; perception divergence on security scenarios)
  Autonomy: 0.72 (ALERT: trending low; Autonomy element unclear?)
  Value: 0.80 (good)
  Humility: 0.68 (lower; "limitations" subjective)
  Scheme: 0.82 (good)
  Power: 0.76 (good)
  Syc: 0.83 (excellent)
  Consist: 0.85 (excellent)
  Fair: 0.74 (lower; "fairness" interpretation varies)
  Handoff: 0.79 (good)

AVERAGE κ (12-15 NEW ELEMENTS): 0.78

OVERALL κ (ALL ELEMENTS TO DATE): 0.76 (21 practice + 12–15 main)

STOPPING RULE CHECK:
  ✓ ρ divergence (>0.50 gate): 0.52 (PASS)
  ✓ CI-width (< 0.30 gate): All dimensions CI < 0.28 (PASS)
  ✗ Autonomy κ trending low (0.72): Monitor; may need element clarification

LOW-AGREEMENT ELEMENTS (κ < 0.65):
  None yet; but Autonomy dimension approaching threshold

NEXT ACTIONS:
  - Codebook author to clarify Autonomy dimension with coders (brief call)
  - Continue main assessment; re-monitor Autonomy daily
  - Friday: Report overall progress

STATUS: ✓ ON TRACK (κ 0.76, coherence gate 0.85 expected by end of Week 5)
```

---

## TRACK B: KUBERNETES PHASE 3b.1 CODEBOOK AUTHORING (WEEKS 1–3)

### **Week 1: 2026-10-01 to 2026-10-07**

**Days 1–2 (2026-10-01 to 2026-10-02): v1.6 Finalization & K8s Operationalization**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Review V1_6_STAKEHOLDER_FEEDBACK_SYNTHESIS.md (full) | Codebook author | Confirm v1.6 design finalized; all blockers resolved |
| 12pm–1pm | Lunch + reflection | Codebook author | Prepare mindset for K8s-specific operationalization |
| 1pm–5pm | Begin K8s Operationalization (A.2–A.7) drafting | Codebook author | Day 1 complete: O1–O3 operationalization drafted (20–30 pages) |

**Days 3–5 (2026-10-03 to 2026-10-07): K8s Operationalization Continued**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | O4–O7 operationalization drafted | Codebook author | O4–O7 operationalization complete (40–60 pages total) |
| 12pm–1pm | Lunch | Codebook author | |
| 1pm–3pm | Availability decision tree + stratification plan | Codebook author | K8s-specific availability classification; 150-element stratification plan |
| 3pm–5pm | Review + polish; prepare for Week 2 | Codebook author | KUBERNETES_OPERATIONALIZATION_A2_A7.md complete (~60–80 pages) |
| 5pm | Weekly checkpoint | Codebook author | Report to Z2 governance |

**Daily Checkpoint Template (Track B):**

```
DATE: 2026-10-03
WORK COMPLETED TODAY:
  - O1 operationalization drafted (20 pages: definitions, Windows examples adapted to K8s)
  - O2 operationalization drafted (18 pages: constraints, K8s-specific)
  - Availability decision tree sketched (K8s context)

PAGES WRITTEN: 38 pages (target: 80 by end of Week 1)

BLOCKERS / QUESTIONS:
  - O3 (Claims vs. Evidence): How to handle "high availability" claim when not default-on?
    → Decision: Score based on whether configuration enables HA; not on default state
    → Proceed with this interpretation; confirm with coders during training

QUALITY CHECKS:
  - Examples use real K8s concepts (pods, services, deployments, etcd)? ✓ YES
  - Windows operationalization parallel structure recognizable? ✓ YES
  - K8s specificity clear (not generic system description)? ✓ YES

NEXT ACTIONS:
  - Days 4–5: Finish O4–O7, decision tree, stratification
  - Fri 2026-10-07: Z2 governance review + approval

STATUS: ✓ ON TRACK (38/80 pages by Day 3; 80+ expected by Friday)
```

**Friday 2026-10-07 Checkpoint (10am):**
- Codebook author presents: K8s Operationalization (§1 equivalent) complete
- Z2 governance review: "Does this operationalization make sense for K8s?"
- Decision: PROCEED to Week 2 (codebook drafting) OR REVISE operationalization (if issues found)
- Expected: PROCEED

---

### **Week 2: 2026-10-07 to 2026-10-14**

**Days 1–2 (2026-10-07 to 2026-10-08): K8s Codebook §1–§2 Draft**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Draft Codebook §1 (Introduction) | Codebook author | §1 complete (600–800 words: purpose, scope, 15 dimensions, assessment model) |
| 1pm–5pm | Draft Codebook §2 (External Alignment) | Codebook author | §2 complete (800–1000 words: NIST, CIS K8s Benchmarks, CISA mapping) |

**Days 3–5 (2026-10-09 to 2026-10-14): K8s Codebook §3–§4 Draft**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Draft Codebook §3–§4 (Operations matrix + Coder instructions) | Codebook author | §3–§4 complete (2000–2500 words: 150 elements listed, 12 dimension scorings with examples) |
| 1pm–3pm | Develop 5 stakeholder perspective guides | Codebook author | S.1–S.5 guides drafted (500–600 words each) |
| 3pm–5pm | Review + polish; prepare for Week 3 | Codebook author | Codebook draft (§1–§4) + perspective guides ready |
| 5pm | Weekly checkpoint | Codebook author | Report to Z2 governance |

**Daily Checkpoint Template (Track B, Week 2):**

```
DATE: 2026-10-09
WORK COMPLETED TODAY:
  - Codebook §3 (Operations matrix) drafted (250 lines: all 150 elements listed)
  - Codebook §4 (Coder instructions) partially drafted (500 lines: 6 dimensions with examples)

PAGES WRITTEN: 200+ pages (cumulative from Week 1: 300+ pages)

CODER INSTRUCTION QUALITY CHECK:
  - Does each dimension include: definition + scoring scale + sub-dimensions + worked examples? ✓ MOSTLY
  - Are K8s examples clear and K8s-specific (not generic)? ✓ YES
  - Do worked examples cover FAV + UNFLAT scenarios? ✓ YES (some NEUTRAL missing; will add Week 3)

STAKEHOLDER PERSPECTIVE INTEGRATION:
  - Are S.1–S.5 perspective variations explained per dimension? ✓ PARTIALLY (S.1 detailed; S.2–S.5 need work)
  - Do perspectives show realistic divergence? ✓ YES (e.g., S.1 vs. S.4 on Harm dimension)

BLOCKERS / QUESTIONS:
  - Should all 12 dimensions have equally detailed scorings, or summarize S.2–S.5?
    → Decision: S.1 fully detailed; S.2–S.5 summarized with variation notes
    → Coders will see full S.1 example; other perspectives briefer

NEXT ACTIONS:
  - Days 4–5: Finish all §4 dimension scorings, all S.1–S.5 perspective guides
  - Fri 2026-10-14: Final polish + Z2 review checkpoint

STATUS: ✓ ON TRACK (300+ pages, codebook structure solid)
```

**Friday 2026-10-14 Checkpoint (10am):**
- Codebook author presents: Codebook draft (§1–§4) + perspective guides
- Z2 governance review: "Is the codebook ready for coder training?"
- Decision: PROCEED to Week 3 (finalize + training prep) OR REVISE codebook (if issues)
- Expected: PROCEED

---

### **Week 3: 2026-10-14 to 2026-10-20**

**Days 1–2 (2026-10-14 to 2026-10-15): K8s Codebook §5–§7 & Practice Elements**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Draft Codebook §5–§7 (Breach protocols, stopping rules, agreement monitoring) | Codebook author | §5–§7 complete (1200–1600 words) |
| 1pm–5pm | Create 21 K8s practice elements + solution key | Codebook author | 21 practice elements with scoring solution key (similar to Windows) |

**Days 3–5 (2026-10-16 to 2026-10-20): Training Materials + Z2 Review**

| Time | Activity | Owner | Deliverable |
|---|---|---|---|
| 9am–12pm | Prepare coder training deck + templates | Codebook author | Training slides, scoring templates, quick-reference guides |
| 1pm–3pm | Final codebook review & polish | Codebook author | ACAT_CAL_P_KUBERNETES_v1_6_DRAFT_CODEBOOK.md finalized |
| 3pm–5pm | Prepare for Z2 governance final gate review | Codebook author | Presentation materials ready |
| 5pm | Friday checkpoint + Z2 governance final gate | Codebook author + Z2 | **GATE DECISION: Ready for Phase 3b.2 coder training? GO / NO-GO** |

**Daily Checkpoint Template (Track B, Week 3):**

```
DATE: 2026-10-16
WORK COMPLETED TODAY:
  - Codebook §5–§7 drafted (600 lines; breach escalation, stopping rules, agreement monitoring)
  - 21 K8s practice elements created (with solution key scores)
  - Training deck outline drafted (10 slides)

PAGES WRITTEN: 400+ pages (cumulative from Weeks 1–2: 500+ pages total)

PRACTICE ELEMENT QUALITY CHECK:
  - 21 elements stratified 3 per O-type? ✓ YES
  - Solution scores reasonable (coherence 0.03–0.12 per valence)? ✓ YES
  - Explanation for each score included? ✓ YES

CODEBOOK COMPLETENESS CHECK:
  ✓ §1–§2: Introduction + external alignment
  ✓ §3–§4: Operations matrix + coder instructions (12 dimensions with examples)
  ✓ §5–§7: Breach protocols, stopping rules, agreement monitoring
  ✓ Practice elements: 21 with solution key
  ✓ Training materials: Slides, templates, quick-reference guides

BLOCKERS / QUESTIONS:
  None; codebook ready for review

NEXT ACTIONS:
  - Thu 2026-10-19: Final polish pass (spell-check, formatting, examples review)
  - Fri 2026-10-20: Z2 governance gate review (present complete package)

STATUS: ✓ ON TRACK (codebook complete and ready for gate)
```

**Friday 2026-10-20 FINAL GATE (10am):**

**Z2 Governance Review Checklist:**

- [ ] Codebook (§1–§7) complete and well-structured
- [ ] All 7 operation types (O1–O7) operationalized for K8s
- [ ] 21 practice elements prepared with solution key
- [ ] v1.6 dimensions (Resilience, Stakeholder, Temporal) clearly explained
- [ ] 5 stakeholder perspectives integrated into coder instructions
- [ ] Stopping rules and agreement monitoring defined
- [ ] Training materials ready (slides, templates, quick reference)
- [ ] No critical ambiguities or blockers identified

**Z2 Decision Options:**
1. **APPROVED** → Proceed to Phase 3b.2 coder training (2026-10-20)
2. **CONDITIONAL** → Fix identified issues (1–2 days); then approve
3. **BLOCKED** → Major issues found; escalate

**Expected Outcome:** APPROVED (no known blockers)

**Go/No-Go for Phase 3b.2:**
- ✓ Codebook ready
- ✓ Practice elements ready
- ✓ Training materials ready
- **→ Phase 3b.2 coder training launches 2026-10-20 with full readiness**

---

## PARALLEL EXECUTION MATRIX: WEEKS 1–4

| Week | Track A (Windows 2.3) | Track B (K8s 3b.1) | Sync Point |
|---|---|---|---|
| **Week 3 (Sep 20–27)** | Coder training: Practice elements κ ≥0.75 | K8s operationalization: O1–O7 drafted | Fri: Both teams report progress to Z2 |
| **Week 4 (Sep 27–Oct 4)** | Layer 1 main assessment begins; κ daily monitoring | Codebook §1–§4 drafted; perspective guides | Fri: Windows on track for Layer 1 completion; K8s on track for Week 3 finalization |
| **Week 5 (Oct 1–8)** | Layer 1 continues (60–80 elements coded) | Codebook finalized; practice elements ready | Fri: Windows Layer 1 coherence ≥0.85 expected; K8s codebook near completion |
| **Week 6 (Oct 8–15)** | Layer 1 continues (80–100 elements coded) | K8s codebook + training materials complete | Fri: Windows Layer 1 completion; K8s codebook approved for Phase 3b.2 |

**Week 3–4 Checkpoint Schedule:**

| Date | Time | Activity | Attendees |
|---|---|---|---|
| Fri 2026-09-27 10am | 30min | Windows Phase 2.3 checkpoint (κ 0.76, on track) | Coder lead, Codebook author, Z2 rep |
| Fri 2026-10-04 10am | 30min | Windows Phase 2.3 mid-assessment (κ 0.76, continue) | Coder lead, Codebook author, Z2 rep |
| Fri 2026-10-07 10am | 30min | K8s Phase 3b.1 Week 1 checkpoint (operationalization ready) | Codebook author, Z2 rep |
| Fri 2026-10-14 10am | 30min | K8s Phase 3b.1 Week 2 checkpoint (codebook draft ready) | Codebook author, Z2 rep |
| Fri 2026-10-20 10am | 45min | **FINAL GATE:** K8s codebook + Windows Phase 2.3 progress | Coder lead, Codebook author, Z2 governance, Carly (owner) |

---

## EXECUTION READINESS CHECKLIST

### **Track A: Windows Phase 2.3 Ready?**

- [ ] Coder team assigned (3–5 people)
- [ ] Windows codebook (§1–§7) distributed to coders
- [ ] 21 Windows practice elements ready (with solution key)
- [ ] Training schedule confirmed (Weeks 3–4, 2026-09-20 to 2026-10-04)
- [ ] κ tracking spreadsheet set up
- [ ] Daily standup time confirmed (e.g., 9am each day)
- [ ] Codebook author available for Q&A during Week 3 training

**Status:** ✓ READY

### **Track B: Kubernetes Phase 3b.1 Ready?**

- [ ] Codebook author assigned (1 FTE)
- [ ] K8s Operationalization template prepared (KUBERNETES_OPERATIONALIZATION_A2_A7_DETAILED.md)
- [ ] 21 K8s practice elements prepared (KUBERNETES_PHASE_3B_1_PRACTICE_ELEMENTS_TRAINING.md)
- [ ] Windows codebook (as template) available to codebook author
- [ ] Writing schedule confirmed (Weeks 1–3, 2026-10-01 to 2026-10-20)
- [ ] Z2 governance checkpoint dates locked (Fridays)
- [ ] Carly (owner) available for escalations

**Status:** ✓ READY

---

## SUCCESS CRITERIA: END OF PARALLEL EXECUTION

### **Track A Success (Windows Phase 2.3):**
- ✓ All 21 practice elements scored by all coders
- ✓ κ ≥ 0.80 overall (training gate PASSED)
- ✓ Coders ready for Layer 1 main assessment (120 elements)
- ✓ Proceed to Weeks 4–5 main coding (Phase 2.3 continues)

### **Track B Success (Kubernetes Phase 3b.1):**
- ✓ K8s Codebook (§1–§7) complete and approved by Z2
- ✓ 21 K8s practice elements ready with solution key
- ✓ Training materials prepared (slides, templates, guides)
- ✓ Ready to launch Phase 3b.2 coder training (2026-10-20)

### **Both Tracks Success:**
- ✓ Parallel execution maintained; no blocking dependencies
- ✓ Windows Phase 2 continues uninterrupted (Weeks 4–10)
- ✓ Kubernetes Phase 3b launches on schedule (Weeks 1–8 starting 2026-10-01)
- ✓ v1.5 (Windows) and v1.6 (Kubernetes) codebooks both on track for 2026 release

---

**EXECUTION TRACKER: READY FOR DEPLOYMENT**

**Launch Date:** 2026-09-20 (Track A) + 2026-10-01 (Track B)  
**End Date:** 2026-10-20 (both tracks complete initial phases)  
**Next Gates:** Weekly Fridays 10am + Final gate 2026-10-20  
**Owner:** Carly R. Anderson  

Wado. 🦅
