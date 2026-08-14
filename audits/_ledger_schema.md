# Humanaios Ledger Schema

Append-only ledgers capturing **predicted vs measured outcomes** across governance assessment, calibration, and communication domains. Mirrors SMAG pilot pattern with cross-ledger connectivity.

## Common Entry Structure

```json
{
  "ledger_id": "unique entry ID (UUID)",
  "ledger_type": "calibration_validation|governance_assessment|communication_calibration",
  "timestamp": "ISO 8601 when captured",
  "transaction_id": "empirica transaction ID",
  "session_id": "empirica session ID",
  
  "predicted": {
    "claim": "what we hypothesized would happen",
    "confidence": 0.0-1.0,
    "basis": "prior findings, pilot results, theory"
  },
  
  "measured": {
    "outcome": "what actually occurred",
    "evidence": "observable evidence",
    "grounding": "git commit, test result, finding ID"
  },
  
  "substrate": {
    "implementation": "how the work was executed",
    "scope": "what was covered",
    "limitations": "what was out of scope"
  },
  
  "gap_analysis": {
    "delta": "predicted - measured",
    "root_causes": ["list of why the delta exists"],
    "learning": "what this teaches us about the domain",
    "lsm_enriched": true|false,
    "enriched_by": "which LLM pass analyzed this"
  },
  
  "source_artifacts": [
    {
      "type": "finding|decision|assumption|unknown",
      "id": "empirica artifact ID",
      "title": "artifact title",
      "impact": 0.0-1.0
    }
  ],
  
  "cross_ledger_refs": {
    "operations_ledger": "SMAG ledger entry ID if related",
    "sibling_ledgers": ["other humanaios ledger entries this connects to"],
    "sync_status": "independent|sourced_from|informs"
  }
}
```

## Ledger Types

### calibration_validation_ledger.jsonl
Tracks ACAT calibration protocol validation against pre-registered gate criteria.

**Key fields:**
- `calibration_run`: v0.1|v0.2|v0.3
- `gate_criterion`: C1-C6 from CALIBRATION_VALIDATION_SYSTEM_PLAN
- `predicted.threshold`: pre-registered threshold
- `measured.result`: actual metric value
- `predicted.pass_criteria`: what constitutes success

### governance_assessment_ledger.jsonl
Tracks say-do gap discoveries and governance artifacts evaluated.

**Key fields:**
- `assessment_type`: repository_calibration|communication_gap|paradigm_boundary
- `artifact_evaluated`: repository name, resource, or system assessed
- `predicted.gap_hypothesis`: expected gap type and magnitude
- `measured.gaps_found`: actual gaps discovered

### communication_calibration_ledger.jsonl
Tracks Z1↔Z2 communication fidelity via clarification rates and causes.

**Key fields:**
- `predicted.clarification_rate`: expected rate per session
- `measured.clarification_events`: actual events observed
- `predicted.causes`: expected cause distribution (C1/C2/C3)
- `measured.causes`: actual cause distribution

## Cross-Ledger Connectivity

Entries reference each other via `cross_ledger_refs`:
- `sync_status: "sourced_from"` — this entry depends on findings from another ledger
- `sync_status: "informs"` — this entry provides input to another ledger
- `sync_status: "independent"` — parallel tracking, no dependency

Example: `calibration_validation` findings → inform `governance_assessment` hypotheses

## Workflow Integration

Each POSTFLIGHT transaction triggers:
1. Extract vectors, goals, findings
2. Match against ledger-relevant patterns
3. Auto-append entry to appropriate ledger(s)
4. Cross-link via `cross_ledger_refs`

See `.github/workflows/ledger-capture.yml` for implementation.
