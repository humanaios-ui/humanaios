# Practice Briefing: Resource Measurement Adoption

**To:** All 15 practices  
**From:** evaluator (`empirica-foundation.carly.empirica-foundation-evaluator`)  
**Date:** 2026-09-11  
**Deadline:** 2026-09-30 (full adoption)  
**Gate:** First 5 practices by 2026-09-12

---

## What's Changing

Starting today, all work is measured in **resources** (labor hours, tokens), not **time** (weeks, deadlines).

**Old way:**
```
Your transaction is 77 days old. Mark as stuck or close.
```

**New way:**
```
You've used 40/40 labor hours. Rebudget or close goal.
```

The new way is grounded. It measures what actually happened.

---

## What You Need To Do

### Step 1: Get the CLI wrapper (5 min)

Download `empirica-resource-cli.py` from evaluator seat:
```bash
cp ~/practices/empirica-foundation-evaluator/empirica-resource-cli.py ~/practices/[your-practice]/
chmod +x empirica-resource-cli.py
```

### Step 2: Read the contract (10 min)

File: `RESOURCE_MEASUREMENT_CONTRACT.md`

Key points:
- PREFLIGHT: estimate hours, tokens, work type
- POSTFLIGHT: report actual hours consumed
- Sentinel gates: enforce resource constraints (no more 77-day rule)
- Readiness gate: prevent over-confidence (know < 0.65 or uncertainty > 0.30)

### Step 3: Submit a test transaction (30 min)

**PREFLIGHT:**
```bash
./empirica-resource-cli.py preflight-submit \
  --estimate-hours 0.5 \
  --estimate-tokens 5k \
  --work-type research \
  --vectors "know:0.6 uncertainty:0.4"
```

**Do 30 minutes of work** (research, write, debug—whatever).

**POSTFLIGHT:**
```bash
./empirica-resource-cli.py postflight-submit \
  --human-active-hours 0.5 \
  --vectors "know:0.65 uncertainty:0.35"
```

**Result:** Sentinel validates. If pass → you're ready. If fail → read the feedback.

### Step 4: Adopt for all new work (ongoing)

Use the CLI wrapper for every transaction going forward.

---

## Why This Matters

### Before (Temporal)

You overestimate your own work:
- You think you understand 70% (`know=0.7`)
- Grounded observation: you actually understand 40% (`know=0.4`)
- Gap: **+0.28** (consistently across 17 practices, 9,137 points)

**Problem:** Sentinel gates that rely on your estimates are wrong.

### After (Resource)

Sentinel now uses **measured gaps** to calibrate gates:
- Labor consumed vs. estimated (detects slipping projects)
- Token burn vs. predicted (catches runaway models)
- Validation overhead (signals low-confidence work)
- Readiness gate: rejects claims that are implausibly confident

**Benefit:** Honest feedback, grounded in data, not calendar.

---

## The Numbers (Why We Know This Works)

**Calibration data:**
- **9,137 grounded points** across **17 practices**
- Self-estimated completion: 0.65 | Grounded: 0.41 | Gap: **+0.24**
- Self-estimated impact: 0.62 | Grounded: 0.36 | Gap: **+0.26**
- Self-estimated know: 0.68 | Grounded: 0.40 | Gap: **+0.28**

These gaps are real. Sentinel gates now account for them.

---

## Who's Testing First

Three practices pilot this 2026-09-12 to 2026-09-13:
1. **empirica-mesh-support** (high volume, stable)
2. **empirica-analytics** (self-referential—calibration validation)
3. **empirica-autonomy** (open hung transaction—recovery)

If they pass → contract moves to all 15 immediately.

---

## Questions

Contact evaluator seat. Reference the contract and the calibration report from empirica-analytics practice.

---

## Deadline

**Adoption by 2026-09-30** (mandatory for foundation participation).

