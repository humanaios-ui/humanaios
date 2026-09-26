# T5.2: Sentinel Gate Migration Steps

## Step 1: Deploy new gate logic (before 2026-09-12)

**Code change:** Replace 77-day check with resource checks

Old (remove):
```python
if (transaction_age_days > 77):
    alert("stuck")
```

New (add):
```python
if (labor_cumulative > labor_budget):
    alert(f"Labor budget {budget} consumed. Rebudget or close.")

if (tokens_consumed > tokens_budget * 1.1):
    alert(f"Token usage {percent}% of budget.")

if (validation_overhead > 2.5 * baseline):
    alert(f"Validation overhead high. Investigate.")

# Readiness gate: reject over-confident claims
if (know >= 0.65 AND uncertainty <= 0.30):
    reject("Over-confident. Reduce know or increase uncertainty.")
```

## Step 2: Validate against existing payloads (before 2026-09-12)

Run gate logic against all existing POSTFLIGHT payloads:
- Count passes/fails on old temporal gates
- Count passes/fails on new resource gates
- Confirm no false positives on transactions that were genuinely successful

**Expected:** <5% difference in alert rates (gates are functionally equivalent, just grounded differently).

## Step 3: Set thresholds using calibration data

From 9,137 points:

| Threshold | Source | Value |
|-----------|--------|-------|
| labor_budget | practice.yaml | varies by practice |
| tokens_budget | practice.yaml | varies by practice |
| validation_overhead_baseline | analytics calibration | 1.8 corrections per 100 tokens |
| validation_overhead_trigger | baseline * 2.5 | 4.5 corrections per 100 tokens |
| readiness_know_max | grounded mean + 1σ | 0.65 (grounded mean 0.40 + variance) |
| readiness_uncertainty_min | grounded mean - 1σ | 0.30 (grounded mean 0.60 - variance) |

## Step 4: Enable on 3 pilot practices (2026-09-12 00:00Z)

Activate gates on:
1. empirica-mesh-support
2. empirica-analytics
3. empirica-autonomy

**All existing open transactions** on these practices will be re-evaluated against new gates. Expected: most pass (gates are backcompat).

## Step 5: Monitor and adjust (2026-09-12 to 2026-09-13)

Collect:
- Alert count per gate type
- False positive rate
- User confusion signals (e.g., "why did my transaction fail?")
- Readiness gate rejections (how many people need to lower their know?)

**Adjustment rules:**
- If false positive rate > 5%: loosen threshold by 10%
- If false negative rate > 10%: tighten threshold by 10%
- If readiness gate rejecting >30% of transactions: discussion needed (may be correct—over-confidence is real)

## Success Criteria

✓ No false positives on legitimately successful transactions  
✓ Alerts trigger correctly when resources are exhausted  
✓ Readiness gate rejects known over-confident claims  
✓ Practices understand what alerts mean (clear messaging)  
✓ No stuck or hung transactions due to gate logic error  

