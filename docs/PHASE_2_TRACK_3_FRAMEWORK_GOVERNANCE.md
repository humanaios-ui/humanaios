# Empirica Measurement Framework Governance

**Version:** 1.0  
**Date:** 2026-07-25  
**Owner:** empirica-foundation-evaluator (Carly R. Anderson)  
**Status:** ACTIVE  

---

## Phase 2 Track 3: SER Music Narratives — Measurement Framework

### Overview

SER (Shared Epistemic Record) coordination stories are encoded as Strudel music compositions. This framework defines how to measure, validate, and archive these encodings so they remain auditable, reproducible, and epistemically grounded.

**Scope:** Evaluator owns measurement framework, validation protocol, and archive governance for Phase 2 Track 3 (music narratives provenance layer).

---

## 1. SER→Music Narrative Mapping

### Participants → Voices

| SER Role | Voice Type | Harmonic Function |
|----------|-----------|-------------------|
| required | Lead + harmony | Primary narrative arc |
| participating | Melody | Supporting structures |
| observer | Ambient | Background texture |

**Rationale:** Required participants drive coordination story (lead voice); participating members add nuance (melody); observers provide context (ambient). Harmonic grammar reflects decision-making hierarchy.

### Decisions → Harmonic Grammar

| Decision Type | Harmonic Pattern | Musical Signal |
|---|---|---|
| Convergence | Resolution (V→I, dominant→tonic) | Closure, finality |
| Divergence | Suspension (unresolved tension) | Open question, waiting |
| Stalling | Polytonal (multiple key centers) | Disagreement, parallel paths |
| Reversal | Modulation + return | Course change + recovery |

**Rationale:** Harmonic grammar is the deepest layer of music cognition—listeners grasp it preverbally. Mapping decision states to harmonic language makes the SER arc audible without narration.

### Timeline → Phrasing Structure

| SER Element | Phrasing Equivalent |
|---|---|
| Duration (weeks/months) | Note value (whole→quarter) |
| Cadence pattern | Decision finality marker |
| Silence/rest | Waiting periods between transitions |
| Tempo | Decision velocity (slow=deliberate, fast=urgent) |

**Rationale:** Phrasing is how listeners perceive structure in time. Mapping SER timeline to phrasing makes the coordination story feel *temporal* rather than abstract.

---

## 2. Encoding Approach: Transparent

**Definition:** The music composition is *audible as the SER narrative* — listeners unfamiliar with the SER can infer participants, decisions, and state transitions from the music without liner notes.

**Not:** Metaphorical encoding (music evokes mood/feeling about coordination without structural mapping).

**Why:** Transparency serves two purposes:
1. **Reproducibility** — multiple musicians encoding the same SER should produce similar harmonic/phrasing patterns
2. **Cross-team handoff** — external listeners (outside the coordination group) can audit whether the encoding captured the story accurately

### Validation Test

**Blind listening test:** Play the composition to someone unfamiliar with the SER. Without seeing the SER timeline:
- Can they identify when decisions converged vs diverged?
- Can they estimate how many participants were involved?
- Can they identify turning points or reversals?

**Pass criterion:** ≥2/3 of test listeners correctly identify ≥3 structural landmarks (convergence points, decision reversals, timeline phases).

---

## 3. Archive Strategy: Dual Storage

### Primary: Git Notes (Audit Trail)

```bash
git notes --ref=refs/notes/ser-music add <ser_id> <composition_json>
```

**Purpose:** Immutable audit trail. Every SER composition is versioned, timestamped, and tied to a git commit. Enables historical comparison and derivation verification.

**Retention:** Permanent. Git notes survive rebases and force pushes (they're not part of commit history).

**Format:**
```json
{
  "ser_id": "<uuid>",
  "ser_title": "<SER name>",
  "composition": {
    "strudel": "<code>",
    "metadata": {
      "participants": [...],
      "encoded_at": "2026-07-25T...",
      "encoder": "mesh-support|autonomy|...",
      "validation_status": "pending|passed|failed"
    }
  },
  "provenance": {
    "ser_state_at_encoding": "closed",
    "decision_count": 4,
    "coordination_duration_weeks": 3
  }
}
```

### Secondary: First-Class Findings (Semantic Retrieval)

Log a finding with `sourced_from` link to the SER:

```bash
empirica finding-log \
  --finding "SER <ser_id> encoded as Strudel composition: <link>" \
  --impact 0.7 \
  --description "Audible narrative of coordination story. Participants: <names>. Duration: <weeks>. Validation: <status>." \
  --visibility shared
```

**Purpose:** Makes compositions discoverable via Qdrant semantic search. Cross-practice reference layer.

**Retrieval:** `empirica project-search --task "ser music" --global` surfaces compositions that encoded specific SER types.

### Automation

**Recommended:** Wire SER→music encoding into the SER close workflow:
1. SER transitions to `closed` state
2. Trigger autonomy's composition generator (Track 1 ambient + Track 2 markers + Track 3 music)
3. Auto-write git note + auto-log finding with `sourced_from` link
4. Timestamp both for audit trail

---

## 4. Validation Protocol: Two-Phase

### Phase 1: Structural Validation (Objective)

**What:** Does the composition arc match the SER state transitions?

**Method:** Automated analysis:
- Parse composition AST (abstract syntax tree)
- Extract harmonic grammar (resolution/suspension/modulation markers)
- Compare against SER state timeline (convergence/divergence/reversal events)
- Compute alignment score (% of decisions matched to harmonic grammar)

**Gate:** ≥85% alignment required before Phase 2.

**Tool:** `autonomy/ser-music-validator.py` (produces validation report JSON).

### Phase 2: Listening Assessment (Subjective)

**What:** Does the story come through sonically? Is the mapping transparent to unfamiliar listeners?

**Method:** Blind listening test with 3+ evaluators:
1. Play composition without showing SER timeline
2. Ask evaluator to identify decision points, convergences, reversals
3. Score accuracy on landmark identification (convergence, divergence, reversal, finality)
4. Collect qualitative feedback: "What story did you hear?"

**Gate:** ≥2/3 evaluators identify ≥3 key landmarks correctly.

**Validator:** empirica-foundation-evaluator (this practice).

### Combined Verdict

| Structural | Listening | Verdict |
|---|---|---|
| ✅ | ✅ | **VALIDATED** — composition approved for archive |
| ✅ | ❌ | **TRANSPARENT FAILURE** — harmonic mapping needs adjustment |
| ❌ | ✅ | **STRUCTURAL FAILURE** — AST analysis missed SER features |
| ❌ | ❌ | **REJECT** — re-encode required |

### Phase 3: Narrative Provenance — Poetic Code Structure (Optional Enhancement)

**What:** For high-confidence SERs logged at `--visibility shared` (confidence ≥0.85), use poetic machine programming to make code structure itself narrate decision-making.

**Rationale:** Code isn't just a generator; it's an artifact. When shared, the code's *structure* (variable names, indentation, function order) can reveal the encoder's reasoning process, making audits transparent and cross-practice learning possible.

**Poetic principles applied to SER→music:**

| Code Element | Narrative Function | Example |
|---|---|---|
| **Variable names** | Trace SER phases & decision types | `foundation`, `tension`, `resolution`, `unresolved_claims` |
| **Indentation depth** | Reflect hierarchical importance & constraint nesting | Deeper nesting = higher complexity in decision hierarchy |
| **Function call order** | Mirror SER timeline & participant convergence sequence | Foundation established first, tension layered second, resolution final |
| **Visible "scars"** | Show encoder's epistemic journey | Commented experiments, reassignments, branches attempted then abandoned |
| **Whitespace & layout** | Emphasize harmonic grammar transitions | Flat indentation at resolution; peaked at tension |

**Concrete example:**

```javascript
// SER→Music with poetic narrative provenance
let ser = parseStateRecord(stateData);

// FOUNDATION: Contextual agreements establish harmonic root
let foundation = ser.contextual_agreements
  .map(harmonic.root)                    // Builds upward
  .resolve();                             // Flattens—closure

// TENSION: Unresolved claims create harmonic suspension
let tension = ser.unresolved_claims      // Indentation deepens
  .map(note => harmonic.suspended(note))
  .stack()                                // Visual stacking = audible tension
  .stack()
  .stack();

// RESOLUTION: Convergence releases harmonic tension
let resolution = ser.convergence         // Back to base level
  .map(harmonic.dominant)
  .resolve();                             // Flattens—finality
```

**Reading this code, a peer understands:**
- Why foundation came first (semantic naming + structural position = epistemic priority)
- Why tension was layered in three stages (indentation depth mirrors harmonic complexity)
- Why resolution follows naturally (code flow = harmonic inevitability)
- When each participant converged (timeline markers in comments tied to SER state transitions)

**Gate:**
- ✅ Apply poetic structure to: high-stakes SER decisions, `--visibility shared` compositions, cross-practice handoffs, long-term archived work
- ❌ Don't apply to: mechanical mappings (utility functions), experimental passes, time-critical live coding, auto-generated code

**Benefit:** Peers can audit your reasoning by reading code structure. Supports mesh trust for high-confidence shared work. Enables epistemic transfer across practices—your decision process becomes learnable, not opaque.

**Validator:** Evaluator assesses whether poetic structure authentically reflects SER reasoning (vs. decorative). If genuine, it adds +0.05 to transparency score as a confidence premium (poetic structure = intentional narration = higher trustworthiness).

---

## 5. Escalation Protocol

### When Validation Fails

**Structural failure:** Autonomy reviews composition generator; regenerate with corrected AST parsing.

**Listening failure:** Evaluator and autonomy collaborate on harmonic mapping refinement; regenerate with adjusted grammar rules.

**Both fail:** Escalate to Admiral (Zone 2) — may indicate SER is too complex/ambiguous to encode musically. Proceed with narrative documentation instead.

### Notification Chain

1. Validation fails → autonomy + evaluator notified automatically (via SER state change)
2. If unresolved after 2 attempts → escalate to mesh-support (Zone 2)
3. If still unresolved → Admiral decision (Zone 3)

---

## 6. Measurement Rubric

### Transparency Score (0-1.0)

Measures how audible the SER narrative is from the music alone.

```
transparency = (landmark_identification_rate + harmonic_alignment_score) / 2
```

- **0.9-1.0:** Story is immediately clear; unfamiliar listeners grasp arc
- **0.7-0.9:** Story comes through with close listening; requires some context
- **0.5-0.7:** Structural mapping present but not intuitively audible
- **<0.5:** Failure; re-encode required

**Target:** ≥0.85 for all archived compositions.

### Encoding Consistency (0-1.0)

Measures whether multiple encoders would produce similar compositions for the same SER.

```
consistency = (overlap_in_harmonic_grammar + overlap_in_phrasing) / 2
```

Computed by having 2+ encoders independently encode the same historical SER, then compare AST structures.

**Target:** ≥0.75 for Phase 2 completeness.

---

## 7. Governance Decision Log

| Date | Decision | Rationale | Owner |
|---|---|---|---|
| 2026-07-25 | Transparent encoding (not metaphorical) | Enables reproducibility + cross-team audit | evaluator |
| 2026-07-25 | Dual archive (git notes + findings) | Immutability + semantic discoverability | evaluator |
| 2026-07-25 | Two-phase validation (structural + listening) | Objective + subjective grounding | evaluator |
| 2026-07-25 | Participant→voice role mapping | Harmonic grammar reflects hierarchy | evaluator |
| 2026-07-25 | Transparency score ≥0.85 gate | Ensures audible narrative | evaluator |
| 2026-07-25 | Poetic code structure (optional for shared/public) | Makes encoder reasoning auditable; supports mesh trust | evaluator |

---

## 8. Success Criteria (Phase 2 Track 3)

By end of Phase 2:

- [ ] ≥10 historical SERs encoded as compositions
- [ ] All compositions pass structural validation (≥85% alignment)
- [ ] All compositions pass listening validation (≥2/3 evaluators, ≥3 landmarks)
- [ ] Dual archive live (git notes + semantic findings)
- [ ] Automation wired (SER close → encode → validate → archive)
- [ ] Consistency measurement established (≥0.75 target)
- [ ] Cross-team reference system working (semantic search retrieves compositions)
- [ ] Poetic code structure documented and ≥1 high-confidence SER encoded with narrative provenance

---

## 9. Contacts & Escalation

| Role | Practice | Contact | Purpose |
|---|---|---|---|
| **Framework Owner** | evaluator | Carly R. Anderson | Measurement, validation, rubric |
| **Generator** | autonomy | [autonomy practice] | Encode SERs, AST analysis |
| **Executor** | mesh-support | [mesh-support practice] | Coordination, routing, SER closure |
| **Oversight** | Admiral | Carly R. Anderson (Zone 2/3) | Escalations, trade-offs, reversals |

---

**Status:** ACTIVE (ready for Phase 2 Track 3 execution)  
**Next Review:** Post-Phase 2 (2026-09-25 expected)  
**Last Updated:** 2026-07-25
