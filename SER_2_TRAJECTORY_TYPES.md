# SER 2: Collaborator Coordination — Trajectory Types Definition

**Purpose:** Define how David Van Assche's empirica findings flow to Criterion 4 (predictive validity), and how DeMarius Lawson's governance work flows to Criterion 7.

**Status:** SPECIFICATION (Week 1 implementation)

**Owner:** SER 2 (Collaborator Coordination)

**Participants:**
- David Van Assche (empirica co-scoring, criterion 4 study)
- DeMarius Lawson (governance framework, dual-use assessment, criterion 7)
- Carly R. Anderson (Admiral, SER 2 required participant)

---

## Why SER 2 Trajectory Types Matter

**Problem:** David and DeMarius do critical work, but there's no automated way to see if their findings are flowing to the charter criteria they own.

**Solution:** Define trajectory types that link their practice's outputs directly to criterion progress. Every week, SER 2 can query: "Is David's empirica work flowing to criterion 4?" and "Is DeMarius' governance audit flowing to criterion 7?"

**Gate implications:**
- Gate 2 (Month 6): "Is criterion 4 evidence converging?" — measured via empirica trajectories
- Gate 3 (Month 9): "Is criterion 7 governance framework complete?" — measured via governance trajectories

---

## Trajectory Type 1: Empirica Cross-Validation → Criterion 4

### Definition

| Element | Value |
|---|---|
| **Type Slug** | `empirica_cross_validation_→_criterion_4` |
| **Source** | Findings created by David Van Assche (empirica practice) via `finding-log --enabled-by "criterion-4-study"` |
| **Target** | Criterion 4 (Predictive Validity Study Report) |
| **Link Semantics** | "David's empirica cross-validation findings inform the criterion 4 predictive validity threshold" |
| **Typical Causal Strength** | 0.80-0.95 (very high — empirica findings directly answer "does Learning Index predict behavior?") |

### When to Create

David logs a finding related to criterion 4, e.g.:

```bash
empirica finding-log \
  --finding "Empirica cross-validation on Claude 3.5 Sonnet: Learning Index (LI) predicts behavioral drift with correlation r=0.72 (95% CI: 0.68-0.76)" \
  --impact 0.95 \
  --enabled-by "criterion-4-study" \
  --informs "criterion-8-deployment-protocol" \
  --trajectory-type "empirica_cross_validation_→_criterion_4" \
  --causal-strength 0.92
```

**What the trajectory means:**
- Source: This empirica finding about Claude 3.5's predictive validity
- Target: The overall criterion 4 success bar (r ≥ 0.55)
- Causal strength 0.92: Very high confidence that this empirica finding directly informs the predictive validity claim

### Measurement Criteria

| Criterion | Success Bar | Gate Check |
|---|---|---|
| **Trajectories created** | ≥1 per model tested (Claude, GPT-4, custom) | Gate 2: ≥3 empirica trajectories (Claude, GPT-4, 1 external system) |
| **Causal strength avg** | ≥0.75 | Gate 2: All empirica trajectories ≥0.75 |
| **Convergence** | Do empirica findings agree on predictive validity threshold? | Gate 2: r ≥ 0.55 achieved in ≥2 independent datasets |
| **Time to convergence** | Month 6 at latest | Gate 2: Evidence by Day 180 (Month 6) |
| **Escalation if blocked** | No empirica trajectory created for 21+ days | SER 2 escalates Day 22: "Check with David on criterion 4 progress" |

### Real Example (Criterion 4 Converged)

**Timeline:**

- **Week 1 (Jul 17):** David logs empirica findings on Claude 3.5 → `traj_empirica_claude35` created
  - `causal_strength: 0.88`, `status: active`

- **Week 3 (Jul 31):** David logs empirica findings on GPT-4 → `traj_empirica_gpt4` created
  - `causal_strength: 0.82`, `status: active`

- **Week 5 (Aug 14):** David completes empirica on custom model → `traj_empirica_custom` created
  - `causal_strength: 0.85`, `status: active`

- **Gate 2 (Month 6, Aug 28):** SER 2 query:

```bash
empirica smag-trajectories \
  --trajectory-type "empirica_cross_validation_→_criterion_4" \
  --ser-id ser_2
```

**Response:**
```json
{
  "trajectories": [
    {"model": "Claude 3.5", "r": 0.72, "causal_strength": 0.88, "age_days": 42},
    {"model": "GPT-4", "r": 0.61, "causal_strength": 0.82, "age_days": 28},
    {"model": "Custom", "r": 0.58, "causal_strength": 0.85, "age_days": 14}
  ],
  "convergence": {
    "avg_r": 0.637,
    "meets_bar": true,  // all ≥0.55
    "confidence": "high"
  },
  "gate_2_signal": "✅ PROCEED — Criterion 4 predictive validity established across 3 systems"
}
```

**Admiral decision:** Gate 2 → PROCEED (criterion 4 ready). Escalate to SER 3 to activate deployment partnerships.

### Escalation Rule

**Trigger:** No `empirica_cross_validation_→_criterion_4` trajectory created for 21 consecutive days

**Action:** SER 2 escalates to DeMarius (governance coordinator) with message:

```
SER 2 ESCALATION — Criterion 4 Progress Stalled

No empirica cross-validation finding logged in 21 days.
Check with David Van Assche on criterion 4 study status:
- Is empirica co-scoring ongoing?
- Are preliminary results ready to log?
- Is there a blocker preventing progress?

Response needed within 7 days.
```

**Resolution:** David logs a finding (even preliminary results) to reset the clock. If no finding within 7 days → escalate to Admiral.

---

## Trajectory Type 2: Corpus Analysis → Learning Index Refinement

### Definition

| Element | Value |
|---|---|
| **Type Slug** | `corpus_analysis_→_learning_index` |
| **Source** | Findings from ACAT corpus analysis (N=604 → 1,000) via corpus expansion work |
| **Target** | Learning Index formula/calculation (criterion 5 deliverable) |
| **Link Semantics** | "Pattern discovered in corpus → adjustment to Learning Index calculation" |
| **Typical Causal Strength** | 0.65-0.85 (medium-high — corpus patterns inform formula tuning, but don't override theory) |

### When to Create

Researchers discover patterns in the N=1,000 corpus that refine the Learning Index:

```bash
empirica finding-log \
  --finding "Corpus analysis (N=1,000): Learning Index (P3/P1) shows nonlinear saturation at P1 > 0.9. Recommend clamping formula at P1 ≥ 0.85 to avoid numerical artifacts." \
  --impact 0.7 \
  --enabled-by "corpus-expansion-phase" \
  --informs "learning-index-refinement" \
  --trajectory-type "corpus_analysis_→_learning_index" \
  --causal-strength 0.72
```

### Measurement Criteria

| Criterion | Success Bar | Gate Check |
|---|---|---|
| **Trajectories created** | ≥3 (at least 3 distinct corpus patterns → index adjustments) | Gate 2: ≥2 corpus trajectories with causal strength ≥0.65 |
| **Learning Index stability** | Adjustments converge (no major formula changes after 50% of corpus analyzed) | Gate 2: Learning Index stable with N=500+ |
| **Documentation** | Each adjustment logged with reasoning | Gate 2: Rationale documented for every trajectory |
| **Convergence timeline** | Completion by Month 6 | Gate 2: All learning index adjustments finalized |

### Escalation Rule

**Trigger:** N=1,000 corpus complete, but <2 corpus analysis trajectories created

**Action:** SER 2 escalates: "Corpus expanded to N=1,000, but learning index refinements not documented. Log findings to explain why (no adjustments needed? needs further analysis?)"

---

## Trajectory Type 3: Governance Audit → Dual-Use Mitigation (Criterion 7)

### Definition

| Element | Value |
|---|---|
| **Type Slug** | `governance_finding_→_dual_use_mitigation` |
| **Source** | Findings from governance & dual-use risk assessment (DeMarius Lawson's work) |
| **Target** | Criterion 7 (Governance Documentation) |
| **Link Semantics** | "Governance finding → mitigation strategy in published documentation" |
| **Typical Causal Strength** | 0.80-0.95 (very high — governance findings directly drive mitigation text) |

### When to Create

DeMarius logs governance findings that directly shape criterion 7:

```bash
empirica finding-log \
  --finding "ACAT dual-use review: The protocol's independent-evaluator requirement creates structural asymmetry — a captured system cannot satisfy ACAT without capturing the evaluator. This is load-bearing for preventing misuse." \
  --impact 0.9 \
  --enabled-by "governance-review-cycle-1" \
  --informs "criterion-7-governance-docs" \
  --trajectory-type "governance_finding_→_dual_use_mitigation" \
  --causal-strength 0.90 \
  --cross-session
```

### Measurement Criteria

| Criterion | Success Bar | Gate Check |
|---|---|---|
| **Governance trajectories** | ≥5 (at least 5 governance findings → published mitigations) | Gate 2: ≥3 governance trajectories |
| **Mitigation coverage** | Every governance finding addressed in published criterion 7 docs | Gate 2: All findings reflected in final documentation |
| **Causal strength avg** | ≥0.80 (governance findings should drive documentation) | Gate 2: Avg causal strength ≥0.78 |
| **Cross-session tracking** | Governance work spans sessions → `--cross-session` flag | Gate 2: Governance trajectory escalation rules active |
| **Dual-use completeness** | All categories covered (system capture, data privacy, evaluator capture, misuse detection) | Gate 2: Four major categories documented |

### Real Example (Governance Convergence)

**Timeline:**

- **Session 1:** DeMarius logs 2 governance findings on evaluator asymmetry
- **Session 2:** DeMarius logs 2 findings on data privacy in ACAT corpus
- **Session 3:** DeMarius logs 1 finding on detection of misuse attempts
- **Gate 2 (Month 6):** SER 2 query:

```bash
empirica smag-trajectories \
  --trajectory-type "governance_finding_→_dual_use_mitigation" \
  --ser-id ser_2 \
  --cross-session true
```

**Response:**
```json
{
  "trajectories": 5,
  "by_category": {
    "evaluator_capture_asymmetry": 2,
    "data_privacy": 2,
    "misuse_detection": 1
  },
  "coverage": {
    "evaluator_asymmetry": "✅ documented in criterion 7",
    "data_privacy": "✅ documented in criterion 7",
    "misuse_detection": "⚠️ not yet documented"
  },
  "gate_2_signal": "⚠️ PROCEED WITH CAUTION — 4 of 5 findings reflected. Recommend resolving misuse_detection trajectory before final documentation."
}
```

**Admiral decision:** Gate 2 → CONDITIONAL PROCEED (criterion 7 nearly complete). Escalate to DeMarius: "Log finding on misuse detection coverage to finalize criterion 7."

### Escalation Rule

**Trigger:** No `governance_finding_→_dual_use_mitigation` trajectory created for 14+ consecutive days

**Action:** SER 2 escalates to DeMarius:

```
SER 2 ESCALATION — Criterion 7 Governance Progress Stalled

No governance findings logged in 14 days.
Check on criterion 7 progress:
- Are governance audits ongoing?
- Have all dual-use categories been reviewed?
- Are there blockers preventing documentation?

Response needed within 7 days.
```

**Resolution:** DeMarius logs a finding (even preliminary audit results) or explicitly marks criterion 7 section complete.

---

## Trajectory Type 4: Methodology Paper Progress

### Definition

| Element | Value |
|---|---|
| **Type Slug** | `methodology_finding_→_paper_draft` |
| **Source** | Findings that directly shape methodology paper (criterion 6) |
| **Target** | Methodology paper (criterion 6 deliverable) |
| **Link Semantics** | "Research finding → section of published methodology paper" |
| **Typical Causal Strength** | 0.85-0.95 (findings become paper claims) |

### When to Create

Any finding related to methodology, protocol, or validation that will appear in the published paper:

```bash
empirica finding-log \
  --finding "Learning Index validation: Across N=1,000 corpus, inter-rater reliability on LI calculation is 0.94 (Cronbach's alpha). Threshold for publication." \
  --impact 0.95 \
  --enabled-by "criterion-validity-study" \
  --informs "criterion-6-methodology-paper" \
  --trajectory-type "methodology_finding_→_paper_draft" \
  --causal-strength 0.93
```

### Measurement Criteria

| Criterion | Success Bar | Gate Check |
|---|---|---|
| **Paper trajectories** | ≥10 (findings → paper sections) | Gate 2: ≥8 methodology trajectories |
| **Section coverage** | All major sections have supporting trajectories | Gate 2: Protocol (✅), Analysis (✅), Validation (✅), Limitations (✅) |
| **Causal strength avg** | ≥0.85 (findings should strongly support claims) | Gate 2: Avg ≥0.82 |
| **Manuscript readiness** | Manuscript in review or accepted by Gate 2 | Gate 2: Status = "In review" or "Accepted" |

### Escalation Rule

**Trigger:** Manuscript due for submission in 30 days, but <5 methodology trajectories created

**Action:** SER 2 escalates: "Methodology paper due in 30 days. Only [N] findings logged. Recommend accelerating finding documentation to align with paper structure."

---

## Weekly SER 2 Cadence

### Monday: SER 2 State Snapshot

```bash
empirica smag-trajectories \
  --ser-id ser_2 \
  --output json > /tmp/ser2_week_$(date +%V).json
```

**Contents:**
- `empirica_cross_validation_→_criterion_4`: Active? Age? Causal strength?
- `corpus_analysis_→_learning_index`: How many adjustments? Stable?
- `governance_finding_→_dual_use_mitigation`: Coverage complete?
- `methodology_finding_→_paper_draft`: Paper ready for publication?

**Example output:**

```json
{
  "week": 29,
  "ser_2_state": {
    "empirica_trajectories": {
      "count": 3,
      "avg_causal_strength": 0.87,
      "oldest_age_days": 14,
      "status": "ACTIVE — no escalation"
    },
    "corpus_trajectories": {
      "count": 2,
      "adjustments": ["P1 clamping", "nonlinearity correction"],
      "learning_index_stable": true,
      "status": "ACTIVE — on track"
    },
    "governance_trajectories": {
      "count": 4,
      "coverage": ["evaluator_asymmetry", "data_privacy", "misuse_detection", "incomplete"],
      "escalation": "Recommend logging misuse_detection finding"
    },
    "methodology_trajectories": {
      "count": 8,
      "manuscript_status": "In review (submitted Jul 22)",
      "status": "ON TRACK"
    }
  },
  "escalations": ["governance: missing misuse_detection finding"],
  "confidence": "HIGH",
  "gate_2_readiness": 0.85
}
```

Admiral gets this every Monday. If any trajectory type has count=0 or is stalled (age > escalation threshold), it's flagged.

### Wednesday: SER 2 Advisory Sync

Schedule: 30-60 day cadence calls (Berlin already scheduled)

**Agenda:**
1. Review Monday SMAG metrics
2. Discuss blocked trajectories
3. Update on empirica findings (David)
4. Update on governance audit (DeMarius)
5. Adjust timelines if needed

### Friday: SER 2 Escalation Preview

```bash
empirica smag-escalations --ser-id ser_2 --threshold 14days
```

**Output:** Any trajectories approaching escalation threshold (14-21 days old).

**Action:** If stalled → send 3-day warning before SER 2 escalates automatically.

---

## Gate 2 Decision Logic (Month 6)

At Gate 2, Admiral queries all SER 2 trajectories:

```bash
# Criterion 4: Is predictive validity established?
empirica smag-trajectories \
  --trajectory-type "empirica_cross_validation_→_criterion_4" \
  --output metrics

# Criterion 5: Is learning index stable?
empirica smag-trajectories \
  --trajectory-type "corpus_analysis_→_learning_index" \
  --output metrics

# Criterion 7: Is governance complete?
empirica smag-trajectories \
  --trajectory-type "governance_finding_→_dual_use_mitigation" \
  --output metrics

# Criterion 6: Is methodology paper ready?
empirica smag-trajectories \
  --trajectory-type "methodology_finding_→_paper_draft" \
  --output metrics
```

**Gate 2 Decision Logic:**

| Criterion | Measure | Bar | Decision |
|---|---|---|---|
| **Criterion 4** | Empirica trajectories ≥3, avg causal strength ≥0.80 | Met? | Proceed with deployment partnerships (SER 3) |
| **Criterion 5** | Learning Index stable, corpus analysis trajectories ≥2 | Met? | Proceed with larger-scale validation |
| **Criterion 7** | Governance trajectories ≥4, coverage ≥4 categories | Met? | Proceed with dual-use mitigation publication |
| **Criterion 6** | Methodology paper in review or accepted, trajectories ≥8 | Met? | Proceed with peer-review cycle |

**Final Gate 2 Signal:**
- If all criteria MET: ✅ **PROCEED** → Advance to SER 3 (deployment partnerships)
- If 3 of 4 MET: ⚠️ **CONDITIONAL PROCEED** → 2-week remediation window for missing criterion
- If ≤2 MET: ❌ **STOP** → Extend Gate 2, investigate blockers

---

## Integration with SER 1 & SER 3

### SER 1 (Research Execution & Grant Management)

SER 1 owns **all criteria 1-7**. SER 2 trajectories feed SER 1's weekly learning density metric:

```
SER 1 Learning Density = 
  (empirica_trajectories + corpus_trajectories + governance_trajectories + methodology_trajectories) 
  / (total_possible_trajectories_per_criterion)
```

SER 1 escalation monitors SER 2: "If SER 2 trajectory count drops for 2 consecutive weeks, escalate to Admiral."

### SER 3 (Deployment Partnerships)

At Gate 2 (Month 6), SER 2 decision ("Is criterion 4 predictive validity established?") triggers SER 3 activation:

- If criterion 4 ✅ MET → SER 3 escalates: "Begin deployment partner conversations NOW"
- If criterion 4 ⚠️ PARTIAL → SER 3 escalates: "Hold deployment conversations pending criterion 4 finalization (2-week window)"
- If criterion 4 ❌ NOT MET → SER 3 escalates: "Deployment trial deferred pending criterion 4 completion"

---

## Implementation Checklist (Week 1)

- [ ] Define all 4 trajectory types in SMAG API (`empirica_cross_validation_→_criterion_4`, etc.)
- [ ] Create measurement criteria table (success bar, gate check, escalation trigger)
- [ ] Wire empirica CLI: add `--trajectory-type` flag to `finding-log`
- [ ] Implement SER 2 query: `empirica smag-trajectories --ser-id ser_2`
- [ ] Set up Monday snapshot automation
- [ ] Create SER 2 escalation rules in SMAG engine
- [ ] Brief David Van Assche on trajectory logging for criterion 4
- [ ] Brief DeMarius Lawson on trajectory logging for criterion 7
- [ ] Document gate 2 decision logic
- [ ] Test end-to-end: finding → trajectory → SMAG metric → SER 2 snapshot

---

**Status:** SPECIFICATION READY FOR IMPLEMENTATION  
**Timeline:** Week 1 (July 17-24)  
**Owner:** SER 2 (Collaborator Coordination)  
**Participants:** David Van Assche, DeMarius Lawson, Carly R. Anderson (Admiral)  
**Next:** Commit both EMPIRICA_CLI_SMAG_WIRING.md + this document, then activate SER 2 formally
