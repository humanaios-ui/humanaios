#!/usr/bin/env python3
"""
Audit Findings Integrator v1.0

Converts repo_audit_v1_1.py JSON output → empirica log-artifacts batch format.

Pipeline:
1. Read audit_report.json (from audit tool)
2. Group findings by severity (P0/P1 → immediate, P2/P3 → deferred)
3. Transform to empirica artifact schema
4. Emit JSON for `empirica log-artifacts -` (batch ingest)
5. Link via sourced_from to CHECK gate fix decision

Usage:
  python3 repo_audit_v1_1.py > audit_report.json
  python3 audit_findings_integrator.py audit_report.json <project_id> <repo_name>
  # Output: findings_batch.json (ready for `empirica log-artifacts -` batch ingest)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def parse_args():
    """Parse CLI args: audit_report.json <project_id> <repo_name>"""
    if len(sys.argv) < 4:
        print("Usage: audit_findings_integrator.py <audit_report.json> <project_id> <repo_name>")
        print("  project_id: empirica project UUID (e.g., '428902a7-19dd-4598-b655-51a4a689934f')")
        print("  repo_name: descriptive name (e.g., 'humanaios-ui/operations')")
        sys.exit(1)
    return {
        "report_file": sys.argv[1],
        "project_id": sys.argv[2],
        "repo_name": sys.argv[3],
    }

def load_audit_report(report_file: str) -> Dict[str, Any]:
    """Load JSON audit report."""
    with open(report_file, "r") as f:
        return json.load(f)

def transform_finding_to_node(finding: Dict, repo_name: str, index: int) -> Dict[str, Any]:
    """
    Transform audit finding → empirica finding node.

    Empirica node schema (corrected):
    {
      "ref": "find_<unique>",
      "type": "finding",
      "data": {
        "finding": "...",  # required field
        "impact": 0.0-1.0,
        "category": "link_broken|schema_missing|...",
        "details": {...}
      }
    }
    """
    method = finding.get("method", "unknown")
    category = finding.get("category", "untyped")
    severity = finding.get("severity", "P3")
    file_path = finding.get("file_path") or "repo"
    message = finding.get("message", "No message")

    # Map severity → impact (P0=0.9, P1=0.7, P2=0.4, P3=0.2)
    impact_map = {"P0": 0.9, "P1": 0.7, "P2": 0.4, "P3": 0.2}
    impact = impact_map.get(severity, 0.2)

    # Generate UNIQUE ref per finding (not grouped by method+category)
    node_ref = f"find_{repo_name.replace('/', '_')}_{index}"

    return {
        "ref": node_ref,
        "type": "finding",
        "data": {
            "finding": message,  # empirica requires this field
            "impact": impact,
            "category": category,
            "severity": severity,
            "method": method,
            "file_path": file_path,
            "line": finding.get("line"),
            "details": finding.get("details", {}),
            "enrichment": finding.get("enrichment"),
        }
    }

def create_batch_payload(findings: List[Dict], project_id: str, repo_name: str) -> Dict:
    """
    Create batch JSON for `empirica log-artifacts -`.

    Schema:
    {
      "project_id": "<UUID>",
      "nodes": [...],
      "edges": [
        {"from": "find_...", "to": "decision_...", "relation": "sourced_from"},
        ...
      ]
    }
    """
    nodes = [transform_finding_to_node(f, repo_name, i) for i, f in enumerate(findings)]

    # Split by severity: P0/P1 are immediate, P2/P3 are deferred
    p0p1_indices = [i for i, f in enumerate(findings) if f.get("severity") in ("P0", "P1")]

    # Create edges linking P0/P1 findings to the CHECK gate fix decision
    # (the human decision for improving empirica-evaluator CHECK discipline)
    edges = []
    for idx in p0p1_indices:
        node_ref = f"find_{repo_name.replace('/', '_')}_{idx}"
        edges.append({
            "from": node_ref,
            "to": "decision_check_gate_discipline_fix_empirica_evaluator",
            "relation": "sourced_from",
        })

    payload = {
        "project_id": project_id,
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "source": "repo_audit_v1_1",
            "repo": repo_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(findings),
                "p0": sum(1 for f in findings if f["severity"] == "P0"),
                "p1": sum(1 for f in findings if f["severity"] == "P1"),
                "p2": sum(1 for f in findings if f["severity"] == "P2"),
                "p3": sum(1 for f in findings if f["severity"] == "P3"),
            }
        }
    }
    return payload

def main():
    args = parse_args()

    # Load audit report
    try:
        report = load_audit_report(args["report_file"])
    except FileNotFoundError:
        print(f"Error: {args['report_file']} not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {args['report_file']} is not valid JSON", file=sys.stderr)
        sys.exit(1)

    # Extract findings
    findings = report.get("findings", [])
    if not findings:
        print("Warning: No findings in audit report", file=sys.stderr)
        findings = []

    # Transform to empirica batch
    batch = create_batch_payload(findings, args["project_id"], args["repo_name"])

    # Emit JSON to stdout (ready for `empirica log-artifacts -`)
    print(json.dumps(batch, indent=2))

    # Also print a summary to stderr
    meta = batch["metadata"]["summary"]
    print(
        f"\n📊 Audit Integration Summary:",
        f"\n   Total findings: {meta['total']}",
        f"\n   P0 (Critical): {meta['p0']}",
        f"\n   P1 (High): {meta['p1']}",
        f"\n   P2 (Medium): {meta['p2']}",
        f"\n   P3 (Low): {meta['p3']}",
        f"\n   → Ready for: empirica log-artifacts - < findings_batch.json",
        file=sys.stderr,
    )

if __name__ == "__main__":
    main()
