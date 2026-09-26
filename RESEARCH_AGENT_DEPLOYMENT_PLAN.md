# Research Agent Deployment Plan

**Status:** Ready for Pilot Deployment  
**Target Timeline:** 2026-09-17 (24h pilot) → 2026-09-18 (staggered fleet rollout)  
**Success Criteria:** Research agents polling cleanly, findings routed to Cortex, patterns detected and published

---

## Components Being Deployed

### Agent Extensions
- `ResearchHandler` — Routes research_task proposals from evaluator
- `PatternDetector` — Scans local findings for cross-practice signals
- Enhanced `StatusReporter` — Publishes research findings as shared artifacts

### Standalone Practice
- `empirica-research-coordinator` — Aggregates findings from 15 practices, detects patterns, routes research tasks

### Capabilities
1. **Research Proposal Polling:** Evaluator inbox polling every 5min
2. **Finding Aggregation:** Collects findings from all 15 practices via Cortex
3. **Pattern Detection:** Cross-practice pattern identification (high-impact, temporal clustering, etc.)
4. **Research Routing:** Dispatches to empirica-resource-miner, empirica-temporal-oracle, empirica-analytics, opportunity-aggregator, local-machine-optimizer
5. **Artifact Publishing:** Logs patterns + research suggestions as shared Cortex artifacts

---

## Deployment Steps

### Phase 0: Pre-Flight Checklist (TODAY)
```bash
# Verify all files present
ls -1 agent/research_coordinator.py agent/autonomous_agent.py agent/status_reporter.py

# Syntax check (already passed)
python3 -m py_compile agent/research_coordinator.py agent/autonomous_agent.py agent/status_reporter.py

# Verify commits
git log --oneline | head -3
# Should show: 411c3d0 (Phase 1 fixes), 0c7a100 (research handlers), etc.

# Verify research practices exist and can be addressed
empirica practice-context --ai-id empirica-resource-miner --output json | jq .ai_id_mesh
empirica practice-context --ai-id empirica-temporal-oracle --output json | jq .ai_id_mesh
```

### Phase 1: Deploy to Pilot (empirica-autonomy)
```bash
# Already running Phase 1 agents; add research handlers
cd ~/practices/empirica-autonomy/.empirica/agents

# Update autonomous_agent.py with research handlers
cp ~/practices/empirica-foundation-evaluator/agent/autonomous_agent.py ./
cp ~/practices/empirica-foundation-evaluator/agent/status_reporter.py ./

# Restart agent with research handlers active
./start_autonomous_agent.sh empirica-foundation.carly.empirica-autonomy 30

# Monitor first hour
tail -f /tmp/autonomous-agents/empirica-autonomy.log | grep -E "ResearchHandler|PatternDetector|research"

# Expected output:
# [2026-09-17 XX:XX:XX] agent-empirica-autonomy INFO: Received research task: ...
# [2026-09-17 XX:XX:XX] detector-empirica-autonomy INFO: Scanning local findings for patterns
```

### Phase 2: Deploy ResearchCoordinator (Dedicated Practice)
```bash
# Create empirica-research-coordinator practice
mkdir -p ~/practices/empirica-research-coordinator/.empirica/agents

# Create project.yaml
cat > ~/practices/empirica-research-coordinator/.empirica/project.yaml << 'EOF'
ai_id: empirica-foundation.carly.empirica-research-coordinator
project_type: coordinator
description: "Research aggregation + pattern detection for 15-practice fleet"
EOF

# Copy research coordinator code
cp ~/practices/empirica-foundation-evaluator/agent/research_coordinator.py \
   ~/practices/empirica-research-coordinator/.empirica/agents/research_coordinator.py

# Start coordinator
cd ~/practices/empirica-research-coordinator/.empirica/agents
python3 research_coordinator.py empirica-foundation.carly.empirica-research-coordinator 300

# Monitor logs
tail -f /tmp/research-coordinator.log
```

### Phase 3: Deploy to Pilot Practices (empirica-mesh-support, empirica-outreach)
```bash
# Same as Phase 1, stagger by 30 minutes

# empirica-mesh-support
cd ~/practices/empirica-mesh-support/.empirica/agents
cp ~/practices/empirica-foundation-evaluator/agent/autonomous_agent.py ./
cp ~/practices/empirica-foundation-evaluator/agent/status_reporter.py ./
./start_autonomous_agent.sh empirica-foundation.carly.empirica-mesh-support 30

# empirica-outreach (after 30min)
cd ~/practices/empirica-outreach/.empirica/agents
cp ~/practices/empirica-foundation-evaluator/agent/autonomous_agent.py ./
cp ~/practices/empirica-foundation-evaluator/agent/status_reporter.py ./
./start_autonomous_agent.sh empirica-foundation.carly.empirica-outreach 30
```

### Phase 4: Monitor Pilot (4 hours)
```bash
# Watch for:
# 1. Agent polling: "Handling N proposals" appears regularly
# 2. Research handler: ResearchHandler activates when research_task received
# 3. Pattern detection: PatternDetector scans + publishes findings
# 4. Cortex integration: Findings appear in artifact browser

# Check fleet health
empirica project-search --task "Agent health" --scope project

# Expected: One finding per agent per hour showing success rate >= 90%
```

### Phase 5: Go/No-Go Decision
**GO criteria (all must pass):**
- ✅ All 3 pilot agents running for 4h straight (0 crashes)
- ✅ Poll cycles: >= 480 (one per 30s × 14400s)
- ✅ Success rate: >= 90% (proposal handling failures < 10%)
- ✅ Research findings: >= 5 findings published per practice
- ✅ Cortex logging: Zero dropped completion records

**NO-GO triggers:**
- ❌ Agent crash (process dies, doesn't restart)
- ❌ Poll failure rate > 10% (timeout/connection errors)
- ❌ Zero research findings published (Cortex integration broken)
- ❌ StatusReporter failures (completion notifications not sent)

---

## Staggered Fleet Rollout (If Pilot Passes)

| Time | Practice | Status |
|------|----------|--------|
| T+0h | empirica-autonomy | 🚀 Pilot start |
| T+30m | empirica-mesh-support | Deploy |
| T+1h | empirica-outreach | Deploy |
| T+4h | **GO/NO-GO Decision** | ⏸️ Pause for review |
| T+4h:30m | empirica-humanaios | Deploy (if GO) |
| T+5h:30m | website | Deploy |
| T+6h:30m | empirica-resource-miner | Deploy |
| T+7h:30m | empirica-temporal-oracle | Deploy |
| T+8h:30m | empirica-analytics | Deploy |
| T+9h:30m | opportunity-aggregator | Deploy |
| T+10h:30m | local-machine-optimizer | Deploy |
| T+11h:30m | empirica-mesh-support-2 | Deploy (if multi-instance) |
| T+12h:30m | **Full Fleet Live** | ✅ All 15 running |

**Total deployment time:** 12.5 hours (staggered 1h between each after pilot)

---

## Monitoring Dashboard

### Real-Time Metrics
```bash
# Fleet health summary (run hourly during rollout)
empirica project-search --task "Agent fleet health" --scope project

# Expected output: Finding with breakdown
# - Agents active: 15
# - Total proposals handled: 847
# - Success rate: 94%
# - Avg proposals per agent: 56.5
# - Last reported: 2026-09-17 XX:XX UTC
```

### Per-Agent Status
```bash
# Check individual agent health
empirica project-search --task "Agent health: empirica-autonomy" --scope project
```

### Research Findings Published
```bash
# Monitor pattern detection
empirica project-search --task "Research Pattern" --scope project --global

# Expected: One finding per pattern detected per practice cycle
# Example: "Cross-Practice Pattern: High-impact finding (>3 practices)"
```

---

## Health Monitoring Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Poll Success Rate | < 95% | < 80% |
| Proposal Handling Errors | > 5% | > 15% |
| Research Findings/Cycle | < 2 | < 1 |
| Cortex Logging Failures | > 1/hour | > 5/hour |
| Avg Response Time | > 5s | > 10s |
| Memory Usage | > 500MB | > 1GB |

---

## Escalation & Recovery

### Poll Timeout
- **Symptom:** "Poll timeout" in logs
- **Recovery:** Automatic retry with exponential backoff (2s → 4s → 8s)
- **Escalation:** After 5 consecutive timeouts, agent shuts down + logs `unknown-log`

### Handler Crash
- **Symptom:** Exception in handler during proposal processing
- **Recovery:** Catch exception, return failure result, reply to proposal
- **Escalation:** Log `mistake-log` if pattern emerges (same handler failing repeatedly)

### Cortex Logging Failure
- **Symptom:** StatusReporter.report_research_finding() fails
- **Recovery:** Retry with exponential backoff
- **Escalation:** Alert if > 5 consecutive failures

### Agent Process Death
- **Symptom:** Process exits or log stops updating
- **Recovery:** Manual restart via deployment script
- **Escalation:** Log `unknown-log` + page on-call if not restarted within 5min

---

## Rollback Plan

**Trigger:** Fleet success rate drops below 80% OR critical blocker found

```bash
# Step 1: Stop all agents
killall -f autonomous_agent.py
killall -f research_coordinator.py

# Step 2: Log failure reason
empirica finding-log --finding "Research agent fleet rollback" \
  --description "Reason for rollback: [...]" \
  --impact 0.9

# Step 3: Restore previous agent code (Phase 1 only, no research handlers)
git checkout HEAD~2 agent/autonomous_agent.py
git checkout HEAD~2 agent/status_reporter.py

# Step 4: Restart agents on pilot only
./start_autonomous_agent.sh empirica-foundation.carly.empirica-autonomy 30

# Step 5: Wait for data recovery
# All findings published to Cortex are preserved (durable)
# Recent proposals still in mailbox will be reprocessed
```

---

## Failure Modes & Prevention

| Failure Mode | Probability | Prevention |
|---|---|---|
| Research proposal parsing error | Low | Schema validation in ResearchRouter |
| Cortex API timeout | Medium | Exponential backoff, timeout=30s |
| Circular routing (A→B→A) | Low | Prevent via target_claudes check |
| Pattern detector memory leak | Low | Scan results cleared after publish |
| Mailbox poll race conditions | Low | Atomic proposal lock via empirica CLI |

---

## Success Looks Like

After 24h (pilot + staggered rollout), empirica artifact log shows:

```
Finding: Research Agent Fleet Status — 94% Success Rate
  - Agents deployed: 15
  - Agents healthy: 15
  - Total proposals handled: 12,847
  - Total findings aggregated: 387
  - Patterns detected: 23
  - Avg handling time: 2.3s per proposal
  - Last reported: 2026-09-17 23:15 UTC

Finding: Research Pattern: High-Impact Findings (5 practices affected)
  - Pattern detected across autonomy, outreach, mesh-support, humanaios, website
  - Frequency: 5 findings
  - Severity: 0.8
  - Recommendation: Schedule cross-practice research on [topic]

Decision: Research agents deployed to all 15 practices
  - Pilot phase (3 practices, 4h): ✓ PASSED
  - Fleet phase (15 practices, 12h): ✓ PASSED
  - All success criteria met
  - Fleet ready for sustained operation

... (one per agent per hour showing success rates)
```

---

## Questions & Support

- **Agent not starting?** Check logs: `/tmp/autonomous-agents/<practice>.log` or `/tmp/research-coordinator.log`
- **Proposals not being routed?** Verify mailbox: `empirica mailbox poll --ai-id <id> --status accepted`
- **Research findings not published?** Test Cortex: `empirica finding-log --finding "test" --visibility shared`
- **Unclear fleet status?** Query artifacts: `empirica project-search --task "Agent fleet health"`
- **Need to pause deployment?** Kill agents: `killall -f autonomous_agent.py`; restart at any point in staggered schedule

---

## Appendix: Script Templates

### deploy-pilot.sh
```bash
#!/bin/bash
set -e

EVALUATOR_DIR=~/practices/empirica-foundation-evaluator
PILOT_PRACTICES=("empirica-autonomy" "empirica-mesh-support" "empirica-outreach")

for practice in "${PILOT_PRACTICES[@]}"; do
  echo "Deploying research handlers to $practice..."
  
  PRACTICE_DIR=~/practices/$practice/.empirica/agents
  mkdir -p "$PRACTICE_DIR"
  
  cp "$EVALUATOR_DIR/agent/autonomous_agent.py" "$PRACTICE_DIR/"
  cp "$EVALUATOR_DIR/agent/status_reporter.py" "$PRACTICE_DIR/"
  
  cd "$PRACTICE_DIR"
  ./start_autonomous_agent.sh "empirica-foundation.carly.$practice" 30
  
  echo "✓ $practice deployed"
  sleep 30
done

echo "✓ Pilot deployment complete"
```

---

*Deployment plan stable. Ready for Phase 1 pilot validation (2026-09-17 00:00).*
