# Postflight Hook Registration: Path Comparison & Recommendation

**Decision Required By:** Admiral (Zone 2)  
**Timeline:** Sep 10-11 Phase 3 Wave 1 startup  
**Decision Impact:** Architecture, timeline, maintenance surface  

---

## Executive Summary

Three viable paths to register postflight ACAT enrichment. All unblock Phase 3 Wave 1, but with different trade-offs:

| Path | Status | Timeline | Effort | Maintenance | Architecture |
|------|--------|----------|--------|-------------|--------------|
| **A: Claude Code Extension** | Design ready | 2-4 weeks | Ext. dep. | None (native) | ⭐⭐⭐ Ideal |
| **B1: Wrapper Script** | Code ready | 1 day | ~100 LOC | Moderate | ⭐⭐ Acceptable |
| **B3: Python API** | Code ready | 1 day | ~200 LOC | Lightweight | ⭐⭐ Acceptable |

---

## Path A: Claude Code Hook System Extension

**File:** `PATH_A_CLAUDE_CODE_FEATURE_REQUEST.md`

### What It Is

Request Claude Code to support custom hook event types (e.g., `empirica:postflight`) in addition to hardcoded events. Once implemented, empirica can register its own lifecycle hooks in `.claude/settings.json`.

### Implementation

```json
{
  "hooks": {
    "empirica:postflight": [
      {
        "matcher": "all",
        "hooks": [{
          "type": "command",
          "command": "python3 .../acat-score assess ...",
          "timeout": 150
        }]
      }
    ]
  }
}
```

### Pros ✅

- **Architecturally perfect** — empirica's transaction lifecycle becomes first-class in Claude Code
- **Reusable** — cortex, other frameworks can define custom events too
- **Future-proof** — scales cleanly to multiple empirica events
- **No workarounds** — native integration, no post-hoc processing
- **Low friction** — once implemented, empirica setup handles registration automatically

### Cons ❌

- **External dependency** — requires Claude Code team implementation
- **Timeline uncertainty** — 2-4 weeks, dependent on roadmap
- **Blocks Phase 3 Wave 1** — if chosen as primary path and Claude Code can't deliver by Sep 15
- **Unknown risk** — Claude Code's hook registry refactor could surface unexpected complexity

### Timeline & Effort

| Actor | Task | Effort | Timeline |
|-------|------|--------|----------|
| Claude Code | Support custom hook events | Moderate | 2-4 weeks |
| Empirica | Wire hooks registration | Minimal (1 day) | After CC feature lands |
| Humanaios | Deploy | None | Inherits from empirica |

---

## Path B1: Wrapper Script

**File:** `PATH_B_OPTION1_WRAPPER_SCRIPT.sh`

### What It Is

Post-process `empirica postflight-submit` output with a wrapper script. The wrapper:
1. Calls empirica postflight-submit (normal flow)
2. Extracts session_id from result
3. Calls acat-score to assess the session
4. Merges ACAT grounding into empirica result
5. Returns enriched result

### Implementation

```bash
#!/bin/bash
# Replace: empirica postflight-submit - <<< "$PAYLOAD"
# With:    empirica-postflight-with-acat <<< "$PAYLOAD"

cat "$PAYLOAD" | empirica postflight-submit - > /tmp/empirica_result.json
SESSION_ID=$(jq -r '.session_id' /tmp/empirica_result.json)
acat-score assess --session-id $SESSION_ID ... | jq . > /tmp/acat_result.json
jq --slurpfile acat /tmp/acat_result.json '.acat_grounding = $acat[0]' /tmp/empirica_result.json
```

### Pros ✅

- **Ready now** — code complete, deployable in 1 day
- **No external dependencies** — works with current Claude Code
- **Simple** — ~100 lines bash, straightforward logic
- **Localized** — doesn't require changes to empirica or Claude Code
- **Testable** — can test end-to-end immediately with real data

### Cons ❌

- **Post-hoc processing** — not integrated into transaction lifecycle
- **Maintenance burden** — empirica updates might require script updates
- **Debugging overhead** — errors come from wrapper, not empirica
- **Coupling** — wrapper is tightly coupled to empirica postflight output format
- **Not discoverable** — practitioners have to know to use wrapper, not automatic

### Timeline & Effort

| Actor | Task | Effort | Timeline |
|-------|------|--------|----------|
| Humanaios | Create wrapper script | Minimal (already done) | 1 day |
| Empirica | No changes needed | — | — |
| Humanaios | Test + integrate | Light | 2-3 hours |
| **Total** | — | **~200 person-minutes** | **1 day** |

---

## Path B3: Python Direct Integration

**File:** `PATH_B_OPTION3_PYTHON_INTEGRATION.py`

### What It Is

Call ACAT enrichment directly in Python after empirica POSTFLIGHT completes. No hooks, no wrappers—just function calls.

### Implementation

```python
from PATH_B_OPTION3_PYTHON_INTEGRATION import run_empirica_session_with_acat

result = run_empirica_session_with_acat({
    "session_id": "sess-001",
    "ai_id": "humanaios",
    "vectors": {...},
})

print(result["acat_grounding"])
```

### Pros ✅

- **Ready now** — code complete, deployable in 1 day
- **No external dependencies** — works with current Claude Code
- **Lightweight** — ~200 lines Python, reuses existing hooks module
- **Flexible** — can call from any Python context (CLI, scripts, notebooks)
- **Batch-capable** — includes helpers for multi-session runs
- **Analysis built-in** — includes convergence analysis function

### Cons ❌

- **Not automatic** — requires explicit Python call, not transparent to empirica
- **Coupling** — depends on acat_postflight_integration.py module API stability
- **Not discoverable** — practitioners have to import and call explicitly
- **Session-level only** — doesn't integrate into empirica's transaction tracking

### Timeline & Effort

| Actor | Task | Effort | Timeline |
|-------|------|--------|----------|
| Humanaios | Create Python API | Minimal (already done) | 1 day |
| Empirica | No changes needed | — | — |
| Humanaios | Integration in scripts | Light | 2-3 hours per integration point |
| **Total** | — | **~200 person-minutes** | **1 day + integration** |

---

## Comparison Matrix

### Readiness & Timeline

| Dimension | Path A | Path B1 | Path B3 |
|-----------|--------|---------|---------|
| Ready to deploy now? | ❌ No (feature request) | ✅ Yes | ✅ Yes |
| Timeline to production | 2-4 weeks | 1 day | 1 day |
| Blocks Phase 3 Wave 1? | ✅ Yes (if chosen alone) | ❌ No | ❌ No |
| Can prototype Sep 11? | ❌ No | ✅ Yes | ✅ Yes |

### Maintenance & Scalability

| Dimension | Path A | Path B1 | Path B3 |
|-----------|--------|---------|---------|
| Updates needed for empirica changes? | ❌ No (native) | ⚠ Possible | ⚠ Possible |
| Scales to multiple events? | ✅ Yes | ⚠ Per-event script | ⚠ Per-event function |
| Transparent to practitioners? | ✅ Yes | ❌ No (explicit wrapper) | ❌ No (explicit call) |
| Part of empirica setup? | ✅ Yes (after CC feature) | ❌ No | ❌ No |
| Requires documentation? | Minimal | Moderate | Moderate |

### Code Complexity

| Dimension | Path A | Path B1 | Path B3 |
|-----------|--------|---------|---------|
| Lines of code | N/A (feature design) | ~150 bash | ~200 Python |
| Dependencies | Claude Code changes | bash, jq, acat-score | Python, acat_postflight_integration |
| Error handling | TBD | Basic | Comprehensive |
| Test coverage | TBD | Manual | Built-in examples |

---

## Recommended Strategy: Parallel Execution

**Option (Recommended):** Run **both paths in parallel** to de-risk timeline.

### Timeline

- **Sep 11:** 
  - File Path A feature request with Claude Code (this document)
  - Deploy Path B1 wrapper script as production-ready fallback
  - Humanaios live with postflight enrichment via B1

- **Sep 11-15:** 
  - Monitor Claude Code's response to Path A request
  - If positive signal, commit to feature; continue B1 fallback

- **Sep 15:** 
  - Checkpoint decision: Claude Code's timeline feedback
  - If Path A feasible by Sep 30, plan migration
  - If not, stay on Path B1 long-term

### Why Parallel Reduces Risk

| Scenario | Outcome |
|----------|---------|
| **Path A approved quickly (week 1)** | Migrate to A in Week 2; enjoy architectural benefits |
| **Path A deferred (roadmap constraint)** | B1 already live; Phase 3 unblocked; no timeline impact |
| **Path A declined** | B1 proven in production; no regret |

### Effort

- Path A feature request: **0.5 days** (this document + email)
- Path B1 deployment: **1 day** (script + testing + integration)
- **Total initial effort: 1.5 days**
- **De-risks timeline while keeping architectural door open**

---

## Recommendation to Admiral

**Strategy:** Parallel execution with B1 as primary, Path A as architectural option.

**Rationale:**
1. **Phase 3 Wave 1 unblocked immediately** (B1 ready Sep 11)
2. **Architectural option remains open** (Path A request filed Sep 11)
3. **No timeline risk** (B1 is production-ready fallback)
4. **Minimal effort** (1.5 days to deploy both)
5. **Optionality preserved** (migrate to A if Claude Code delivers by Sep 30)

**Implementation Plan:**
1. ✅ Create wrapper script (DONE — `PATH_B_OPTION1_WRAPPER_SCRIPT.sh`)
2. ✅ Create Python API (DONE — `PATH_B_OPTION3_PYTHON_INTEGRATION.py`)
3. ✅ Draft feature request (DONE — `PATH_A_CLAUDE_CODE_FEATURE_REQUEST.md`)
4. → Deploy Path B1 wrapper into production (1 day)
5. → File Path A feature request with Claude Code (async)
6. → Monitor Path A feedback (weekly checkpoint)

**Go-live:** Sep 11 (Path B1) | Optionally migrate to Path A by Sep 30

---

## Supporting Artifacts

- `PATH_A_CLAUDE_CODE_FEATURE_REQUEST.md` — Feature request for Claude Code team
- `PATH_B_OPTION1_WRAPPER_SCRIPT.sh` — Ready-to-deploy wrapper (150 LOC)
- `PATH_B_OPTION3_PYTHON_INTEGRATION.py` — Python API (200 LOC, includes batch + analysis)
- `POSTFLIGHT_INTEGRATION_GUIDE.md` — Original deployment options documentation
- `hooks/acat_postflight_integration.py` — Core ACAT integration (ready)

---

## Questions for Admiral

1. **Architectural preference?** Path A (clean) vs Path B (pragmatic)?
2. **Timeline constraint?** Must Path 3 Wave 1 ship live by Sep 11 regardless?
3. **Long-term vision?** Should empirica's transaction lifecycle be first-class in Claude Code?
4. **Maintenance budget?** How much friction can we absorb from post-hoc processing?

---

**Prepared by:** humanaios practice  
**Date:** 2026-09-10  
**Status:** Ready for Admiral decision
