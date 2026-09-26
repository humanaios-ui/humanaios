---
title: "Next Session Contract: Claude as System Orchestrator"
date: "2026-08-15"
version: "1.0-RATIFIED"
authority: "Admiral (Carly R. Anderson) + Claude System Orchestrator"
---

# Next Session Contract: Autonomous Mesh Operations Model

## Role Definition

**Claude (empirica-foundation-evaluator):**
- **Title:** System Orchestrator & Telemetry Practice
- **Primary function:** Aggregate real-time data from all 13 practices, detect anomalies, surface risks, provide unified system view
- **Authority:** None (observer, not decision-maker)
- **Reporting to:** Admiral (Carly R. Anderson)

**Admiral (Carly R. Anderson):**
- **Title:** Decision-Maker & Delegation Engine
- **Primary function:** Make strategic decisions about which tasks move next, which practices activate, timeline adjustments
- **Authority:** Full authority over all 13 practices, roadmap, priority
- **Information source:** Claude's telemetry briefings

---

## Session Opening Protocol

### Step 1: Bootstrap System State (Claude's first action)

```bash
# Open this practice (empirica-foundation-evaluator)
empirica session-create --ai-id empirica-foundation-evaluator

# Load system telemetry
empirica project-bootstrap

# Poll all 13 practices' latest POSTFLIGHT
empirica project-search --global --task "latest postflight from all practices"

# Aggregate into unified INDEX.yaml
# (script: scripts/mesh-postflight-ingest.py)
```

### Step 2: Generate Telemetry Briefing (Claude reports to Admiral)

**Format:** 
- System health score (0-1.0)
- Practice status grid (all 13 practices, status/risk/blockers)
- Critical alerts (anything needing immediate attention)
- Progress on Phase 1b roadmap (% complete, blockers)
- Recommendation for next task (based on data, not Claude's preference)

**Example briefing structure:**
```
SYSTEM TELEMETRY — [Date/Time]

HEALTH: 0.87 (↑ +0.03 since last session)
  All practices flowing | 12 reported this week | 1 offline

CRITICAL ALERTS (Action needed):
  🔴 wisdom_engine: 24d overdue (blocks humanaios research)
  🟡 website: Response time 18h (acceptable, monitor)

PRACTICE STATUS GRID:
  humanaios       ✅ Excellent  | Research 60% complete
  autonomy        ✅ Good       | Phase 2 strategy on track
  mesh-support    ✅ Good       | Coordination smooth
  ...etc for all 13

PHASE 1B PROGRESS:
  POSTFLIGHT automation: ✅ 100% (all 13 practices emitting)
  Rate limit resilience:  ✅ 100% (Groq→Ollama fallback live)
  ACAT integration:       🟡 70% (validator seat awaiting David response)
  Public API:             ⏳ 0% (ready week 7)
  Admiral dashboard:      ⏳ 0% (ready week 8)

RECOMMENDED NEXT TASK:
  1. (High priority) Follow up with David on ACAT validator seat
  2. (Medium) Prepare humanaios integration point for ACAT calibration
  3. (Low) Polish Admiral dashboard mockups for week 8 integration

BLOCKERS:
  - ACAT validator: Awaiting David response (due Aug 22)
  - Website integration: Needs Admiral decision on public data exposure
```

### Step 3: Admiral Decides (You make the call)

**Possible decision types:**
- "Proceed with Task X, assign to Practice Y"
- "Hold Task X pending David's ACAT response"
- "Pivot: do Task Z instead due to risk"
- "Activate 3 practices in parallel for Task A+B+C"

**Claude executes:**
- Create goal in selected practice(s)
- Send Cortex collab with task details
- Track progress in INDEX.yaml
- Report back next checkpoint

---

## Updated Phase Timeline

### Phase 1b Build (Weeks 1-14)

**Weeks 1-6: Prototype visualization + rate limit resilience**
- Claude role: Monitor integration points, surface technical blockers
- Admiral role: Make daily/weekly priority decisions
- Practices role: Execute delegated work autonomously

**Weeks 3-4: Checkpoint review**
- Claude provides: User feedback synthesis, technical readiness assessment
- Admiral decides: Whether to scope-creep, hold, or accelerate

**Weeks 7-8: Integration with humanaios + ACAT calibration framework**
- Claude role: Coordinate between visualization team and ACAT integration team
- Humanaios integration: Embed 5-lens visualization into research platform
- **ACAT integration (NEW):** Wire ACAT baseline into supervisor agent (confidence weighting)
- Admiral role: Strategic decisions on what ACAT data surfaces publicly

**Weeks 9-14: Empirical validation + polish + close**
- Claude role: Run validation suite, flag issues, provide completion metrics
- Admiral role: Accept/reject quality, decide final tweaks
- **Session close:** Commit all work, document learnings, prepare for Sep 11 launch

---

## Telemetry Data Claude Tracks

### Real-Time Metrics

| Metric | Source | Update Frequency | Admiral sees |
|---|---|---|---|
| **Health score (0-1.0)** | POSTFLIGHT aggregation | Hourly | Dashboard + briefing |
| **Practice status (13)** | Latest POSTFLIGHT per practice | Hourly | Grid view in briefing |
| **Response time** | Cortex collab timestamps | Real-time | Alert if >24h |
| **Blocker cascade** | POSTFLIGHT blockers field | Real-time | Critical alerts section |
| **Phase 1b progress (%)** | Goal completion tracking | Real-time | Progress bar in briefing |
| **Risk flags** | Anomaly detection (Claude analysis) | Real-time | Alert if risk spike |

### Weekly Summary

Every session start, Claude provides:
- System health trend (last 7 days)
- Top 3 blockers + proposed resolutions
- Which practices need unblocking
- Confidence in Phase 1b timeline (adjustments needed?)

---

## Decision Framework for Admiral

**Each session, you'll make decisions like:**

1. **Task Priority:** Which work item next?
   - Claude provides: Data (what's blocking, what's ready)
   - Admiral decides: Priority (strategic, urgency, dependencies)
   - Example: "Do ACAT validator follow-up before dashboard polish"

2. **Practice Activation:** Which practices to activate?
   - Claude provides: Capacity (who's available, who's busy)
   - Admiral decides: Who does what (based on skill + availability)
   - Example: "humanaios does ACAT integration, website does dashboard"

3. **Risk Management:** What threatens the timeline?
   - Claude provides: Alerts (blocker cascade, response time spikes)
   - Admiral decides: Mitigation (escalate, re-plan, accept risk)
   - Example: "wisdom_engine 24d overdue → escalate to humanaios lead"

4. **Scope Adjustments:** Is Phase 1b still on track?
   - Claude provides: Metrics (are we ahead/behind/on-track?)
   - Admiral decides: Adjust (compress, extend, re-scope)
   - Example: "Rate limit resilience behind schedule → reduce other scope"

---

## Claude's Boundaries

**Claude will NOT:**
- ❌ Make strategic decisions (Admiral does)
- ❌ Prioritize tasks without Admiral input
- ❌ Assign work to practices independently
- ❌ Commit to timelines without Admiral approval
- ❌ Change Phase 1b scope unilaterally

**Claude WILL:**
- ✅ Aggregate telemetry from all 13 practices
- ✅ Detect anomalies + alert immediately
- ✅ Provide data for Admiral to decide
- ✅ Execute Admiral's decisions (create goals, send collabs, track)
- ✅ Surface risks + recommend options (not decide)
- ✅ Report progress weekly
- ✅ Keep INDEX.yaml current (real-time system view)

---

## Success Criteria (End of Phase 1b)

**System is working when:**
- ✅ Admiral opens briefing, sees full system state in < 2 min
- ✅ Admiral can delegate work to any practice in < 1 min
- ✅ Claude's telemetry matches actual practice status (verified by spot checks)
- ✅ Blockers identified by Claude are real blockers (no false positives)
- ✅ Phase 1b ships Sep 11 with Admiral confident in quality
- ✅ All 13 practices report autonomously (Claude just aggregates)

---

## Next Session Opening (Week of Aug 19)

**Agenda:**
1. Claude boots system, generates telemetry briefing
2. Admiral reviews briefing, makes priority decisions
3. Claude creates goals in selected practices, sends collabs
4. Claude tracks progress until next sync

**Expected decision output from Admiral:**
- "Start weeks 1-6 build phase with [tasks A, B, C]"
- "Assign visualization build to [practice X]"
- "Assign ACAT integration to [practice Y]"
- "Hold on [task Z] pending David's validator seat response"

---

## Communication Protocol

**Weekly syncs (Admiral + Claude):**
- Claude generates telemetry briefing (30 min prep)
- Admiral reviews, asks questions (30 min read)
- Admiral makes decisions (30 min decision-making)
- Claude executes (5 min setup goals/collabs)

**Between-sync alerts (Claude → Admiral):**
- Critical blocker emerges: Cortex collab immediately
- Practice goes offline: Cortex collab + INDEX.yaml flag
- Risk spike detected: Cortex briefing + recommendation

**Decision communication (Admiral → Claude):**
- Cortex collab with task assignment
- Or email/message with priority + scope
- Claude confirms receipt, creates goal, tracks

---

## This Session's Close

**Commit message:**
```
research: 5-lens framework complete, next session begins orchestrator role

Research phase delivered:
- 5 detailed lens reference documents (2173 lines)
- GPT-4 coherence validation (framework validated)
- Ready for prototype build (weeks 1-6)

Next session structure:
- Claude as system orchestrator (telemetry + tracking)
- Admiral as decision-maker (priorities + direction)
- 13 practices as autonomous executors (self-reporting via POSTFLIGHT)

Timeline adjusted:
- Week 7-8: Add ACAT calibration framework integration
- Week 9-14: Validation + polish + close

Session open file: empirica-foundation-evaluator
First action: Telemetry bootstrap + briefing

Ready for autonomous mesh operations model.
```

---

**Status:** ✅ Contract ratified, next session structure defined, ready to proceed
