# Ollama Setup Guide — mesh-support (Escalation Tester)

**Practice:** mesh-support (Coordination + monitoring lead)  
**Role in SER 2:** Observer (non-escalation participant)  
**Phase 1 Task:** Prepare escalation monitoring + F-50 firewall surveillance  
**Deadline:** Infrastructure ready by end Week 2 (2026-07-13)  
**Ollama Use:** Optional local development harness for testing state transitions and timeout scenarios

---

## Why Ollama for Escalation Testing?

You're responsible for:
- **Escalation monitoring:** 4h timer per SER 2 state transition
- **F-50 firewall surveillance:** Detecting feedback loops (execution → ACAT)
- **Data provenance tracking:** Sessions → calibration dataset

**Current approach:**
- Manual logic review + live SER 2 testing
- Errors surface during production transitions (high-risk)
- Limited ability to test timeout scenarios locally

**With Ollama:**
- Local Qwen2.5-coder for state machine testing
- Simulate timeout scenarios (what happens if participant doesn't ack?)
- Test edge cases (blocking, recovery, escalation re-pings)
- Validate monitoring logic before deployment
- Zero API costs during design iteration

**Your benefit:** Production stability via early error detection; fewer surprises Week 3+

---

## Week 1 Setup (5 minutes)

### Step 1: Install Ollama

Visit [ollama.com](https://ollama.com) and download for your platform.  
Launch and wait for local server (`http://localhost:11434`).

### Step 2: Pull Qwen2.5-Coder

```bash
ollama pull qwen2.5-coder
```

### Step 3: Point Claude Code to Ollama

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
claude --model qwen2.5-coder
```

---

## Week 1 Development (Days 1-5)

### Your Design Tasks

1. **Escalation Timer Logic** (4h per state transition, required-participant re-ping)
2. **State Transition Monitoring** (track SER 2 as it moves through states)
3. **F-50 Firewall Surveillance** (detect feedback loops from execution → ACAT)
4. **Data Provenance Tracking** (sessions → calibration dataset audit trail)

### Using Ollama for Escalation Design

**Week 1a (Days 1-2): State Transition Testing**

Use Ollama to explore timeout scenarios:

```bash
claude --model qwen2.5-coder << 'EOF'
Design escalation monitoring for SER 2 state machine.

SER 2 has 4 states: open, in_progress, blocked, closed
Required participants: autonomy, humanaios (must ack within 4h)
Participating: outreach (no escalation timer)
Observer: mesh-support (you)

Test case 1:
- SER 2 transitions open → in_progress at 10am
- autonomy acks immediately
- humanaios doesn't ack (still pending at 2pm, 4h mark)
- Escalation timer fires: re-ping humanaios

What data must the timer track? When does it reset?

Test case 2:
- SER 2 blocked at 3pm
- Both autonomy + humanaios must ack to unblock
- autonomy acks at 4pm, humanaios still pending at 7pm (4h+)
- Does escalation re-fire? Who gets pinged?

Show me the timer state machine.
EOF
```

Qwen helps you think through timeout logic. Refine.

**Week 1b (Days 2-3): F-50 Firewall Surveillance**

Use Ollama to design detection logic:

```bash
claude --model qwen2.5-coder << 'EOF'
Design F-50 firewall violation detection.

F-50 rule: Execution state NEVER feeds back into ACAT scoring.

How do you detect a violation? What signals would indicate a feedback loop?

Scenario: autonomy routes finding "empirica vector X underconfident" to a practice.
The practice executes a fix. In the next session cycle, empirica re-measures vector X.

Question: How do you confirm this finding didn't loop back into ACAT scoring?

What logs/signals do you monitor? What constitutes a CRITICAL alert vs warning?

Show me the detection rules + alert taxonomy.
EOF
```

Qwen generates detection patterns. Test them against the framework rules.

**Week 1c (Days 3-4): Data Provenance Tracking**

Use Ollama to design audit trail:

```bash
claude --model qwen2.5-coder << 'EOF'
Design data provenance tracking for Empirica-ACAT calibration dataset.

Every session must be traceable:
- Session ID
- Empirica vectors (from PREFLIGHT + POSTFLIGHT)
- ACAT phase score (from acat-score CLI)
- Convergence delta (δ = empirica_vector - acat_phase_score)
- Observability: which practice, which phase, which week

Later analysis needs to:
1. Query "all sessions from humanaios, Week 3" → 50 rows
2. Calculate Brier score per vector
3. Filter outliers (|δ| > 0.20) for accountability
4. Extract lessons (what patterns repeat?)

What data model ensures this is queryable? PostgreSQL schema?
Qdrant vector store for semantic search?
Git notes for audit trail + versioning?

Show me the data architecture.
EOF
```

Qwen generates data model options. Pick the right one for Week 3+ retrieval.

---

## Week 2: Validation & Infrastructure Setup (Day 5)

**By end Week 2 (2026-07-13):**
- ✅ Escalation timer logic finalized + tested
- ✅ F-50 firewall surveillance rules documented
- ✅ Data provenance schema designed (queryable, auditable)
- ✅ Monitoring dashboards ready to deploy

**Success = infrastructure ready for SER 2 live deployment.** Whether you used Ollama or pure design is secondary — the infrastructure is ready.

---

## Week 2 Checkpoint (Friday EOD)

Report to evaluator:

- **Status:** ✅ Infrastructure ready / ⚠️ Friction / ❌ Skipped
- **Feedback:**
  - Setup time: ___ minutes
  - Design coverage: Did Ollama help explore timeout edge cases? (Yes/Partial/No)
  - Iteration speed: ___ (faster than pure reasoning? Same?)
  - Blockers: (none / describe)

**Evaluator decision (Week 2 EOW):** Continue recommending Ollama or deprecate?

---

## Week 3: SER 2 Go-Live

Your escalation monitoring + F-50 surveillance go live:

1. **Listener fires** — SER 2 created, state = open
2. **Transitions flow** — States change, escalation timers tick
3. **Escalations trigger** — Re-pings sent at 4h mark
4. **F-50 monitoring** — Watch for feedback loops (should be zero)
5. **Data provenance logged** — Every session coupled empirica + ACAT

Ollama remains available locally for testing future scenarios, but production uses your deployed monitoring.

---

## Troubleshooting

**Q: Ollama won't start?**  
A: Check disk space. Restart app. Verify `localhost:11434/api/tags` in browser.

**Q: Design gets too complex?**  
A: Abandon Ollama. Use diagrams + pure reasoning. No penalty.

**Q: When do I stop using Ollama?**  
A: Week 2 checkpoint decides. Metrics show benefit? Keep locally. Friction > benefit? Abandon.

---

## Success Criteria (Week 2)

- ✅ Escalation timer logic finalized
- ✅ F-50 firewall surveillance designed
- ✅ Data provenance schema documented
- ✅ Setup friction < 10 min total
- ✅ Design coverage improved (edge cases, timeout scenarios explored)

If metrics show stability improvement in Week 3+, Ollama becomes recommended for future infrastructure testing.

---

**Ready? Start Week 1 with Step 1: Install Ollama. Report status Friday EOD.**

*Optional, low-risk. The deadline is fixed; Ollama is the validation accelerant.*
