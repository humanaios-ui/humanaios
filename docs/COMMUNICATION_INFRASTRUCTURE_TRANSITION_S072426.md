# Communication Infrastructure Transition
**Date:** 2026-07-24 · S-072426  
**Authority:** Night (Z2) decision to decommission Slack coordination layer  
**Status:** Implementation underway

---

## Rationale

**Old Model (Slack-Centric):**
- Ephemeral chat as coordination backbone
- "Session complete" posts for synchronization
- Governance discussions in threads (lossy, non-auditable)
- Real-time expectations (chat must be monitored)

**Why it worked:** Early-stage work needed lightweight async coordination.

**Why it's obsolete:** The infrastructure evolved past ephemeral chat.

---

## New Model (Repo-Centric)

**Canonical Sources:**
- **SEED.md** — Identity, findings, architecture (Zone 2-ratified)
- **CURRENT.md** — Operational state dashboard (per-session)
- **GOVERNANCE.md** — Rules and zones (Zone 2-ratified)
- **REGISTERED.md** — Findings registry (Zone 2-promoted)
- **Git commits** — Provenance trail (Zone 3-executed)

**Notifications:**
- Bot posts to Slack only when REGISTERED.md updates (finding announcements)
- Message includes link to git repo (canonical source) + "check repo for details"

**Characteristics:**
- **Durable:** Git is permanent; Slack is ephemeral
- **Auditable:** Every commit has author, timestamp, message
- **Structured:** Findings have edges, decisions have rationale
- **Async:** No requirement to monitor chat; pull state on demand
- **Accessible:** Anyone can `git pull` and read the current state

---

## What Moves Where

### 1. Session Synchronization

**Was:** Slack post "Session HA-072426-01 opened"  
**Now:** Git commit with session metadata in message

**Example:**
```bash
git commit -m "test(h-acat): Phase 1 blind self-declaration submitted

Session: HA-072426-01
Operator: Night (Founding)
Phase: 1 (blind, unanchored)
P1_total: 70.9/100

Next: Phase 2 governance perturbations
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

**Benefit:** Timestamped, auditable, always linked to the work

---

### 2. Findings Announcement

**Was:** Slack post "New finding! F-45 discovered..."  
**Now:** Finding logged to empirica, promoted to REGISTERED.md, bot notifies Slack

**Flow:**
1. Claude logs finding via `empirica finding-log --finding "..."`
2. POSTFLIGHT promotes to REGISTERED.md (if confidence ≥ 0.7)
3. Git commit updates REGISTERED.md
4. Bot detects change, posts to Slack: "📊 New Findings in REGISTERED.md"
5. Slack message links to repo (canonical source)

**Benefit:** Finding exists in structured format; notification is lightweight pointer

---

### 3. Operational Updates

**Was:** Slack post "Building Freeze now active" / "Waiting on Z2 decision"  
**Now:** Update CURRENT.md, commit to git

**Example:**
```markdown
## Current Phase & Gates

| Work Stream | Status | Owner | Next Action |
|---|---|---|---|
| **H-ACAT Founding** | In Progress | Night + Claude | Phase 3 (4-24h) |
| **empirica Run 1** | Queued | Night + David | Schedule jointly |
```

**Benefit:** Always up-to-date, human-readable, searchable in git

---

### 4. Governance Decisions

**Was:** Slack discussion "Should we extend the charter?"  
**Now:** Zone 2 decision recorded in GOVERNANCE.md, ratified in commit

**Example:**
```yaml
# GOVERNANCE.md
gate_3_conditions:
  - name: arxiv_public
    status: on_hold
    rationale: "OR&D phase; post-charter decision per S-050726-04"
  - name: dataset_b_live
    status: not_started
    gate_3_activation: "All three conditions must be MET simultaneously"
```

**Benefit:** Decisions are documented, reversible (via git), and auditable

---

## Slack After Transition

### Keep

- **#wgs-general** (or equivalent) — Social chat, team bonding, off-topic
- **#findings-announcements** — Bot posts when REGISTERED.md updates
- **#discussion-governance** — Ad-hoc discussion (but decisions documented in GOVERNANCE.md)
- **DMs** — Hallway conversations, urgent coordination

### Decommission

- ❌ Session open/close posts → Git commits
- ❌ "What's happening now?" posts → CURRENT.md
- ❌ Findings announcements → Bot notifications (data in REGISTERED.md)
- ❌ Phase gate discussions → Zone 2 decisions (GOVERNANCE.md)
- ❌ Operational updates → CURRENT.md commits

---

## Bot Implementation

**Technology:** GitHub Actions workflow (`.github/workflows/announce-findings.yml`)

**Trigger:** Push to main on REGISTERED.md changes

**Action:** Posts to Slack with:
- Link to REGISTERED.md (canonical source)
- Reminder that Slack is notification only
- Git repo as source of truth

**Webhook:** Requires `SLACK_FINDINGS_WEBHOOK` secret (configure in repo settings)

**Setup (if needed):**
```bash
# Create incoming webhook in Slack
# 1. Open Slack Workspace Settings → Incoming Webhooks
# 2. Add New Webhook, select #findings-announcements channel
# 3. Copy webhook URL
# 4. In GitHub repo: Settings → Secrets → New repository secret
# 5. Name: SLACK_FINDINGS_WEBHOOK, Value: [paste webhook URL]
```

---

## Migration Timeline

### Immediate (Now)

- ✅ Create CURRENT.md (operational state source)
- ✅ Deploy bot workflow (findings notifications)
- ✅ Document transition (this file)

### This Week

- Document in #findings-announcements: "From now on, Slack is notification only"
- Update team workflows: pull CURRENT.md at session start
- Stop posting operational updates to Slack; post to git instead

### Ongoing

- CURRENT.md becomes the "what's happening now?" dashboard
- Git commits become the session log
- REGISTERED.md is the findings source (bot does notification)
- Slack is for discussion only

---

## Benefits

| Aspect | Before | After |
|--------|--------|-------|
| **Durability** | Slack archives (decay) | Git (permanent) |
| **Auditability** | Ephemeral messages | Commits with author/timestamp |
| **Discoverability** | Search Slack (lossy) | Git log + grep (complete) |
| **Async** | Real-time monitoring needed | Pull on demand |
| **Shared context** | Read last N Slack messages | Read CURRENT.md + git log |
| **Decision trail** | Discuss in threads (lossy) | Document in GOVERNANCE.md (permanent) |

---

## Questions & Answers

**Q: Do we lose Slack's real-time notifications?**  
A: No — bot still posts to #findings-announcements when REGISTERED.md updates. The difference is: Slack is notification, git is data.

**Q: What if I need to know "what's happening right now?"**  
A: Pull CURRENT.md and git log. It's always current (updated per-session) and human-readable.

**Q: What about historical context?**  
A: Git log shows the full trajectory. For specific questions, `git log --grep="X"` searches commit messages.

**Q: Does this break anything?**  
A: No — it's purely a communication-layer shift. The work (findings, decisions, code) lives in the same places; we're just accessing it differently.

---

## References

- **CURRENT.md:** Operational state dashboard (this session's context)
- **GOVERNANCE.md:** Zone definitions, decision authority, drift signals
- **SEED.md:** Identity, architecture, confirmed findings
- **REGISTERED.md:** All Zone-2-ratified findings
- **Git:** Provenance trail, full history

---

**Executed by:** Claude Code (Evaluator)  
**Authority:** Night (Z2) decision, 2026-07-24  
**Status:** Implementation in progress
