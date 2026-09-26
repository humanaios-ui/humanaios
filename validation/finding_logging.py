"""
T1.4: Automated Finding Logging

Wire checkpoint violations into empirica's finding-log system.
When a checkpoint detects a violation, automatically create a grounded finding with:
  - violation_type (temporal_language_in_resource, missing_required_field, etc)
  - violation_text (the actual text that violated)
  - pattern_matched (which regex pattern matched)
  - rejection_reason (why it was rejected)
  - validation_rule (which checkpoint rule triggered)
  - Full provenance edges: caused_by (session), grounded_by (validation_rule)

Findings are automatically logged to empirica's finding system, making violations
visible, auditable, and part of the epistemic graph.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json
from datetime import datetime

from checkpoints import CheckpointViolation, ViolationType


@dataclass
class FindingNode:
    """A finding artifact for log_artifacts."""
    ref: str  # e.g., "FND-A1", "FND-B2"
    type: str = "finding"
    data: Dict[str, Any] = None

    def to_dict(self):
        return {
            "ref": self.ref,
            "type": self.type,
            "data": self.data or {}
        }


@dataclass
class EdgeDefinition:
    """An edge between artifacts."""
    from_ref: str
    to_ref: str
    relation: str  # evidence, grounded_by, caused_by, etc
    description: str = ""

    def to_dict(self):
        return {
            "from": self.from_ref,
            "to": self.to_ref,
            "relation": self.relation,
            "description": self.description
        }


class ViolationLogger:
    """Log checkpoint violations as empirica findings."""

    # Map violation types to checkpoint names
    CHECKPOINT_MAP = {
        ViolationType.MISSING_REQUIRED_FIELD: "preflight",
        ViolationType.SCHEMA_VALIDATION_ERROR: "preflight",
        ViolationType.TEMPORAL_LANGUAGE_IN_RESOURCE: "preflight",
        ViolationType.TEMPORAL_LANGUAGE_IN_GROUNDING: "check",
        ViolationType.TEMPORAL_LANGUAGE_IN_VERDICT: "postflight",
        ViolationType.TEMPORAL_LANGUAGE_IN_OUTPUT: "output"
    }

    @staticmethod
    def violation_to_finding(
        violation: CheckpointViolation,
        session_id: str,
        finding_id_prefix: str = "FND"
    ) -> FindingNode:
        """
        Convert a checkpoint violation to a finding artifact.

        Args:
            violation: The checkpoint violation
            session_id: Session ID for causality edge
            finding_id_prefix: Prefix for finding ref (e.g., "FND-A1")

        Returns:
            FindingNode ready for log_artifacts
        """
        checkpoint_abbrev = {
            "preflight": "A",
            "check": "B",
            "postflight": "C",
            "output": "D"
        }.get(violation.checkpoint, "X")

        # Create finding ref
        finding_ref = f"{finding_id_prefix}-{checkpoint_abbrev}"

        # Build finding data
        finding_data = {
            "finding": (
                f"Resource-Accounting-Guard validation: "
                f"{violation.violation_type.value} in {violation.checkpoint} checkpoint"
            ),
            "description": violation.message,
            "violation_type": violation.violation_type.value,
            "checkpoint": violation.checkpoint,
            "field": violation.field,
            "rejection_reason": violation.action.value,
            "details": violation.details[:3] if violation.details else [],
            "impact": 0.9,  # Validation violations are high impact
            "epistemic_source": "automated_validation",
            "visibility": "local"
        }

        # Create the node
        finding = FindingNode(
            ref=finding_ref,
            type="finding",
            data=finding_data
        )

        return finding

    @staticmethod
    def create_log_artifacts_payload(
        violations: List[CheckpointViolation],
        session_id: str,
        checkpoint_name: str,
        finding_id_base: str = "FND"
    ) -> Dict[str, Any]:
        """
        Create a log_artifacts payload for a batch of violations.

        Args:
            violations: List of checkpoint violations
            session_id: Session ID for causality tracking
            checkpoint_name: Name of the checkpoint (preflight, check, etc)
            finding_id_base: Base for finding refs

        Returns:
            Dict ready to pass to empirica log_artifacts
        """
        if not violations:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []

        # Create findings
        for i, violation in enumerate(violations, 1):
            finding = ViolationLogger.violation_to_finding(
                violation, session_id, finding_id_base
            )
            nodes.append(finding.to_dict())

            # Edge: violation caused by this session
            edges.append({
                "from": finding.ref,
                "to": f"SESSION-{session_id}",
                "relation": "caused_by",
                "description": f"Violation detected in session {session_id}"
            })

            # Edge: grounded by validation rule
            validation_rule_ref = f"RULE-{checkpoint_name.upper()}-{violation.violation_type.value}"
            edges.append({
                "from": finding.ref,
                "to": validation_rule_ref,
                "relation": "grounded_by",
                "description": f"Validated by {checkpoint_name} checkpoint rule"
            })

        return {
            "nodes": nodes,
            "edges": edges
        }

    @staticmethod
    def format_for_empirica_cli(payload: Dict[str, Any]) -> str:
        """
        Format log_artifacts payload for empirica CLI.

        Returns JSON string ready to pipe to `empirica log_artifacts -`
        """
        return json.dumps(payload, indent=2)


class FindingCreator:
    """High-level API for creating findings from violations."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.violations: List[CheckpointViolation] = []

    def add_violation(self, violation: CheckpointViolation):
        """Add a violation to the batch."""
        self.violations.append(violation)

    def add_violations(self, violations: List[CheckpointViolation]):
        """Add multiple violations to the batch."""
        self.violations.extend(violations)

    def log_findings(self) -> Dict[str, Any]:
        """
        Log all violations as findings.

        Returns:
            log_artifacts payload ready for empirica
        """
        if not self.violations:
            return {"nodes": [], "edges": []}

        # Group by checkpoint
        by_checkpoint = {}
        for v in self.violations:
            checkpoint = v.checkpoint
            if checkpoint not in by_checkpoint:
                by_checkpoint[checkpoint] = []
            by_checkpoint[checkpoint].append(v)

        # Create findings for each checkpoint group
        all_nodes = []
        all_edges = []
        finding_counter = 1

        for checkpoint, violations_for_checkpoint in by_checkpoint.items():
            payload = ViolationLogger.create_log_artifacts_payload(
                violations_for_checkpoint,
                self.session_id,
                checkpoint,
                f"FND"
            )

            # Rename refs to ensure uniqueness
            for node in payload["nodes"]:
                old_ref = node["ref"]
                new_ref = f"FND-{finding_counter}"
                finding_counter += 1
                node["ref"] = new_ref

                # Update edge references
                for edge in payload["edges"]:
                    if edge["from"] == old_ref:
                        edge["from"] = new_ref

            all_nodes.extend(payload["nodes"])
            all_edges.extend(payload["edges"])

        return {
            "nodes": all_nodes,
            "edges": all_edges
        }

    def clear(self):
        """Clear the violation batch."""
        self.violations = []


# ============================================================================
# INTEGRATION HELPERS: Wire checkpoints to finding logging
# ============================================================================

def log_checkpoint_violations(
    violations: List[CheckpointViolation],
    session_id: str,
    checkpoint_name: str
) -> str:
    """
    Convert checkpoint violations to empirica log_artifacts JSON.

    Usage:
        violations = checkpoint.validate(payload)
        json_payload = log_checkpoint_violations(violations, session_id, "preflight")
        # Then: empirica log-artifacts - <<< json_payload

    Returns:
        JSON string ready for `empirica log-artifacts -`
    """
    payload = ViolationLogger.create_log_artifacts_payload(
        violations, session_id, checkpoint_name
    )
    return ViolationLogger.format_for_empirica_cli(payload)


def create_finding_batch(
    violations_by_checkpoint: Dict[str, List[CheckpointViolation]],
    session_id: str
) -> Dict[str, Any]:
    """
    Create a multi-checkpoint finding batch.

    Args:
        violations_by_checkpoint: {"preflight": [...], "check": [...], ...}
        session_id: Session ID

    Returns:
        log_artifacts payload with all findings
    """
    creator = FindingCreator(session_id)

    for checkpoint, violations in violations_by_checkpoint.items():
        creator.add_violations(violations)

    return creator.log_findings()


# ============================================================================
# EXAMPLE: Usage within checkpoint validation
# ============================================================================

def checkpoint_with_logging_example():
    """
    Example of how to integrate finding logging into checkpoint validation.

    In actual checkpoints.py, you would do:

    ```python
    from checkpoints import PreflightCheckpoint
    from finding_logging import log_checkpoint_violations

    # Validate and get violations
    is_valid, violations = PreflightCheckpoint.validate(payload)

    # If violations found, log them as findings
    if violations and session_id:
        json_payload = log_checkpoint_violations(
            violations, session_id, "preflight"
        )
        # Execute: empirica log-artifacts - <<< json_payload
    ```
    """
    pass
