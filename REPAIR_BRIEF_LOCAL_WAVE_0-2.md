# HumanAIOS Repair Sequence — empirica-foundation-evaluator Local Work

**Status:** Ready for autonomous execution  
**SER:** ser_<pending-creation>  
**Role:** Orchestrator + executor (some fixes are local, others delegated)  
**Date Issued:** 2026-09-11

---

## Your Assignment: 5 Local Fixes + Coordination Role

As the evaluator seat, you own local calibration work, session ritual infrastructure, and coordination with other practices. This assignment includes local execution (5 fixes) plus mesh coordination for upstream work (David fixes).

| Wave | Fix | Title | Effort | Blocker | Scope |
|------|-----|-------|--------|---------|-------|
| 0 | 08 | Close 77-day stale transaction | 10 min | None | Local |
| 0 | 13 | Housekeeping (doctor, uncommitted, duplicates) | 1 session | None | Local |
| 1 | 07 | Fix Evaluator seat identity | 1 session | Fix 13 | Local |
| 1 | 10 | Session ritual hooks (retrieval-first, blocking gates) | 1 session | None | Local |
| 2 | 11 | Graph closure sprint (unknowns/decisions/assumptions) | 3 sessions | Fix 10 | Local |

**Total local effort:** ~6 sessions. **Plus coordination role (no execution burden).**

---

## Wave 0 (Mechanical, No Decisions)

### Fix 08: Close 77-Day Stale Transaction

**What's broken:** A transaction opened 2026-06-26 (session 364c413d…) is stuck in noetic phase. It's been 77 days with no work claimed. Skews every "open transaction" metric and suppresses mailbox polling.

**What to do:**

1. Submit POSTFLIGHT for that session:
```bash
empirica postflight-submit - << 'EOF'
{
  "vectors": {
    "know": 0.50,
    "uncertainty": 0.20
  },
  "reasoning": "Closing a stale transaction opened 2026-06-26 with no work claimed; vectors reflect no learning"
}
EOF
```

2. Log a mistake artifact:
```bash
empirica mistake-log \
  --mistake "transaction left open 77 days; the enforcer hook did not catch it" \
  --prevention "implement session-end hook that refuses close on zero loops closed" \
  --related-to "fix:10"
```

**Verify:**
```bash
empirica status --output json | jq '.open_instances'
# Should show 0 or 1, not 2+ (the stale one gone)
```

**Time:** 10 minutes.

---

### Fix 13: Housekeeping (Doctor, Uncommitted, Duplicates)

**What's broken:**
1. MCP bundle is 1.13.32, CLI is 1.13.33 (mismatch)
2. Uncommitted work in 17 repos (schema.sql 24 changed files, resource-miner 8, grok-crossref 8)
3. Duplicate practice trees: `practices/humanaios.archive.*` (byte-identical copy with sessions.db), `practices/website/operations-repo` and `practices/empirica-outreach/acat/` (second and third clones)
4. `github/empirica-practice-mesh` has 1.8 GB untracked copy of ~/practices including node_modules

**What to do:**

1. **Reinstall MCP plugin:**
```bash
empirica plugin install empirica --force
empirica doctor  # verify 0 warn
```

2. **Commit or discard uncommitted work** in each repo:
```bash
# Review what's uncommitted
for repo in ~/practices/*/; do
  cd "$repo"
  if [ -n "$(git status --porcelain)" ]; then
    echo "$repo: $(git status --porcelain | wc -l) changes"
  fi
done

# Either commit or git checkout -- . to discard
```

3. **Remove duplicate practice trees:**
```bash
# Archive, don't delete yet (keep for analysis in fix 16)
cd ~/practices
[ -d "humanaios.archive.20260911-112252" ] && \
  mv humanaios.archive.20260911-112252 _archive/

# Remove second/third clones (keep one per repo)
rm -rf website/operations-repo
rm -rf empirica-outreach/acat/  # remove this clone
```

4. **Clean github/empirica-practice-mesh:**
```bash
cd ~/github/empirica-practice-mesh
git status  # see 1.8 GB untracked
echo "node_modules/" >> .gitignore
# Either: rm -rf untracked copies, or git clean -fdx
```

**Verify:**
```bash
empirica doctor                              # 0 warn
git status --porcelain  # in every ~/practices/*: empty
du -sh ~/practices ~/github/empirica-practice-mesh
# Both should be "normal" size (50 MB, not 2 GB)
```

**Commit:** `chore: housekeeping — reinstall MCP, commit uncommitted, remove duplicates`

**Time:** 1 session.

---

## Wave 1 (Measurement Setup)

### Fix 07: Fix Evaluator Seat Identity

**What's broken:** `.breadcrumbs.yaml` in the evaluator directory carries `ai_id: empirica-outreach` (wrong). You also have this in 4 sibling practices (resource-miner found it).

**Scope:** Your calibration belongs to YOU, not outreach. The 2,999 grounded observations in your breadcrumbs are yours.

**What to do:**

1. Regenerate YOUR calibration:
```bash
empirica calibration-report --ai-id empirica-foundation-evaluator --output json
# This reads from YOUR sessions.db, not outreach's
# If the CLI has no regenerate, delete the grounded_calibration block in
# .breadcrumbs.yaml and let the next POSTFLIGHT rebuild it
```

2. Register YOUR seat:
```bash
empirica project-register . --reconcile
# Carly approves if prompted
```

3. Fix sibling practices with the same bug:
```bash
# Check all practices
for d in ~/practices/*/; do
  echo "$d:"
  grep -m1 'ai_id:' "$d/.breadcrumbs.yaml" 2>/dev/null || echo "  (no breadcrumbs)"
  grep -m1 '^ai_id:' "$d/.empirica/project.yaml" 2>/dev/null
done

# For each mismatch: regenerate or edit back to correct ai_id
```

**Verify:**
```bash
grep -c "ai_id: empirica-foundation-evaluator" .breadcrumbs.yaml  # >= 3
grep "ai_id: empirica-outreach" .breadcrumbs.yaml  # 0
empirica practice-context --ai-id empirica-foundation-evaluator --output json | jq .ai_id_mesh
# expect: empirica-foundation.carly.empirica-foundation-evaluator
```

**Time:** 1 session.

---

### Fix 10: Retrieval-First Session Ritual (Blocking Gates)

**What's needed:** Session hook that blocks you from closing on zero learning.

**Current state:** 1,973 findings logged, 20 ever retrieved. 680 decisions, none with outcomes. Half of POSTFLIGHTs have empty reasoning. The retrieval/closure discipline is broken.

**What to do:**

1. **Session-init hook enrichment** (`~/.claude/plugins/local/empirica/hooks/session-init.py`):
   - After bootstrap, inject a "STATE" block: 5 oldest open unknowns, 3 most recent decisions with no outcome, last grounded divergence, inbox result (cortex_inbox_poll)
   - Cap at 60 lines. Move the constitution pointer below it.

2. **Session-end hook with blocking gate** (`session-end-postflight.py`):
   - Before auto_postflight, query the session's artifacts
   - If the session logged zero of {unknown resolved, decision outcome, finding with edge to prior session}:
     ```
     Exit code 2: "Close one loop before closing the session: resolve an unknown, 
     record a decision outcome, or link a finding."
     ```
   - Block empty reasoning: < 120 chars → exit code 2 + message
   - Fold the acat-score assess into auto_postflight when CLI is on PATH (no system install, no root, fallback silently on timeout)

3. **Integrate acat-score measurement** (optional, if available):
```bash
# Patch into auto_postflight
if command -v acat-score &>/dev/null; then
  acat_grounding=$(acat-score assess --session-id <sid> 2>/dev/null)
  merge acat_grounding into postflight payload
else
  # silent fallback
fi
```

**Verify:**
```bash
# Run three test sessions
# Check sessions.db: unknown resolution count increases
# Verify: no POSTFLIGHT with empty reasoning
# Verify: at least one finding per session has an edge to a prior artifact
```

**Time:** 1 session.

---

## Wave 2 (Calibration Work)

### Fix 11: Graph Closure Sprint

**What's needed:** Resolve 300 unknowns (oldest first). Make every decision outcome-bearing. Verify assumptions.

**Scope:** 25 per session, oldest first. Three verbs only:
- **Resolve** (evidence exists)
- **Retract** (was never real unknown)
- **Keep** (with named next action)

**What to do:**

1. Generate worklist per session:
```bash
empirica unknown-list --output json | jq 'sort_by(.created_at) | .[0:25]' > unknowns_batch_1.json
```

2. Batch-close:
```bash
empirica resolve-artifacts - << 'EOF'
[
  {
    "artifact_id": "<unknown_id>",
    "action": "resolve",
    "resolution_evidence_id": "<finding_id>"
  },
  ...
]
EOF
```

3. **Repeat 3 sessions** (25 unknowns per session, 75 total across three sittings)

4. **Same for decisions:** add outcome or mark stale
```bash
empirica decision-list --output json | jq 'sort_by(.created_at) | .[0:15]'
# Add outcome or tag stale
```

5. **Same for assumptions:** verify, falsify, or drop

**Verify:**
```bash
empirica unknown-list --output json | wc -l  # drop from 300 to 225
empirica decision-list --output json | jq '[.[] | select(.outcome != null)] | length'  # rise above 50%
```

**Time:** 3 sessions, spread over time (one per sitting).

---

## Coordination Role (Mesh)

You also coordinate upstream work with David. This doesn't require execution; it requires **preparation and proposal**:

### Fix 09: Listener Crash Loop (David's Upstream Work)

**Your role:** Gather evidence, prepare proposal, send via mesh-support.

- Listener logs show 21 restarts/day (7,000 across 13 logs)
- Probe target: `cortex.getempirica.com/v1/users/me/roster` returns 502, DNS failures, timeouts
- Request: upstream fix the probe target or raise the fail threshold from 240s to 1800s

**When to send:** After you've collected the logs and verified the pattern. Send via:
```bash
empirica collab --target empirica-mesh-support \
  --title "Evidence: Listener crash loop (fix 09) — ready for David proposal" \
  --summary "[evidence of 21 restarts/day, logs, requested action]"
```

### Fix 12: Readiness Gate (David's Upstream Work)

**Your role:** Document the issue, prepare proposal.

- Gate blocks honest uncertainty (+0.25): `max_uncertainty 0.35` fails, should be >= 0.60
- Recommend: local thresholds + upstream proposal to compare against grounded correction

**When to send:** After fix 10 creates examples of blocked sessions. Send evidence to David via mesh-support.

### Fix 26: Upstream Defects Report (Final)

**Your role:** After 09 and 12 are complete, send one final message to David summarizing all upstream issues:
1. Listener probe target (fix 09)
2. Readiness gate semantics (fix 12)
3. Identity leak in breadcrumbs (fix 07)
4. empirica loop list failing

---

## Execution Checklist

**Wave 0:**
- [ ] Fix 08: Stale transaction closed (10 min)
- [ ] Fix 13: Housekeeping complete (1 session)

**Wave 1:**
- [ ] Fix 07: Evaluator identity correct across practices (1 session)
- [ ] Fix 10: Session ritual hooks deployed + blocking gates active (1 session)
- [ ] Prepare evidence for fixes 09, 12 (collect logs, document)

**Wave 2:**
- [ ] Fix 11: Graph closure sprint (unknowns 300 → 225, decisions gain outcomes) — 3 sessions spread

**Coordination:**
- [ ] Send David proposal (fix 09 + 12 evidence) via empirica-mesh-support
- [ ] Send final upstream defects report (fix 26)

## If You Get Stuck

Escalate to mesh-support immediately:
```bash
empirica collab --target empirica-mesh-support \
  --title "Blocker: [fix] [symptom]" \
  --summary "[what you tried, where broke]"
```

---

**Next:** Wait for SER proposal. Execute Wave 0 and 1 immediately (no blockers). Prepare coordination evidence. Wave 2 (closure sprint) spreads over 3+ sessions.
