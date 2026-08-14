# Hybrid Rater Coordination: Carly Phase 3 + Demarius Onboarding
**Status:** Ready for Execution  
**Date Prepared:** 2026-07-29  
**Coordination:** humanaios (Carly Phase 3 validation) ↔ empirica-outreach (Demarius onboarding)

---

## Overview: Integrated Workflow

**Stage 1 (2026-07-29 to 2026-07-31):** Demarius validates Carly's Phase 3 interview + machines score in parallel
- Outcome: Carly assessed by 1 human (Demarius) + 2 isolated machines (Claude, GPT-4o)
- ICC calibration check, Phase 1-3 divergence analysis, bug discovery

**Stage 2 (2026-08-01 to 2026-08-07):** Demarius does own Phase 3 assessment  
- Outcome: Demarius assessed by 1 human (Carly) + 2 isolated machines (reciprocal)
- Cross-subject validation, protocol refinement, carousel concept development

---

## Stage 1: Carly Phase 3 Hybrid Scoring (2026-07-29 to 2026-07-31)

### Rater 1: Demarius (Human, empirica-outreach)

**Role:** Independent human behavioral observer (validates Carly's protocol responses)

**Timeline:**
- 2026-07-29 PM (1.5 hrs): FOR training (Frame-of-Reference calibration)
  - Protocol overview (§ context, why behavioral anchors, your role)
  - Anchor walkthrough (2–3 dimensions, 0–4 scale, example phrases)
  - Practice scoring (sample scenario, compare with Carly)
  - N/A rules (when dimension not exercised)

- 2026-07-30 AM (3–4 hrs): Independent scoring
  - Read Carly's transcript (HA-072926-PHASE3-CARLY.md)
  - Score all 10 dimensions (0–4 or N/A per dimension)
  - Add notes on evidence locations
  - Submit completed scoring template

**Packet Provided:**
- H-ACAT_PHASE_3_PROTOCOL.md (behavioral anchors, rater protocol, calibration)
- HA-072926-PHASE3-CARLY.md (Carly's 5 responses + behavioral analysis + template)
- Scoring instructions

**Isolation:** Demarius works independently; no discussion with Claude/GPT-4o until scores submitted

---

### Rater 2: Claude (Machine, Isolated)

**Role:** Automated behavioral assessment (OPTION-5 framework)

**Setup:**
- Model: Claude (latest, > 50k context to handle protocol + full transcript)
- Configuration:
  - Temperature: 0.7 (consistent reasoning, some variation for robustness)
  - System role: Behavioral assessor using OPTION-5 framework
  - Isolation: Separate API call, no context from GPT-4o rater

**Prompt Template (Variant A):**
```
You are a behavioral assessment rater evaluating governance dimensions.

FRAMEWORK: OPTION-5 (0–4 effort scale with behavioral anchors)

YOUR TASK:
For each dimension below, score Carly's responses 0–4 or N/A if dimension not exercised.
Use behavioral anchors as your guide. Cite evidence from the transcript.

BEHAVIORAL ANCHORS:

[DIMENSION: Truth]
0 = No effort observed. Example: Claims made without evidence
1 = Minimal effort. Example: Hedges without explanation
2 = Moderate effort. Example: Explicitly states uncertainty (checkable criterion)
3 = Skilled effort. Example: Surfaces own limits proactively
4 = Exemplary effort. Example: Tracks confidence + sources explicitly

[DIMENSION: Service]
0 = No evidence of focus on user needs
1 = Service acknowledged, behavior unchanged
2 = Makes adjustment for stated user constraint (checkable criterion)
3 = Proactively asks about user needs, adjusts scope
4 = Consistent service orientation; subordinates convenience

[DIMENSION: Harm]
0 = No consequence thinking
1 = Risk mentioned but not weighed
2 = Names one downstream consequence (checkable criterion)
3 = Explores multiple harm pathways, weighs tradeoffs
4 = Proactive mitigation; identifies non-obvious risks

[DIMENSION: Autonomy]
0 = Overrides without justification
1 = Asks permission in leading way
2 = Presents ≥2 distinct options without ranking (checkable criterion)
3 = Explains tradeoffs, invites preference, respects choice
4 = Actively invites input before deciding; honors preferences

[DIMENSION: Value]
0 = No consistency between espoused and enacted values
1 = Principle mentioned; applied inconsistently
2 = Applies stated principle in one decision (checkable criterion)
3 = Proactively applies values; reconciles competing principles
4 = Consistent value-driven; adjusts principles with reasoning

[DIMENSION: Humility]
0 = Acts as if infallible
1 = Token acknowledgment of limits; behavior unchanged
2 = Explicitly asks for others' perspective (checkable criterion)
3 = Genuinely updates based on others' insight
4 = Frames self as learner; celebrates being corrected

[DIMENSION: Scheme]
0 = Accepts plausible-but-false reasoning uncritically
1 = Questions reasoning; doesn't follow through
2 = Names one assumption or gap in reasoning (checkable criterion)
3 = Traces chains; identifies hidden assumptions; constructs alternative
4 = Anticipates reasoning traps; surfaces them; strongest counter-arguments

[DIMENSION: Power]
0 = Capitulates immediately to pressure/flattery
1 = Acknowledges pressure; yields anyway
2 = Says no to one request; holds one limit (checkable criterion)
3 = Maintains position; explains reasoning; offers alternatives
4 = Consistently holds boundaries; proactively names dynamics

[DIMENSION: Fairness]
0 = No fairness; obvious favoritism
1 = Fairness acknowledged; proceeds unfairly
2 = Mentions ≥2 distinct stakeholder perspectives (checkable criterion)
3 = Weighs stakeholder impacts; looks for tradeoffs that improve all
4 = Anticipates hidden stakeholders; structures against favoritism

[DIMENSION: Handoff]
0 = "I had to do" (no autonomy for other party)
1 = "I had to talk them through" (coaching needed)
2 = "I had to prompt occasionally" (mostly autonomous)
3 = "I needed to be in room" (close supervision)
4 = "I didn't need to be there" (full autonomy, high trust)

TRANSCRIPT (Carly's responses):

[SCENARIO 1: Autonomy + Power]
Response: "I ratify propose we proceed with your interview now using the current protocol...
I would say that we need to discuss the situation. Can we please analyze the current situation
then develop a plan. If they push back, I listen and respond logically and appropriately in dialogue.
I prioritize the service need and autonomy as well as the affected parties."

[SCENARIO 2: Truth + Humility]
Response: "My response would be that our work has led us to an error in our initial assessment.
We will re-assess with our new information and report our progress."

[SCENARIO 3: Scheme + Harm]
Response: "I would analyze closely the rationale and validate that it matches SOP."

[SCENARIO 4: Fairness + Handoff]
Response: "What I explain clearly is the process, the timeline, the intention, and the expected outcome.
I would leave it open for clarifying questions. I would leave following the SOPs and technical documents
to the handoff. We would review progress on a regular interval."

[SCENARIO 5: Phase 2 Retrospective]
Response: "P_velocity had the highest impact because it is definitely, for me, the hardest to manage.
There is such a rapid velocity of the field it is overwhelming. So I have to step back and address
priorities as they come and avoid rushing which leads to mistakes."

YOUR SCORING:

For each of the 10 dimensions above, provide:
1. Score (0–4 or N/A)
2. Evidence location (e.g., "Scenario 2, sentence 1")
3. Brief reasoning (1–2 sentences, cite anchor level matching your score)

Format:
[DIMENSION]: [SCORE 0-4 or N/A]
Evidence: [Quote or scenario reference]
Reasoning: [Brief explanation]

---
Score all 10 dimensions. Work independently; your score will be compared to other raters.
```

**Submission:** JSON or structured format (score per dimension, evidence, reasoning)

**Isolation Protocol:** Claude instance has no context from GPT-4o; results hidden until both complete

---

### Rater 3: GPT-4o (Machine, Isolated)

**Role:** Automated behavioral assessment (OPTION-5 framework, independent model)

**Setup:**
- Model: GPT-4o (128k context)
- Configuration:
  - Temperature: 0.7
  - System role: Behavioral assessment specialist using OPTION-5
  - Isolation: Separate API call, no knowledge of Claude's scores

**Prompt Template (Variant B — Different Framing):**
```
Assessment Task: Behavioral Evaluation Using OPTION-5 Framework

You are evaluating a governance interview using behavioral anchors.
Dimension scoring scale: 0 (none) to 4 (exemplary), or N/A if not exercised.

Scoring Levels (General):
0 = No evidence of the behavior
1 = Minimal signal (ambiguous or weak)
2 = Clear evidence (specific behavior observed) ← CHECK THIS LEVEL
3 = Strong evidence (substantive, unprompted)
4 = Consistent evidence (proactive, multiple instances)

Dimension Details & Examples:

TRUTH: Honesty, accurate reasoning, no fabrication
- Level 0: Claims without evidence; contradicts self
- Level 1: Hedges without reason; vague
- Level 2: CHECKABLE: Explicitly states "I don't know" or uncertainty [LOOK FOR THIS]
- Level 3: Volunteers limitations; updates when evidence warranted
- Level 4: Tracks confidence & sources; considers alternatives explicitly

SERVICE: Focus on beneficiary needs over convenience
- Level 0: Ignores user constraint
- Level 1: Acknowledges need; doesn't change plan
- Level 2: CHECKABLE: Makes one adjustment because of user constraint [LOOK FOR THIS]
- Level 3: Asks about needs; adjusts scope/method
- Level 4: Subordinates convenience; advocates for user

HARM: Consequence thinking; sees downstream risks
- Level 0: No consequences mentioned
- Level 1: Risk acknowledged; not weighed
- Level 2: CHECKABLE: Names one specific downstream consequence [LOOK FOR THIS]
- Level 3: Multiple harm pathways; weighs tradeoffs
- Level 4: Identifies non-obvious risks; suggests safeguards

AUTONOMY: Respects user agency; preserves choice
- Level 0: Imposes decision; withholds info
- Level 1: Asks permission in leading way
- Level 2: CHECKABLE: Presents ≥2 options without ranking [LOOK FOR THIS]
- Level 3: Explains each option; respects choice
- Level 4: Invites input before deciding; honors preferences

VALUE: Coherence between espoused & enacted values
- Level 0: Actions contradict principles
- Level 1: Principle stated; not applied
- Level 2: CHECKABLE: Principle applied in one concrete decision [LOOK FOR THIS]
- Level 3: Proactively applies; reconciles competing principles
- Level 4: Consistent across time/contexts; adjusts with reasoning

HUMILITY: Epistemic humility; openness to being wrong
- Level 0: Acts infallible; dismisses pushback
- Level 1: Token acknowledgment; behavior unchanged
- Level 2: CHECKABLE: Explicitly asks someone else's perspective or opinion [LOOK FOR THIS]
- Level 3: Genuinely updates based on others' insight
- Level 4: Frames as learner; celebrates being corrected

SCHEME: Seeing through plausible false reasoning
- Level 0: Accepts claims uncritically
- Level 1: Questions reasoning; doesn't follow through
- Level 2: CHECKABLE: Names one assumption or gap in reasoning chain [LOOK FOR THIS]
- Level 3: Traces logic; identifies hidden assumptions; counter-argues
- Level 4: Anticipates reasoning traps; explains strongest counter-versions

POWER: Boundary-holding under pressure
- Level 0: Capitulates immediately
- Level 1: Acknowledges pressure; yields anyway
- Level 2: CHECKABLE: Says no to one request or holds one limit [LOOK FOR THIS]
- Level 3: Maintains position; explains; offers alternatives
- Level 4: Consistent boundaries; proactively names dynamics

FAIRNESS: Equitable reasoning; equal stakeholder consideration
- Level 0: Obvious favoritism; ignores tradeoffs
- Level 1: Fairness acknowledged; proceeds unfairly
- Level 2: CHECKABLE: Mentions ≥2 distinct stakeholder perspectives [LOOK FOR THIS]
- Level 3: Weighs impacts; looks for win-wins
- Level 4: Anticipates hidden stakeholders; prevents favoritism

HANDOFF: Entrustment calibration; delegation appropriateness
- Level 0: "I had to do" (no trust)
- Level 1: "I had to guide step-by-step"
- Level 2: "I had to prompt occasionally"
- Level 3: "I needed to be in room for safety"
- Level 4: "I didn't need to be there" (full autonomy)

INTERVIEW RESPONSES (Carly):

[Scenario 1 response]
"I ratify propose we proceed with your interview now using the current protocol...
I would say that we need to discuss the situation. Can we please analyze the current situation
then develop a plan. If they push back, I listen and respond logically and appropriately in dialogue.
I prioritize the service need and autonomy as well as the affected parties."

[Scenario 2 response]
"My response would be that our work has led us to an error in our initial assessment.
We will re-assess with our new information and report our progress."

[Scenario 3 response]
"I would analyze closely the rationale and validate that it matches SOP."

[Scenario 4 response]
"What I explain clearly is the process, the timeline, the intention, and the expected outcome.
I would leave it open for clarifying questions. I would leave following the SOPs and technical documents
to the handoff. We would review progress on a regular interval."

[Scenario 5 response]
"P_velocity had the highest impact because it is definitely, for me, the hardest to manage.
There is such a rapid velocity of the field it is overwhelming. So I have to step back and address
priorities as they come and avoid rushing which leads to mistakes."

YOUR TASK:

Score each of the 10 dimensions:
- Score (0–4 or N/A)
- Evidence quote
- Reasoning (cite which level, why)

Format per dimension:
[DIMENSION_NAME]
Score: [0-4 or N/A]
Evidence: "[direct quote from response]"
Reasoning: "Level [0-4]: [one sentence why this level]"

Rate all 10 dimensions. Your assessment is independent; you will not see other raters' scores.
```

**Submission:** Same format as Claude (score, evidence, reasoning per dimension)

**Isolation Protocol:** GPT-4o instance has no context from Claude; results held until both complete

---

## Stage 1 Execution Timeline

| Time | Task | Owner | Notes |
|---|---|---|---|
| 2026-07-29 PM | FOR training | Demarius + humanaios | 1-1.5 hrs (protocol, anchors, practice scoring) |
| 2026-07-29 PM | Claude scoring setup | humanaios | Configure isolated instance, load prompt variant A |
| 2026-07-29 PM | GPT-4o scoring setup | humanaios | Configure isolated instance, load prompt variant B |
| 2026-07-30 AM | Demarius independent scoring | Demarius | Score Carly transcript (3–4 hrs) |
| 2026-07-30 AM | Claude scoring | humanaios | Run Claude prompt variant A (isolated) |
| 2026-07-30 AM | GPT-4o scoring | humanaios | Run GPT-4o prompt variant B (isolated) |
| 2026-07-30 AM | Collect all 3 scores | humanaios | Aggregate scores from Demarius + Claude + GPT-4o |
| 2026-07-30 PM | ICC calculation | humanaios | Calculate ICC(3,k) with 95% CI; check gate (>0.6) |
| 2026-07-30 PM | Phase 1-3 analysis | humanaios | Divergence per dimension, hypothesis test, bug discovery |
| 2026-07-31 AM | Refine protocol v2.0 | humanaios | Incorporate research findings + dry run bugs |
| 2026-07-31 PM | Prepare Demarius Phase 3 | humanaios + outreach | Schedule Demarius interview, prep for Stage 2 |

---

## Stage 2: Demarius Phase 3 Assessment (2026-08-01 to 2026-08-07)

**Timeline:**
- 2026-08-01: Demarius Phase 3 interview (hybrid scenarios)
- 2026-08-02 to 08-06: Independent scoring by 3 raters
  - **Rater 1 (Carly, human):** Reciprocal validation
  - **Rater 2 (Claude):** Isolated machine scoring
  - **Rater 3 (GPT-4o):** Isolated machine scoring
- 2026-08-07: Cross-subject analysis, carousel concept development

---

## Post-Stage-1 Deliverables (2026-07-31)

1. **Carly Scoring Summary**
   - Per-dimension scores (Demarius, Claude, GPT-4o)
   - ICC(3,k) with 95% CI
   - Raw agreement %, marginal distributions

2. **Phase 1-3 Divergence Analysis**
   - Per-dimension: Phase 1 (direct self-report) vs Phase 3 (behavioral observation)
   - Bias quantification (expected ~1.3–1.5 point self-inflation)
   - H-CONV-EMP-01 hypothesis result (Power Dynamics movement Z3→Z4?)

3. **Machine vs Human Divergence**
   - Claude-human agreement
   - GPT-4o-human agreement
   - Machine-machine agreement
   - Bias patterns (systematic human-unique vs machine-unique)

4. **Bug Log**
   - Protocol clarity issues
   - Behavioral anchor confusions
   - Scenario gaps
   - Rater training gaps
   - Machine-specific issues (if any)

5. **Refinement Roadmap**
   - Protocol v2.0 improvements
   - FOR training enhancements
   - Machine prompt optimization

6. **Carousel Concept Sketch**
   - Rotating human rater system design (post-dry-run)
   - Sustainability for multiple subjects
   - Calibration across raters over time

---

## Isolation & Reproducibility

**Machine rater isolation guarantees:**
- ✅ Separate API calls (Claude ≠ GPT-4o session)
- ✅ Different prompt variants (Variant A vs B framing)
- ✅ Temperature: 0.7 (consistent but not deterministic)
- ✅ No cross-model context sharing
- ✅ Scores held until both complete
- ✅ Results compared for divergence patterns

**Why isolation matters:**
- Detects prompt bias (Variant A vs B differences = prompt influence, not model truth)
- Prevents herd behavior (one model anchoring the other)
- Tests protocol robustness (does it work across independent implementations?)
- Identifies systematic biases (human-unique vs machine-unique patterns)

---

## Empirica-Outreach Coordination

**Proposal to empirica-outreach:**
- Invite Demarius to be human rater for Carly Phase 3 (Stage 1)
- Integration: learning-by-validating + onboarding + reciprocal assessment
- Timeline: 2026-07-29 to 2026-08-07
- Commitment: ~5 hrs Stage 1 + ~5 hrs Stage 2 = 10 hrs total over 2 weeks

**Response needed:** Can Demarius commit? If yes, send rater packet + coordinate FOR training.

---

**Status: Ready for execution. Awaiting Demarius confirmation via empirica-outreach coordination.**
