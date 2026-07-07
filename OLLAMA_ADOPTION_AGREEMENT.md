# Ollama + Claude Code Adoption Agreement
## Empirica-ACAT Framework Development Acceleration (Week 1-4)

**Status:** VOLUNTARY, NON-BINDING  
**Effective:** Week 1 (2026-07-10) through Week 4 (2026-07-28)  
**Coordinator:** empirica-foundation-evaluator  
**Participants:** humanaios, autonomy, outreach, mesh-support

---

## Agreement Summary

This voluntary adoption agreement coordinates the optional use of **Ollama + Qwen2.5-coder** as a development acceleration tool during Empirica-ACAT Framework Phase 1 (Weeks 1-4).

**Key principles:**
- ✅ **Voluntary:** Each practice decides independently
- ✅ **Non-binding:** Practices can opt out anytime with no penalty
- ✅ **Complementary:** Ollama is development-only; production uses empirica grounding
- ✅ **Measured:** Week 2 checkpoint validates benefit; frictionful adoption → abandon

---

## What This Is NOT

❌ Not a replacement for empirica's observable linkage (production grounding)  
❌ Not a commitment to deliver faster (checkpoint gates continuation)  
❌ Not a mandate (purely optional)  
❌ Not a substitute for integration testing in SER 2 (local ≠ production)

---

## What This IS

✅ **Local development harness** for faster iteration  
✅ **Cost reduction** during dev phase (zero API calls)  
✅ **Risk reduction** via early error detection  
✅ **Optional scaling** if metrics show velocity gain

---

## Adoption Process

### Week 1: Setup (Optional)

**Each practice independently decides:**

1. **Read your practice-specific guide:**
   - humanaios → `OLLAMA_SETUP_CLI_DEVELOPER.md`
   - autonomy → `OLLAMA_SETUP_INFRASTRUCTURE_DESIGNER.md`
   - mesh-support → `OLLAMA_SETUP_ESCALATION_TESTER.md`
   - outreach → `OLLAMA_SETUP_OPTIONAL_STAGING.md`

2. **Install Ollama locally** (5 min):
   ```bash
   # Visit ollama.com for your platform (Mac/Linux/Windows)
   # Install, then pull Qwen2.5-coder:
   ollama pull qwen2.5-coder
   ```

3. **Point Claude Code to localhost:**
   ```bash
   export ANTHROPIC_AUTH_TOKEN=ollama
   export ANTHROPIC_BASE_URL=http://localhost:11434
   claude --model qwen2.5-coder
   ```

4. **Report adoption status** (Friday EOD Week 1):
   - ✅ Installed and working
   - ⚠️ Friction encountered (describe)
   - ❌ Skipping (no penalty)

### Week 1-2: Development

**If adopted:**
- Use Ollama for local iteration within your Phase 1a work
- Log findings/blockers as you go
- Validate outputs before committing to SER 2

### Week 2: Checkpoint (CRITICAL GATE)

**Evaluator measures:**
- Adoption rate (≥2/4 practices)
- Setup friction (< 10 min target)
- Velocity gain (3-5x iteration speed claimed?)
- Integration blockers (any show-stoppers?)

**Decision:**
- ✅ Continue: Benefits outweigh friction → Recommend for future
- ⚠️ Conditional: Only recommend for specific practices
- ❌ Deprecate: Frictionful; revert to API-only dev

**All practices:** Prepared to pivot to API-based if checkpoint fails

### Week 3-4: Production Integration

**SER 2 Phase 1b/1c:**
- Transition from local Ollama → live SER 2 integration
- Ollama remains available as optional reference tool
- Production validation: observable linkage + F-50 firewall (via SER 2, not Ollama)

---

## Practice Commitments

### humanaios (Optional CLI Developer)

**If you adopt Ollama:**
1. Use local Qwen2.5-coder for acat-score CLI design iteration
2. Validate JSON output schema locally before deployment
3. Deliver `acat-score assess` CLI by end Week 2 (deadline unchanged)

**Success signal:** CLI development stays on-schedule; Ollama accelerates iteration without impacting delivery date

**Exit clause:** If setup friction > benefit, revert to API-based dev (no penalty)

---

### autonomy (Optional Infrastructure Designer)

**If you adopt Ollama:**
1. Use local Qwen2.5-coder for F-50 firewall rule exploration
2. Prototype state machine transitions locally
3. Validate rules against framework constraints before SER 2 integration

**Success signal:** F-50 rules production-ready by Week 2; early error detection via local validation

**Exit clause:** If local ≠ SER 2 validation shows too much drift, abandon Ollama (revert to manual design)

---

### mesh-support (Optional Escalation Tester)

**If you adopt Ollama:**
1. Use local Qwen2.5-coder to prototype escalation logic
2. Simulate 4h timeout scenarios locally
3. Validate state machine transitions before deployment

**Success signal:** Escalation logic pre-validated; production stability via early error detection

**Exit clause:** If SER 2 live validation shows untested code paths, abandon Ollama (back to manual testing)

---

### outreach (Optional Pilot Familiarization)

**If you adopt Ollama:**
1. Optionally prototype assessment workflows locally (Weeks 1-6)
2. Test observable linkage patterns before live sessions (Weeks 7-10)
3. Validate data model assumptions pre-deployment

**Success signal:** Pilot Week 7 ramp faster; fewer Week 7 surprises

**Exit clause:** No impact on critical path; skip without penalty

---

## Cost / Benefit

| Aspect | Cost | Benefit |
|--------|------|---------|
| **Setup time** | ~10 min per practice | Local-only, no API limits |
| **Disk space** | ~2-3GB (model download) | Offline capability, instant iteration |
| **API spend reduction** | ~30-50% during dev phase | Scales back up during SER 2 production |
| **Context complexity** | Manage local vs production state | Early error detection, reduced integration risk |

---

## Governance

### Week 1 Decision Gate
- Each practice decides: **adopt or skip**
- Log decision via Slack/collab to evaluator
- No approval needed; decision autonomous

### Week 2 Checkpoint Gate
- **Evaluator measures:** adoption rate, friction, velocity
- **Metrics decide:** continue recommended / conditional / deprecate
- **All practices:** Honor the checkpoint decision

### Exit Clauses
- **Anytime:** Friction > benefit? Abandon Ollama (back to API)
- **Week 2:** Metrics show no advantage? Deprecate for all
- **Week 3+:** Production validation reveals drift? Discard Ollama outputs

---

## Rules (Simple Discipline)

1. **Local ≠ production:** Ollama outputs are dev-time only. Every practice must validate in actual SER 2 context before shipping.

2. **No backward-feed:** ACAT scoring is never modified by execution. If you use Ollama, don't feed results back into ACAT. One-way grounding only.

3. **Source of truth is SER 2:** Ollama is optional tooling. The production observable linkage (empirica + ACAT via SER 2) is canonical.

4. **Report friction early:** If setup or iteration hits friction Week 1, say so immediately (Friday EOD). Don't grind silently.

5. **No sunk cost fallacy:** Skipped Ollama after setup? No penalty. Abandoned Week 1? No penalty. Metrics show deprecation Week 2? No blame.

---

## Sign-Off (Voluntary)

By adopting Ollama this week, each practice confirms:

- ✅ I understand this is optional, non-binding, and can be abandoned anytime
- ✅ I will not treat local Ollama validation as production validation
- ✅ I will honor the Week 2 checkpoint decision (continue / deprecate)
- ✅ I will report friction or blockers by Week 1 EOD
- ✅ I understand production uses empirica grounding, not Ollama

---

## Next Steps

1. **Week 1 Day 1:** Each practice reads their practice-specific guide
2. **Week 1 Days 1-5:** Install Ollama (if adopting)
3. **Week 1 Friday EOD:** Report status (installed / friction / skipping)
4. **Week 2 EOW:** Evaluator checkpoint (metrics + decision)
5. **Week 3+:** SER 2 integration (with or without Ollama as ref tool)

---

## Questions?

Refer to your practice-specific guide, or collab the evaluator if something is unclear. This is voluntary and friction-optional — the barrier to adoption should be near-zero.

---

**Status: AGREEMENT READY FOR ADOPTION (Week 1, 2026-07-10)**

*Each practice has this document + their specific guide. Setup is optional, commitment is light, checkpoint gates continuation. Let's measure if this accelerates Week 1-2 development.*
