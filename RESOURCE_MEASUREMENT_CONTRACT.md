# Resource Measurement Contract — Standard for All Practices

**Effective:** 2026-09-11 | **Grounded on:** 9,137 calibration points | **Gap:** +0.24 (completion), +0.26 (impact)

## What This Is

A contract: how we measure work in **resources** (labor hours, tokens), not **time** (weeks, deadlines, 77-day stuck thresholds).

## Three Requirements

### 1. PREFLIGHT estimates resources
```bash
./empirica-resource-cli.py preflight-submit \
  --estimate-hours 1.5-2.0 --estimate-tokens 40k-50k \
  --work-type research --vectors "know:0.7 uncertainty:0.3"
```

### 2. POSTFLIGHT reports actual consumption
```bash
./empirica-resource-cli.py postflight-submit \
  --human-active-hours 1.75 --vectors "know:0.85 uncertainty:0.15"
```

### 3. Sentinel gates enforce resource constraints
- **Labor check:** consumed ≤ budget (alert if >budget)
- **Token check:** burned ≤ budget * 1.1 (warning if >110%)
- **Validation overhead:** corrections/refinements ≤ 2.5x baseline
- **Readiness gate:** know < 0.65 OR uncertainty > 0.30 (prevents over-confidence)

## Grounded Baselines (9,137 points, 17 practices)

| Metric | Self-Report | Grounded | Gap |
|--------|---|---|---|
| completion | 0.65 | 0.41 | **+0.24** |
| impact | 0.62 | 0.36 | **+0.26** |
| know | 0.68 | 0.40 | **+0.28** |

**Meaning:** You systematically overestimate by ~25%. Sentinel gates account for this.

## Readiness Gate (enforced)

Your transaction fails POSTFLIGHT if:
- `know ≥ 0.65` AND `uncertainty ≤ 0.30` (over-confident)

Example of PASSING POSTFLIGHT:
- know: 0.55 (lower than your baseline 0.68) ✓
- uncertainty: 0.35 (higher than your baseline ~0.30) ✓

## Pilot Practices (2026-09-12 to 2026-09-13)

Three practices test gates first:
1. **empirica-mesh-support** (high volume, stable)
2. **empirica-analytics** (calibration data self-check)
3. **empirica-autonomy** (open hung transaction recovery)

If pass → contract moves to all 15 immediately.  
If fail → gates adjusted; retry 2026-09-14.

## Adoption Path

1. Get `empirica-resource-cli.py` from evaluator
2. Read this contract
3. Submit test PREFLIGHT (estimate task: 30 min, 5k tokens)
4. Submit test POSTFLIGHT (report actual)
5. Sentinel validates; gates are learning

---

Non-optional by 2026-09-30. All 15 practices adopt.

