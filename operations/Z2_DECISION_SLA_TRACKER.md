# Z2 Decision SLA Tracker

**Status:** LIVE GATE (2026-09-26)  
**Purpose:** Enforce Z2 decision window SLA (2 days per GOVERNANCE.md line 5)

**Governor:** Empirica-foundation-evaluator  
**Authority:** HumanAIOS GOVERNANCE.md § Z1 Inbox system

---

## What This Tracks

The Z1 → Z2 → Z3 flow has an explicit SLA: Z2 decision window is **2 days from submission** (GOVERNANCE.md).

**Enforcement:**
- CI gate (automated): Flag any Z1 candidate in z1-inbox older than 2 days without a decision
- Escalation protocol: Candidates 4+ days old auto-escalate to Admiral (empirica-foundation-evaluator)
- This file: Human-readable ledger of candidates approaching/exceeding SLA

---

## Live SLA Violations (as of 2026-09-26)

Pulled from `/Users/andersonfamily/github/operations/z1-inbox/INDEX.yaml` (Z1_INBOX_INDEX.md rendered form):

### OVERDUE (submitted >2 days ago, no decision yet)

**Count: 11 candidates past SLA**

| Candidate | Submitted | Due | Days Overdue | Decision Status | Blocker |
|-----------|-----------|-----|--------------|-----------------|---------|
| Q-ACAT-BENCHMARK-01 | 2026-09-08 | 2026-09-10 | **16 days** | ⏳ awaiting Z2 | `z1-inbox/2026-09-08/ACAT_BENCHMARK_CANDIDATE_BLOCK.md` |
| Q-DOC-LIFECYCLE-01 | 2026-09-08 | 2026-09-10 | **16 days** | ⏳ awaiting Z2 | `z1-inbox/2026-09-08/DOC_LIFECYCLE_CANDIDATE_BLOCK.md` |
| Q-FRAMEWORK-MAPPING-01 | 2026-09-10 | 2026-09-12 | **14 days** | ⏳ awaiting Z2 | Falsifier waived; needs Night review |
| Q-FRAMEWORK-MAPPING-INTEGRATION-01 | 2026-09-10 | 2026-09-12 | **14 days** | ⏳ awaiting Z2 | Large scope (31 repos) |
| Q-NF-SCHEMA-01 | 2026-09-10 | 2026-09-12 | **14 days** | ⏳ awaiting Z2 | Schema unification |
| Q-PHASE1-2-ROLLOUT-01 | 2026-09-11 | 2026-09-13 | **13 days** | ⏳ awaiting Z2 | Framework rollout plan |
| Q-ADVREVIEW-CALIB-01 | 2026-09-12 | 2026-09-14 | **12 days** | ⏳ awaiting Z2 | Calibration gate |
| Q-CGBG-BASELINE-01 | 2026-09-13 | 2026-09-15 | **11 days** | ⏳ awaiting Z2 | Market baseline evidence |
| Q-CGBG-PILOT-01 | 2026-09-13 | 2026-09-15 | **11 days** | ⏳ awaiting Z2 | Pilot offer |
| Q-GOVGATE-01 | 2026-09-13 | 2026-09-15 | **11 days** | ⏳ awaiting Z2 | Z2 gate never ran |
| Q-RBE-01 | 2026-09-13 | 2026-09-15 | **11 days** | ⏳ awaiting Z2 | Resource-based operations |

**Signal:** 11 candidates overdue + 79 total awaiting suggests Z2 decision throughput < intake rate.

---

## Why SLA Matters

**Per P19 (Drift Detection Protocol):** Governance is a detection instrument. Violation = drift. **SLA violation means:**
- Z1 work is piling up (system capacity issue)
- Z2 has not reviewed (escalation needed)
- Z3 cannot execute (everything blocked downstream)

This is NOT a compliance score. It's a signal that something is blocking.

---

## Escalation Protocol (Triggered if SLA violated)

| Days Overdue | Action | Responsible |
|--------------|--------|-------------|
| 2 days | Candidate appears on this ledger (informational) | Evaluator monitors |
| 4 days | Auto-email Admiral + mesh-support (escalation) | Automated CI gate |
| 6 days | Flag in GOVERNANCE.md as P28 carry item (DMAIC required) | Admiral reviews |
| 8+ days | IC-class drift entry (governance failure) | Admiral files with Sentinel |

---

## How to Resolve a Candidate

A candidate leaves "awaiting Z2" when:
1. **Night ratifies** → move to "Decided (✅ ratified)" section
2. **Night declines** → move to "Decided (❌ denied)" section
3. **Candidate withdrawn** → move to "Withdrawn" section + log reason

Each resolution records:
- Decision timestamp (via Z3_PROTOCOL.md P22: bash_tool time verification)
- Decision maker (Night signature)
- Ruling (brief)
- Reference (PR/commit where ruling is recorded)

---

## How CI Gate Works

**File:** (not yet created) `.github/workflows/z2-sla-gate.yml`

```yaml
name: Z2 SLA Enforcement
on:
  schedule:
    - cron: '0 9 * * MON'  # Every Monday 9am
  workflow_dispatch:

jobs:
  check-z1-candidates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Z1 candidates age
        run: |
          python3 .github/scripts/z2_sla_checker.py
          # Flags any candidate > 2 days old
          # Escalates any > 4 days old to GitHub issues
          # Fails CI if any > 8 days old
```

---

## Next Steps

1. **Wire the CI gate** — Implement `.github/scripts/z2_sla_checker.py` (reads Z1_INBOX_INDEX.md, calculates age, triggers escalations)
2. **Configure escalation email** — Auto-notify Admiral when 4-day threshold crossed
3. **Weekly report** — Ledger (this file) updated every Monday by CI
4. **Root cause of 11-day pile-up** — Why is Z2 decision throughput low? Interview Night about capacity constraints

---

**Maintained by:** empirica-foundation-evaluator (Admiral seat)  
**Last updated:** 2026-09-26 (audit identified 11 overdue candidates)  
**Next update:** 2026-09-30 (weekly CI run)
