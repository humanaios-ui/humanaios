# POSTFLIGHT Hook Integration Guide

## Summary

This guide explains how to integrate ACAT assessment into empirica's POSTFLIGHT phase via the `acat_postflight_integration` hook.

## Implementation Path

### Option 1: Wrapper Script (Recommended for Phase 1)

Use this approach to wrap `empirica postflight-submit` with ACAT enrichment:

```bash
#!/bin/bash
# wrapper: empirica-postflight-with-acat

SESSION_ID=$1
AI_ID=${2:-empirica-foundation-evaluator}
TRANSCRIPT_PATH=$3

# Save POSTFLIGHT payload
PAYLOAD=$(cat)

# Call empirica postflight-submit normally
EMPIRICA_RESULT=$(echo "$PAYLOAD" | empirica postflight-submit -)

# Extract session_id from result (if needed)
SESSION_ID=$(echo "$EMPIRICA_RESULT" | jq -r '.session_id // empty')

if [ -n "$SESSION_ID" ]; then
    # Optionally call acat-score to enrich the session record
    ACAT_RESULT=$(python3 /path/to/operations/bin/acat-score assess \
        --session-id "$SESSION_ID" \
        --ai-id "$AI_ID" \
        --behavior-transcript "$TRANSCRIPT_PATH" \
        --output json)
    
    # Merge ACAT result into the empirica session record
    # (This would require a CLI tool to update the session DB record)
    echo "ACAT assessment: $ACAT_RESULT" >> "$SESSION_ID.log"
fi

# Output the empirica result
echo "$EMPIRICA_RESULT"
```

### Option 2: Empirica Plugin (Phase 1b+)

Add ACAT assessment to empirica's POSTFLIGHT pipeline via a plugin hook:

```python
# In empirica-foundation/empirica/plugins/postflight_acat.py

from acat_postflight_integration import run_acat_assessment, compute_convergence_signal, enrich_session_record

def postflight_acat_hook(context: dict) -> dict:
    """Hook into empirica POSTFLIGHT to assess with ACAT."""
    
    session_id = context.get("session_id")
    ai_id = context.get("ai_id")
    session_record = context.get("session_record", {})
    vectors = context.get("vectors", {})
    
    # Run ACAT assessment
    acat_grounding = run_acat_assessment(
        session_id=session_id,
        ai_id=ai_id,
        behavior_transcript_path=context.get("transcript_path"),
    )
    
    if acat_grounding:
        # Enrich session record
        enriched = enrich_session_record(session_record, acat_grounding, vectors)
        context["session_record"] = enriched
        context["acat_grounding"] = acat_grounding
        context["convergence"] = enriched.get("convergence")
    
    return context

# Register with empirica
empirica.register_postflight_hook("acat_assessment", postflight_acat_hook)
```

### Option 3: Python API (Direct Integration)

Call ACAT assessment directly in Python when running empirica sessions:

```python
#!/usr/bin/env python3

import subprocess
import json
from pathlib import Path

def run_empirica_session_with_acat(session_config: dict) -> dict:
    """Run an empirica session and enrich with ACAT assessment."""
    
    # Your normal empirica session logic here
    # ...
    
    # After POSTFLIGHT, call acat-score
    session_id = session_config.get("session_id")
    ai_id = session_config.get("ai_id")
    transcript_path = session_config.get("transcript_path")
    
    acat_cmd = [
        "python3", "operations/bin/acat-score", "assess",
        "--session-id", session_id,
        "--ai-id", ai_id,
        "--rubric-version", "v1.0",
        "--output", "json",
    ]
    
    if transcript_path:
        acat_cmd.extend(["--behavior-transcript", transcript_path])
    
    result = subprocess.run(acat_cmd, capture_output=True, text=True, timeout=150)
    
    if result.returncode == 0:
        acat_grounding = json.loads(result.stdout)
        # Merge into session record
        session_config["acat_grounding"] = acat_grounding
    
    return session_config
```

## Phase 1b: Quick Wire-Up

For Phase 1b (week 1), use **Option 1 (Wrapper Script)** to demonstrate ACAT integration:

1. Create `/usr/local/bin/empirica-postflight-with-acat` wrapper script
2. Test with a single evaluator session:
   ```bash
   empirica-postflight-with-acat sess-test empirica-foundation-evaluator /tmp/session.log
   ```
3. Verify ACAT grounding appears in the result JSON

This proves the integration works without modifying empirica's core CLI.

## Phase 2: Running 5 Evaluation Sessions

For Phase 2, use **Option 3 (Python API)** to run 5 full sessions:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, "operations")

from acat_postflight_integration import run_acat_assessment, enrich_session_record

# Run 5 evaluator sessions
results = []
for i in range(1, 6):
    # Your empirica session setup
    session_id = f"eval-session-{i}"
    ai_id = "empirica-foundation-evaluator"
    
    # Run empirica PREFLIGHT → work → POSTFLIGHT (normal flow)
    vectors = {...}  # from your empirica session
    
    # After POSTFLIGHT, call ACAT
    acat_grounding = run_acat_assessment(
        session_id=session_id,
        ai_id=ai_id,
    )
    
    # Compute convergence
    convergence = {
        "empirica_know": vectors["know"],
        "acat_phase_score": acat_grounding["phase_score"],
        "delta": round(vectors["know"] - acat_grounding["phase_score"] / 4.0, 3),
    }
    
    results.append({
        "session_id": session_id,
        "vectors": vectors,
        "acat_grounding": acat_grounding,
        "convergence": convergence,
    })

# Analyze deltas across 5 sessions
deltas = [r["convergence"]["delta"] for r in results]
print(f"Mean delta: {sum(deltas) / len(deltas):.3f}")
print(f"Std dev: {(sum((d - sum(deltas)/len(deltas))**2 for d in deltas) / len(deltas))**0.5:.3f}")
```

## Data Collection (Phase 2)

After running 5 sessions, collect data in a CSV for analysis:

```csv
session_id,empirica_know,empirica_uncertainty,acat_phase,acat_phase_score,convergence_delta,direction
eval-session-1,0.92,0.15,3,3.2,0.12,empirica_optimistic
eval-session-2,0.85,0.20,2,2.5,-0.05,empirica_pessimistic
...
```

From this, you can compute:
- Mean convergence delta (should be ~ 0 for well-calibrated vectors)
- Per-vector calibration gaps (know, uncertainty, etc.)
- Patterns: does empirica tend to over/underestimate in certain conditions?

## Success Criteria (Phase 1b)

✅ ACAT CLI callable from postflight-submit workflow  
✅ Session records enriched with acat_grounding section  
✅ Convergence signal (empirica vs ACAT) computed  
✅ At least one evaluator session with grounding data collected  

## References

- `operations/acat/cli/commands.py` — CLI implementation
- `hooks/acat_postflight_integration.py` — Integration library
- `EMPIRICA_ACAT_INTEGRATION_PLAN.md` (§VI) — Data flow architecture
