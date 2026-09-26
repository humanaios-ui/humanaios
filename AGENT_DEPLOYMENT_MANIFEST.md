# Autonomous Practice Agent — Deployment Manifest

**Status:** Ready for Phase 1 Test Deployment  
**Target:** empirica-autonomy (2026-09-16)  
**Success Criteria:** 24h unattended autonomous operation with 0 manual interventions

---

## What's Being Deployed

### Files
- `agent/autonomous_agent.py` — Core AutonomousAgent class
- `agent/status_reporter.py` — Status reporting to Cortex
- `agent/start_autonomous_agent.sh` — Deployment script

### Capabilities
1. **Polling Loop:** Polls mailbox every 30s (configurable)
2. **Proposal Routing:** Dispatches by type (collab_brief, proposal, escalation)
3. **Task Execution:** Calls handlers; tracks execution time
4. **Status Reporting:** Logs completions + health to Cortex
5. **Error Handling:** Exponential backoff on poll failures; max 5 consecutive errors before shutdown

---

## Deployment Steps

### 1. Prepare empirica-autonomy
```bash
cd ~/practices/empirica-autonomy

# Create agent directory
mkdir -p .empirica/agents

# Copy agent files
cp ../empirica-foundation-evaluator/agent/autonomous_agent.py .empirica/agents/
cp ../empirica-foundation-evaluator/agent/status_reporter.py .empirica/agents/
cp ../empirica-foundation-evaluator/agent/start_autonomous_agent.sh .empirica/agents/
chmod +x .empirica/agents/start_autonomous_agent.sh
```

### 2. Start Agent
```bash
cd ~/practices/empirica-autonomy/.empirica/agents

# Start with 30s poll interval
./start_autonomous_agent.sh empirica-foundation.carly.empirica-autonomy 30

# Verify it's running
ps aux | grep autonomous_agent.py
```

### 3. Monitor (First Hour)
```bash
# Watch logs in real-time
tail -f /tmp/autonomous-agents/empirica-autonomy.log

# Expected output:
# [2026-09-16 XX:XX:XX] [agent-empirica-autonomy] INFO: Agent started for empirica-foundation.carly.empirica-autonomy
# [2026-09-16 XX:XX:30] [agent-empirica-autonomy] INFO: Handling N proposals
# ...
```

### 4. Verify Status Logging (After first cycle)
```bash
# Check empirica artifacts logged
empirica project-search --task "Agent health" --scope project

# Expected: Finding logged with health metrics
```

---

## Success Metrics (24h Test Window)

| Metric | Target | Pass Criteria |
|--------|--------|---------------|
| **Uptime** | 24h continuous | ≥23h (max 1h downtime allowed) |
| **Polls completed** | 2880 (30s × 86400) | ≥2880 |
| **Error recovery** | 0 unrecovered errors | All errors handled, no hard crashes |
| **Proposal handling** | Varies by activity | 100% of received proposals replied to |
| **Health reports** | 24 (1 per hour) | ≥20 health reports logged |
| **Cortex logging** | All completions recorded | 0 dropped completion records |

---

## What Success Looks Like

After 24h, empirica artifact log should show:

```
Finding: Agent health: empirica-autonomy — 95% success rate
  - Proposals handled: 847
  - Succeeded: 805
  - Failed: 42
  - Poll cycles: 2876
  - Avg proposals per cycle: 0.29

Decision: Executed: [proposal_title_1]
  Source: empirica-foundation.carly.empirica-outreach
  Outcome: task_executed
  Execution time: 2.34s

Decision: Executed: [proposal_title_2]
  Source: empirica-foundation.carly.empirica-mesh-support
  Outcome: acknowledged
  Execution time: 0.15s

... (one per proposal handled)
```

---

## Failure Modes & Recovery

### Poll Timeout
- **Symptom:** "Poll timeout" in logs
- **Recovery:** Automatic retry with exponential backoff (2s → 4s → 8s → ...)
- **Escalation:** After 5 consecutive timeouts, agent shuts down with health report

### Handler Crash
- **Symptom:** Handler raises exception
- **Recovery:** Catch exception, return ProposalResult(success=False)
- **Escalation:** Reply to proposal with "failed" status; continue to next proposal

### Mailbox Empty
- **Symptom:** No proposals in mailbox for entire cycle
- **Recovery:** Pause poll_interval seconds, continue
- **Escalation:** None; this is normal

### Agent Shutdown
- **Symptom:** Process exits or log stops updating
- **Recovery:** Restart via `./start_autonomous_agent.sh`
- **Escalation:** Log `unknown-log` with reason; notify via Cortex

---

## Rollout Plan (After Test Success)

### Phase 1: Verify on empirica-autonomy (2026-09-16 → 2026-09-17)
- Deploy to autonomy, monitor 24h
- Confirm all success metrics met

### Phase 2: Deploy to 5 practices (2026-09-17 → 2026-09-18)
- Stagger deployments 30m apart: empirica-mesh-support, empirica-outreach, humanaios, website, empirica-resource-miner
- Monitor fleet health dashboard

### Phase 3: Deploy to remaining 10 practices (2026-09-18 → 2026-09-19)
- Full rollout across all 15 practices
- Fleet success rate target: ≥90%

---

## Monitoring Dashboard (Future)

Once fleet is running, evaluator seat will have:
```
Autonomous Agent Fleet Status
├── Total agents: 15
├── Agents healthy: 15
├── Fleet success rate: 94.2%
├── Total proposals handled: 12,847
├── Avg proposals per agent: 856
└── Last reported: 2026-09-16 22:15 UTC
```

Accessible via: `empirica project-search --task "Agent fleet health"`

---

## Rollback

If agent fails all success metrics:

1. Stop all agents: `killall -f autonomous_agent.py`
2. Log failure reason: `empirica finding-log --finding "Agent deployment failed: ..."`
3. Return to manual coordination loop (existing workflow)
4. Debug root cause before retry

---

## Questions & Support

- **Agent not starting?** Check logs in `/tmp/autonomous-agents/<practice>.log`
- **Proposals not being handled?** Check mailbox status: `empirica mailbox poll --ai-id <id>`
- **Cortex logging failures?** Verify empirica CLI works: `empirica finding-log --finding "test"`
- **Fleet health unclear?** Review findings/decisions logged per practice
