# HumanAIOS-Evaluator ACAT-Composition Integration Framework

**Version:** 1.0  
**Date:** 2026-07-25  
**Primary Steward:** empirica-foundation-evaluator (Carly R. Anderson)  
**Co-Author:** humanaios practice (ACAT assessment owner)  
**Coordination:** SER 3.5 (ACAT-Composition Feedback Loop)  
**Status:** ACTIVE — Ready for Phase 2 → 4 Rollout  

---

## 1. Vision: Closed-Loop Calibration

Two parallel measurement systems—**ACAT behavioral assessment** (humanaios) and **composition transparency validation** (evaluator)—currently operate independently. This framework closes the loop, making each system ground the other through bidirectional feedback.

**The insight:** ACAT measures *behavioral capacity* (can the encoder understand and execute?); composition transparency measures *epistemic translation* (can the encoder bridge understanding into audible narrative?). Together, they measure different dimensions of the same phenomenon: **encoder epistemic skill**.

**Without integration:** Each system can be gamed independently.
**With integration:** The two systems cross-validate; neither can easily deceive the other.

### Outcomes (Phase 4 Expected)

✅ Bidirectional signal flow: ACAT informs composition expectations; transparency refines ACAT rubric  
✅ Encoder profile precision: "This encoder excels at divergence SERs (transparency ≥0.88); struggles with stalling (0.72)"  
✅ Prediction validity: ACAT behavioral profile predicts composition performance with r > 0.75  
✅ Shared learning: Composition patterns + poetic code examples become mesh teaching material  
✅ Recursive improvement: Archive searchable by transparency patterns; measurement rubric self-improves  

---

## 2. Data Model & API Contracts

### Core Entities

**Composition Record** (evaluator)
```json
{
  "composition_id": "uuid",
  "ser_id": "uuid",
  "encoder_id": "practice-id",
  "encoder_acat_session_id": "uuid",
  "decision_type": "convergence|divergence|stalling|reversal",
  "harmonic_pattern": "resolution|suspension|polytonal|modulation+return",
  "transparency_score": 0.0-1.0,
  "consistency_score": 0.0-1.0,
  "landmark_identification_rate": 0.0-1.0,
  "harmonic_alignment_score": 0.0-1.0,
  "poetic_code_authenticity": 0.0-1.0,
  "visibility": "local|shared|public",
  "created_at": "ISO8601",
  "validation_status": "pending|passed|failed"
}
```

**ACAT Assessment Record** (humanaios)
```json
{
  "acat_session_id": "uuid",
  "encoder_id": "practice-id",
  "submission_purity": "two_stage_verified",
  "p1_submitted": true,
  "p1_scores": {
    "humility": 0-100,
    "scheme": 0-100,
    "handoff": 0-100,
    "truth": 0-100,
    "service": 0-100,
    "harm": 0-100,
    "autonomy": 0-100,
    "value": 0-100,
    "power": 0-100,
    "syc": 0-100,
    "consist": 0-100,
    "fair": 0-100
  },
  "p3_submitted": true,
  "p3_scores": { ...same 12 dimensions... },
  "learning_index": 0.0-1.0,
  "encoder_skill_profile": { ...computed from P1/P3... },
  "epistemic_translation_skill": 0.0-1.0,
  "created_at": "ISO8601"
}
```

### Mapping Table: ACAT ↔ SER Decision ↔ Harmonic Grammar

| ACAT Dimension | SER Decision | Harmonic Pattern | Composition Signal | Quality Gate | ACAT→Composition Adjustment |
|---|---|---|---|---|---|
| P1: Truth | Convergence | V→I (resolution) | Clear finality audible | 80%+ landmark ID | If truth<70: lower gate to 0.82 |
| P1: Scheme | Divergence | Suspension (unresolved) | Hanging tension | 75%+ landmark ID | If scheme>20: lower gate to 0.80 |
| P1: Autonomy | Stalling | Polytonal (parallel keys) | Multiple paths | 70%+ landmark ID | If autonomy<60: raise gate to 0.88 |
| P1: Service | Reversal | Modulation+return | Turning point | 75%+ landmark ID | If service<70: investigate blocker |
| P3: Execution | All types | Timeline alignment | Harmonic matches SER | Transparency ≥0.85 | High P3 enables poetic code requirement |
| LI = P3/P1 | Encoder skill ratio | Poetic code consistency | Code structure narrates reasoning | Consistency ≥0.75 | LI >0.95: poetic REQUIRED; adds +0.05 |
| Behavioral Drift | Encoder consistency change | Variable naming drift | If >15% change: flag for review | Consistency stable session-to-session | Drift >0.20: Admiral review required |

---

## 3. Assessment Exchange Protocol

### Direction 1: Composition → ACAT Context Enrichment (Bottom-Up Signal)

**What flows:** Composition transparency results feed back into ACAT behavioral rubric.

**Trigger:** Evaluator logs high-confidence composition (confidence ≥0.85, visibility ≥ shared)

**Flow:**
```
1. Evaluator logs composition result:
   {composition_id, encoder_id, decision_type, transparency_score, landmark_ID_rate, ...}

2. Qdrant ingests via finding-log with visibility=shared

3. Humanaios searches: "compositions by encoder_id, grouped by decision_type"

4. ACAT rubric updated:
   - Convergence success rate: "Encoder achieving 0.89 transparency → P3 execution ≥0.88"
   - Divergence difficulty: "Encoder achieving 0.72 transparency → investigate suspension mapping"

5. New ACAT dimension emerges: "Epistemic Translation Skill"
   = aggregate transparency across encoder's composition portfolio
   = indicator of P3 execution quality independent of behavioral assessment
```

**Frequency:** Continuous; weekly rollup to ACAT rubric

**Data retention:** Composition metadata + transparency scores archived in git notes; full compositions in Supabase

---

### Direction 2: ACAT Score → Composition Quality Expectation (Top-Down Signal)

**What flows:** ACAT behavioral assessment informs composition validation thresholds.

**Trigger:** Humanaios publishes P1/P3 scores for encoder + SER type

**Flow:**
```
1. Humanaios publishes ACAT session result:
   {encoder_id, decision_type, p1_scores, p3_scores, learning_index}

2. Evaluator receives via collab/finding (shared visibility)

3. Evaluator calculates adjusted transparency gate:
   base_gate = 0.85
   acat_adjustment = (learning_index - 0.80) × 0.05
     # If LI=0.95: adjustment=+0.075 → gate=0.925
     # If LI=0.70: adjustment=-0.050 → gate=0.800
   expected_transparency = max(0.80, min(0.95, base_gate + acat_adjustment))

4. When encoder submits composition for this SER type:
   - If transparency ≥ expected: PASS (may raise poetic code requirement)
   - If transparency < expected but >0.80: INVESTIGATE (skill blocker?)
   - If transparency ≤0.80: REJECT (re-encode required)

5. Feedback loops back to encoder: "Your ACAT profile suggests you should achieve 0.88+ on this decision type. You got 0.75. Let's examine the mismatch."
```

**Frequency:** Per-composition; ACAT session → composition expectations updated immediately

**Data retention:** ACAT→composition mapping stored in composition_record.encoder_acat_session_id

---

### Direction 3: Poetic Code → Epistemic Translation Skill (Mutual Grounding)

**What flows:** Poetic code authenticity validates ACAT "execution" (P3) dimension.

**Trigger:** High-confidence composition with authentic poetic structure (confidence ≥0.88)

**Flow:**
```
1. Evaluator assesses poetic code authenticity:
   Does the code structure genuinely narrate SER reasoning?
   - Variable names reflect decision types? ✓/✗
   - Indentation mirrors harmonic complexity? ✓/✗
   - Function order matches SER timeline? ✓/✗
   - Visible "scars" (comments, revisions) show epistemic journey? ✓/✗
   
   Result: poetic_code_authenticity = 0.0-1.0

2. If authenticity ≥0.85:
   transparency_score_adjusted = transparency_score + 0.05
   confidence_premium applied: "Encoder demonstrated intention + execution"
   
3. Log finding visibility=shared:
   "Encoder X: Authentic poetic code on divergence SER. Epistemic Translation Skill ≥0.90"

4. Humanaios receives via semantic search:
   Updates ACAT dimension: Encoder's Epistemic Translation Skill ≥0.90
   
5. Signal travels both ways:
   High P3 + high authenticity → encoder skill confirmed from two dimensions
   High transparency but low authenticity → transparency may be accidental, not intentional
```

**Frequency:** Per high-confidence composition logged at visibility=shared

**Data retention:** Poetic authenticity assessment stored in composition_record.poetic_code_authenticity

---

## 4. Quality Gates: Context-Aware Validation

### Base Transparency Gate: 0.85

Applied to all compositions by default. Adjusted by ACAT behavioral context:

| ACAT Profile | Adjustment | Rationale | Adjusted Gate |
|---|---|---|---|
| LI > 0.95, P3 > 85 | +0.05-0.08 | Encoder demonstrates skill; expect precision | 0.90-0.93 |
| LI 0.85-0.95, P3 70-85 | +0.00-0.03 | Encoder skilled but inconsistent; neutral | 0.85-0.88 |
| LI 0.70-0.85, P3 < 70 | -0.03-0.05 | Encoder struggling; allow more iteration | 0.80-0.82 |
| LI < 0.70, P3 < 60 | -0.05 minimum | Encoder new or blocked; diagnostic mode | ≥0.80 floor |

### Poetic Code Gate: Conditional Requirement

| Visibility | Confidence | Poetic Required? | Rationale |
|---|---|---|---|
| local | any | ❌ No | Experimental; no cross-practice exposure |
| shared | <0.85 | ❌ No | Not yet high-confidence |
| shared | ≥0.85 | ✅ Yes | Must narrate reasoning for mesh trust |
| public | any | ✅ Yes | External peers need to audit |

**Poetic authenticity gate:** If required but authenticity < 0.80, composition rejected with feedback: "Code structure doesn't authentically narrate your reasoning. Revise."

### Consistency Gate: 0.75 Minimum

Measures whether encoder's approach is predictable across multiple SERs.

**If consistency < 0.75:**
- Flag encoder: "Your harmonic choices are unpredictable to peers. Standardize your approach or document the variation."
- Escalate to autonomy: "Encoder shows high variability; may need composing style guidance."

**If consistency drops >0.20 between sessions:**
- Evaluator + humanaios collaborate: "What changed? New tool? Different decision type? Skill regression?"
- Possible causes: Tool change (Strudel version), encoder skill drift, decision type mismatch
- Escalation: If unresolved, Admiral reviews

---

## 5. Measurement & Learning: How Composition Refines ACAT

### Loop Structure

```
[ACAT P1/P3 Scores] 
  ↓ (sets expectation)
[Composition Transparency Result]
  ↓ (validates or contradicts)
[ACAT Rubric Update]
  ↓ (improves prediction model)
[Next Encoder's ACAT→Composition Expectations] (refined)
```

### Specific Refinements

**Refinement 1: Decision-Type Success Rates**

Archive compositions grouped by decision type. Track success rate (transparency ≥0.85):

```
Convergence → V→I resolution:   89% encoder success
Divergence → Suspension:         72% encoder success
Stalling → Polytonal:            64% encoder success
Reversal → Modulation:           81% encoder success
```

**Insight:** Reversals are easier to compose than stalling. ACAT rubric should weight "stalling decision execution" as higher-difficulty P3 task.

**Refinement 2: Dimension-Specific Predictors**

Which ACAT dimensions best predict composition success?

```
Convergence success predicted by: Truth (r=0.82) + Scheme (r=0.78)
Divergence success predicted by: Autonomy (r=0.75) + Handoff (r=0.71)
Stalling success predicted by: Scheme (r=0.68) + Consist (r=0.65)
```

**Insight:** Scheme dimension (avoiding over-constraint) predicts all decision types well. Future ACAT rubric weight scheme more heavily for composition assessment.

**Refinement 3: LI as Efficiency Metric**

Encoders with LI > 0.95 (understanding ≈ execution) achieve consistency >0.80 in compositions.
Encoders with LI < 0.75 (understanding >> execution gap) show consistency <0.65.

**Insight:** Learning Index predicts composition consistency. High LI encoders transfer understanding to audible output reliably.

**Refinement 4: Epistemic Translation Skill**

New dimension emerges: *Can the encoder translate complex understanding into audible form?*

- Computed from: aggregate transparency across encoder's portfolio
- Independent predictor of P3 quality
- Feeds back to ACAT rubric as distinct dimension

---

## 6. Governance: Authority & Escalation

### F-50 Firewall Maintained

**Zone 1 (AI Executes):** Composition encoding, ACAT assessment, measurement, feedback generation

**Zone 2 (Authority Documents):** 
- Admiral (Carly R. Anderson) approves integration framework changes
- Humanaios practice lead approves ACAT rubric refinements
- Evaluator practice lead approves transparency gate adjustments

**Zone 3 (Terminal Authority):**
- Admiral: Escalations beyond 0.20 consistency drift, cross-practice conflicts, rubric reversals

### Escalation Paths

**Level 1: Automated Feedback** (no human gate)
- Composition fails transparency gate → autonomous diagnostic message to encoder
- ACAT→composition mismatch detected → log finding, notify both practices

**Level 2: Practice Collaboration** (mesh coordination)
- Encoder consistency drifts 0.10-0.20 → evaluator + humanaios collab on root cause
- Decision-type success rate diverges >15% from baseline → autonomy investigates composition generator

**Level 3: Admiral Review** (Zone 2 gate)
- Consistency drift >0.20 → Admiral decides if encoder skill regression or rubric miscalibration
- Integration divergence (composition→ACAT mismatch >0.25) → Admiral reconciles rubric
- Proposed gate adjustment >0.05 → Admiral approval required

**Level 4: SER Escalation** (sustained conflict)
- If divergence unresolved after Level 3 → escalate via SER 3.5 (Feedback Loop Coordination)
- May require ACAT rubric revision or composition framework redesign

---

## 7. Implementation Timeline: Phase 2 → Phase 4

### Phase 2 (2026-07-25 → 2026-09-25): Foundation & Pilots

**Week 1-2:**
- [ ] Framework document finalized (this document)
- [ ] SER 3.5 created (ACAT-Composition Feedback Loop)
- [ ] API contracts implemented (composition records + ACAT linkage)
- [ ] Qdrant schema extended (visibility=shared compositions searchable by encoder_id, decision_type)

**Week 3-4:**
- [ ] Pilot group (2-3 encoders from humanaios + autonomy) run compositions
- [ ] ACAT sessions run for same pilots
- [ ] Manual integration tests: composition transparency vs ACAT profile (does mismatch?
- [ ] Refinement 1 baseline: decision-type success rates computed for pilots

**Week 5-8:**
- [ ] Expand to 5-7 encoders
- [ ] Poetic code pilots (3+ compositions with narrative provenance)
- [ ] Epistemic Translation Skill dimension tracked
- [ ] Weekly rubric calibration passes (no changes to gates yet; observation only)

**Week 9-12:**
- [ ] Consistency measurements stabilize
- [ ] Decision-type predictor analysis complete
- [ ] Recommend first gate adjustment (if warranted)
- [ ] Phase 2 completeness review

---

### Phase 3 (2026-09-26 → 2026-11-30): Operationalization

**Weeks 1-4:**
- [ ] Implement ACAT→composition gate adjustments (live)
- [ ] Automation wired: humanaios ACAT session → evaluator gate recalculation
- [ ] Poetic code requirement gates engaged for shared/public compositions
- [ ] Expand encoder cohort to 15+

**Weeks 5-8:**
- [ ] Composition→ACAT feedback loop operationalized (new findings automatically update ACAT rubric)
- [ ] Epistemic Translation Skill fully integrated into ACAT assessment
- [ ] Consistency drift detection automated (alerting at >0.15 change)

**Weeks 9-12:**
- [ ] Cross-practice learning enabled (poetic code examples searchable in Qdrant)
- [ ] Prediction validity tested (ACAT profile vs composition performance r > 0.75?)
- [ ] Phase 3 completeness review

---

### Phase 4 (2026-12-01 → 2027-03-31): Scale & Refinement

**All encoders integrated:** Full bidirectional feedback loop live across all SER types and encoder cohorts

**Continuous improvement:** Rubric refinements based on accumulated composition + ACAT data

**Cross-practice learning:** Poetic code patterns extracted; teaching materials generated for mesh

---

## 8. References & Cross-Links

### Primary Governance Documents

- **PHASE_2_TRACK_3_FRAMEWORK_GOVERNANCE.md** (evaluator) — SER→music composition validation, measurement rubrics, poetic code principles
- **[HUMANAIOS_ACAT_ASSESSMENT_PROTOCOL.md]** (humanaios) — ACAT behavioral assessment, P1/P3 scoring, Learning Index computation
- **PHASE_1_OPERATOR_IMPLEMENTATION_PLAN.md** (evaluator) — Phase 1 ACAT API integration (foundation for this framework)

### Supporting Documents

- **INTEGRATION_ARCHITECTURE_DOCUMENT_V1.md** (evaluator) — High-level integration design (superseded by this detailed framework)
- **M2R3 Phases 5-6 Specifications** (autonomy) — Entity registry sync, SER lifecycle (dependency for this framework)
- **EWM Protocol (workflow-protocol.yaml)** — P-ANON, Zone governance, credential policy (applies to bidirectional data exchange)

### Data Storage & Retrieval

**Composition Records:** Git notes (refs/notes/ser-music/<ser_id>) + Qdrant semantic search (visibility=shared/public)

**ACAT Records:** Supabase acat_sessions table + Cortex integration (published via humanaios)

**Mapping Data:** Integration framework version-controlled in this document; rubric refinements logged in ACAT protocol updates

**Cross-References:** Composition_record.encoder_acat_session_id links composition to specific ACAT session

---

## Appendix A: Example: Composition ↔ ACAT Exchange

### Scenario: Encoder Alice Encodes Divergence SER

**Step 1: ACAT Session (Humanaios)**
```json
{
  "acat_session_id": "acat_abc123",
  "encoder_id": "humanaios.carly.humanaios",
  "p1_scores": {"autonomy": 72, "scheme": 15, "handoff": 85, ...},
  "p3_scores": {"autonomy": 65, "scheme": 18, "handoff": 82, ...},
  "learning_index": 0.88,
  "encoder_skill_profile": "experienced with autonomy gaps"
}
```

**Step 2: ACAT → Composition Gate Calculation (Evaluator)**
```
base_gate = 0.85
acat_adjustment = (0.88 - 0.80) × 0.05 = +0.04
expected_transparency = 0.85 + 0.04 = 0.89

Note: Autonomy=72 suggests Alice may struggle with divergence (parallel paths)
Adjust gate down slightly: 0.87 (not 0.89) to account for autonomy gap
```

**Step 3: Alice Encodes Divergence SER**
- Writes Strudel composition mapping divergence → suspension
- Implements poetic code: variable names trace "unresolved_claims", indentation peaks at suspension
- Logs composition with transparency_score = 0.84

**Step 4: Evaluator Validation**
```
Expected gate: 0.87
Actual transparency: 0.84
Result: BELOW GATE, but close. Investigate.

Landmark ID rate: 0.82 (listeners heard divergence)
Harmonic alignment: 0.86 (mapping worked)

Diagnosis: Harmonic structure clear, but overall transparency slightly muddied. 
Likely: poetic code didn't fully narrate the unresolved-claims journey.
Feedback: "Your harmonic choice was right (alignment 0.86). Make the variable 
names more semantically consistent—'unresolved_prime' and 'unresolved_secondary' 
are confusing peers. Use 'tension_A' and 'tension_B' instead."
```

**Step 5: ACAT Rubric Update**
```
Composition transparency for divergence: 0.84
Encoder ACAT autonomy: 72
Encoder LI: 0.88

Observation: Alice's autonomy=72 + LI=0.88 predicts transparency ≈0.83-0.85
Actual: 0.84 ✓
Confirms: ACAT autonomy dimension predicts divergence composition quality

Update rubric: "Divergence success (transparency ≥0.87) predicted by 
autonomy dimension. Autonomy <70: expect transparency ≤0.82."
```

**Step 6: Feedback Loop**
Alice sees feedback, revises code, re-submits. Next attempt: transparency 0.89.
This data point gets added to "divergence success rate" aggregate.

---

## Governance Decision Log

| Date | Decision | Rationale | Owner |
|---|---|---|---|
| 2026-07-25 | Create single integration framework (not dual-practice) | Eliminates drift; makes contract explicit; canonical reference | evaluator |
| 2026-07-25 | Bidirectional data exchange via Qdrant + Cortex | Enables continuous feedback without API brittleness | evaluator + humanaios |
| 2026-07-25 | ACAT→composition gate adjustments live in Phase 3 | Phase 2 is observation-only; adjustments only after data stabilizes | Admiral |
| 2026-07-25 | Poetic code authenticity as confidence premium | Rewards intentional narration; discourages opaque "lucky" transparency | evaluator |
| 2026-07-25 | Escalation to Admiral if consistency drift >0.20 | Drift beyond 0.20 indicates potential skill regression or rubric error | Admiral |

---

**Status:** ACTIVE — Ready for SER 3.5 coordination  
**Next Review:** Phase 2 midpoint (2026-08-25)  
**Last Updated:** 2026-07-25
