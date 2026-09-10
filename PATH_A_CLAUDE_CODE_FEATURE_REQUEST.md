# Path A: Claude Code Hook System Extension

## Feature Request: Custom/User-Defined Hook Events

**Target:** Claude Code team (anthropics/claude-code)  
**Purpose:** Enable custom hook event types for framework integration (empirica postflight assessment)  
**Timeline:** Dependent on Claude Code development schedule  
**Effort (our side):** Minimal (once feature exists)

---

## Problem Statement

Empirica needs to hook into the Claude Code lifecycle for session assessment enrichment (ACAT scoring post-POSTFLIGHT). Claude Code's current hook system uses hardcoded event types (PreToolUse, PostToolUse, SessionStart, etc.), which prevents registration of empirica's custom lifecycle events (postflight, preflight, session_init).

**Current architecture:**
- Empirica transactions: PREFLIGHT → CHECK → PRAXIC → POSTFLIGHT
- Empirica goal: Enrich POSTFLIGHT session records with ACAT assessment scoring
- Blocker: Can't register empirica-specific events in `.claude/settings.json`

---

## Proposed Solution: Custom Hook Event Support

### Requirements

1. **User-defined hook event names** — allow `.claude/settings.json` to register hooks for arbitrary event names, not just the predefined set
2. **Namespace convention** — recommend `practice:event-name` or `app:event-name` pattern to avoid collisions
3. **Validation** — warn if custom event names are never fired (indicates misconfiguration)

### Example Configuration (Post-Implementation)

```json
{
  "hooks": {
    "SessionStart": [...],
    "empirica:postflight": [
      {
        "matcher": "all",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/operations/bin/acat-score assess --session-id $SESSION_ID",
            "timeout": 150
          }
        ]
      }
    ]
  }
}
```

### Empirica Integration (What We'd Do)

Once Claude Code supports custom events, empirica setup would:

1. Register hooks in `.claude/settings.json` under `empirica:postflight`, `empirica:preflight`, etc.
2. Fire custom events at appropriate transaction points (POSTFLIGHT phase end)
3. Pass context to hook scripts via environment variables or stdin
4. Log hook results to session record

---

## Comparison: Effort & Timeline

| Dimension | Effort | Timeline | Risk |
|-----------|--------|----------|------|
| Claude Code development | Moderate (hook registry refactor) | 2-4 weeks | Low (backward compatible) |
| Empirica integration | Minimal (wire existing hooks) | 1 day | Low (isolated to hook registration) |
| Humanaios deployment | None (inherits from empirica) | 0 | None |
| **Total timeline to live** | — | 2-4 weeks | — |

---

## Advantages

✅ **Clean architecture** — empirica's transaction lifecycle is first-class in Claude Code  
✅ **Reusable** — other frameworks (cortex, etc.) can define their own custom events  
✅ **Future-proof** — scales to multiple custom events without hardcoding  
✅ **Low friction** — no wrapper scripts or post-hoc integration layers  

---

## Disadvantages

❌ **External dependency** — requires Claude Code team implementation  
❌ **Timeline uncertainty** — dependent on Claude Code's development roadmap  
❌ **Opportunity cost** — blocks Phase 3 Wave 1 if chosen as primary path  

---

## Recommendation to Admiral

**Path A is architecturally superior** but timeline-dependent. **Recommend parallel execution:**
1. File feature request with Claude Code (this document)
2. Implement Path B as fallback (ready in 1-2 days)
3. If Claude Code supports custom events by Sep 15, migrate to Path A
4. If not, stay on Path B (wrapper script is production-ready)

This de-risks Phase 3 Wave 1 while keeping architectural option open.
