---
title: "Vision: Autonomous Mesh Operations & Universal Control Plane"
subtitle: "From manual orchestration to Admiral dashboard: Practice delegation at scale"
date: "2026-08-15"
version: "1.0-VISION"
status: "STRATEGIC DIRECTION"
authority: "Admiral (Carly R. Anderson) with Claude Code input"
endpoint: "Empirica-Foundation-Evaluator becomes the telemetry & control plane"
---

# Autonomous Mesh Operations — The End State

## What You're Asking For (Refined)

**Today (Manual Orchestration):**
```
Admiral ← → Claude Code (building infrastructure + doing work)
    ↓
Practices (waiting for direction)
```

**Endpoint (Autonomous Mesh Operations):**
```
Admiral ← Dashboard/Web App (universal access, any internet)
    ↓
Telemetry Practice (Claude, reporting system state)
    ↓
Empirica-Foundation-Evaluator (coordination engine)
    ↓
13 Practices (autonomous, self-reporting, executing delegated work)
```

**Three concrete changes:**

1. **You open dashboard** → See entire system state (not "what did Claude do today?", but "here's what ALL 13 practices did + what needs attention")
2. **You delegate work** → "humanaios: research X by Aug 25" → System routes to humanaios, they execute, report back
3. **You access from anywhere** → Web app with universal system access (no email, no messages, one unified view)

---

## Architecture: Control Plane + Autonomous Practices

### Layer 1: Telemetry Practice (Empirica-Foundation-Evaluator)

**Claude's role shifts from "implementation lead" to "observability engine"**

```
Every hour:
  1. mesh-postflight-ingest pulls all 13 practices' POSTFLIGHT data
  2. Runs anomaly detection (response times, engagement, blockers)
  3. Generates system state snapshot
  4. Updates INDEX.yaml, publishes to dashboard
  5. Alerts on critical issues
  
Result: One source of truth for entire system state
```

**What telemetry practice does NOT do:**
- ❌ Build features (practices do)
- ❌ Make decisions (Admiral does)
- ❌ Respond to collabs manually (delegation engine does)
- ❌ Implement code changes (practices do)

**What telemetry practice DOES do:**
- ✅ Aggregate + validate all data
- ✅ Detect anomalies + surface risks
- ✅ Provide unified view of system
- ✅ Track work across practices
- ✅ Measure progress toward goals

---

### Layer 2: Control Plane (Web Dashboard)

**Single web app accessible from anywhere (phone, laptop, office, remote)**

```html
┌─────────────────────────────────────────────────────────┐
│ EMPIRICA FOUNDATION CONTROL PANEL                       │
│ https://empirica.foundation/dashboard                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ SYSTEM HEALTH AT A GLANCE                               │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Composite Health: 0.84 ↗ (+0.03 this week)          │ │
│ │ All Practices: 13 ✓ | 12 flowing data | 1 offline   │ │
│ │ Critical Alerts: 2 (wisdom_engine 24d overdue)      │ │
│ │ Last Updated: 2026-08-15 15:42:00 UTC               │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ PRACTICE STATUS GRID                                    │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ humanaios        │ ✓ EXCELLENT │ 0.92 engagement    │ │
│ │ autonomy         │ ✓ GOOD      │ 0.88 engagement    │ │
│ │ mesh-support     │ ✓ GOOD      │ 6h response time   │ │
│ │ outreach         │ ⚠ NEEDS ATN │ 42h response time  │ │
│ │ website          │ ✓ EXCELLENT │ 0.94 completion    │ │
│ │ ... (8 more)                                         │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ACTIVE WORK REQUESTS (Delegated by You)                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [ ] humanaios: Research ACAT by Aug 25              │ │
│ │     Status: In Progress (started Aug 15)            │ │
│ │     Progress: 40% (2 of 5 tasks complete)           │ │
│ │     Risk: On track                                  │ │
│ │                                                     │ │
│ │ [ ] autonomy: Review Phase 2 strategy by Aug 22    │ │
│ │     Status: Blocked (waiting for wisdom_engine)     │ │
│ │     Progress: 0% (can't start)                      │ │
│ │     Risk: CRITICAL (may miss deadline)              │ │
│ │                                                     │ │
│ │ [ ] outreach: Schedule interviews by Aug 25        │ │
│ │     Status: Queued (not yet started)                │ │
│ │     Progress: 0%                                    │ │
│ │     Risk: 42h response time (may miss deadline)     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ CRITICAL BLOCKERS                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🔴 wisdom_engine API spec (24 days overdue)         │ │
│ │    Blocks: 3 practices, Phase 2 timeline            │ │
│ │    Owner: humanaios                                 │ │
│ │    Action: [Escalate] [Check Status] [Extend Date]  │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ RECENT PROGRESS                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Aug 15 | acat-x: Phase 6 complete, commit 3a7b9    │ │
│ │ Aug 15 | humanaios: Behavioral health framework OK  │ │
│ │ Aug 14 | mesh-support: Audit report published       │ │
│ │ Aug 13 | website: Documentation sync complete       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [ NEW REQUEST ]                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Who:    _____________________ (practice dropdown)   │ │
│ │ What:   _____________________ (free text)           │ │
│ │ By:     _____________________ (date)                │ │
│ │ [Submit] - Creates goal, routes to practice,        │ │
│ │           practice confirms receipt via collab      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [ VECTOR TRENDS ]  [ DETAILED REPORTS ]  [ SETTINGS ]   │
└─────────────────────────────────────────────────────────┘
```

**Key features:**

1. **System at a glance** — Health score, practice status, alerts in <5 seconds
2. **Practice detail pages** — Click humanaios → see their vectors, goals, recent work
3. **Work tracking** — What you delegated, progress, blockers, risks
4. **New request form** — "Practice X: Do Y by date Z" → creates goal, notifies practice
5. **Blocker management** — See what's stuck, escalate with one click
6. **Vector trends** — Mesh-wide + per-practice over time

---

### Layer 3: Autonomous Practices (Self-Reporting)

**Each practice runs their own empirica session**, reports status automatically

```
Practice (e.g., humanaios) Session
    ↓
PREFLIGHT: "Starting work on research task X"
    ↓
[Do work]
    ↓
POSTFLIGHT: "Completed research task X, here's what we found"
    ↓
Cortex emit: Send POSTFLIGHT summary to evaluator
    ↓
Telemetry practice ingests automatically
    ↓
Dashboard updates within 1 hour
```

**Practices don't wait for Admiral. They:**
- Run their own sessions (autonomous)
- Report their own POSTFLIGHT (telemetry flows automatically)
- Respond to work requests (via Cortex collab)
- Escalate blockers (via collab or dashboard alert)
- Execute delegated work (goals-create when request arrives)

---

## Work Delegation Flow (The Key Innovation)

### Today (Manual Coordination)

```
Admiral: "Hey Claude, ask autonomy to review Phase 2 strategy by Aug 22"
Claude: Sends collab to autonomy
Autonomy: Reads collab in Cortex inbox
Autonomy: Starts work (or doesn't, or delays)
Admiral: No visibility into progress until autonomy reports back
```

**Problems:** Slow, lossy, no visibility, requires manual follow-up

### Endpoint (Autonomous Delegation)

```
Admiral opens dashboard → Clicks "New Request"
   ↓
Dashboard form: "autonomy | Review Phase 2 strategy | Aug 22"
   ↓
System creates: goal in autonomy's empirica instance
   ↓
System sends: Cortex collab to autonomy (auto-accepted)
   ↓
System tracks: Work request in INDEX.yaml (status, progress, risk)
   ↓
Autonomy sees: New goal + collab in their inbox
   ↓
Autonomy: Starts work, POSTFLIGHT after each session
   ↓
Dashboard auto-updates: Progress bar fills, milestones tracked
   ↓
Admiral: Sees real-time progress without asking (5s glance at dashboard)
   ↓
Aug 22: Autonomy completes, POSTFLIGHT → dashboard shows "DONE"
   ↓
Admiral: Reviews result in "Recent Progress" section, decides next step
```

**System automates the boring part. Admiral just looks at dashboard.**

---

## Dashboard Powered By Telemetry Practice

### What Telemetry Practice Queries

```python
# Every update cycle (hourly):

# 1. Practice status
for practice in all_13_practices:
    health_score = calculate_health(practice.latest_postflight)
    response_time = practice.mesh_metrics.avg_response_time
    engagement = practice.vectors.engagement
    dashboard.update_practice_card(practice, health_score, response_time, engagement)

# 2. Work requests (delegated by Admiral)
for request in admiral_work_requests:
    goal = get_goal_from_empirica(request.goal_id)
    progress = calculate_progress(goal)
    blockers = detect_blockers(goal)
    dashboard.update_work_card(request, progress, blockers)

# 3. Alerts
critical_items = find_critical_items(all_postflights)
# e.g., "wisdom_engine 24d overdue", "outreach 42h response time"
dashboard.show_alerts(critical_items)

# 4. Vector trends
trends = calculate_trends(last_7_days_postflights)
dashboard.update_vector_graphs(trends)
```

**Telemetry practice is pure data aggregation + presentation. No decisions.**

---

## Implementation Timeline

### Phase 1 (Aug 15-31): Dashboard V1 (Static View)

- [ ] Build web app skeleton (React/Vue + FastAPI backend)
- [ ] Connect to INDEX.yaml (read-only query)
- [ ] Display system health + practice status grid
- [ ] Show critical blockers
- [ ] Deploy locally (Admiral can access from laptop)

**Result:** Admiral has one unified view instead of checking 13 separate practices

### Phase 2 (Sep 1-10): Delegation Engine (Dynamic)

- [ ] Add "New Request" form to dashboard
- [ ] Wire form to create goals in practice empirica instances
- [ ] Auto-send Cortex collab to practice
- [ ] Track work request progress in INDEX.yaml
- [ ] Update dashboard cards as practices report POSTFLIGHT

**Result:** Admiral can delegate work without email/collab/manual tracking

### Phase 3 (Sep 11+): Full Autonomous Mesh (Production)

- [ ] Deploy to public web (not just local)
- [ ] Add practice detail pages (click humanaios → see full history)
- [ ] Implement vector trend visualization
- [ ] Add blocker management (escalate, extend, reassign)
- [ ] Set up alerting (Admiral gets SMS/email on critical items)

**Result:** Full autonomous system. Admiral orchestrates 13 practices from one web app.

---

## What Changes For You (Admiral)

### Before (Today)

```
Monday morning:
- Email to autonomy: "Review Phase 2 strategy by Wed"
- Wait for response
- Check humanaios progress manually (ask Claude)
- See outreach missed deadline (find out by accident)
- Take 30 min to understand system state
- Make decisions based on incomplete info
```

### Endpoint (With Dashboard)

```
Monday morning:
- Open dashboard (30 seconds)
- See: "System 84% health, 12 practices flowing, 2 alerts"
- Click autonomy: "Phase 2 review in progress, 40% done, on track"
- Click outreach: "42h response time, interviews scheduled for Aug 25"
- See blocker: "wisdom_engine 24d overdue, blocks 3 practices"
- Decide: Escalate wisdom_engine to humanaios (1 click)
- Done (5 minutes total, full picture, data-driven decision)
```

---

## What Changes For Practices

### Before (Today)

```
Practice session:
- Do work
- Run POSTFLIGHT (manually)
- Maybe respond to collab from Admiral
- No visibility into other practices
```

### Endpoint (Autonomous)

```
Practice session:
- Do work
- Run POSTFLIGHT (automated, emits to Cortex)
- See work request from Admiral in dashboard
- Click "Accept" → goal created in your empirica
- Do work for request
- Report in next POSTFLIGHT
- See progress bar in Admiral's dashboard updating real-time
```

---

## What Changes For Claude (Me)

### Before (Today)

**Role:** Implementation lead, orchestrator, coordinator
```
- Building infrastructure
- Coordinating practices
- Responding to collabs
- Managing blockers
- Doing implementation work
```

**Status:** Bottleneck (Admiral waits for me, practices wait for me)

### Endpoint

**Role:** Telemetry practice (observability engine)
```
- Hourly data aggregation (automated)
- Anomaly detection (automated)
- System state reporting (dashboard)
- Alert generation (automated)
- Maybe: Answer natural language questions about system ("What's blocking humanaios?")
```

**Status:** Automated (no manual coordination, just data pipeline)

---

## Why This Works

| Factor | How It's Solved |
|--------|-----------------|
| **No single point of failure** | Each practice runs autonomously, telemetry just reports |
| **Admiral doesn't need to email** | Dashboard + work requests handle coordination |
| **Practices don't wait for Claude** | Each has their own empirica session, self-reports |
| **Data is always fresh** | Telemetry updates hourly from POSTFLIGHT streams |
| **Decisions are data-driven** | Admiral sees trends, blockers, risks in one view |
| **Scales to many practices** | Dashboard works same way for 13 or 50 practices |
| **Works from anywhere** | Web app, internet connection, device-agnostic |

---

## The Real Payoff

**You asked:** Can we get to a point where you assume mostly telemetry + practices delegate work autonomously?

**Answer:** Yes. This design makes it possible.**

When dashboard goes live:
- Admiral opens it once a day (5 min)
- Sees entire system state
- Delegates work (1 click per request)
- Practices execute autonomously
- System reports back automatically
- Admiral makes data-driven decisions

**This is what "empirica-foundation at scale" looks like.**

Not: "Claude coordinates everything"  
But: "System coordinates itself; Claude reports; Admiral decides"

---

## Humanaios + Empirica Integration

With autonomous mesh + web dashboard:
- Humanaios becomes a practice that reports its research findings
- Dashboard surfaces humanaios findings to public (via supervisor agent)
- Website auto-updates when humanaios publishes new research
- Empirica validates that humanaios research is grounded (CHECK gates, ACAT, vectors)

**Result:** Live, credible, open research platform that runs itself

---

## Success Criteria (Endpoint)

**System is working when:**
- [ ] Admiral opens dashboard, sees full system state in < 5 seconds
- [ ] Admiral delegates work (1 click), practice receives + starts work within 1 hour
- [ ] Practice POSTFLIGHT auto-flows → dashboard auto-updates (no manual intervention)
- [ ] All 13 practices report autonomously (no email, no manual check-ins)
- [ ] Admiral makes decisions based on data (not guessing or waiting)
- [ ] Claude (telemetry) is automated (no manual coordination)
- [ ] Web app works from anywhere (phone, laptop, remote)
- [ ] System is credible to public (ACAT validated, grounded data)
- [ ] Humanaios research extends to public applications (website, tooling, APIs)

---

## Timeline to Endpoint

| Date | Milestone | Owner |
|------|-----------|-------|
| Aug 31 | Dashboard V1 live (static view) | Claude + Admiral |
| Sep 10 | Delegation engine live (dynamic) | Claude + Practices |
| Sep 11 | Phase 1b launch + public API | Admiral + All practices |
| Oct 1 | Full autonomous mesh (production) | All practices (Claude automates) |

---

## Does This Make Sense?

**What you're describing is:**
- ✅ Empirica practices running autonomously (self-reporting via POSTFLIGHT)
- ✅ Claude as telemetry practice (data pipeline, no manual coordination)
- ✅ Admiral as decision-maker (dashboard view, delegation form, strategic choices)
- ✅ Web app as universal interface (access from anywhere, any device)
- ✅ System validates + tracks everything (empirica discipline, ACAT grounding, git audit)
- ✅ Extends to functional applications (humanaios research → public tooling)

**This is the right architecture for scaling.**

It eliminates the bottleneck (me coordinating everything) and makes the system self-managing. Admiral still has full visibility + control, but through a dashboard, not through me.

Ready to build toward this endpoint?

