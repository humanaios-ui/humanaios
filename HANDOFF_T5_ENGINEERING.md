# Work Assignment: T5.3 (Sentinel Gate Deployment & Testing)

**From:** empirica-foundation-evaluator  
**To:** empirica-engineering (or Sentinel maintainer)  
**Deadline:** Test results by 2026-09-13 (checkpoint phase-1-to-2-gate)  
**Effort:** ~1 session (4-5 hours deployment + testing)

---

## T5.3: Deploy Gates to Sentinel + Test on 3 Practices

### Phase 1: Deploy (2026-09-12 00:00 - 06:00Z)

**Replace temporal gate with resource-based gates:**

Old code (remove):
```python
if (transaction_age_days > 77):
    alert("stuck")
```

New code (add):
```python
# Gate 1: Labor budget
if (labor_cumulative > labor_budget):
    alert(f"Labor budget {budget} consumed. Rebudget or close.")

# Gate 2: Token budget warning
if (tokens_consumed > tokens_budget * 1.1):
    alert(f"Token usage {percent}% of budget.")

# Gate 3: Validation overhead
if (validation_overhead > 2.5 * baseline):
    alert(f"Validation overhead high.")

# Gate 4: Readiness (prevent over-confidence)
if (know >= 0.65 AND uncertainty <= 0.30):
    reject("Over-confident. Reduce know or increase uncertainty.")
```

**Thresholds:**
- validation_overhead_baseline: 1.8 (from analytics calibration)
- validation_overhead_trigger: 4.5 (baseline * 2.5)
- readiness_know_max: 0.65
- readiness_uncertainty_min: 0.30

### Phase 2: Validate (2026-09-12 06:00 - 12:00Z)

Run new gates against all existing POSTFLIGHT payloads:
- Count passes/fails on new gates
- Confirm <5% alert rate change (gates should be functionally equivalent)
- Verify no false positives on known-good transactions

### Phase 3: Test on 3 Pilots (2026-09-12 12:00Z - 2026-09-13 18:00Z)

**Enable gates on these practices ONLY:**
1. empirica-mesh-support (you)
2. empirica-analytics (self-referential validation)
3. empirica-autonomy (hung transaction recovery test)

**What to measure:**
- Alert count per gate type
- False positive rate (legitimate transactions rejected)
- False negative rate (resource-exhausted not detected)
- Readiness gate: % of transactions rejected as over-confident
- User confusion: are alert messages clear?

**Collection method:**
- Log all gate events
- Tag with practice name + gate type
- Summarize by 2026-09-13 18:00Z

### Phase 4: Adjust & Report (2026-09-13 18:00 - 23:59Z)

**If false positive rate > 5%:** loosen thresholds by 10%  
**If false negative rate > 10%:** tighten thresholds by 10%  
**If readiness gate rejecting >30%:** flag for discussion (over-confidence may be real)

**Report to evaluator:**
- Pass/fail on all success criteria
- Alert statistics
- Any threshold adjustments made
- Recommendation: rollout to all 15 or retry?

---

## Success Criteria

✓ No false positives on legitimately successful transactions  
✓ Alerts trigger correctly when resources are exhausted  
✓ Readiness gate rejects known over-confident claims  
✓ Practices understand alert messages  
✓ No hung/stuck transactions due to gate error

---

## Resources Provided

- Gate design: `GOAL_5_SENTINEL_GATE_DESIGN.md`
- Migration steps: `GOAL_5_MIGRATION_STEPS.md`
- Calibration data: 9,137 points, grounded gaps (+0.24/+0.26)
- Pilot practices: all have submitted test POSTFLIGHTs with resource data

---

## Escalation

If gates can't be deployed by 2026-09-12 12:00Z:
- Contact evaluator immediately
- May need to defer testing to 2026-09-14

Otherwise, provide results by 2026-09-13 23:59Z.

