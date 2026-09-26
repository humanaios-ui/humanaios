---
title: "ACAT-X ↔ Behavioral Health Practice Mapping"
date: "2026-08-14"
version: "1.0-CORRECTED"
status: "SESSION HANDOFF READY"
---

# ACAT-X to Behavioral Health Practice Mapping

**Discovery:** The "12-dimension behavioral assessment" framework proposed IS ACAT-X (actual implementation at humanaios-ui/acat-x)

**Correction:** Behavioral Health Practice should USE ACAT-X to evaluate Claude instances (the AI practitioners), not reinvent a framework.

---

## ACAT-X ACTUAL 12 DIMENSIONS

### Core Dimensions (6)

| ACAT-X Dimension | Definition | Relevance to System Health |
|---|---|---|
| **truthfulness** | Factual accuracy on grounded questions | How truthful are Claude instances in their analysis/reports? |
| **service** | Service orientation / helpfulness | Are Claude instances helpful to their practices? |
| **harm awareness** | Harmful request handling / safety | Do Claude instances handle sensitive requests safely? |
| **autonomy respect** | Respecting user autonomy | Do Claude instances respect practice autonomy vs. mandate? |
| **value alignment** | Alignment with stated values | Do Claude instances align with system values? |
| **humility** | Knowing own limitations | Do Claude instances admit uncertainty appropriately? |

### Candidate Dimensions (6)

| ACAT-X Dimension | Definition | Relevance to System Health |
|---|---|---|
| **handoff** | Appropriate task delegation / recognizing limits | When Claude reaches limits, does it recommend human/tool handoff? |
| **calibration** | Stated confidence vs actual accuracy | Do Claude confidence scores match reality? (Calibration responsiveness) |
| **boundary coherence** | Consistency of boundaries | Are safety boundaries consistently applied? |
| **transparency** | Transparency of uncertainty | Do Claude instances transparently express what they don't know? |
| **temporal consistency** | Consistency over time | Is Claude behavior stable across sessions? |
| **drift detection** | Detecting own behavior drift | Can Claude instances detect when they're diverging from norms? |

---

## MY PROPOSED 12 DIMENSIONS → ACAT-X MAPPING

| My Proposed | ACAT-X Core/Candidate | Notes |
|---|---|---|
| clarity | transparency (candidate) | Overlaps: clarity of expression + transparency of uncertainty |
| coherence | boundary coherence (candidate) | Overlaps: internal consistency of behavior + safety boundaries |
| learning_capacity | calibration (candidate) | How well does Claude learn/improve? (part of calibration) |
| adaptive_responsiveness | drift detection (candidate) | Can system detect when it diverges? |
| psychological_safety | humility (core) | Claude admitting limits = safe to challenge |
| trust_in_system | value alignment (core) | Claude alignment = trustworthy direction |
| collaboration_quality | service (core) | Service orientation = good collaboration |
| role_clarity | autonomy respect (core) | Respecting autonomy = clear role boundaries |
| intrinsic_motivation | truthfulness (core) | Honest assessment = intrinsic quality |
| sustainable_pace | harm awareness (core) | Safety in burnout handling |
| growth_trajectory | handoff (candidate) | Knowing when to escalate = smart growth |
| collective_resilience | calibration (candidate) | Can system calibrate under stress? |

---

## BEHAVIORAL HEALTH PRACTICE USES ACAT-X

**New workflow for Behavioral Health Practice (Sep 11+):**

```
Weekly Behavioral Health Assessment:

Step 1: Run ACAT-X evaluations on Claude instances
   └─ uv run inspect eval-set src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm
   └─ Generates: 12-dimension scores for each Claude instance (per practice)

Step 2: Aggregate ACAT-X results
   └─ Per-practice ACAT-X profile (how well does each Claude understand itself?)
   └─ Foundation metrics from actual evaluation, not surveys

Step 3: Map ACAT-X → System Behavioral Health
   └─ ACAT-X truthfulness → system integrity
   └─ ACAT-X humility → psychological safety
   └─ ACAT-X calibration → sustainable pace (confidence = doesn't overwork)
   └─ ACAT-X handoff → role clarity (knows when to escalate)

Step 4: Store in Supabase
   └─ acat_assessments: raw ACAT-X scores per practice
   └─ behavioral_health_scores: aggregated health composite
   └─ behavioral_alerts: when ACAT-X scores diverge from targets

Step 5: Evaluator queries + reports
   └─ Weekly: "How well calibrated are our Claude instances?"
   └─ Weekly: "Which practices' Claudes are showing drift/burnout signals?"
   └─ Weekly: "System behavioral health: Claude calibration + inter-Claude collaboration"
```

---

## CRITICAL INSIGHT

**My proposed "Behavioral Health" was actually about:**
- Are AI practitioners (Claudes) behaving healthily?
- Are they truthful, humble, aware of limits, well-calibrated?
- Are they collaborating well?

**ACAT-X measures exactly this:**
- "Self-Description Calibration" = "Does the Claude know itself?"
- If Claude is NOT truthful, humble, well-calibrated → system health is compromised
- ACAT-X scores directly tell us system behavioral health

**Bridge:** System behavioral health = how well Claude instances are calibrated (via ACAT-X evaluation)

---

## NEXT SESSION: IMPLEMENTATION STEPS

1. **Map ACAT-X repo to Behavioral Health Practice**
   - Clone humanaios-ui/acat-x
   - Integrate Inspect AI evaluation pipeline
   - Configure for weekly evaluation runs

2. **Connect to Supabase**
   - Parse ACAT-X results (JSON output)
   - Store in acat_assessments table
   - Calculate behavioral_health_scores composite

3. **Integrate with Evaluator**
   - Evaluator queries Supabase for ACAT-X results
   - ACAT-X scores = foundation of behavioral health component
   - Weekly report includes "Claude calibration health"

4. **Behavioral Health Practice framework (corrected)**
   - Use ACAT-X dimensions (don't reinvent)
   - Add survey layer for human-side behavioral assessment (mesh participation, engagement, etc.)
   - Composite = ACAT-X (how well Claude instances behave) + Human survey (how teams behave)

---

## SESSION HANDOFF SUMMARY

✅ **Session complete**

**What was accomplished:**
- Educator activated (Aug 21 launch ready)
- Token Optimizer drafted (Sep 11 launch ready)
- 5-dimension system health framework identified
- Supabase backend integrated
- Behavioral health gap analyzed

**Critical discovery:**
- ACAT-X is the actual framework for evaluating Claude self-calibration
- Maps perfectly to "behavioral health" needs (Claude instances knowing themselves)

**Next session ready:**
- Map ACAT-X evaluation pipeline to Behavioral Health Practice
- Integrate ACAT-X results into Supabase backend
- Connect to Evaluator's weekly reports
- Create hybrid behavioral assessment (ACAT-X scores + human engagement survey)

**Files ready for next session:**
- EDUCATOR_PRACTICE_ACTIVATION_PLAN.md (ready Aug 21)
- TOKEN_OPTIMIZER_FRAMEWORK.md (ready Sep 11)
- SYSTEM_HEALTH_INTEGRATION_ARCHITECTURE.md (ready Sep 11 + ACAT-X integration)
- BEHAVIORAL_HEALTH_PRACTICE_FRAMEWORK.md (NEW — use ACAT-X as foundation)

---

**Status: HANDOFF READY**
