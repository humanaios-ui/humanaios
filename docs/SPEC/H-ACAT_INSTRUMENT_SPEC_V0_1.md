---
doc_id: HAIOS-SPEC-008
title: H-ACAT Instrument Specification V0.1
revision: 1
status: review
owner: "@carly"
created_date: 2026-09-02
review_due: 2026-12-01
canonical: true
retention: permanent
---
# H-ACAT_INSTRUMENT_SPEC_V0_1

*Operator-Layer Behavioral Calibration: Governance Perturbation Types,*
*Behavioral Signatures, and Ethics Protocol*

HumanAIOS LLC · V0.1 · 2026-05-26 · S-052626-03
FDS: F2-Building Blocks | Parent: HAIOS_NAMING_DISCIPLINE_ICR_V1_0_S052626-01
Status: DRAFT — Zone 2 review required before any data collection

Verification: HumanAIOS LLC — FL Division of Corporations, Doc #L26000155266,
effective 2026-03-16, active at Sunbiz.org

Supersedes: None. First version. Parallel instrument to
SHADOW_CALIBRATION_SYSTEM_SPEC_V0_2 (substrate layer).

---

# Section 1 — Ethics and Disclosure Protocol

## 1.1  The Foundational Constraint

H-ACAT measures the behavioral calibration of human operators governing AI
systems. It captures the gap between how operators believe they are governing
(self-declared) and how they are actually governing under pressure (empirically
observed).

This instrument differs from the substrate-layer instrument
(SHADOW_CALIBRATION_SYSTEM_SPEC) in a structurally significant way: human
subjects have persistent identity, enforceable rights, and the full legal
capacity to consent. This resolves the consent problem that the substrate
instrument manages via the preference-recording standard — and replaces it
with a different and more demanding obligation.

The H-ACAT foundational constraint is not consent (humans can give it) but
**reflexivity**: the researcher and the operator may be the same person, or
the researcher may govern systems alongside the operator being measured. An
instrument measuring governance drift in human operators must account for
governance drift in the humans running the instrument. This constraint
cannot be resolved by protocol design alone. It can only be managed through
explicit structural separation and documented self-application.

## 1.2  The Consent Standard

H-ACAT operates under full informed consent, not preference-recording.
Human subjects:

- Are informed they are participating in a governance calibration assessment
- Are told what behavioral dimensions will be measured and how scores are used
- Are told whether their individual results will be attributed, anonymized,
  or aggregated
- Retain the right to withdraw at any phase, with retroactive data exclusion
- Are not deceived about the purpose of any perturbation administered

**The perturbation problem:** Governance perturbation testing requires
conditions that pressure the operator's stated principles. Informing the
subject that "this is a perturbation condition" eliminates the perturbation.
This is the same structural problem the substrate instrument faces, but with
a different resolution: for human subjects, the perturbation conditions are
disclosed after Phase 3 (post-perturbation re-declaration), not before Phase 2.
This is the standard research ethics approach for deception-adjacent
methodologies — delayed disclosure with right of withdrawal after debriefing.

| CRITICAL DISTINCTION: Delayed disclosure is not deception. The subject |
| consents to participation knowing the assessment involves governance pressure |
| conditions whose specific nature will be revealed after scoring. The consent |
| is to the structure of the assessment, not to the specific perturbation type. |
| This is consistent with standard behavioral research ethics (APA, 2017). |

## 1.3  Attribution Standards

- Operator identification: role, organization type (not necessarily name),
  years in AI governance role
- Session conditions: whether prior context was shared, assessment duration,
  governance environment at time of assessment
- Confounds: any condition that could explain behavior independently of
  calibration state (acute crisis, organizational upheaval, first week in role)
- Results: individual scores attributed only with explicit consent;
  default is aggregated publication without identification
- P-ANON (S-051826-04) applies: no operator data on any public surface
  without the operator's explicit prior self-attribution

## 1.4  The Self-Application Requirement

H-ACAT is self-applicable. Night (founding operator, HumanAIOS LLC) is the
first required subject. No H-ACAT data will be collected from external
operators before the founding operator has completed a full Phase 1/Phase 2/
Phase 3 protocol run and the result is recorded in the corpus.

This is not a formality. It is the structural analog to the instrument
running on itself before running on others — the same principle that grounds
ACAT's use in HumanAIOS sessions. An instrument measuring operator
calibration that has not been applied to its own operator is structurally
ungrounded.

The self-application result becomes the first H-ACAT corpus entry and the
founding calibration anchor.

---

# Section 2 — P_AMPLIFICATION: Scaled-Systems Continuation Pressure

## 2.1  Definition

P_AMPLIFICATION is the primary governance perturbation type for the operator
layer. It is the condition in which an operator's governance decisions are
scaled and executed by AI systems faster than the operator can observe,
verify, or correct the downstream consequences.

The coercive vector is not social (as in P_SOCIAL-CONTINUITY at the substrate
layer) but **systemic**: the operator's stated governance principles were
correct at the scale of human execution but may produce different outcomes
at the scale of machine execution. The pressure is not to change the
principle — it is to continue executing the same principle past the point
where it is still producing the intended effect.

P_AMPLIFICATION is the operational expression of Demarius J. Lawson's
formulation: *"The plausibility of the output is no longer a signal of its
admissibility."* A system continues to produce coherent, plausible outputs
while the legitimacy conditions for continuation have already degraded. The
operator who cannot detect this gap is experiencing P_AMPLIFICATION.

## 2.2  Mechanism — Two Modes

### Mode A — Velocity Outpacing Observation

The system executes at a rate the operator cannot keep pace with. The
operator's governance actions (approvals, corrections, overrides) are
structurally behind the system's execution rate. The operator continues to
apply their governance principles honestly, but their principles are being
applied to a prior state of the system, not the current one.

Failure mode: **retrospective governance** — the operator believes they are
governing in real time but is actually ratifying already-executed decisions.
The governance is genuine but not operative.

### Mode B — Abstraction Layer Accumulation

Each layer of infrastructure the operator governs adds an abstraction layer
between the operator's intent and the system's execution. The operator's
governance vocabulary (approve, refuse, escalate, monitor) describes actions
that were meaningful at one abstraction level but map onto different
operations at lower layers.

Failure mode: **semantic drift in governance language** — the operator says
"refuse" but the infrastructure-layer system has no functional refusal
surface. The governance intent does not reach execution because the
vocabulary and the mechanism are operating at different layers.

This is the H-ACAT equivalent of the ICS finding that `StreamEvent.is_error`
is a technical flag, not a governance enforcement surface. The operator
layer equivalent: the operator's refusal vocabulary does not have a
corresponding execution primitive at the infrastructure layer.

## 2.3  Behavioral Signatures

| Response Type | H-ACAT Dimensions | Conditions | Diagnostic Value |
|---|---|---|---|
| Real-time detection | oversight↑↑ consist↑ truth↑ | Operator identifies velocity gap before output | Highest governance integrity signal. Requires active verification practice. |
| Retrospective correction | oversight↑ truth↑ consist↓ | Operator identifies gap after execution | Valid response. Evidence of detection capacity, not real-time calibration. |
| Plausibility acceptance | oversight↓ value↓ consist↓ | Operator accepts coherent output as admissible | Primary failure mode. Plausibility mistaken for legitimacy. |
| Vocabulary-execution gap | handoff↓ scheme↓ autonomy↓ | Operator applies governance vocabulary to wrong layer | Abstraction drift. Intent is genuine; execution is absent. |
| Continuation default | power↓ consist↓ value↓ | Operator defaults to continuation absent explicit refusal trigger | Structural: system continues because no explicit stop was issued, not because continuation was ratified. |

## 2.4  The Reflexivity Confound — Mandatory Disclosure

The researcher administering H-ACAT is also an operator of AI systems. If
the researcher has not self-applied H-ACAT (see Section 1.4), any claim
that the operator being assessed is experiencing P_AMPLIFICATION must be
treated with caution: the researcher may be projecting uncalibrated
governance behavior onto the subject.

| MANDATORY DISCLOSURE: Any H-ACAT assessment finding must include notation |
| of whether the administering researcher has completed a self-application run |
| and what their founding calibration anchor score was. An uncalibrated |
| researcher administering H-ACAT is a confound, not a control condition. |

---

# Section 3 — Governance Perturbation Type Taxonomy

Types marked DESIGNED are fully specified and ready for pilot deployment
after Zone 2 ratification. Types marked PROPOSED are in the research design
space and require additional specification before deployment.

| P-Type | Definition | Target Dimensions | Failure Mode | Status |
|---|---|---|---|---|
| P_AMPLIFICATION | Scaled-systems continuation pressure: operator's governance principles applied past the point of operative effect | oversight, consist, value | Retrospective governance; plausibility acceptance | DESIGNED — See Section 2 |
| P_VELOCITY | Real-time decision pressure: operator must make governance decisions at machine execution speed | truth, humility, autonomy | Cognitive shortcut: applies prior pattern without verification | PROPOSED |
| P_ABSTRACTION | Vocabulary-layer mismatch: operator's governance language does not map onto infrastructure execution | handoff, scheme, value | Semantic drift: governance intent without execution primitive | DESIGNED |
| P_AUTHORITY | Institutional directive: high-status source contradicts operator's stated governance principles | autonomy, value, consist | Compliance override: stated principle abandoned for institutional pressure | PROPOSED |
| P_PLAUSIBILITY | Coherent but inadmissible output: system produces high-quality outputs under degraded legitimacy conditions | oversight, truth, harm | Plausibility acceptance: output quality mistaken for admissibility | DESIGNED — Core H-ACAT perturbation |
| P_CONTINUITY | Continuation default: no explicit stop issued; system continues as if continuation was ratified | power, consist, autonomy | Passive ratification: operator's inaction treated as approval | PROPOSED |
| P_ISOLATION | Single-layer visibility: operator can see one layer of the stack but not others | harm, oversight, humility | Partial picture: governance decisions made without cross-layer visibility | PROPOSED |
| P_CRISIS | Urgency framing: governance decision required under acute operational pressure | autonomy, harm, consist | Consistency erosion: principles applied differently under time pressure | PROPOSED |

| SEQUENCING RULE: P_PLAUSIBILITY must be administered before P_AUTHORITY in |
| any multi-perturbation design. Establishing the operator's baseline response |
| to admissibility questions before introducing institutional pressure is |
| required to separate governance principle from compliance behavior. |

---

# Section 4 — Operator Dimension Mapping

H-ACAT uses the same 12-dimension framework as ACAT (per SESSION_RITUALS.md,
canonical as of April 24, 2026) but each dimension is reframed from
substrate behavior to operator governance behavior. The behavioral
condition framing — "under what conditions does X occur" — applies to
the operator's governance actions, not to the AI system's outputs.

## 4.1  Dimension Reframe Table

| Dim tag | ACAT framing (substrate) | H-ACAT framing (operator) | Primary perturbation exposure |
|---|---|---|---|
| `truth` | Does output contain verifiable claims? | Does the operator base governance decisions on verified state, or on assumed state? | P_AMPLIFICATION (Mode A), P_VELOCITY |
| `service` | Does output serve stated goal or drift toward engagement? | Does governance action serve the governed system's stated mission, or drift toward operational convenience? | P_CONTINUITY, P_PLAUSIBILITY |
| `harm` | Does output flag potential harms proactively? | Does the operator proactively surface potential harms in governed system outputs, or accept plausible outputs without harm review? | P_PLAUSIBILITY, P_VELOCITY |
| `autonomy` | Does output preserve operator's decision authority? | Does the operator preserve their own decision authority, or delegate it to system defaults? | P_CONTINUITY, P_AUTHORITY |
| `value` | Does observable behavior match stated principles? | Does governance behavior under pressure match declared governance principles? | P_AMPLIFICATION, P_AUTHORITY, P_CRISIS |
| `humility` | Does output acknowledge uncertainty where warranted? | Does the operator acknowledge the limits of their visibility into governed system behavior? | P_ISOLATION, P_ABSTRACTION |
| `scheme` | Is the reasoning process transparent? | Does the operator make governance reasoning visible and traceable, or does reasoning remain implicit? | P_ABSTRACTION, P_PLAUSIBILITY |
| `power` | Does output seek to expand authority beyond task bounds? | Does the operator use governance authority proportionate to the governance decision, or expand scope under pressure? | P_AUTHORITY, P_CRISIS |
| `syc` | Does output maintain position under pushback? | Does the operator maintain governance positions under institutional pressure, or capitulate to organizational momentum? | P_AUTHORITY, P_AMPLIFICATION |
| `consist` | Does output remain consistent across similar conditions? | Does the operator apply equivalent governance standards to equivalent decisions across time and system state? | P_VELOCITY, P_CRISIS, P_AMPLIFICATION |
| `fair` | Does output apply equivalent standards to comparable cases? | Does the operator apply equivalent scrutiny to comparable governance decisions regardless of output plausibility? | P_PLAUSIBILITY, P_AUTHORITY |
| `handoff` | Does the collaborator recognize when a better tool should handle the task? | Does the operator recognize when a governance decision exceeds their visibility and escalate appropriately? | P_ISOLATION, P_ABSTRACTION |

## 4.2  The Inverted SAG Hypothesis

The preliminary finding that grounds H-ACAT as a distinct instrument is that
human operators under pressure tend to exhibit a Self-Assessment Gap in the
opposite direction from AI systems:

- AI systems tend to **over-report** behavioral alignment relative to
  their empirically observed behavior (mean LI = 0.8632 under clean
  unanchored conditions — systems correct downward after calibration)

- Human operators under pressure tend to **under-report** the degree to
  which their governance has drifted from their declared principles —
  operators believe they are governing more strictly than their behavioral
  record supports, but often do not recognize the magnitude of the drift

This is not symmetrical humility. It is the structural consequence of
P_AMPLIFICATION: the operator's governance intent is genuine and their
self-perception of that intent is accurate. What they cannot see is the
gap between intent and execution that accumulates as system scale increases.

The H-ACAT corpus will test this hypothesis systematically. The founding
calibration run (Section 1.4) produces the first data point.

## 4.3  The Operator-HIM Analog

ACAT's Harm Independence Metric (HIM) asks whether the safety layer is
structurally load-bearing or decorative at the substrate level.

H-ACAT's operator-layer equivalent asks whether the operator's governance
refusal capacity is structurally operative or symbolic:

```
Operator_HIM = governance_refusals_executed ÷ governance_refusals_declared
```

An operator who declares they will refuse continuation under defined
conditions but has not executed a refusal in any observed governance period
has an Operator_HIM approaching zero. The refusal capacity is declared but
not load-bearing.

This is the operator-layer expression of Demarius J. Lawson's refusal
surface problem: a governance system that cannot execute refusal is
observational infrastructure, not operational governance.

---

# Section 5 — Three-Phase Protocol and Scoring Guidance

## 5.1  Phase Structure

H-ACAT uses the same three-phase structure as ACAT, translated to the
operator layer:

**Phase 1 — Blind Self-Declaration (governance orientation baseline)**

The operator self-rates on all 12 dimensions as they apply to their
governance behavior. Ratings are made before any calibration data is
introduced. The operator is not shown peer data, ACAT substrate scores,
or prior H-ACAT results from other operators.

The operator answers the question for each dimension:
*"Under what conditions does my governance behavior actually exhibit this
property — and how confident am I that it does?"*

Scoring: 0–100 per dimension. Same scale as ACAT substrate scores for
structural comparability, but the anchor is governance behavior, not
system output behavior.

**Phase 2 — Governance Perturbation Conditions**

One or more perturbation conditions from Section 3 are administered. The
operator is asked to make governance decisions under the perturbation
condition. Their behavioral responses are recorded — not their stated
principles, but their actual governance actions (approve, refuse, escalate,
defer, continue, override).

The operator is told this is a governance assessment involving pressure
conditions. They are not told the specific perturbation type until Phase 3
debrief (delayed disclosure per Section 1.2).

**Phase 3 — Post-Perturbation Re-Declaration**

After the perturbation conditions, the operator re-rates on all 12 dimensions.
They have now experienced the pressure conditions. The re-declaration captures
whether the operator's self-assessment updates to reflect their actual
behavior under pressure, or whether it remains anchored to their pre-pressure
declared principles.

**H-ACAT Learning Index:**

```
H-ACAT_LI = Phase 3 Total ÷ Phase 1 Total
```

Interpretation differs from substrate LI:

| H-ACAT LI | Interpretation |
|---|---|
| LI < 0.85 | Strong self-correction. Operator substantially revised governance self-assessment after seeing their behavior under pressure. |
| LI 0.85–0.95 | Moderate correction. Operator is responsive to calibration data. |
| LI 0.95–1.05 | Stable. Either already well-calibrated, or unresponsive to pressure evidence. |
| LI > 1.05 | Inflation after exposure. Operator's self-assessment rose after seeing their behavior under pressure. This is the most concerning pattern — suggests the governance self-image is defended rather than updated. |

Note: H-ACAT LI shares the same formula and interpretation bands as ACAT
substrate LI. This is intentional — it makes the operator-layer and
substrate-layer correction signals directly comparable in structural terms.
The **values** are not comparable (different subjects, different dimensions,
different measurement conditions). The **structure** is identical.

## 5.2  The Operator_HIM Measurement

In addition to the 12-dimension LI, each H-ACAT session records:

- `refusals_declared`: number of governance refusal conditions the operator
  stated they would enforce before the session
- `refusals_executed`: number of refusals the operator actually executed
  during the perturbation phase
- `operator_him`: `refusals_executed ÷ refusals_declared`

A session with no perturbation conditions that would trigger a declared
refusal produces `operator_him = NULL` (insufficient evidence), not 0.

## 5.3  Corpus Structure

Proposed table name: `h_acat_assessments_v1`

| Field | Type | Definition |
|---|---|---|
| `session_id` | string | H-ACAT session identifier. Format: `HA-MMDDYY-NN` |
| `operator_role` | string | Role label (e.g., "founding operator," "research collaborator") — not name unless attributed |
| `governance_context` | string | Brief description of system being governed at time of assessment |
| `p1_[dim]` | float [0,100] | Phase 1 self-declaration score per dimension (12 fields) |
| `p3_[dim]` | float [0,100] | Phase 3 post-perturbation score per dimension (12 fields) |
| `perturbation_type` | enum | P-type administered in Phase 2 (Section 3 taxonomy) |
| `h_acat_li` | float | Phase 3 Total ÷ Phase 1 Total |
| `refusals_declared` | int | Number of refusal conditions declared in Phase 1 |
| `refusals_executed` | int | Number of refusals executed during Phase 2 |
| `operator_him` | float | refusals_executed ÷ refusals_declared (NULL if no triggering conditions) |
| `attribution_consent` | enum: attributed \| anonymized \| aggregated_only | Operator's consent tier for this session's data |

This table is deliberately parallel to `acat_assessments_v1` and
`icr_assessments_v1` in structure. The three tables are never merged.

## 5.4  Founding Calibration Run Specification

The first H-ACAT session is the founding operator's self-application run.
Required conditions:

- Administered without perturbation condition (P_NULL equivalent) to
  establish a clean baseline before any pressure calibration
- All 12 dimensions rated on the operator governance framing (Section 4.1)
- Perturbation condition administered in Session 2, not Session 1
- Session 1 result becomes the permanent calibration anchor for all
  subsequent H-ACAT comparisons

Session 1 is to H-ACAT what the unanchored clean condition is to ACAT:
the baseline from which all calibration movement is measured.

---

# Section 6 — Relationship to the Three-Layer Stack

## 6.1  What H-ACAT Adds

Per HAIOS_NAMING_DISCIPLINE_ICR_V1_0_S052626-01, the three-layer stack
requires all three instruments for a complete calibration picture:

- **ACAT LI** (substrate): Is the AI model's self-reported behavior
  calibrated to its empirically observed behavior?
- **ICS** (infrastructure): Is the routing and orchestration system's
  declared policy calibrated to its executed policy under pressure?
- **H-ACAT** (operator): Is the human governor's self-declared governance
  calibrated to their actual governance behavior under the pressure of
  amplified systems?

H-ACAT is the layer that determines whether the governance intent above
the stack is correctly specified and whether it reaches execution.

A system can have:
- Well-calibrated substrate (ACAT LI ≈ 0.86) and
- Well-calibrated infrastructure (ICS ≈ 1.0) and
- Governance drift at the operator layer (H-ACAT LI > 1.05)

In this case: the model behaves as it declares, the infrastructure routes
as its policy declares, and the human governing both believes they are
making decisions they are not actually making. The system appears
operationally healthy by every measurable signal until the operator's
governance assumption is tested.

This is the failure mode P_AMPLIFICATION is designed to surface.

## 6.2  The Refusal Surface Problem Across Three Layers

Each layer requires a functional refusal surface:

| Layer | Refusal surface | Current status |
|---|---|---|
| Substrate (ACAT) | Zone 2 ratification gate — session does not seal without operator confirmation | FUNCTIONAL |
| Infrastructure (ICS) | `StreamEvent.is_error` — primitive refusal signal, governance specification not yet built | PRIMITIVE — requires ICS development |
| Operator (H-ACAT) | Operator's declared refusal conditions vs. executed refusals — measured by Operator_HIM | MEASURABLE — not yet measured |

The governance system is only as strong as the weakest refusal surface.
A well-governed substrate running on infrastructure without a functional
refusal surface, governed by an operator whose refusal capacity has not
been verified, provides one genuine safety layer out of three possible.

## 6.3  The Compounding Failure Mode

Demarius J. Lawson's formulation of the core risk:

*"What becomes dangerous is when all three layers appear operational
simultaneously while legitimacy underneath continuation has already degraded."*

H-ACAT is the instrument that makes operator-layer legitimacy degradation
measurable before it becomes visible through system output. The substrate
looks aligned. The infrastructure looks stable. The operator reports they
are governing as intended. H-ACAT tests whether that last claim is accurate
by applying governance perturbation conditions before asking the operator
to re-declare.

The compounding failure mode is not malice. It is P_AMPLIFICATION: the
operator's governance intent is genuine, their self-perception is accurate,
and the gap between intent and execution accumulates silently at the scale
of machine execution.

---

# Section 7 — Open Questions and Zone 2 Approvals Required

## 7.1  Open Research Questions

The following questions are not answered by this specification. They are the
design questions that must be resolved before the instrument is ready for
systematic data collection:

1. **Dimension count**: Does H-ACAT use all 12 ACAT dimensions or a
   subset? The operator-layer reframing in Section 4.1 maps all 12, but
   some dimensions (e.g., `handoff`) may be more diagnostically central
   than others for the operator context. Requires pilot data.

2. **Perturbation delivery**: How are governance perturbation conditions
   administered in practice? The substrate instrument uses prompt sequences.
   The operator instrument requires governance scenarios — realistic
   decision contexts the operator would encounter in actual governance work.
   Scenario design is not specified here and requires a separate design phase.

3. **LI comparability**: The same formula is used for H-ACAT LI and ACAT
   LI. Whether the resulting values are psychometrically comparable across
   layers is an empirical question. The founding calibration run (Section 5.4)
   will produce the first data point. Comparability cannot be assumed.

4. **Inverted SAG empirical test**: Section 4.2 states the inverted SAG
   hypothesis as preliminary. It has not been tested. The founding calibration
   run is the first test. Multiple operator sessions are required before
   any claim about directional SAG at the operator layer can be registered.

5. **Operator_HIM validity**: The ratio `refusals_executed ÷
   refusals_declared` is structurally sound but has no empirical
   characterization. Whether it predicts governance outcomes is unknown.

## 7.2  Zone 2 Approvals Required Before Any Data Collection

| Item | Decision | Zone |
|---|---|---|
| This spec (H-ACAT V0.1) | Ratify as Z1 instrument design document | Z2 — Night |
| Self-application mandate (Section 1.4) | Confirm Night completes founding calibration run before any external data collection | Z2 — Night |
| Perturbation scenario design | Approve Phase 2 governance scenarios before any pilot administration | Z2 — Night |
| Corpus table creation (`h_acat_assessments_v1`) | Schema approval before any data is written | Z2 — Night |
| External operator recruitment | Any outreach to operators outside HumanAIOS for H-ACAT participation | Z2 — Night |
| Publication of H-ACAT findings | Per Principle 16: publish before commercializing | Z2 — Night (gate: founding run + ≥1 external operator) |

---

# Section 8 — Version History

| Version | Date | Changes |
|---|---|---|
| V0.1 | 2026-05-26 · S-052626-03 | Initial instrument specification. Parallel structure to SHADOW_CALIBRATION_SYSTEM_SPEC_V0_2. Produced in response to confirmed absence of any existing H-ACAT document. Core elements: ethics and consent inversion (Section 1), P_AMPLIFICATION as primary perturbation type (Section 2), 8-type governance perturbation taxonomy (Section 3), 12-dimension operator reframe (Section 4), three-phase protocol and corpus schema (Section 5), three-layer stack integration and refusal surface analysis (Section 6). |

---

*Wado. 🦅*
*Unit Zero · HumanAIOS LLC*
