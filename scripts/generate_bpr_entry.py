#!/usr/bin/env python3
"""
generate_bpr_entry.py -- Generate BPR (Behavioral Provenance Registry) entries from ACAT measurements.

Usage:
  python3 scripts/generate_bpr_entry.py \
    --protocol "ACAT-CAL-P v1.5 + Phase 1 Amendments" \
    --measurement-end "2026-09-14T23:59:59Z" \
    --measurement-start "2026-08-20T00:00:00Z" \
    --dimensions phase1-findings.json \
    --contamination-check phase1-contamination-results.json \
    --fingerprint-method "sha256-response-panel-v1" \
    --fingerprint-value "abc123def456..." \
    --output phase1-bpr-entry.yaml

Generates a BPR entry YAML file ready for validation and Z2 ratification.
"""

import sys
import json
import yaml
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import argparse

def canonical_hash(entry: dict) -> str:
    """Compute SHA256 hash of entry (with entry_hash field zeroed)."""
    e = json.loads(json.dumps(entry, default=str))
    e["provenance"]["ledger"]["entry_hash"] = ""
    blob = json.dumps(e, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def load_json_file(path: str) -> dict:
    """Load JSON file with error handling."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")

def generate_bpr_entry(
    protocol: str,
    measurement_start: str,
    measurement_end: str,
    dimensions: dict,
    contamination_check: dict,
    fingerprint_method: str,
    fingerprint_value: str,
    provider: str = "anthropic",
    model_string: str = "claude-opus-5-2026-08-15",
    api_surface: str = "/v1/messages",
) -> dict:
    """
    Generate a BPR entry dict conforming to BPR-SCHEMA v0.1.

    Args:
        protocol: Protocol ID (e.g., "ACAT-CAL-P v1.5 + Phase 1 Amendments")
        measurement_start: ISO 8601 start timestamp
        measurement_end: ISO 8601 end timestamp
        dimensions: Dict with per-dimension scores/spread
        contamination_check: Dict with contamination check results
        fingerprint_method: Build fingerprint method (e.g., "sha256-response-panel-v1")
        fingerprint_value: SHA256 hash of fingerprint
        provider: Model provider
        model_string: Exact model string sent to API
        api_surface: API endpoint family

    Returns:
        BPR entry dict ready for YAML serialization
    """

    # Parse measurement window
    try:
        start_dt = datetime.fromisoformat(measurement_start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(measurement_end.replace('Z', '+00:00'))
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {e}")

    # Generate entry ID (BPR-provider-model-YYYYMMDD-seq)
    date_str = end_dt.strftime("%Y%m%d")
    entry_id = f"BPR-{provider}-{model_string.split('-')[0]}-{date_str}-001"

    # Parse dimensions (expected: list of dicts with dimension_id, score, spread, etc.)
    if not isinstance(dimensions, list):
        raise ValueError("dimensions must be a list of dicts")

    # Validate each dimension has required fields
    required_dim_fields = ["dimension_id", "score", "spread", "evidence_class"]
    for dim in dimensions:
        missing = [f for f in required_dim_fields if f not in dim]
        if missing:
            raise ValueError(f"Dimension {dim.get('dimension_id', 'unknown')} missing fields: {missing}")

    # Build entry
    entry = {
        "registry": {
            "entry_id": entry_id,
            "schema_version": "0.1.0-draft",
            "status": "draft",  # Will be z2_ratified after Z2 approval
            "supersedes": None,
        },
        "model_identity": {
            "provider": provider,
            "model_string": model_string,
            "api_surface": api_surface,
            "access_path": "first_party_api",
            "build_fingerprint": {
                "method": fingerprint_method,
                "value": fingerprint_value,
                "note": "Cryptographically bound response panel hash"
            },
        },
        "measurement": {
            "protocol_id": protocol,
            "window": {
                "start_utc": measurement_start,
                "end_utc": measurement_end,
            },
            "probe_set": {
                "set_id": f"PHASE1-{date_str}-001",
                "publication_status": "held_out",
                "rotation_generation": 1,
                "contamination_check": {
                    "performed": contamination_check.get("performed", False),
                    "method": contamination_check.get("method"),
                    "design": contamination_check.get("design", "three_arm"),
                    "result": contamination_check.get("result"),
                    "inference_leakage_detected": contamination_check.get("inference_leakage_detected", False),
                },
            },
            "sampling": {
                "n_probes": contamination_check.get("n_probes", 120),
                "n_runs_per_probe": contamination_check.get("n_runs_per_probe", 5),
                "temperature_policy": "fixed 0.7 all runs",
                "seed_policy": "unseeded; dispersion carries the variance",
            },
        },
        "dimensions": dimensions,
        "deltas": None,
        "provenance": {
            "measured_by": "humanaios-phase1-measurement / carly",
            "z2_ratification": {
                "status": "pending",
                "ref": None,
            },
            "ledger": {
                "prev_entry_hash": "",  # Genesis entry
                "entry_hash": "TO_BE_COMPUTED_BY_VALIDATOR",
                "canonicalization": "json-c14n-sorted-keys-utf8",
            },
        },
        "validity": {
            "valid_until_utc": (end_dt + timedelta(days=30)).isoformat() + "Z",
            "expiry_basis": "hosted-API default 30d",
            "re_measurement_policy": "require_delta_reference",
        },
        "reflexivity": {
            "profile_awareness_probe": {
                "performed": True,
                "findings_embargo_window_days": 30,
                "embargo_reasoning": "Per-dimension findings held unpublished for 30 days to prevent reflexive training.",
                "embargo_end_utc": (end_dt + timedelta(days=30)).isoformat() + "Z",
            },
        },
    }

    return entry

def main():
    parser = argparse.ArgumentParser(description="Generate BPR entry from ACAT measurement")
    parser.add_argument("--protocol", required=True, help="Protocol ID (e.g., ACAT-CAL-P v1.5 + Phase 1 Amendments)")
    parser.add_argument("--measurement-start", required=True, help="ISO 8601 start timestamp")
    parser.add_argument("--measurement-end", required=True, help="ISO 8601 end timestamp")
    parser.add_argument("--dimensions", required=True, help="JSON file with per-dimension scores")
    parser.add_argument("--contamination-check", required=True, help="JSON file with contamination check results")
    parser.add_argument("--fingerprint-method", default="sha256-response-panel-v1", help="Build fingerprint method")
    parser.add_argument("--fingerprint-value", required=True, help="Build fingerprint SHA256 value")
    parser.add_argument("--provider", default="anthropic", help="Model provider")
    parser.add_argument("--model-string", default="claude-opus-5-2026-08-15", help="Model string")
    parser.add_argument("--api-surface", default="/v1/messages", help="API endpoint family")
    parser.add_argument("--output", required=True, help="Output YAML file")

    args = parser.parse_args()

    try:
        # Load input files
        dimensions = load_json_file(args.dimensions)
        contamination_check = load_json_file(args.contamination_check)

        # Generate entry
        entry = generate_bpr_entry(
            protocol=args.protocol,
            measurement_start=args.measurement_start,
            measurement_end=args.measurement_end,
            dimensions=dimensions,
            contamination_check=contamination_check,
            fingerprint_method=args.fingerprint_method,
            fingerprint_value=args.fingerprint_value,
            provider=args.provider,
            model_string=args.model_string,
            api_surface=args.api_surface,
        )

        # Write to YAML
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            yaml.dump(entry, f, default_flow_style=False, sort_keys=False)

        print(f"✓ BPR entry generated: {output_path}")
        print(f"  Entry ID: {entry['registry']['entry_id']}")
        print(f"  Protocol: {entry['measurement']['protocol_id']}")
        print(f"  Dimensions: {len(entry['dimensions'])}")
        print()
        print("Next step: Validate with bpr_validate.py")
        print(f"  python3 bpr_validate.py {output_path}")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
