# Ollama Setup Guide — humanaios (CLI Developer)

**Practice:** humanaios (ACAT owner)  
**Role in SER 2:** Required tier  
**Phase 1 Task:** Build acat-score CLI tool  
**Deadline:** End of Week 2 (2026-07-13)  
**Ollama Use:** Optional local development harness for CLI design iteration

---

## Why Ollama for CLI Development?

You're building `acat-score assess` — a command-line wrapper around ACAT's HTTP API.

**Current approach:**
- Iterate against Anthropic API (tokens = money)
- API latency per iteration (slower feedback loop)
- Context resets between sessions

**With Ollama:**
- Local Qwen2.5-coder (32K context, tool-calling support)
- Zero API costs during iteration
- 3-5x faster feedback loop
- Full context retained across turns
- Works offline (no API outages)

**Your benefit:** Rapid CLI design + schema validation → on-time Week 2 delivery

---

## Week 1 Setup (5 minutes)

### Step 1: Install Ollama

Visit [ollama.com](https://ollama.com) and download for your platform:
- **macOS:** Ollama.app (universal binary)
- **Linux:** Download script or Docker
- **Windows:** Ollama for Windows

Install and launch. On macOS/Linux, Ollama starts a local server on `http://localhost:11434`.

### Step 2: Pull Qwen2.5-Coder

```bash
ollama pull qwen2.5-coder
```

First pull downloads ~8GB. Subsequent runs are instant (cached locally).

### Step 3: Point Claude Code to Ollama

In your shell, before running `claude` or Claude Code:

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
```

Then invoke Claude Code:

```bash
claude --model qwen2.5-coder
```

Or in Claude Code (if using IDE extension):
- Settings → Anthropic API Base URL: `http://localhost:11434`
- Model: `qwen2.5-coder`

**Verify it works:**
```bash
claude --model qwen2.5-coder << 'EOF'
What is JSON schema validation in Python?
EOF
```

Expected: Response about JSON schema, no API call to Anthropic.

---

## Week 1 Development (Days 1-5)

### Your CLI Spec (from ACAT_CLI_ASSESSMENT.md)

```bash
acat-score assess \
  --session-id <uuid> \
  --ai-id <practice> \
  --behavior-transcript <path> \
  --rubric-version v1.0 \
  --output json
```

**Returns:**
```json
{
  "phase": 3,
  "phase_score": 3.2,
  "confidence": 0.88,
  "rubric_alignment": {
    "clarity": "met",
    "independence": "met"
  },
  "observations": [...]
}
```

### Using Ollama for Design Iteration

**Week 1a (Days 1-2): CLI Design**

Use Ollama to explore design patterns:

```bash
claude --model qwen2.5-coder << 'EOF'
I'm building a CLI tool for ACAT assessments. Help me design:

1. Entry point: acat-score assess
2. Input: --session-id, --ai-id, --behavior-transcript, --rubric-version
3. Output: JSON {phase, phase_score, confidence, rubric_alignment, observations}

Show me the Python argparse structure + main entry point skeleton.
EOF
```

Qwen will generate code locally. No wait for API, no token burn.

**Week 1b (Days 2-3): Implementation**

Use Ollama for implementation help:

```bash
claude --model qwen2.5-coder << 'EOF'
Implement the assess command. The core logic is already in acat.core.assess(). 
I need:
- Parse arguments from CLI
- Call core.assess(session_id, ai_id, behavior_transcript, rubric_version)
- Format output as JSON
- Handle errors with exit codes

Show me the command handler code.
EOF
```

Iterate freely. Wrong approach? Ask again. No API costs.

**Week 1c (Days 3-4): Schema Validation**

Use Ollama to validate JSON output schema:

```bash
claude --model qwen2.5-coder << 'EOF'
Validate that my CLI output matches this schema:
{
  "phase": int (1-3),
  "phase_score": float,
  "confidence": float (0-1),
  "rubric_alignment": {string: string},
  "observations": [string]
}

Here's my current output code: [paste code]

Does it match? Any gaps?
EOF
```

### Local Testing (Optional)

Test your CLI locally before pushing:

```bash
# Run your CLI
acat-score assess \
  --session-id test-001 \
  --ai-id humanaios \
  --behavior-transcript /tmp/test.log \
  --rubric-version v1.0 \
  --output json
```

Verify JSON structure. Fix issues. Repeat.

---

## Week 2: Delivery (Day 5)

**By end Week 2 (2026-07-13):**
- ✅ `acat-score assess` command deliverable
- ✅ JSON output matches schema
- ✅ Exit codes: 0 (success), non-zero (error)
- ✅ No stderr HTTPException leaks

**Success = on-time delivery.** Whether you used Ollama or API is secondary — the deadline is fixed.

---

## Week 2 Checkpoint (Friday EOD)

Report to evaluator:

- **Status:** ✅ On track / ⚠️ Friction / ❌ Skipped
- **Feedback:**
  - Setup time: ___ minutes
  - Iteration speed: ___ (X times faster than API? Same? Slower?)
  - Blockers: (none / describe)

**Evaluator decision (Week 2 EOW):** Continue recommending Ollama or deprecate for future?

---

## Week 3+: Production Integration

Your `acat-score` CLI goes live:

1. **POSTFLIGHT hook** invokes `acat-score assess` atomically
2. **Session record** enriched with `{phase, phase_score, confidence, rubric_alignment}`
3. **Convergence signal** (δ) calculated and logged
4. **Observable dataset** ready for Phase 2 grounding measurement

Ollama remains available locally if you want to prototype future commands, but production uses your compiled binary (no dependency on Ollama).

---

## Troubleshooting

**Q: Ollama install hangs or won't start**  
A: Check disk space (~3GB for model). Restart the Ollama app. Verify `http://localhost:11434/api/tags` returns JSON (browser test).

**Q: Claude Code connects to API instead of localhost**  
A: Verify env vars are set:
```bash
echo $ANTHROPIC_AUTH_TOKEN  # should print: ollama
echo $ANTHROPIC_BASE_URL    # should print: http://localhost:11434
```
If using IDE extension, check settings panel — env vars may not propagate into the IDE process.

**Q: Model responses are slow**  
A: Qwen2.5-coder is 7B parameters; slower than Claude but still usable. First run after restart is slowest (model loaded into memory). Subsequent turns are faster.

**Q: Ollama output doesn't match API schema**  
A: Remember: Ollama is dev-time iteration. Before committing to SER 2, validate your code against the real HTTP API once.

**Q: When should I stop using Ollama?**  
A: Week 2 checkpoint decides. If metrics show friction > benefit, abandon. If metrics show velocity gain, keep using locally (Week 3+). Either way, production integration (SER 2) happens as planned.

---

## Success Criteria (Week 2)

- ✅ acat-score CLI delivered on time (Week 2, 2026-07-13)
- ✅ JSON output matches schema 100%
- ✅ Setup friction < 10 min total
- ✅ Iteration speed gain reported

If all 4 ✅, Ollama becomes recommended practice. Otherwise, API-only development is fine.

---

**Ready? Start Week 1 with Step 1: Install Ollama. Report status Friday EOD.**

*This is optional. No penalty if friction is high or you prefer API-based iteration. The deadline is the commitment; Ollama is the accelerant.*
