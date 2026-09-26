# Governance Audit Ritual

**Status:** LIVE (activated 2026-09-26)  
**Cadence:** Monthly (last Monday of month)  
**Duration:** ~2 hours  
**Owner:** empirica-foundation-evaluator (Admiral seat)

---

## What This Ritual Does

Monthly automated audit of governance enforcement across three GitHub repos (operations, humanaios, lasting-light-ai) and 20 empirica practices. Detects drift before it compounds.

**Detects:**
- Missing pinned commits (governance references commits that don't exist)
- Stale registries (GOVERNANCE_RATIFICATIONS_REGISTRY, decision logs)
- Semantic drift (terms used inconsistently across files)
- Orphaned practices (no documented edges to repos)
- SLA violations (Z1 candidates overdue in z1-inbox)
- Monitoring gaps (postflight INDEX stale >30 days)

**Outputs:**
- Drift findings logged to empirica (`finding-log`)
- SLA violations published to Z2_DECISION_SLA_TRACKER.md
- Recommendations logged for Admiral review

---

## Monthly Ritual Checklist

### Phase 1: Verification (30 min)

- [ ] **Pinned commits:** Check 3 pinned commits exist
  - `cd ~/github/operations && git show 3c2ad73` (or current pinned commit)
  - Repeat for humanaios, lasting-light-ai
  - Log finding if any commit is not found

- [ ] **Registries non-empty:** 
  - `wc -l ~/github/operations/GOVERNANCE_RATIFICATIONS_REGISTRY.yaml`
  - If `decisions: []` still true → finding logged
  - Check Z1_INBOX_INDEX.md "Decided" section has growth

- [ ] **Postflight INDEX current:**
  - `stat -f%Sm -t "%Y-%m-%d" ~/practices/empirica-foundation-evaluator/.postflight/INDEX.yaml`
  - If >30 days old → finding logged
  - Check mesh-postflight-ingest.py is running

- [ ] **Semantic consistency:**
  - Grep operations/GOVERNANCE.md for "ratif", "Z2", "Phase 2", count meanings
  - If ≥3 incompatible meanings per term → finding logged

---

### Phase 2: Graph Integrity (20 min)

- [ ] **Practice edges:** Count non-empty edges across 20 practices
  - `find ~/practices -name project.yaml -exec grep -l "edges:" {} \;`
  - If still mostly empty → finding logged
  - Track progress (target: 50% of practices have edges by 2026-10-26)

- [ ] **Repo connections:** Do all 3 repos have associated practices?
  - operations → humanaios-ui? empirica-mesh-support? evaluator?
  - humanaios → humanaios? 
  - lasting-light-ai → (orphan)
  - Log any missing edges as opportunities

---

### Phase 3: SLA Enforcement (10 min)

- [ ] **Z1 Inbox age:** Run z2_sla_checker.py
  - `python3 ~/practices/empirica-foundation-evaluator/.empirica/scripts/z2_sla_checker.py`
  - Counts candidates by age bracket (0-2d, 3-4d, 5-8d, 8+d)
  - Updates Z2_DECISION_SLA_TRACKER.md
  - Escalates any 8+ days to Admiral with IC-class flag

- [ ] **Z2 decision throughput:** 
  - Count ratifications last 30 days (from git log or Z2_RATIFICATION_LOG.md)
  - Compare to Z1 intake rate (new candidates added per month)
  - If throughput < intake → finding logged (capacity issue)

---

### Phase 4: Learning (20 min)

- [ ] **Lessons from drift:** Review all drift findings from last month
  - Are same findings repeating? → dead-end, escalate
  - Are new drift patterns emerging? → lesson, catalog for practices

- [ ] **Hypothesis test:** Did any opportunity from last audit get executed?
  - Track execution rate of Connect/Coordinate/Collaborate/Continue opportunities
  - Low execution → finding logged (suggests priorities misaligned)

---

### Phase 5: Reporting (40 min)

- [ ] **Log findings:** Use `empirica finding-log` for each drift finding
  - Include path, line number, expected vs actual state
  - Link to prior month's findings if repeating

- [ ] **Log unknowns:** If cause of drift is unclear (e.g., why IS postflight INDEX stale?)
  - Use `empirica unknown-log` + mark for investigation

- [ ] **Update PRACTICE_REPO_INVENTORY.md:** Sync status, next verification date

- [ ] **Post to mesh:** Alert mesh-support + Admiral of critical findings
  - Use `empirica cortex-mailbox-send` (type: collab_brief)

- [ ] **Close ritual:** POSTFLIGHT with `work_type: audit`, report calibration

---

## Automation Setup

### Files Needed

1. **CI Workflow:** `.github/workflows/governance-audit.yml`
   ```yaml
   name: Monthly Governance Audit
   on:
     schedule:
       - cron: '0 9 ? * MON#5'  # Last Monday of month at 9am
     workflow_dispatch:
   jobs:
     audit:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Run governance audit ritual
           run: |
             python3 .empirica/scripts/governance_audit_ritual.py
   ```

2. **Audit Script:** `.empirica/scripts/governance_audit_ritual.py`
   - Implements checklist above
   - Outputs structured findings (JSON)
   - Auto-logs to empirica via CLI

---

## Success Criteria

By 2026-10-26 (one month from audit):
- [ ] Pinned commits exist and are verifiable
- [ ] GOVERNANCE_RATIFICATIONS_REGISTRY has ≥5 entries
- [ ] Postflight INDEX updated within 7 days of today
- [ ] ≥50% of practices have documented edges to repos
- [ ] Z2 SLA violations < 5 candidates (from current 11)
- [ ] Semantic drift test shows consistent terminology across 3 files

If <50% met → escalate to Admiral as governance capacity issue.

---

## How to Trigger Manually

```bash
cd ~/practices/empirica-foundation-evaluator && \
empirica preflight-submit --work-type audit --task-context "Governance drift audit ritual" && \
python3 .empirica/scripts/governance_audit_ritual.py && \
empirica postflight-submit --vectors 'know:0.95' --reasoning "Monthly audit complete"
```

---

**Owned by:** empirica-foundation-evaluator (Admiral)  
**Next run:** 2026-09-30 (last Monday of Sep)  
**Escalation:** Admiral + mesh-support if critical findings exceed 3  
**Archive:** Findings tagged `governance-audit-YYYY-MM` for retrospective analysis
