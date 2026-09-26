# Inbox Cleanup Protocol — Transaction Discipline Addition

**Date:** 2026-07-30  
**Raised by:** Admiral (Carly R. Anderson)  
**Status:** RECOMMENDED FOR ADOPTION

---

## Issue

`/empirica:inbox-cleanup` function exists but is NOT integrated into PREFLIGHT or POSTFLIGHT boundaries. This creates a **transaction discipline gap**: inbox state (part of `context` vector) can contain noise from prior transactions.

---

## Recommendation: Pre-PREFLIGHT Placement

**Formal protocol:**

```bash
# Step 1: Clean inbox state (outside measurement window)
empirica inbox-cleanup

# Step 2: Open measurement window
empirica preflight-submit - << 'EOF'
{
  "task_outcome": "...",
  "vectors": {...},
  ...
}
EOF

# Step 3-N: Noetic → CHECK → Praxic phases
[transaction work]

# Final: Close measurement window
empirica postflight-submit - << 'EOF'
{
  "task_outcome": "...",
  "vectors": {...},
  ...
}
EOF
```

---

## Why Pre-PREFLIGHT (Not Post-POSTFLIGHT)

| Aspect | Pre-PREFLIGHT | Post-POSTFLIGHT |
|--------|---------------|-----------------|
| **context vector baseline** | ✅ Clean slate | ❌ Includes prior noise |
| **state vector accuracy** | ✅ Clear starting point | ❌ Mixed with transaction state |
| **measurement integrity** | ✅ Uncontaminated | ❌ Prior work leaks in |
| **logical flow** | ✅ Clean → measure → execute | ❌ Measure → execute → clean |

---

## Integration Points

### For Phase 2 Weekly Standups
```bash
# Every standup session (Track A Tues, Track B Wed):
empirica inbox-cleanup  # Clear prior-week proposals
empirica preflight-submit  # Open measurement window
[standup work]
empirica postflight-submit  # Close measurement window
```

### For General Transaction Discipline
Add to `/epistemic-transaction` skill:
- Pre-PREFLIGHT: `empirica inbox-cleanup` (required step)
- Rationale: Inbox state is part of `context` vector; clean baseline ensures uncontaminated measurement

---

## Action Items

- [ ] Admiral confirms this protocol for Phase 2 adoption
- [ ] Update `/epistemic-transaction` skill to include pre-PREFLIGHT cleanup step
- [ ] Update system prompt transaction discipline section
- [ ] Begin Week 2 standups with `inbox-cleanup` pre-PREFLIGHT

---

**Status:** RECOMMENDED FOR ADOPTION  
**Authority:** Admiral (Carly R. Anderson)

