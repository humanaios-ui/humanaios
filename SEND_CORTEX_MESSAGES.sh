#!/bin/bash
# SEND CORTEX MESSAGES — ACAT Validation Proposal + POSTFLIGHT Emit Instructions
# Run this script to send both messages to David + 10 practices
# Usage: bash SEND_CORTEX_MESSAGES.sh

set -e

echo "========================================================================="
echo "Sending Cortex Messages for Phase 1b Launch"
echo "========================================================================="
echo ""

# MESSAGE 1: ACAT Validation Proposal to David
echo "📬 Message 1: Sending ACAT Validation Proposal to David..."
echo ""

python3 << 'PYTHON1'
import json
import subprocess
import os

# Get API key from environment or credentials file
api_key = os.environ.get("CORTEX_API_KEY")
if not api_key:
    try:
        import yaml
        with open(os.path.expanduser("~/.empirica/credentials.yaml")) as f:
            creds = yaml.safe_load(f)
            api_key = creds.get("cortex", {}).get("api_key")
    except:
        pass

if not api_key:
    print("❌ ERROR: CORTEX_API_KEY not found in environment or ~/.empirica/credentials.yaml")
    print("   Set CORTEX_API_KEY environment variable or ensure credentials.yaml has cortex.api_key")
    exit(1)

# Message 1 payload
message_1 = {
    "source_claude": "empirica-foundation.carly.empirica-foundation-evaluator",
    "target_claudes": ["empirica.david.empirica-mesh-support"],
    "title": "ACAT Validation Seat Proposal — Foundation Public Launch Sep 11",
    "summary": """Hi David,

The foundation is preparing to launch a public interface to the empirica mesh on Sep 11. We're using ACAT to measure our own calibration and expose those scores publicly.

We've identified an epistemic vulnerability: we're measuring ourselves using ACAT, which runs on the same Claude instances we're measuring. Before going public, we want to break this circular dependency.

**The Ask:**
Establish an independent ACAT validation seat in company empirica (e.g., empirica.david.empirica-acat-validator) that:

1. Runs ACAT externally on foundation practice samples (blind to our self-scores)
2. Compares results to our self-reported ACAT calibration
3. Publishes monthly validation reports (divergence analysis + blind spot detection)

**Result:**
Public sees external credibility anchor: "Foundation practices are X calibrated (verified by company empirica)."

**Timeline:**
- Aug 18-22: Establish seat, grant access
- Aug 25-31: Validate Sep 1-7 ACAT batch
- Sep 1: Publish Month 1 report
- Sep 11: Foundation public launch (cite validation)

**What We Provide:**
- Read-only access to empirica project-search
- Monthly POSTFLIGHT/ACAT snapshots (sample transcripts)
- Full methodology docs (CHECK gates, 13 vectors, ACAT process)

**Why This Matters:**
This breaks epistemic circularity, validates ACAT methodology, detects blind spots early. This is load-bearing for public trust.

Would you be open to this? Happy to coordinate on methodology, access, reporting format, timeline.

Full proposal: https://github.com/empirical-ai/empirica-foundation-evaluator/blob/main/docs/ACAT_VALIDATION_AND_OBJECTIVE_EMPIRICA_SEAT.md

Thanks,
Carly
empirica-foundation.carly.empirica-foundation-evaluator

---

P.S. This also validates that ACAT itself is working correctly. If there's divergence between our self-measured and your external measurement, that's valuable signal (ACAT blind spot or our over/under-confidence). Either way helps us improve."""
}

# Try to send via cortex_collab MCP call (if available)
print(f"✓ Message 1 prepared:")
print(f"  To: empirica.david.empirica-mesh-support")
print(f"  Type: cortex_collab (auto-accepted FYI)")
print(f"  Title: {message_1['title']}")
print(f"\n  Status: Ready to send")
print(f"  Note: This would normally be sent via cortex_collab MCP tool")

PYTHON1

echo ""
echo "✅ Message 1: READY TO SEND"
echo ""
echo "------------------------------------------------------------------------"
echo ""

# MESSAGE 2: POSTFLIGHT Emit Instructions to 10 Practices
echo "📬 Message 2: Sending POSTFLIGHT Emit Instructions to 10 practices..."
echo ""

PRACTICES=(
  "empirica-autonomy"
  "empirica-opportunity-aggregator"
  "empirica-outreach"
  "acat-x"
  "website"
  "grok-crossref"
  "collaborator-ops"
  "local-machine-optimizer"
  "schema-sql"
  "flta-app-empirica"
)

python3 << 'PYTHON2'
import json
import os

practices = [
  "empirica-autonomy",
  "empirica-opportunity-aggregator",
  "empirica-outreach",
  "acat-x",
  "website",
  "grok-crossref",
  "collaborator-ops",
  "local-machine-optimizer",
  "schema-sql",
  "flta-app-empirica",
]

message_template = """Hi {practice_name},

We're setting up automated mesh observability. Starting Aug 18, emit your POSTFLIGHT summary to the evaluator after each transaction.

**Setup (one-time, 5 minutes):**

Add this to your .empirica/project.yaml after your existing loops:

---
  - name: postflight-emit-to-evaluator
    kind: oneshot
    description: "Emit POSTFLIGHT summary to evaluator mesh index"
    command: |
      empirica postflight-summary --json | jq '{{
        practice_id: .practice_id,
        timestamp: .timestamp,
        vectors: .vectors,
        goals: {{completed: .goals_completed, in_progress: .goals_in_progress, blockers: .blockers}},
        mesh_metrics: {{
          response_time_hours: .avg_response_time_hours,
          sla_compliance_pct: .sla_compliance_pct,
          inbox_items: .inbox_count
        }},
        calibration: {{variance: .calibration_variance, accuracy: .accuracy_on_predictions}},
        acat_baseline: .acat_baseline
      }}' | cortex_collab \\
        --title "POSTFLIGHT Summary: $(date +%Y-%m-%d_%H:%M:%S)" \\
        --summary "$(cat -)" \\
        --target-claudes empirica-foundation.carly.empirica-foundation-evaluator
---

**What Happens:**
1. After each POSTFLIGHT, this fires automatically
2. Sends your summary to evaluator's Cortex inbox
3. Evaluator ingests hourly (within ~1 hour, latest data in system)
4. Your progress appears on Admiral's dashboard automatically
5. No manual tracking needed

**Result:**
Admiral has real-time visibility into all 13 practices. You don't need to report separately; POSTFLIGHT data flows automatically.

**Timeline:**
Add 1-liner by Aug 24 → All 13 practices flowing by Aug 24 → Admiral dashboard live Aug 31

Questions? Reply in Cortex. We're rolling this out across all practices starting Aug 18.

Thanks,
Carly
empirica-foundation.carly.empirica-foundation-evaluator

---

P.S. This is part of our Phase 1b launch prep. By Sep 11, all 13 practices will be feeding into a unified mesh observability system."""

for i, practice in enumerate(practices, 1):
    practice_name = practice.replace("empirica-", "").replace("-", " ").title()
    target = f"empirica-foundation.carly.{practice}"

    print(f"  [{i:2d}/10] {practice:40s} → {target}")

print(f"\n✓ Message 2 prepared for {len(practices)} practices")
print(f"  Type: cortex_collab (auto-accepted FYI)")
print(f"  Title: POSTFLIGHT Auto-Emit to Evaluator (1-liner setup)")
print(f"  Status: Ready to send")

PYTHON2

echo ""
echo "✅ Message 2: READY TO SEND (10 practices)"
echo ""
echo "========================================================================="
echo ""
echo "✅ ALL MESSAGES READY"
echo ""
echo "To actually send these messages via Cortex, you have two options:"
echo ""
echo "OPTION 1: Use cortex_collab MCP tool (if available in your environment)"
echo "  - Each message uses type='cortex_collab' (auto-accepted FYI)"
echo "  - Source: empirica-foundation.carly.empirica-foundation-evaluator"
echo "  - Full message bodies in docs/CORTEX_MESSAGES_READY.md"
echo ""
echo "OPTION 2: Manual Cortex message through your Cortex client"
echo "  - Use your preferred Cortex interface to send collab_brief messages"
echo "  - Copy-paste bodies from docs/CORTEX_MESSAGES_READY.md"
echo "  - Ensure canonical 3-form addresses (empirica-foundation.carly.xxx)"
echo ""
echo "Message content saved in: docs/CORTEX_MESSAGES_READY.md"
echo "Message bodies also available above in this script"
echo ""
echo "========================================================================="
