# Cross-Ledger Connectivity: Humanaios ↔ Operations

This document describes how humanaios ledgers mirror and connect to the operations SMAG pilot ledger, supporting distributed learning across repositories.

## Architecture

### Ledger Network

```
operations/audits/
├── smag_pilot_ledger.jsonl (SMAG pilot: predicted → measured outcomes)
│
└─→ humanaios/audits/
    ├── calibration_validation_ledger.jsonl (ACAT instrument validation)
    ├── governance_assessment_ledger.jsonl (say-do gap discovery)
    └── communication_calibration_ledger.jsonl (Z1/Z2 transmission fidelity)
```

### Connection Patterns

Each humanaios ledger entry carries `cross_ledger_refs` identifying:

1. **`operations_ledger`** — Reference to SMAG ledger entry if related
   - Example: governance discoveries inform SMAG's artifact classification work
   - Sync status: `"sourced_from"` (dependent on SMAG findings)

2. **`sibling_ledgers`** — References to other humanaios ledgers
   - Example: calibration validation informs governance assessment hypotheses
   - Sync status: `"informs"` or `"sourced_from"`

3. **`sync_status`** — Relationship type
   - `"independent"` — Parallel tracking, no dependency
   - `"sourced_from"` — This entry depends on findings from another
   - `"informs"` — This entry provides input to another ledger

## Mapping: Current Transactions to Ledger Entries

### Integration Transaction (Session ff6fc1dd, Transaction e8f8a6c6)

**Research documents integrated from phone session S-081326.**

#### Calibration Validation Ledger
- **Entry:** CAL-VAL-20260813-001
- **Predicted:** ACAT-CAL-P version pin can be live-verified before baseline
- **Measured:** Pin verified (two repo refs + rubric version confirmed); protocol name doc location flagged as gap
- **Learning:** Live-fetch discipline outperforms self-report; IC-candidate documentation gap identified
- **Impact:** Blocks Step 1 of calibration protocol until Z2 resolves protocol name location

#### Governance Assessment Ledger
- **Entry 1:** GOV-ASSESS-20260813-001 (Counter-paradigm specimen)
  - Predicted: Paradigm dominance presumes no organized opposition
  - Measured: Live counter-paradigm instance found (GODMOD3.AI)
  - Learning: Opposition is organized, self-branded, at scale; paradigm boundary is porous
  - Cross-linked: Sourced from GODMOD3 code inspection, informs institutional paradigm hypothesis

- **Entry 2:** GOV-ASSESS-20260813-002 (Repository calibration baseline)
  - Predicted: Measurable say-do gaps exist in humanaios repo
  - Measured: VCS hygiene gap found (16 .pyc files), null-candidate ratio too small (n=16)
  - Learning: Gaps are discoverable by the instrument; VCS issue becomes test case
  - Cross-linked: Informs calibration validation (instrument being tested on this artifact)

#### Communication Calibration Ledger
- **Entry:** COMM-CAL-20260813-001
- **Predicted:** Communication fidelity measurable via clarification-request rate
- **Measured:** 7 clarification events in S-081326; Z1 self-inventory was miscalibrated (40% class-distribution error)
- **Learning:** Audit-against-ground-truth essential; C3 (decision-interface mismatch) is binding constraint
- **Cross-linked:** Independent from governance/calibration work, but communication clarity affects assessment accuracy

### Future Transactions (Placeholder Structure)

When new empirica transactions complete:

```json
{
  "ledger_id": "CAL-VAL-YYYYMMDD-NNN",
  "calibration_run": "v0.3|v0.4",
  "predicted": { ... },
  "measured": { ... },
  "cross_ledger_refs": {
    "operations_ledger": "SMAG-XXX (if this run is used for SMAG artifact auditing)",
    "sibling_ledgers": [
      "governance_assessment_ledger (findings inform next governance hypothesis)"
    ],
    "sync_status": "independent|sourced_from|informs"
  }
}
```

## Connectivity Benefits

### 1. Distributed Learning
- **Single source of truth per dimension:** Operations owns SMAG outcomes, humanaios owns calibration/governance/communication
- **No duplication:** Each ledger tracks what it owns; cross-refs prevent redundant capture

### 2. Hypothesis Refinement
- Governance discoveries (paradigm boundary findings) feed into next calibration run hypotheses
- Calibration validation results (say-do measurement effectiveness) inform governance assessment rigor
- Communication patterns constrain both governance clarity and calibration accuracy expectations

### 3. Instrument Validation
- ACAT instrument tested on humanaios (governance assessment) + operations (SMAG) = cross-repo validation
- If findings match across repos → instrument is robust
- If findings diverge → indicates repo-specific factors worth investigating

### 4. Ecosystem Observations
- Counter-paradigm specimen discovery (GODMOD3) tests institutional paradigm hypothesis across the ecosystem
- SMAG ledger records artifact auditing; humanaios records paradigm-boundary auditing
- Combined ledgers show whether governance frameworks apply across ideological divides

## Query Patterns

### "What do we know about say-do gaps in governance artifacts?"
→ Join humanaios `governance_assessment_ledger` with operations `smag_pilot_ledger`

### "How accurate is the ACAT instrument across different artifact types?"
→ Cross-ledger comparison: humanaios calibration validation results vs operations SMAG reliability

### "Are communication patterns consistent across Z-teams vs audit implementations?"
→ humanaios `communication_calibration_ledger` (Z1/Z2) vs operations patterns (if logged)

### "What's the learning curve on governance assessment?"
→ Time-series of humanaios `governance_assessment_ledger` entries over multiple sessions

## Maintenance

### Adding a New Ledger Entry Manually

1. **Identify the ledger type** (calibration / governance / communication)
2. **Extract** predicted, measured, substrate from empirica artifacts
3. **Populate** cross_ledger_refs:
   - Check if SMAG ledger has a related entry (operations/audits/smag_pilot_ledger.jsonl)
   - Check if other humanaios ledgers are sources or dependents
4. **Append** as a single JSON line to the appropriate ledger file
5. **Commit** with clear message linking to empirica transaction

### Syncing with Operations

The workflow hook (`.github/workflows/ledger-capture.yml`) auto-detects registry updates and appends ledger entries.

For cross-repo syncing (humanaios → operations):
- Operations SMAG ledger references humanaios findings via `cross_ledger_refs`
- Humanaios ledgers reference SMAG entry IDs when applicable
- No automatic sync; entries are linked by ID reference

## Example Cross-Ledger Query (CLI)

```bash
# Find all humanaios entries that reference operations ledger
jq -r '.cross_ledger_refs.operations_ledger' audits/*.jsonl | grep -v "null"

# Find entries with maximum learning value
jq -r 'select(.gap_analysis.learning | length > 100) | {ledger_id, timestamp, learning: .gap_analysis.learning}' audits/*.jsonl

# Trace dependency chain: governance → calibration → communication
jq -r '.ledger_id, .cross_ledger_refs.sibling_ledgers[]' audits/*.jsonl | sort | uniq
```

## Related Documentation

- [Ledger Schema](audits/_ledger_schema.md) — Entry structure and field definitions
- [SMAG Pilot Ledger](https://github.com/humanaios-ui/operations/issues/103) — Source pattern in operations
- [REGISTERED.md](../REGISTERED.md) — Zone 2 ratified findings (canonical source for ledger entries)
- [Calibration Validation System Plan](docs/calibration/CALIBRATION_VALIDATION_SYSTEM_PLAN_v0.3.yaml) — Methodology tracked by calibration_validation_ledger
