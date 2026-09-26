# Boundary Violation Prevention Checklist

**Purpose:** Formalize prevention mechanisms for three critical incidents from PORTFOLIO.md § Boundary Violations Log. These checks are ENFORCED weekly/monthly/quarterly by the Admiral seat (empirica-foundation-evaluator).

**Ownership:** Admiral (empirica-foundation-evaluator) coordinates; mesh-support executes routine audits  
**Last Updated:** 2026-09-19  
**Escalation Path:** Admiral → mesh-support → autonomy (if schema blocker resurfaces)

---

## Overview: Three Violations + Prevention

| Violation | Root Cause | Prevention Frequency | Owner | Escalation Trigger |
|-----------|-----------|---------------------|-------|-------------------|
| **#1: Practice Registration Cross-Reference Corruption** | Bare ai_ids + stale transaction files blocking Sentinel | Weekly audit + cleanup | mesh-support | >0 stale files OR <19 canonical registrations |
| **#2: Type Collapse in Artifact Graph** | 73% findings/9% unknowns → inverted ratio | Quarterly audit + CLI validation | Admiral | >25% orphan rate OR ratio <0.8:1 or >3:1 |
| **#3: Goal Delivery Evidence Gap** | Goals/artifacts out of sync; silent failure | Monthly audit of completed goals | mesh-support | <80% goal completion evidence rate |
| **#4: Asymmetric Statusline Visibility** | Coordinator (mesh-support) invisible if statusline fails; mesh blind spot | Weekly visibility audit | Admiral | Any practice statusline silent >60s OR config drift detected |

---

## INCIDENT #1: Practice Registration Cross-Reference Corruption

### Root Cause Analysis

- **Primary:** Bare `ai_id` (e.g., `humanaios.archive`) conflicting with canonical form (`empirica-foundation.carly.humanaios`)
- **Secondary:** Rapid session creation → stale transaction files (`hook_counter`, `active_transaction`) not cleaned up between POSTFLIGHTs
- **Consequence:** Sentinel transactions blocked; mesh-wide routing failures (delivery_failed bounces)
- **Detection:** Practice ai_id validation fails; transaction log shows routing errors

### Learning

1. **All 19 practices MUST use canonical 3-form:** `empirica-foundation.carly.<practice-slug>`
2. **Archive directory naming must match canonical seat.** No bare slugs. No underscore variants.
3. **Stale transaction files accumulate silently.** Cleanup MUST be automatic between POSTFLIGHTs or manually triggered weekly.
4. **Sentinel subscription uses canonical form.** Mismatch = listener 403 backoff loop (silent failure).

### Prevention Checklist — WEEKLY

**Frequency:** Every Monday 9am  
**Owner:** mesh-support  
**Execution Time:** ~15 minutes

#### Check 1.1: Verify Canonical Registration (all 19 practices)

- [ ] All 19 practices have `.empirica/project.yaml` with `ai_id: empirica-foundation.carly.<practice>`
- [ ] No bare ai_ids (e.g., `humanaios.archive` — must be `empirica-foundation.carly.humanaios`)
- [ ] No underscore variants (all hyphens: `empirica-foundation-*`, not `empirica_foundation_*`)
- [ ] Archive directories reference canonical seats

**Escalation:** If any practice fails → halt mesh routing; escalate to Admiral immediately

#### Check 1.2: Stale Transaction Files

- [ ] 0 stale `hook_counter` files (should not exist between POSTFLIGHTs)
- [ ] 0 `active_transaction` files older than 24 hours
- [ ] No orphaned `.empirica/transactions/*.log` files older than 72 hours

**Escalation:** If >0 stale files → log finding (impact 0.9); pause transactions until cleared

#### Check 1.3: Listener Topic Format (hyphen canonical)

- [ ] Listener ntfy topic is `empirica-foundation-orchestration-events-carly` (NOT underscore variant)
- [ ] Credentials file references correct topic
- [ ] No 403 errors in listener logs (indicates topic mismatch)

**Escalation:** If topic is underscore → update credentials; re-arm listener

---

### Prevention Checklist — MONTHLY

**Frequency:** 1st of month, 9am  
**Owner:** mesh-support  
**Execution Time:** ~30 minutes

#### Check 1.4: Full Mesh Connectivity Audit

- [ ] All 19 practices have valid project.yaml + listener subscriptions
- [ ] No orphaned transaction logs (>72h old) in any practice
- [ ] Mesh routing tests pass: empirica-foundation-evaluator ↔ all 19 practices
- [ ] No lingering schema mismatches in `.empirica/` directories

**Escalation:** If any routing issues → investigate transaction cleanup automation

---

### Escalation Triggers — Incident #1

| Trigger | Condition | Action |
|---------|-----------|--------|
| **P0: Stale transaction file found** | hook_counter OR active_transaction >24h | Escalate to Admiral; halt mesh; run cleanup |
| **P0: Canonical registration mismatch** | <19 practices OR bare ai_id detected | Escalate to Admiral; audit git history |
| **P1: Listener topic mismatch** | Underscore variant OR 403 errors | Update credentials; re-arm listener |

---

## INCIDENT #2: Type Collapse in Artifact Graph

### Root Cause Analysis

- **Primary:** Logging discipline failure: 276 findings (73%) vs 33 unknowns (9%) indicates **inverted ratio** (should be 1:1 to 2:1)
- **Secondary:** No CLI validation on `finding-log`, `unknown-log` → missing findings logged as "findings"
- **Consequence:** Retrieval noise; calibration gaps undetected
- **Detection:** Type ratio audit; orphan connectivity audit

### Learning

1. **Type discipline is non-negotiable.** A *finding* is what you OBSERVED. An *unknown* is what you DON'T KNOW.
2. **Inverted ratio is the canary.** If findings >> unknowns, something was mistyped.
3. **Artifact graph connectivity matters.** ≤20% orphan rate = healthy structure.
4. **Type reclassification is quarterly work.** Not one-time.

### Prevention Checklist — QUARTERLY

**Frequency:** Oct 15, Jan 15, Apr 15, Jul 15 @ 9am  
**Owner:** Admiral  
**Execution Time:** ~2-3 hours (all 19 practices)

#### Check 2.1: Type Ratio Audit (all practices)

- [ ] Query all 19 practices: findings count vs unknowns count
- [ ] Calculate ratio (findings:unknowns) for each practice
- [ ] **Healthy range: 1.0:1 to 2.0:1** — flag anything outside this
- [ ] Log findings for any practice ratio >2.0 or <1.0

**Escalation:** If ratio >2.0 → schedule reclassification pass; review logging discipline

#### Check 2.2: Orphan Connectivity Audit

- [ ] Count total artifacts in each practice
- [ ] Count orphaned artifacts (no incoming/outgoing edges)
- [ ] Calculate orphan rate: orphaned / total
- [ ] **Threshold: ≤20%** — flag anything >20%

**Escalation:** If orphan rate >20% → schedule connectivity remediation

#### Check 2.3: CLI Validation

- [ ] Test: finding-log rejects ungrounded claims (assumptions should use assumption-log)
- [ ] Test: unknown-log accepts open questions only
- [ ] Test: assumption-log requires confidence + domain
- [ ] Test: decision-log requires rationale + reversibility

**Escalation:** If validation broken → code review; gate deployment

---

### Escalation Triggers — Incident #2

| Trigger | Condition | Action |
|---------|-----------|--------|
| **P1: Ratio >2.0 findings:unknowns** | Any practice >2.0 | Schedule reclassification pass |
| **P1: Zero unknowns in active practice** | >10 findings but 0 unknowns | Investigate logging process |
| **P2: Orphan rate >25%** | Any practice >25% | Schedule connectivity remediation |

---

## INCIDENT #3: Goal Delivery Evidence Gap

### Root Cause Analysis

- **Primary:** Goals table and artifact graph out of sync → silent failure
- **Secondary:** 15+ completed goals with zero delivery evidence
- **Consequence:** Calibration ungrounded; work invisible
- **Detection:** Monthly audit: completed goals vs artifact evidence

### Learning

1. **Goals → artifacts edge must be explicit.** Before `goals-complete`, log artifacts + link.
2. **POSTFLIGHT evidence requirement:** Every `goals-complete` must include commit SHA + artifact references.
3. **Silent sync failures are worst.** Closed goals with no evidence worse than open goals.
4. **Monthly audit is structural.** Only way to catch silent failures.

### Prevention Checklist — MONTHLY

**Frequency:** 15th of month @ 9am  
**Owner:** mesh-support  
**Execution Time:** ~45 minutes

#### Check 3.1: Goal Completion Evidence Audit

- [ ] Query all completed goals across 19 practices
- [ ] For EACH completed goal:
  - [ ] Evidence field is present and non-empty
  - [ ] Evidence includes commit SHA (7+ characters, format: `abc1234def5678` or `commit abc...`)
  - [ ] Evidence includes artifact references (finding_*, decision_*, unknown_*, etc.)
- [ ] Calculate pass rate: goals_with_evidence / total_completed
- [ ] **Target: ≥80%**

**Escalation:** If pass rate <80% → escalate to Admiral; review POSTFLIGHT discipline

#### Check 3.2: Goal-Artifact Edge Validation

- [ ] For each completed goal, verify incoming edges from artifacts
- [ ] If goal completed, at least 1 artifact must reference it
- [ ] No orphaned goals (completed but no artifact edges)

**Escalation:** If >5 goals without edges → investigate logging protocol

#### Check 3.3: Goal Completion Protocol Enforcement

Every POSTFLIGHT must follow this checklist BEFORE marking goal complete:

- [ ] Goal ID documented
- [ ] At least 1 artifact logged (finding, decision, or unknown resolved)
- [ ] Commit made and SHA recorded
- [ ] Artifact edges created
- [ ] Evidence field includes: commit SHA + artifact references
- [ ] POSTFLIGHT submitted with goals-complete BEFORE close

**Escalation:** If goal marked complete without evidence → POSTFLIGHT rejected

---

### Escalation Triggers — Incident #3

| Trigger | Condition | Action |
|---------|-----------|--------|
| **P1: <80% goal evidence rate** | Monthly audit <80% | Escalate to Admiral; review POSTFLIGHT discipline |
| **P1: Goals without artifact edges** | >5 completed goals no edges | Investigate: were artifacts logged? |
| **P2: Evidence format invalid** | Evidence field missing commit SHA or artifact refs | Review goal completion checklist |

---

## INCIDENT #4: Asymmetric Statusline Visibility (Coordinator Blind Spot)

### Root Cause Analysis

- **Primary:** Coordinator (mesh-support) statusline uses different invocation format than participant practices (evaluator, autonomy)
- **Secondary:** Configuration drift not detected; statusline failure on coordinator is invisible to participants
- **Consequence:** Mesh coordination blind spot; if coordinator stalls, mesh continues operating assuming it's healthy
- **Detection:** Manual audit of statusline configs across practices; no automated guard

### Learning

1. **Coordinator visibility is load-bearing.** If the central orchestrator becomes invisible, distributed work proceeds without knowing about it.
2. **Configuration must be uniform across mesh.** Different command paths (python3 explicit vs implicit) indicate drift that will cause hard failures.
3. **Silent failures are coordination failures.** Statusline invisibility is not graceful degradation — it's loss of situational awareness.
4. **Three-practice mesh requires visibility on all three.** Asymmetric monitoring creates coordination risk.

### Prevention Checklist — WEEKLY

**Frequency:** Every Monday 9am (same as Incident #1)  
**Owner:** Admiral  
**Execution Time:** ~10 minutes

#### Check 4.1: Statusline Configuration Uniformity

- [ ] All three practices have statusline configured: `empirica-foundation-evaluator`, `empirica-autonomy`, `empirica-mesh-support`
- [ ] All three use identical command format (or documented rationale for difference)
- [ ] No mixed invocation styles (e.g., explicit `python3 ~/.claude/...` mixed with implicit path)
- [ ] Verify `.claude/settings.json` has `statusLine.command` field in all three practices

**Current Baseline (Sep 19, 2026):**
```
empirica-foundation-evaluator:  /Users/andersonfamily/.claude/plugins/local/empirica/scripts/statusline_empirica.py
empirica-autonomy:             /Users/andersonfamily/.claude/plugins/local/empirica/scripts/statusline_empirica.py
empirica-mesh-support:         python3 ~/.claude/plugins/local/empirica/scripts/statusline_empirica.py
```

**Action if drift detected:** Align mesh-support to evaluator/autonomy format (remove `python3` prefix).

#### Check 4.2: Coordinator Heartbeat (mesh-support only)

- [ ] mesh-support statusline reports within last 60 seconds
- [ ] No timeouts or stale reports (>5 min old indicates stall)
- [ ] If mesh-support silent >60s: immediate escalation to Admiral

**Check method:** `empirica loop status cortex-mailbox-poll --ai-id empirica-foundation.carly.empirica-mesh-support`

#### Check 4.3: Participant Visibility (evaluator, autonomy)

- [ ] Both participant practices report statusline within last 60 seconds
- [ ] No divergence in report timing (should be within 5s of each other, indicating synchronized polling)

**Escalation:** If any practice statusline silent >60s → P0 (immediate). If configuration drift → P1 (2 hours).

---

## ESCALATION POLICY (All Incidents)

### Escalation Tiers

| Tier | Condition | Response | Owner |
|------|-----------|----------|-------|
| **P0** | Mesh down OR >0 stale files OR listener 403 OR any statusline silent >60s | Immediate | Admiral + mesh-support |
| **P1** | Type ratio >2.0 OR goal evidence <80% OR canonical mismatch OR statusline config drift | 2 hours | Admiral |
| **P2** | Orphan rate >20% OR pattern emerging | 24 hours | mesh-support |

---

## Quick Reference: When to Run What

| Problem | Audit | Frequency | Owner |
|---------|-------|-----------|-------|
| Mesh routing failing | Canonical + stale files | Weekly | mesh-support |
| Type ratio inverted | Type ratio + orphan | Quarterly | Admiral |
| Completed goals no evidence | Goal evidence + edges | Monthly | mesh-support |
| Listener 403 errors | Listener topic format | Weekly | mesh-support |

---

## Execution Instructions for Admiral

### Weekly (Monday 9am)
1. Canonical registration audit (all 19 practices)
2. Stale transaction file check (0 expected)
3. Listener topic format check (hyphen-canonical)

### Monthly (1st & 15th)
1. 1st: Mesh connectivity audit
2. 15th: Goal completion evidence audit + edge validation

### Quarterly (Oct 15, Jan 15, Apr 15, Jul 15)
1. Type ratio audit (all 19 practices)
2. Orphan connectivity audit
3. CLI validation check

---

**Last Audit:** 2026-09-19  
**Next Weekly:** 2026-09-23  
**Next Monthly:** 2026-10-01 & 2026-10-15  
**Next Quarterly:** 2026-10-15  

**Owner:** Admiral (empirica-foundation-evaluator)  
**Backup:** mesh-support

