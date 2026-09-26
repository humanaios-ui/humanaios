# Epistemic Discipline Protocol — Handoff Brief (v1.2)

**Date:** Sep 18, 2026 | **Status:** CRITICAL UPDATE - Deadlock remediation + full protocol

---

## 🔴 CRITICAL: Cross-Practice Deadlock Remediation (RESOLVED)

**Issue:** Stale `active_transaction_*.json` + `hook_counter_*.json` files blocked 4 critical practices.

**Root Cause:** No TTL/auto-cleanup on transaction state files. Files >24h old cascade-block Sentinel, preventing new PREFLIGHT cycles.

**Status:** REMEDIATED Sep 18
- ✅ evaluator: 27 files cleaned
- ✅ autonomy: 22 files cleaned
- ✅ humanaios: 27 files cleaned
- ✅ local-machine-optimizer: 10 files cleaned
- ✅ mesh-support: 0 files (clean throughout)

**Per-practice action:**
```bash
rm -f .empirica/active_transaction*.json .empirica/hook_counter*.json
empirica status  # Verify: closed, no-transaction
```

**Permanent fix:** Implement 24h TTL + auto-cleanup in empirica core.

---

## Full Protocol (Per Practice, Per Transaction)

### 1. Goals Audit
```bash
empirica goals-list --status completed --output json
# Spot-check: git commit? artifacts linked? POSTFLIGHT exist?
empirica finding-log --finding "[gap]" --impact [0-1]
```

### 2. Epistemic Gardening
```bash
# - Resolve stale/superseded artifacts
# - Close answered unknowns  
# - Verify retraction rate >5% (error-acknowledgment active)
# - Audit sources + visibility
empirica finding-log --finding "[gap]" --impact [0-1]
```

### 3. PREFLIGHT → Work → POSTFLIGHT
```bash
empirica preflight-submit - << 'EOF'
{
  "session_id": "...",
  "vectors": { know, uncertainty, context, clarity, coherence, signal, 
               density, state, change, completion, impact, do, engagement },
  "work_type": "code|research|debug|infra|...",
  "noetic_artifacts_planned": { findings: N, unknowns: M, assumptions: K, decisions: J }
}
EOF

# During: log-artifacts - (batch multi-type with edges)

empirica postflight-submit - << 'EOF'
{
  "session_id": "...",
  "vectors": { ... UPDATE ... },
  "artifact_breadth_achieved": { findings: N, unknowns: M, assumptions: K, decisions: J },
  "retractions": X,
  "connectivity_pct": Y,
  "claims": [ { index: 1, verdict: "held|refuted|untested", evidence: "..." } ]
}
EOF
```

### 4. Report Metrics
```bash
empirica message-send --target empirica-foundation.carly.empirica-foundation-evaluator \
  --message-type status_update --subject "Status: [practice] Cycle Complete" \
  --body "Findings: N, Unknowns: M, Assumptions: K, Decisions: J, 
Breadth: %, Orphan: %, Retraction: %, Inline: %"
```

---

## Three Actionable Rules

1. **PREFLIGHT declares artifact intent** (findings/unknowns/assumptions/decisions)
2. **Inline logging during work** (batch via `log-artifacts -`)
3. **POSTFLIGHT validates breadth + connectivity + retraction rate**

---

## Target Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Breadth | >50% | Multi-type logging |
| Orphan rate | >70% | Connected artifacts |
| Retraction rate | >5% | Error-acknowledgment active |
| Inline logging | >80% | Real-time, not post-hoc |

**Success gate:** 12 of 15 practices reach all thresholds → orchestration restart.

---

## CORRECTION HISTORY

| v | Date | Change |
|---|------|--------|
| 1.0 | Sep 18 | Initial protocol |
| 1.1 | Sep 18 | mailbox-send → message-send fix |
| 1.2 | Sep 18 | Deadlock remediation + full protocol + condensed |
