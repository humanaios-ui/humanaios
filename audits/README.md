# Measurement Ledgers: Predicted vs Measured Outcomes

Append-only ledgers capturing **predicted hypotheses vs measured outcomes** across governance assessment, calibration validation, and communication calibration work. Mechanical capture sink with optional LLM enrichment.

Mirror of [SMAG pilot ledger pattern](https://github.com/humanaios-ui/operations/issues/103) with cross-ledger connectivity to operations repository.

## Files

- **`calibration_validation_ledger.jsonl`** — ACAT instrument validation against pre-registered gate criteria
- **`governance_assessment_ledger.jsonl`** — Say-do gap discovery in governance artifacts
- **`communication_calibration_ledger.jsonl`** — Z1↔Z2 transmission fidelity via clarification rates
- **`_ledger_schema.md`** — Entry structure and field definitions
- **`CROSS_LEDGER_CONNECTIVITY.md`** — How these ledgers link to operations and each other

## Quick Start

### Reading a Ledger

Each line is a JSON entry (JSONL format):

```bash
# Pretty-print all entries
cat calibration_validation_ledger.jsonl | jq .

# Find entries by type
jq 'select(.gate_criterion == "instrument_pin_verification")' calibration_validation_ledger.jsonl

# Extract learning from governance assessments
jq -r '.gap_analysis.learning' governance_assessment_ledger.jsonl
```

### Adding an Entry (Manual)

After an empirica POSTFLIGHT, extract predicted/measured and append:

```bash
cat >> calibration_validation_ledger.jsonl << 'EOF'
{"ledger_id": "...", "timestamp": "...", "predicted": {...}, "measured": {...}, ...}
EOF
git add audits/calibration_validation_ledger.jsonl
git commit -m "chore(ledger): Manual entry from transaction XXX"
```

### Auto-Capture (Workflow)

The GitHub Actions workflow (`.github/workflows/ledger-capture.yml`) automatically:
1. Detects REGISTERED.md updates
2. Classifies by pattern (calibration / governance / communication)
3. Appends structured ledger entries
4. Posts PR comment with ledger status

Trigger: Push to main or PR that modifies REGISTERED.md or docs/calibration/

## Entry Structure

Every entry has:

```json
{
  "ledger_id": "unique ID",
  "ledger_type": "calibration_validation|governance_assessment|communication_calibration",
  "timestamp": "when captured",
  "transaction_id": "empirica transaction link",
  
  "predicted": {
    "claim": "what we thought would happen",
    "confidence": 0.0-1.0
  },
  
  "measured": {
    "outcome": "what actually happened",
    "evidence": "observable proof"
  },
  
  "gap_analysis": {
    "delta": "difference and why it matters",
    "root_causes": ["why did prediction differ"],
    "learning": "what this teaches us"
  },
  
  "cross_ledger_refs": {
    "operations_ledger": "SMAG entry ID if related",
    "sibling_ledgers": ["other humanaios ledgers this connects to"],
    "sync_status": "independent|sourced_from|informs"
  }
}
```

Full schema: [_ledger_schema.md](_ledger_schema.md)

## Learning Signals

### High-Signal Gaps
- Predicted and measured diverge significantly → root-cause analysis reveals model mismatch
- Same pattern appears across multiple entries → system insight, not noise
- Gap-analysis learning spans multiple ledgers → cross-domain pattern

### Low-Signal Gaps
- Single outlier with no corroboration
- Difference explainable by confounding variables, not the model
- Gap-analysis says "expected, working as designed"

## Connecting to Operations

Humanaios ledgers reference operations SMAG ledger via:
- `cross_ledger_refs.operations_ledger` — SMAG entry ID
- `cross_ledger_refs.sync_status` — relationship type

Example:
```json
{
  "ledger_id": "GOV-ASSESS-20260813-002",
  "cross_ledger_refs": {
    "operations_ledger": "SMAG-103",
    "sync_status": "sourced_from"
  }
}
```

This means: "Humanaios governance assessment findings are grounded in patterns observed during SMAG audit work."

See [CROSS_LEDGER_CONNECTIVITY.md](CROSS_LEDGER_CONNECTIVITY.md) for full mapping.

## Queries & Analysis

### "What's our prediction accuracy?"
```bash
# Compare predicted confidence to measured outcomes
jq -r '[.predicted.confidence, .gap_analysis.delta] | @csv' calibration_validation_ledger.jsonl
```

### "What's the most surprising finding?"
```bash
# Largest confidence ↔ outcome mismatch
jq -s 'max_by(.predicted.confidence - (.measured.outcome | length))' governance_assessment_ledger.jsonl
```

### "How many entries have cross-ledger links?"
```bash
# Count by sync_status
jq -r '.cross_ledger_refs.sync_status' *.jsonl | sort | uniq -c
```

### "Trace dependencies"
```bash
# All entries that inform or are sourced from others
jq -r 'select(.cross_ledger_refs.sibling_ledgers | length > 0)' audits/*.jsonl
```

## Integration with REGISTERED.md

Each ledger entry should link to source artifacts in REGISTERED.md via:
```json
"source_artifacts": [
  {
    "type": "finding|decision|assumption",
    "id": "empirica artifact ID",
    "title": "from REGISTERED.md",
    "impact": 0.0-1.0
  }
]
```

This makes the audit trail complete:
- REGISTERED.md (canonical findings) ← linked by →
- Ledger entries (predicted vs measured) ← linked by →
- Operations SMAG ledger (ecosystem observations)

## Maintenance

- **Append-only:** Never edit existing entries, only append
- **Versioned:** Use `ledger_id` with date-stamp + sequence for ordering
- **Atomic:** One entry per hypothesis-outcome pair
- **Linked:** Always populate `cross_ledger_refs` to connect the network
- **Enriched:** LLM pass can add `gap_analysis.root_causes` and `learning` after initial capture

## For Contributors

1. After running empirica POSTFLIGHT with findings:
2. Check which ledger type applies (calibration / governance / communication)
3. Extract predicted (from goal/assumption) and measured (from findings)
4. Identify cross-ledger refs (sibling dependencies, operations references)
5. Append as single JSON line
6. Commit with reference to transaction ID

**Do not close this directory** — it is the live capture sink for ongoing measurement work.

## References

- **SMAG Pilot Ledger (source pattern):** [operations/issues/103](https://github.com/humanaios-ui/operations/issues/103)
- **Ledger Schema:** [_ledger_schema.md](_ledger_schema.md)
- **Cross-Ledger Mapping:** [CROSS_LEDGER_CONNECTIVITY.md](CROSS_LEDGER_CONNECTIVITY.md)
- **Calibration Methodology:** [../docs/calibration/](../docs/calibration/)
- **Registry:** [../REGISTERED.md](../REGISTERED.md)
