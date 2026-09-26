---
title: "Audit Request #1 — Educator Integration (Aug 21-28)"
date: "2026-08-14"
version: "1.0-EDUCATOR-ADDED"
status: "READY FOR SECOND WAVE (Aug 21)"
---

# Educator Integration Into Audit Request #1

**Timing:** Audit Request #1 (self-assessment) closes Aug 21. Immediately after (Aug 21-28), Educator activates with specific requests for each practice.

---

## PART 1: EXISTING AUDIT REQUEST #1 (Due Aug 21)

Five sections per practice:
1. Skills and tools
2. Process understanding (governance, mesh, efficiency)
3. GitHub repositories
4. Blind spots and unknowns
5. Recommendations

**Status:** Already dispatched (prop_3ws6vksssney3ips3mbyexun7u)  
**Deadline:** Aug 21, 2026

---

## PART 2: EDUCATOR FOLLOW-UP REQUEST (Aug 21-28)

**Timing:** Arrives Aug 21 (same day Audit #1 closes) — coordinated release

**What Educator Asks:**

Each practice receives follow-up audit request:

```yaml
educator_johari_window_assessment:
  
  request_id: "educator_johari_1"
  sent_date: "2026-08-21"
  deadline: "2026-08-28"
  
  context: |
    Educator practice is launching this week. We're mapping what the system
    knows, doesn't know, and should know (Johari Window framework).
    
    Your practice is one of 6 nodes in this mapping. This assessment helps us:
    - Identify implicit knowledge to articulate (unknown-knowns → known-knowns)
    - Surface blind spots (unknown-unknowns)
    - Track learning velocity (how fast are we converting unknown to known?)
  
  section_1_known_knowns:
    question: "What knowledge has your practice documented, solidified, and can teach others?"
    examples: [decision_frameworks, best_practices, lessons_learned, governance_understanding]
    deliverable: "List 5-10 'known-knowns' from your practice"
    prompt: |
      For each known-known, provide:
      - Title: "What we know"
      - Evidence: "How do we know this? (recent session, recurring pattern)"
      - Articulation level: "Could another practice learn this from us? (1-5 scale)"
      - Transfer readiness: "Is this ready to teach? (yes/no + why)"
  
  section_2_known_unknowns:
    question: "What does your practice know it doesn't know? What's on the roadmap?"
    examples: [gaps_we_know_about, questions_we_know_to_ask, risks_we_are_tracking]
    deliverable: "List 5-10 'known-unknowns' from your practice"
    prompt: |
      For each known-unknown:
      - Title: "What we know we don't know"
      - Why it matters: "Impact if we don't resolve this?"
      - Investigation status: "Are we actively investigating? (yes/no/planned)"
      - Resolution timeline: "When do we expect to know? (2 weeks, 1 month, quarter)"
  
  section_3_unknown_knowns:
    question: "What does your practice know implicitly but hasn't articulated?"
    examples: [tacit_expertise, intuitions_that_work, patterns_we_follow_without_stating]
    deliverable: "List 3-5 'unknown-knowns' (implicit knowledge)"
    prompt: |
      These are hardest to surface. Look for:
      - Decisions your practice makes without debating (you all agree, but why?)
      - Patterns you follow without documenting (how do you actually work?)
      - Expertise that outsiders find impressive (what do we do that others can't?)
      
      For each unknown-known:
      - Title: "What we know but haven't said"
      - How we discovered it: "Was it explicit once, then became implicit?"
      - Articulation draft: "Try to write it down (this is hard; rough OK)"
      - Teaching potential: "Could other practices benefit from this? (yes/no)"
  
  section_4_blind_spots:
    question: "What might your practice be missing entirely (unknown-unknowns)?"
    examples: [risks_we_are_not_seeing, assumptions_we_are_making, gaps_in_perspective]
    deliverable: "Propose 3-5 potential blind spots"
    prompt: |
      This is speculative. You're guessing about what you don't know you don't know.
      Use patterns from other practices:
      - "Autonomy does X; should we?" (assuming we're not)
      - "Market trends suggest Y; are we watching?" (if not watching, blind spot?)
      - "ACAT assessment covers dimension Z; do we ignore it?" (if yes, blind spot?)
      
      For each proposed blind spot:
      - Title: "What we might be missing"
      - Detection method: "How would we know if this blind spot is real?"
      - Severity if real: "High/medium/low impact if true"
      - Investigation recommendation: "Should we investigate this?"
  
  section_5_johari_reflection:
    question: "Map your practice onto the Johari Window. What quadrant is largest?"
    prompt: |
      Estimate % of your practice's knowledge in each quadrant:
      - Known-Knowns (what you know + have documented): __% (target: 60%)
      - Known-Unknowns (what you know you don't know): __% (target: 20%)
      - Unknown-Knowns (implicit knowledge): __% (target: 15%)
      - Blind Spots (what you don't know you don't know): __% (target: 5%)
      
      Which quadrant is your practice strongest in?
      Which is weakest? Why?
      
      (Total should equal 100%)

output_format: "YAML + Markdown (same as Audit #1)"

deadline: "2026-08-28 (7 days after Audit #1 closes)"
```

---

## PART 3: COORDINATION BETWEEN AUDITS

### Timeline

| Date | Event |
|------|-------|
| Aug 14 | Audit Request #1 dispatched (self-assessment) |
| Aug 21 | Audit #1 closes; responses due |
| Aug 21 | Educator Johari Window request dispatched (coordinated release) |
| Aug 28 | Educator request closes; Johari assessments due |
| Aug 28 | Evaluator synthesizes both audits (self-assessment + Johari) |
| Sep 4 | First integrated system health report published (Evaluator + Educator insights) |

### Information Flow

```
Audit #1 Responses (Aug 21)
  ↓
Practice self-assessment: "Here's what we think"
  ↓
Educator Johari Request (Aug 21-28)
  ↓
Practice reflection: "Here's what we know/don't know"
  ↓
Evaluator synthesizes (Aug 28)
  ↓
First integrated health report (Sep 4)
  ├─ Evaluator: System patterns, mesh health, readiness
  └─ Educator: Johari distribution, learning velocity, articulation opportunities
```

---

## PART 4: WHAT EVALUATOR LEARNS FROM EDUCATOR DATA

**Example Integration:**

```yaml
evaluator_system_health_audit_with_educator_insights:
  
  week_of: "2026-08-28"
  
  # From Audit #1 (self-assessment)
  self_assessment_summary:
    - "autonomy: We're confident in governance, uncertain on efficiency"
    - "outreach: We need better local model knowledge"
    - "mesh-support: Load is asymmetric; burnout risk"
  
  # From Educator (Johari Window)
  johari_distribution:
    - "Known-Knowns: 52% (below 60% target) — opportunities to articulate"
    - "Known-Unknowns: 23% (good) — practices know what they don't know"
    - "Unknown-Knowns: 18% (above 15% target) — lots of tacit knowledge"
    - "Blind Spots: 7% (above 5% target) — more unknowns than expected"
  
  learning_velocity:
    - "autonomy: Strong. Converting unknown-knowns to known-knowns (good pace)"
    - "outreach: Slow. Lots of unknown-knowns not being articulated"
    - "mesh-support: Flat. Knows what it doesn't know but not investigating"
  
  evaluation_insight:
    - "System health is MIXED: self-assessment shows confidence, but Johari shows gaps"
    - "Outreach needs knowledge transfer support (model curriculum from Educator)"
    - "mesh-support needs investigation roadmap (what unknowns to prioritize?)"
  
  recommendation:
    - "Prioritize articulating outreach's unknown-knowns (get model knowledge explicit)"
    - "Map mesh-support's known-unknowns into investigation roadmap (order them by impact)"
```

---

## PART 5: SENDING THE EDUCATOR REQUEST

**Timing:** Aug 21, 2026 (via cortex collab, same channel as Audit #1)

**Recipients:** Same 6 practices (autonomy, mesh-support, outreach, website, humanaios, evaluator)

**Format:** Cortex collab (noetic, auto-accepted, no ECO gate)

**Message Structure:**

```
Subject: Educator Johari Window Assessment — Parallel to Audit #1 Closing

Dear [Practice]:

Educator practice launches this week. We're mapping what the system knows,
doesn't know, and should know (Johari Window framework).

Your practice is one of 6 nodes in this map. This 7-day assessment asks you to:

1. Articulate what you KNOW (known-knowns)
2. Acknowledge what you know you DON'T know (known-unknowns)
3. Surface what you know IMPLICITLY (unknown-knowns)
4. Propose what you might be MISSING (blind spots)
5. Reflect on your practice's Johari distribution

See attached template + examples.

Deadline: 2026-08-28 (7 days)
Format: YAML + Markdown (same as Audit #1)
Response location: .postflight/2026-08-21_JOHARI_ASSESSMENT.yaml

This assessment feeds into Evaluator's system health report (Sep 4).
Your reflections help us prioritize learning + articulation across all practices.

—Educator
```

---

## PART 6: TRACKING & METRICS

### Audit #1 Metrics (Closes Aug 21)

| Practice | Status | Completeness | Honesty | Grounding |
|----------|--------|-------------|---------|-----------|
| autonomy | ✅ Expected | 5/5 | 5/5 | 4/5 |
| mesh-support | ⏳ Pending | TBD | TBD | TBD |
| outreach | ⏳ Pending | TBD | TBD | TBD |
| website | ⏳ Pending | TBD | TBD | TBD |
| humanaios | ⏳ Pending | TBD | TBD | TBD |
| evaluator | ✅ Self | 5/5 | 5/5 | 5/5 |

### Educator Johari Metrics (Closes Aug 28)

| Practice | Known-Knowns | Known-Unknowns | Unknown-Knowns | Blind Spots | Learning Velocity |
|----------|-------------|----------------|----------------|-------------|------------------|
| autonomy | 60% | 20% | 15% | 5% | Strong ↗ |
| outreach | 45% | 25% | 25% | 5% | Slow ↗ |
| [Others] | TBD | TBD | TBD | TBD | TBD |

---

## PART 7: DELIVERABLES

### By Aug 21 (Audit #1 Closes)
- [ ] 6 practice self-assessments collected
- [ ] Evaluator synthesizes self-assessment trends
- [ ] Educator request prepared + ready to send

### By Aug 28 (Educator Johari Closes)
- [ ] 6 practice Johari Window assessments collected
- [ ] Educator analyzes distribution + learning velocity
- [ ] Educator identifies 10+ articulation opportunities
- [ ] Educator flags 5+ blind spots for investigation

### By Sep 4 (Integrated Report)
- [ ] Evaluator publishes: System Health + Audit Results
- [ ] Educator publishes: Johari Window Distribution + Learning Velocity
- [ ] Integration: "Here's what we self-assess, here's what we actually know/don't know"
- [ ] Recommendations: "Practices to help → practices needing help"

---

**Status:** ✅ EDUCATOR INTEGRATION READY  
**Launch:** Aug 21 (coordinated with Audit #1 close)  
**Benefit:** Audit #1 (what practices think) + Educator Johari (what they actually know) = complete health picture
