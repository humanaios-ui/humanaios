# H-ACAT Carousel System: Rotating Human Raters (Post-Dry-Run Concept)

**Status:** Design Concept (To be developed after Phase 3 dry run + Demarius validation)  
**Purpose:** Scale behavioral assessment to multiple subjects without recruiting bottleneck  
**Timeframe:** Post-2026-08-07 (after hybrid model validation)

---

## Problem Statement

**Current bottleneck:** Behavioral assessment requires trained human raters.
- Carly dry run: recruiting 1 human rater
- Demarius validation: recruiting 1 human rater
- Future subjects: each requires recruiting 1–3 new humans

**Scaling challenge:** Can't recruit 10+ human raters for 10 subjects. Need sustainable model.

**Solution concept:** Carousel — rotating pool of trained raters who assess multiple subjects sequentially, building expertise over time.

---

## Carousel Architecture

### Concept: Rotating Assessor Pool

```
Subject 1 (Carly)     Subject 2 (Demarius)   Subject 3 (Future)     Subject 4 (Future)
├─ Human Rater A      ├─ Human Rater B       ├─ Human Rater C       ├─ Human Rater A
├─ Machine 1 (Claude) ├─ Machine 1 (Claude)  ├─ Machine 1 (Claude)  ├─ Machine 1 (Claude)
└─ Machine 2 (GPT-4o) └─ Machine 2 (GPT-4o)  └─ Machine 2 (GPT-4o)  └─ Machine 2 (GPT-4o)

Machines: Always Claude + GPT-4o (consistent across subjects)
Humans: Rotate through trained assessors (A → B → C → A → ...)
```

**Advantages:**
- **No recruitment overhead:** Train 3–5 humans once, reuse across subjects
- **Calibration trajectory:** Humans improve with experience (learn from previous assessments)
- **Coverage:** Always have rater available (no scheduling bottleneck)
- **Diversity:** Different humans assess different subjects (robustness)
- **Cost:** Lower per-subject human cost (amortized across assessments)

---

## Core Components

### 1. Rater Pool Management

**Initial cohort:** 3–5 trained human assessors
- Phase 3 raters (Carly: Demarius, Future: TBD)
- Standing availability calendar
- Expertise profile (governance background, assessment experience)

**Rater onboarding:**
- FOR training (Frame-of-Reference calibration, 1.5 hrs)
- Practice scoring on sample (with feedback)
- ICC > 0.6 gate before live assessment
- Post-assessment debrief (lessons learned)

**Rater rotation rule:**
- "Next available rater" algorithm
- Optional: weighted by expertise/availability
- Load-balancing: each rater gets similar assessment count over time

### 2. Assessment Request Pipeline

```
Subject X scheduling
  ↓
Check rater pool availability (next 5 business days)
  ↓
Auto-assign "next available human rater"
  ↓
Send rater packet (protocol, transcript template, scoring guide)
  ↓
FOR training (live or async recorded)
  ↓
Independent scoring (3–4 hrs)
  ↓
Machine scoring in parallel (Claude + GPT-4o, isolated)
  ↓
ICC calibration check (ICC > 0.6 gate)
  ↓
Analysis + feedback to both raters
```

### 3. Calibration Across Raters

**Problem:** Different humans may interpret anchors differently → ICC drift over time

**Solution: Carousel Calibration Events**

Quarterly or after every 5th assessment:
- **Calibration sync:** All carousel raters score a sample transcript together
- **Compare interpretations:** Where did raters diverge? Why?
- **Anchor refinement:** Clarify ambiguous levels based on patterns
- **Re-establish ICC baseline:** Confirm ICC > 0.6 still holds

**Expected outcome:** Raters converge on interpretation over time (learning effect)

### 4. Data & Feedback Loop

**Per-assessment data points:**
- Rater identity + assessment date
- Subject (Carly, Demarius, etc.)
- Per-dimension scores (human + 2 machines)
- ICC per assessment
- Machine vs machine agreement
- Human vs machine divergence patterns
- Rater notes/reflections

**Feedback analysis:**
- Trend: Does ICC improve as humans gain experience?
- Convergence: Do humans interpret anchors more consistently?
- Machine stability: Does Claude/GPT-4o agreement stay stable?
- Divergence patterns: Systematic human-unique vs machine-unique biases?

**Rater feedback:**
- After each assessment: "How clear were anchors? What was confusing?"
- Quarterly: "What patterns are you seeing? Recommendations for anchors?"
- Annual: "Professional development in behavioral assessment"

---

## Implementation Roadmap (Post-Dry-Run)

### Phase 1: Pilot Carousel (Months 1–2 after dry run)
- **Subjects:** Carly (complete) + Demarius (complete) = baseline
- **Raters:** Demarius + Carly rotate assessing each other (proven raters)
- **Goal:** Test rotation logistics, calibration sync process
- **Deliverable:** Carousel manual (procedures, scheduling, feedback loops)

### Phase 2: Expand Pool (Months 2–4)
- **Recruit:** 2–3 additional trained raters (FOR training, practice scoring)
- **Subjects:** 2–3 new subjects (mix of practices)
- **Raters:** Full rotation (A → B → C → A pattern)
- **Goal:** Validate efficiency, ICC stability across new raters
- **Deliverable:** Calibration data (rater learning curves, ICC trends)

### Phase 3: Formalize System (Months 4–6)
- **Carousel infrastructure:** Scheduling system, rater database, feedback tracker
- **Documentation:** Carousel manual, FOR training materials, anchor refinement guide
- **Sustainability:** Budget model (hours per rater), timeline per subject
- **Goal:** Production-ready carousel system
- **Deliverable:** Full H-ACAT assessment service (subjects book assessments, raters rotate, results automated)

---

## Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Rater availability** | ≥3 raters always available | Scheduling data |
| **ICC stability** | ICC > 0.6 sustained | Calibration data per assessment |
| **Rater learning** | ICC improves by 0.05–0.10 after 3–5 assessments | Trend analysis |
| **Machine stability** | Claude-GPT ICC stays ~0.75+ | Machine-machine agreement |
| **Turnaround time** | Subject assessed within 5 business days | Assessment data |
| **Cost per subject** | <$X (rater hours amortized) | Budget tracking |
| **Rater retention** | ≥80% raters available next year | Turnover data |

---

## Risks & Mitigation

| Risk | Mitigation |
|---|---|
| **Rater drift** | Quarterly calibration syncs; re-training if ICC drops |
| **Burnout** | Load-balance rater assignments; annual sabbatical option |
| **Anchor ambiguity** | For each assessment, track "confusing dimensions"; quarterly refinement |
| **Machine consistency** | Monitor Claude-GPT ICC; alert if divergence >0.10 |
| **Scheduling conflicts** | 3-rater minimum; fallback to async scoring if needed |

---

## Carousel vs Alternatives

| Approach | Pros | Cons | Best for |
|---|---|---|---|
| **Carousel (rotating pool)** | Sustainable, no recruiting, raters improve | Calibration overhead, scheduling | 10+ subjects over time |
| **Hybrid (1 human + 2 machine)** | Low human load, fast, validates protocol | Lower human coverage, less diversity | Pilot phase (current) |
| **All-human (3–4 per subject)** | Robust, established method | Recruiting bottleneck, cost | 1–2 subjects only |
| **All-machine (only Claude + GPT-4o)** | Fastest, no recruiting | ICC ~0.60 (lower), different failure modes | Screening-only use |

**Recommended:** Carousel (long-term), with hybrid mode during startup (current)

---

## Deliverables for Carousel Development

After Phase 3 dry run + Demarius validation (2026-08-07):

1. **Carousel Manual**
   - Scheduling procedures
   - Rater onboarding checklist
   - FOR training guide (live + async)
   - Feedback collection process
   - Calibration sync protocol

2. **Rater Tracking System**
   - Rater database (availability, expertise, history)
   - Assessment scheduler (auto-assign next available)
   - ICC tracking per rater over time
   - Feedback dashboard

3. **Calibration Protocol**
   - Quarterly sync structure
   - Anchor refinement process
   - ICC re-baseline procedure
   - Rater development plan template

4. **Cost Model**
   - Budget per rater per assessment (hours)
   - ROI vs recruiting new raters
   - Sustainability timeline
   - Scale curve (cost per subject as volume grows)

5. **Pilot Plan** (Months 1–2)
   - Carly + Demarius rotate assessing (test logistics)
   - Recruit 2–3 additional raters (expand pool)
   - Run 2–3 new subject assessments (validation)
   - Generate calibration data (learning curves)

---

## Conclusion

Carousel model solves the sustainability problem for multi-subject behavioral assessment:
- **Recruiting solved:** Train once, reuse across many subjects
- **Calibration addressed:** Quarterly syncs keep ICC stable
- **Cost managed:** Amortized human hours per subject
- **Expertise built:** Raters improve with experience

**Ready to develop after Phase 3 dry run validation (post-2026-08-07).**

---

**Concept Status:** Design phase. Implementation roadmap ready post-dry-run. Awaiting validation of hybrid model (Carly + Demarius) before commitment.
