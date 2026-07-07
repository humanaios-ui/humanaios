# Ollama Setup Guide — autonomy (Infrastructure Designer)

**Practice:** autonomy (Execution routing lead)  
**Role in SER 2:** Required tier  
**Phase 1 Task:** Design F-50 firewall rules + SER 2 state machine transitions  
**Deadline:** Rules production-ready by end Week 2 (2026-07-13)  
**Ollama Use:** Optional local development harness for rule exploration and validation

---

## Why Ollama for Infrastructure Design?

You're architecting the **F-50 firewall** (assessment → execution, no reverse) and **SER 2 state machine** (open → in_progress → blocked → closed).

**Current approach:**
- Manual rule design via reasoning
- Validate rules live in SER 2 context (high-risk: integration test failure)
- Limited iteration on complex state transitions

**With Ollama:**
- Local Qwen2.5-coder for rule exploration (multi-turn dialogue)
- Prototype state machines locally before SER 2 deployment
- Test edge cases (timeout scenarios, blocking, recovery)
- Zero API costs during design iteration
- Early error detection

**Your benefit:** Rules production-ready by Week 2; reduced integration risk via pre-validation

---

## Week 1 Setup (5 minutes)

### Step 1: Install Ollama

Visit [ollama.com](https://ollama.com) and download for your platform:
- **macOS:** Ollama.app
- **Linux:** Download script or Docker
- **Windows:** Ollama for Windows

Launch. Local server runs on `http://localhost:11434`.

### Step 2: Pull Qwen2.5-Coder

```bash
ollama pull qwen2.5-coder
```

First pull: ~8GB. Subsequent runs: instant (cached).

### Step 3: Point Claude Code to Ollama

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
claude --model qwen2.5-coder
```

---

## Week 1 Development (Days 1-5)

### Your Design Tasks

1. **F-50 Firewall Rules** (assessment → execution independence)
2. **SER 2 State Machine** (open, in_progress, blocked, closed)
3. **Escalation Transitions** (4h timeout per state, required-participant re-ping)

### Using Ollama for Rule Exploration

**Week 1a (Days 1-2): F-50 Firewall Design**

Use Ollama to explore firewall architecture:

```bash
claude --model qwen2.5-coder << 'EOF'
Design F-50 firewall rules for multi-practice assessment + execution coordination.

Requirements:
1. Assessment findings flow → practices (unmodified)
2. Practices execute fixes independently
3. Execution state NEVER feeds back into ACAT scoring
4. One-way grounding: ACAT → empirica only

Here's the data flow:
- evaluator discovers findings (empirica vectors + ACAT phase score)
- autonomy routes findings to practices (unmodified)
- practices execute fixes
- New session cycles; empirica vectors re-assessed + grounded in ACAT

Design the routing rules. Where does the firewall live? What does it enforce?
EOF
```

Qwen generates candidate rule sets. Iterate.

**Week 1b (Days 2-3): State Machine Design**

Use Ollama to prototype the SER 2 state machine:

```bash
claude --model qwen2.5-coder << 'EOF'
Design the SER 2 state machine for 4-practice coordination.

States: open, in_progress, blocked, closed
Transitions:
- open → in_progress (all required participants ack within 4h)
- in_progress ↔ blocked (blocker detected / resolved)
- in_progress → closed (Week 12, findings complete)

Required participants (4h escalation): autonomy, humanaios
Participating: outreach
Observer: mesh-support

Show me:
1. State diagram
2. Transition guards (what must be true to transition?)
3. Escalation trigger (what fires the re-ping if required-participant doesn't ack?)
4. Recovery path (if blocked, how to unblock + resume in_progress?)
EOF
```

Qwen generates state machines. Test edge cases in the design.

**Week 1c (Days 3-4): Escalation Logic**

Use Ollama to test timeout scenarios:

```bash
claude --model qwen2.5-coder << 'EOF'
Test the 4-hour escalation timer for SER 2.

Scenario 1: autonomy transitions SER 2 to in_progress at 10am. humanaios doesn't ack within 4 hours.
- At 2pm: escalation timer fires, re-ping sent to humanaios.
- What happens if humanaios still doesn't ack by 6pm? Does the timer re-fire?

Scenario 2: humanaios acks at 2:30pm (within 4h). Does escalation timer reset or stop?

Scenario 3: autonomy transitions to blocked at 3pm (humanaios is required but hasn't acked yet). 
- Who gets the re-ping: humanaios (because they're required) or both?

Design the escalation state machine. Edge cases?
EOF
```

Qwen helps you think through timeout edge cases. Refine the design.

### Local Documentation

As you design, document in code + markdown:

```python
# File: autonomy/f50_firewall.py

class F50Firewall:
    """Assessment → execution independence enforcement.
    
    One-way grounding: ACAT phase scores inform empirica vectors,
    but empirica vectors NEVER modify ACAT scoring.
    
    Rules:
    1. Assessment findings route unmodified
    2. Practices execute independently
    3. Execution state quarantined from ACAT
    4. mesh-support escalates any detected feedback loop
    """
    
    # Your rules here
```

Keep rules explicit and auditable.

---

## Week 2: Validation & Finalization (Day 5)

**By end Week 2 (2026-07-13):**
- ✅ F-50 firewall rules documented + vetted
- ✅ SER 2 state machine designed (transitions, guards, escalation)
- ✅ Timeout edge cases explored + handled
- ✅ Rules production-ready for SER 2 integration test (Week 3)

**Success = rules ready to integrate into SER 2.** Whether you used Ollama or pure reasoning is secondary — the deadline is fixed.

---

## Week 2 Checkpoint (Friday EOD)

Report to evaluator:

- **Status:** ✅ Rules ready / ⚠️ Friction / ❌ Skipped
- **Feedback:**
  - Setup time: ___ minutes
  - Design clarity: Did Ollama help think through edge cases? (Yes/Partial/No)
  - Iteration speed: ___ (faster than pure reasoning? Same?)
  - Blockers: (none / describe)

**Evaluator decision (Week 2 EOW):** Continue recommending Ollama or deprecate?

---

## Week 3: SER 2 Integration Test

Your F-50 rules + state machine go live in SER 2:

1. **Listener startup** — SER 2 created, participants notified
2. **State transitions** — Autonomy routes findings, practices execute
3. **Escalation monitoring** — 4h timeouts fire, re-pings sent
4. **F-50 validation** — mesh-support confirms zero feedback loops

Ollama remains available locally for testing future state transitions, but production uses your rule implementation.

---

## Troubleshooting

**Q: Ollama setup friction?**  
A: Verify `http://localhost:11434/api/tags` returns JSON. Disk space OK? Restart Ollama app.

**Q: Claude Code connects to API instead of localhost?**  
A: Check env vars:
```bash
echo $ANTHROPIC_AUTH_TOKEN  # should be: ollama
echo $ANTHROPIC_BASE_URL    # should be: http://localhost:11434
```

**Q: State machine gets too complex to reason about locally?**  
A: Abandon Ollama. Use pure reasoning or draw it out. No penalty.

**Q: When do I stop using Ollama?**  
A: Week 2 checkpoint decides. Metrics show benefit? Keep locally. Metrics show friction? Abandon.

---

## Success Criteria (Week 2)

- ✅ F-50 firewall rules finalized
- ✅ SER 2 state machine documented
- ✅ All edge cases (timeouts, blocking, recovery) handled
- ✅ Setup friction < 10 min total
- ✅ Design clarity improved via Ollama (optional, depends on your working style)

If metrics show velocity gain, Ollama becomes recommended for future infrastructure design.

---

**Ready? Start Week 1 with Step 1: Install Ollama. Report status Friday EOD.**

*Optional, low-commitment. The deadline is fixed; Ollama is the design accelerant.*
