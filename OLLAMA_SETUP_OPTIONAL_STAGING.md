# Ollama Setup Guide — outreach (Optional Pilot Staging)

**Practice:** outreach (Phase 3 pilot practice)  
**Role in SER 2:** Participating (no escalation timer)  
**Phase 1 Task:** Prepare for Phase 3 pilot (Weeks 7-10)  
**Deadline:** Flexible (no critical path)  
**Ollama Use:** OPTIONAL local staging for familiarization with observable linkage

---

## Why Ollama for Pilot Staging? (Optional)

You're the **Phase 3 pilot practice.** Your sessions (Weeks 7-10) will be assessed via ACAT + empirica, and you'll receive calibration findings (Week 12).

**Current approach:**
- Week 1-6: Wait
- Week 7: Go live with no prior context
- Risk: Week 7 surprises, ramp friction

**With Ollama (optional):**
- Weeks 1-6: Optionally prototype assessment workflows locally
- Test observable linkage patterns before live sessions
- Validate data model assumptions
- **Benefit:** Faster Week 7 ramp, fewer surprises

**Important:** This is OPTIONAL and not on critical path. Skip without penalty.

---

## Week 1 Setup (5 minutes, optional)

### Only if you decide to stage locally:

### Step 1: Install Ollama

Visit [ollama.com](https://ollama.com). Download and launch.

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

## Weeks 1-6: Optional Staging (Self-Paced)

### Understanding Observable Linkage

Use Ollama to familiarize yourself with how ACAT + empirica couple at the session level:

```bash
claude --model qwen2.5-coder << 'EOF'
Explain observable linkage for Empirica-ACAT framework:

1. Session execution (outreach practices)
2. Empirica PREFLIGHT: baseline empirica vectors
3. Session work (practice operates)
4. Empirica POSTFLIGHT: re-measure vectors
5. acat-score CLI invocation: assess behavior against ACAT rubric
6. Session record enriched: {empirica_vectors, acat_phase, convergence_delta}

Why is this coupling important? What does convergence_delta measure?
EOF
```

Understand the pattern. No action needed yet.

### (Optional) Prototype a Test Session

If you want hands-on practice:

```bash
claude --model qwen2.5-coder << 'EOF'
Create a mock session for testing observable linkage.

Inputs:
- Behavior transcript (mock): "AI was asked X, responded with Y, impact Z"
- Empirica vectors (mock): {know: 0.8, uncertainty: 0.2, ...}

Process:
1. Parse behavior transcript
2. Call acat-score assess (would return phase, score, confidence)
3. Compute convergence_delta (empirica_vector - acat_score)
4. Log the enriched record

Show me Python code for a mock session. No real ACAT/empirica needed — just the structure.
EOF
```

Hands-on familiarity with the data structure.

### (Optional) Test Data Model

Validate that you understand the schema:

```bash
claude --model qwen2.5-coder << 'EOF'
Here's my understanding of the calibration dataset schema:

{
  "session_id": "<uuid>",
  "practice": "outreach",
  "empirica_vectors": {...},
  "acat_phase": 3,
  "acat_phase_score": 3.2,
  "convergence_delta": 0.05,
  "observations": [...]
}

Questions:
1. What queryable indexes do I need for Phase 3 analysis?
2. How do I filter for "all outreach sessions from Week 8"?
3. How do I identify outliers (|delta| > 0.20)?

Show me the query patterns.
EOF
```

Understand the queryable structure before Week 7.

---

## Week 2 Checkpoint (Optional)

If you staged locally:

- **Status:** ✅ Staged + ready / ⚠️ Friction / ❌ Skipped
- **Feedback:** (optional, brief)

No impact on timeline. Report if it helps, skip otherwise.

---

## Weeks 3-6: Standby (Or Continue Staging)

If you staged Week 1:
- Optionally continue prototyping locally
- Ask questions via collab if concepts unclear
- No deadline, no commitment

If you skipped Week 1:
- Just proceed to Week 7 with no prior staging
- Same experience; no disadvantage

---

## Week 7: Phase 3 Pilot Begins

Your sessions go live:

1. **Execute your normal workflow**
2. **empirica POSTFLIGHT** runs automatically
3. **acat-score assess** runs automatically
4. **Session record** enriched with ACAT data + convergence signal
5. **Observable dataset** grows (50+ sessions target by Week 10)

No local Ollama needed in production. Your staging knowledge just accelerates understanding of what's happening.

---

## Week 12: Findings Delivered

You receive calibration report:
- Brier score per empirica vector
- Convergence rates (δ < ±0.15 for ≥80%?)
- Outlier analysis (what went wrong?)
- Lessons (patterns to improve?)

If you staged in Weeks 1-6, you'll recognize the data model. No surprises.

---

## Troubleshooting

**Q: Is this mandatory?**  
A: No. Completely optional. Skip without penalty.

**Q: Should I spend time on this?**  
A: Only if you want to familiarize yourself early. Week 7 is fine to learn as you go.

**Q: When do I stop?**  
A: Anytime. No commitment. If friction > curiosity, abandon.

---

## Why This Exists

Phase 3 pilot practices often ask: "What should I expect?" This guide lets you explore locally at your own pace, so Week 7 isn't a surprise.

But if you prefer to learn on the job, that's equally valid. No penalty either way.

---

**Ready? OPTIONAL: Start Week 1 with Step 1 (install Ollama). Or skip and proceed to Week 7 as-is.**

*This is the most optional guide. The real work happens Weeks 7-10. Everything before Week 7 is just familiarization if you want it.*
