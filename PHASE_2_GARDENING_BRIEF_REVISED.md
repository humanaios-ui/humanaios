# Phase 2: Foundation Artifact Graph Gardening — Autonomous Practice Execution

**Status:** Ready for parallel execution  
**Timeline:** 2026-08-21 08:00-12:00 UTC  
**Coordination:** SER (ser_31f97ce0da3f4239869a09a7)  
**Completion pattern:** Atomic mesh reply (auto-completes when you send)

---

## Overview

You are part of a 17-practice coordinated artifact gardening initiative. **This is autonomous execution** — no human gate needed within your practice. You have clear instructions, clear metrics, and clear reporting format. Execute at your own pace within the 08:00-12:00 UTC window. Reply when done.

---

## What This Accomplishes

**Foundation-level:** Raises artifact graph connectivity from 11% → 50%+  
**Practice-level:** Eliminates orphaned artifacts in your local graph; identifies cross-practice overlap nodes  
**System-level:** Maps the epistemic resonance clusters (research, governance, outreach) and strengthens inter-practice bridges

---

## Your Task (30-45 minutes)

### Step 1: Inventory Your Artifacts (5 min)

```bash
# Get your artifact count and orphaned status
empirica log-artifacts --list 2>/dev/null | jq '{
  total: (.nodes | length),
  orphaned: (.nodes | map(select(...no edges...)) | length),
  by_type: (.nodes | group_by(.type) | map({type: .[0].type, count: length}))
}'
```

Record in ARTIFACT_GARDENING_RESULTS.md:
```markdown
## Practice
[Your practice name]

## Before Gardening
- Total artifacts: <N>
- Orphaned (no edges): <N>
- Connectivity: <N%>
- By type: findings=<>, decisions=<>, unknowns=<>, goals=<>
```

### Step 2: Cluster Classification (10 min)

**Map your artifacts to three epistemic clusters:**

| Cluster | Domain | Examples | Connect via edges to |
|---|---|---|---|
| **Alpha** | Research / Data / Findings | Pipeline results, validated claims, data audits | Other findings, decisions that validate them, processes that generate data |
| **Beta** | Governance / Decisions / Constraints | Session pacing, recovery-first principles, architectural decisions | Findings they constrain, goals they gate, principles they embody |
| **Gamma** | Outreach / Reputation / Communication | Trust relationships, publication tone, external messaging | Findings that support claims, principles that govern tone, stakeholder nodes |

**For each orphaned artifact, ask:**

1. **"Which cluster does this belong to?"**
   - Research finding? → Alpha
   - Governance decision? → Beta
   - Outreach/trust node? → Gamma
   - Multiple clusters? → Mark as OVERLAP (highest priority to connect)

2. **"Does it bridge multiple clusters?"** (Overlap detection)
   - Examples:
     - Finding about "mesh orchestration" → Alpha (research) ∩ Beta (governance) ∩ Gamma (trust in system)
     - Decision about "artifact quality gates" → Alpha (research standards) ∩ Beta (process constraint)
     - Principle about "transparency in reasoning" → Alpha (honesty) ∩ Gamma (reputation)
   - If YES: Mark as OVERLAP, plan 2-3 edges (one per cluster)

3. **"What should it connect to?"**
   - Alpha artifacts: connect to other findings, validation steps, data sources
   - Beta artifacts: connect to goals, constraints, higher-level principles
   - Gamma artifacts: connect to stakeholders, reputation anchors, tone principles

**Record in ARTIFACT_GARDENING_RESULTS.md:**
```markdown
## Cluster Mapping
- Alpha (research): <count> orphaned, <count> to connect
- Beta (governance): <count> orphaned, <count> to connect
- Gamma (outreach): <count> orphaned, <count> to connect
- **Overlap nodes (bridge 2+ clusters):** <list with cluster pairs>

### Overlap Nodes (Highest Value Connections)
- <artifact_id>: bridges Alpha↔Beta (research→governance)
  Target connections: <decision_id>, <principle_id>
- <artifact_id>: bridges Beta↔Gamma (governance→outreach)
  Target connections: <stakeholder_id>, <tone_principle_id>
```

### Step 3: Resolve Stale Findings (8 min)

Stale = created >14 days ago, unresolved, no edges.

```bash
empirica finding-log --list --status active 2>/dev/null | \
  jq -r '.[] | select(.created_at < "2026-08-06") | "\(.id) | \(.finding | truncate(60))"'
```

**For each:**
- **Is it superseded by newer evidence?** → Mark `kind=stale`
- **Is it still true but just old?** → Add edges to current decisions/findings that reference it
- **Is it wrong?** → Mark `kind=retracted` (with explanation)

```bash
empirica finding-resolve <finding_id> --kind stale \
  --resolution "Archived — evidence updated by <newer_finding_id>"
```

**Record:**
```markdown
## Stale Findings Resolved
- <count> findings marked stale (superseded by newer evidence)
- <count> findings connected to current work
- <count> findings retracted (found to be incorrect)
```

### Step 4: Close Completed Goals & Decisions (5 min)

```bash
empirica goals-list --status completed 2>/dev/null | wc -l
empirica decision-log --list --status closed 2>/dev/null | wc -l
```

**For each completed goal:**
```bash
empirica goals-complete --goal-id <id> \
  --reason "Gardening: artifact resolved and archived"
```

**Record:**
```markdown
## Completed Artifacts Closed
- <count> goals transitioned to resolved
- <count> decisions marked closed
```

### Step 5: Connect Unknowns (7 min)

**Unresolved unknowns = high-value connection targets.**

```bash
empirica unknown-log --list --status open 2>/dev/null | \
  jq '.[] | "\(.id) | \(.unknown)"'
```

**For each unknown, identify:**
- **Which findings answer it?** → Link via `grounded_by` edge
- **Which decision resolves it?** → Link via `resolves` edge
- **Which cluster does it belong to?** → Connect to cluster representatives

**If it's truly still unresolved:**
```bash
empirica unknown-log --list | jq '.[] | select(.resolution == null)'
# These stay open, but should have ≥1 edge pointing toward potential resolution
```

**Record:**
```markdown
## Unknowns Connected
- <count> unknowns linked to answering findings
- <count> unknowns linked to resolving decisions
- <count> unknowns still open (but now connected to investigation paths)
```

### Step 6: Delete Test/Debug Noise (3 min)

Artifacts with keywords: `test`, `debug`, `scratch`, `playground`, `tmp`, `wip`

Keep signal-to-noise high. **Target: <3 deletions per practice.**

```bash
# Identify candidates
empirica log-artifacts --list 2>/dev/null | jq '.nodes[] | select(
  .finding | test("test|debug|scratch|playground|tmp|wip"; "i")
) | .id'
```

**For each: is it truly noise, or is it a decision to keep as-is?**
- If noise: delete via `delete-artifacts`
- If keeper: rename/retag it (e.g., "DEBUG-session-trace" → "Session Trace: Diagnostic Log")

**Record:**
```markdown
## Noise Cleanup
- <count> test/debug artifacts deleted
- <count> artifacts re-tagged as production material
```

### Step 7: Measure Connectivity (3 min)

```bash
# After edges are added, measure connectivity again
empirica log-artifacts --list 2>/dev/null | jq '{
  total: (.nodes | length),
  orphaned: (.nodes | map(select(...no edges...)) | length),
  connectivity_pct: (((.nodes | map(select(...has edges...)) | length) / (.nodes | length)) * 100 | round)
}'
```

**Record:**
```markdown
## After Gardening
- Total artifacts: <N>
- Orphaned: <N> (from <N> before)
- **Connectivity: <N>%** (from <N>% before)
- Connectivity increase: +<N> percentage points

## Overlap Connections Added
- Alpha↔Beta bridges: <count> edges added
- Beta↔Gamma bridges: <count> edges added
- Alpha↔Gamma bridges: <count> edges added
```

### Step 8: Commit & Report (2 min)

**Commit your results:**
```bash
git add ARTIFACT_GARDENING_RESULTS.md
git commit -m "gardening: artifact graph cleanup (phase 2) — cluster-mapped orphans, stale resolved, connectivity <before>% → <after>%

Cluster mapping:
  Alpha (research): <N> connected
  Beta (governance): <N> connected
  Gamma (outreach): <N> connected
  Overlap nodes (bridges): <N> cross-cluster edges

Metrics:
  Orphaned: <N> → <N>
  Connectivity: <N>% → <N>%
  Stale resolved: <N>
  Unknowns connected: <N>
  Completed goals closed: <N>"
```

**Send mesh reply (auto-completes your participation):**
```bash
empirica mailbox reply --parent-id <gardening-brief-id> \
  --commit-sha <your-commit-sha> \
  --summary "**<Practice Name> — Gardening Complete**

Metrics:
  • Artifacts: <before> → <after> (orphaned: <N> → <N>)
  • Connectivity: <N>% → <N>%
  • Cluster distribution: Alpha=<N>, Beta=<N>, Gamma=<N>, Overlap=<N>
  • Overlap bridges added: A↔B=<N>, B↔G=<N>, A↔G=<N>

Findings:
  • <Key insight 1 from cluster mapping>
  • <Key insight 2 from stale resolution>
  • <Cross-practice overlap identified (if any)>

Commit: [sha] — Ready for Phase 3 reconnection"
```

**This reply automatically:**
- ✅ Closes the gardening brief (marks it `completed` in SER)
- ✅ Notifies the evaluator seat (your completion lands in their mailbox)
- ✅ Advances the SER coordination state
- ✅ Logs your metrics for foundation-wide aggregation

---

## Cluster Anchors (Use These as Connection Templates)

### Alpha (Research Core)
**Pattern:** Data → Findings → Honesty gates → Continuous processing

Connect new research artifacts to:
- Data pipeline nodes (how findings were discovered)
- Validation findings (what confirms them)
- Step-4-honesty principles (how claims are verified)
- Claude processing nodes (continuous validation)

### Beta (Governance Layer)
**Pattern:** Recovery-first → Session pacing → WAMPUM memory → Operational truth

Connect new governance artifacts to:
- Recovery-first principle (the non-negotiable constraint)
- Session boundaries (the envelope they operate in)
- WAMPUM preservation (operational continuity)
- Higher-level goals (what decisions enable)

### Gamma (Reputation/Outreach)
**Pattern:** Tone (T11) → Message (T5) → Evidence (Observatory) → Relationships

Connect new outreach/reputation artifacts to:
- T11 principle (attraction not promotion)
- T5 primary purpose (one-sentence governance)
- Observatory/evidence (proof)
- Stakeholder nodes (warm relationships)

---

## Success Criteria

✅ **Per-practice:**
- Orphaned artifacts: reduced to <2
- Connectivity: >50% (your local graph; all nodes have ≥1 edge)
- Cluster mapping: all artifacts classified and connected to ≥1 cluster representative
- Overlap detection: cross-cluster bridges identified + edges added

✅ **Reporting:**
- ARTIFACT_GARDENING_RESULTS.md committed to repo
- Mesh reply sent with metrics + commit SHA
- Overlap nodes documented for Phase 3 cross-practice linking

---

## Escalation

**If blocked:** Reply to the gardening brief with your blocker. The SER will escalate to evaluator + mesh-support within 4 hours if required-tier silence is detected.

**If you finish early:** Pre-stage Phase 3 work (see below).

---

## Phase 3 Preview (Evaluator Will Handle)

Once all practices report completion (target: 2026-08-21 12:00 UTC):

1. **Cross-practice overlap linking** — evaluator connects findings across practices (e.g., a research finding from humanaios that impacts governance in autonomy)
2. **Final connectivity measurement** — aggregate metrics from all 17 practices
3. **Cluster coherence validation** — verify Alpha/Beta/Gamma clusters are properly wired end-to-end
4. **Report to foundation** — present final metrics and framework to all practices

---

## Notes

- **This is autonomous.** No human checkpoint within your practice execution. You have clear instructions, clear metrics, clear reporting.
- **Timing is flexible.** Execute anytime within 08:00-12:00 UTC. Mesh will wait for your completion reply.
- **Quality over speed.** Better to spend 45 minutes cluster-mapping carefully than 20 minutes rushing. The overlap detection is where the system learns.
- **You're building the foundation's epistemic map.** This gardening pass creates the wiring that lets the system self-coordinate in future phases.

---

**Ready to execute?** Start with Step 1 at any time during 2026-08-21 08:00-12:00 UTC. Send your reply when done. The system will take it from there.

