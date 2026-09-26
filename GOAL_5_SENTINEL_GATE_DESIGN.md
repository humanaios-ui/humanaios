# Goal 5: Migrate Sentinel Gates to Resource-Based (T5.1 Design)

## Current State

Sentinel gates are **temporal:**
- "Transaction > 77 days → stuck"
- "Session without close → blocker"
- "max_uncertainty 0.35 → blocks honest corrections"

## Proposed Resource-Based Gates

### Gate 1: Labor Budget Exceeded

**Trigger:** `human_labor_cumulative > human_labor_budget`

**Alert message:** "Labor budget 40/40 hours consumed. Rebudget or close goal."

**Why this works:** Honest signal. You've run out of allocated time; either extend budget or close.

### Gate 2: Token Budget Warning

**Trigger:** `ai_tokens_consumed > ai_tokens_budget * 1.1`

**Alert:** "Token usage 110%+ of budget. Review consumption."

**Why:** Catches runaway token burn early (before hitting hard limit).

### Gate 3: Validation Overhead High

**Trigger:** `corrections_per_100_tokens > 2.5 * baseline`

**Baseline (from analytics):** ~1.8 corrections per 100 tokens

**Alert:** "Validation overhead 2.5x baseline. Investigate: too many refinements or corrections."

**Why:** Signals either low-confidence work or excessive revision cycles.

### Gate 4: Readiness Gate (Prevents Over-Confidence)

**Current:** `max_uncertainty 0.35` (blocks honest admissions of uncertainty)

**Proposed:** `know ≥ 0.65 AND uncertainty ≤ 0.30` → **REJECT**

**Grounded logic:**
- 9,137 points show mean grounded know = 0.40
- Self-reported know = 0.68 (+0.28 gap)
- So claiming know=0.65+ is claiming you're more confident than your peers
- Readiness gate now rejects over-confident claims

**Passing example:**
- know: 0.50, uncertainty: 0.40 → PASS ✓ (honest)
- know: 0.70, uncertainty: 0.20 → REJECT ✗ (over-confident)

## Calibration Data

**Source:** 9,137 grounded points, 17 practices, analytics practice

| Metric | Mean Self | Mean Grounded | Gap |
|--------|---|---|---|
| completion | 0.65 | 0.41 | +0.24 |
| impact | 0.62 | 0.36 | +0.26 |
| know | 0.68 | 0.40 | +0.28 |
| uncertainty | 0.32 | 0.60 | -0.28 |

**Key insight:** People underestimate `uncertainty` by -0.28 on average.

## T5.2: Migration Steps

1. Deploy new gate logic to Sentinel (replace 77-day check)
2. Validate against existing POSTFLIGHT payloads (no false positives)
3. Set alert thresholds using calibration data
4. Enable on 3 pilot practices (2026-09-12)

## T5.3: Testing on 3 Practices

**Pilot group:**
- empirica-mesh-support (high volume, known stable)
- empirica-analytics (calibration data validation)
- empirica-autonomy (hung transaction recovery)

**Success criteria:**
- No false positives on passing transactions
- Alerts trigger correctly on resource exhaustion
- Readiness gate rejects known over-confident claims
- Practices understand alerts (not cryptic)

**Timeline:**
- Day 1 (2026-09-12): Deploy to 3 practices
- Day 2 (2026-09-13): Collect feedback, adjust if needed
- Day 3 (2026-09-14): Rollout to all 15 if pass, or retry

