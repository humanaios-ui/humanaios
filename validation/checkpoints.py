"""
T1.3: Validation Checkpoints

Four enforcement gates that reject temporal language and validate resource fields:

Checkpoint A: PREFLIGHT Submission
  - Validate schema (PreflightPayload)
  - Require resource_anchor fields
  - Require resource_scope_this_transaction
  - Reject temporal language in resource fields
  - Action on violation: REJECT with error message

Checkpoint B: CHECK Submission
  - Validate no temporal language in claim grounding
  - Grounding must be: read|ran|retrieved|assumed (not time-based)
  - Action on violation: REJECT with error message

Checkpoint C: POSTFLIGHT Submission
  - Validate schema (PostflightPayload)
  - Require resource_accounting_final fields
  - Reject temporal language in verdicts
  - Reject temporal language in evidence
  - Action on violation: REJECT with error message

Checkpoint D: Output Generation (Before User Sees)
  - Scan generated text for temporal language
  - Optionally: auto-rewrite or reject and force rewrite
  - Action on violation: LOG finding + (reject or allow with flag)
"""

from typing import Tuple, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from resource_accounting_schema import (
    PreflightPayload, PostflightPayload, validate_preflight, validate_postflight
)
from temporal_detection import TemporalDetector, validate_resource_field_for_temporal


class ViolationType(Enum):
    """Types of validation violations."""
    MISSING_REQUIRED_FIELD = "missing_required_field"
    SCHEMA_VALIDATION_ERROR = "schema_validation_error"
    TEMPORAL_LANGUAGE_IN_RESOURCE = "temporal_language_in_resource"
    TEMPORAL_LANGUAGE_IN_GROUNDING = "temporal_language_in_grounding"
    TEMPORAL_LANGUAGE_IN_VERDICT = "temporal_language_in_verdict"
    TEMPORAL_LANGUAGE_IN_OUTPUT = "temporal_language_in_output"


class CheckpointAction(Enum):
    """What to do when a violation is found."""
    REJECT = "reject"  # Reject submission, return error
    WARN = "warn"      # Warn but allow (log finding)
    LOG = "log"        # Silently log finding


@dataclass
class CheckpointViolation:
    """A checkpoint validation violation."""
    violation_type: ViolationType
    checkpoint: str  # "preflight", "check", "postflight", "output"
    message: str
    details: List[str]  # Specific violations
    field: str = ""  # Which field had the violation
    action: CheckpointAction = CheckpointAction.REJECT


# ============================================================================
# CHECKPOINT A: PREFLIGHT VALIDATION
# ============================================================================

class PreflightCheckpoint:
    """Validate PREFLIGHT payloads at submission time."""

    @staticmethod
    def validate(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """
        Validate PREFLIGHT payload.

        Returns: (is_valid, violations)
        """
        violations = []

        # 1. Schema validation
        is_valid, schema_errors = validate_preflight(payload)
        if not is_valid:
            for error in schema_errors:
                violations.append(CheckpointViolation(
                    violation_type=ViolationType.SCHEMA_VALIDATION_ERROR,
                    checkpoint="preflight",
                    message=f"Schema validation failed: {error}",
                    details=[error],
                    action=CheckpointAction.REJECT
                ))
            return False, violations

        # 2. Validate resource_anchor fields exist and have valid values
        if "resource_anchor" not in payload:
            violations.append(CheckpointViolation(
                violation_type=ViolationType.MISSING_REQUIRED_FIELD,
                checkpoint="preflight",
                message="Missing required field: resource_anchor",
                details=["resource_anchor is required (labor_hours_budget, ai_tokens_budget, decisions_pending)"],
                field="resource_anchor",
                action=CheckpointAction.REJECT
            ))
            return False, violations

        # 3. Validate resource_scope_this_transaction exists
        if "resource_scope_this_transaction" not in payload:
            violations.append(CheckpointViolation(
                violation_type=ViolationType.MISSING_REQUIRED_FIELD,
                checkpoint="preflight",
                message="Missing required field: resource_scope_this_transaction",
                details=["resource_scope_this_transaction is required (what_gets_consumed, what_should_change)"],
                field="resource_scope_this_transaction",
                action=CheckpointAction.REJECT
            ))
            return False, violations

        # 4. Scan resource fields for temporal language
        for field_name in ["task_context", "reasoning"]:
            if field_name in payload:
                is_clean, error = validate_resource_field_for_temporal(
                    field_name, payload[field_name]
                )
                if not is_clean:
                    violations.append(CheckpointViolation(
                        violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_RESOURCE,
                        checkpoint="preflight",
                        message=f"Temporal language in {field_name}",
                        details=[error],
                        field=field_name,
                        action=CheckpointAction.REJECT
                    ))

        return len(violations) == 0, violations


# ============================================================================
# CHECKPOINT B: CHECK VALIDATION
# ============================================================================

class CheckCheckpoint:
    """Validate CHECK payloads (gate between noetic and praxic)."""

    @staticmethod
    def validate(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """
        Validate CHECK payload.

        Returns: (is_valid, violations)
        """
        violations = []

        # Check if claims exist
        if "claims" not in payload or not payload["claims"]:
            return True, []  # No claims = nothing to validate

        # Validate each claim's grounding
        for i, claim in enumerate(payload["claims"]):
            if "grounding" not in claim:
                continue

            grounding_text = claim.get("grounding", "")

            # Grounding must be: read, ran, retrieved, assumed
            if grounding_text not in ["read", "ran", "retrieved", "assumed"]:
                violations.append(CheckpointViolation(
                    violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_GROUNDING,
                    checkpoint="check",
                    message=f"Invalid grounding in claim {i}: '{grounding_text}'",
                    details=[f"Grounding must be: read|ran|retrieved|assumed, got '{grounding_text}'"],
                    field=f"claims[{i}].grounding",
                    action=CheckpointAction.REJECT
                ))

            # Check claim description for temporal language
            if "claim" in claim:
                claim_text = claim["claim"]
                matches = TemporalDetector.find_all_matches(claim_text)
                if matches:
                    details = [f"  - {m.pattern_name}: '{m.matched_text}'" for m in matches[:3]]
                    violations.append(CheckpointViolation(
                        violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_GROUNDING,
                        checkpoint="check",
                        message=f"Temporal language in claim {i}",
                        details=details,
                        field=f"claims[{i}]",
                        action=CheckpointAction.REJECT
                    ))

        return len(violations) == 0, violations


# ============================================================================
# CHECKPOINT C: POSTFLIGHT VALIDATION
# ============================================================================

class PostflightCheckpoint:
    """Validate POSTFLIGHT payloads at submission time."""

    @staticmethod
    def validate(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """
        Validate POSTFLIGHT payload.

        Returns: (is_valid, violations)
        """
        violations = []

        # 1. Schema validation
        is_valid, schema_errors = validate_postflight(payload)
        if not is_valid:
            for error in schema_errors:
                violations.append(CheckpointViolation(
                    violation_type=ViolationType.SCHEMA_VALIDATION_ERROR,
                    checkpoint="postflight",
                    message=f"Schema validation failed: {error}",
                    details=[error],
                    action=CheckpointAction.REJECT
                ))
            return False, violations

        # 2. Validate resource_accounting_final fields
        if "resource_accounting_final" not in payload:
            violations.append(CheckpointViolation(
                violation_type=ViolationType.MISSING_REQUIRED_FIELD,
                checkpoint="postflight",
                message="Missing required field: resource_accounting_final",
                details=["resource_accounting_final is required (labor_hours_consumed, ai_tokens_consumed, etc)"],
                field="resource_accounting_final",
                action=CheckpointAction.REJECT
            ))
            return False, violations

        # 3. Validate claims_adjudication verdicts
        if "claims_adjudication" in payload:
            for i, adj in enumerate(payload["claims_adjudication"]):
                if "verdict" in adj:
                    verdict = adj["verdict"]

                    # Verdict must be: held, refuted, untested
                    if verdict not in ["held", "refuted", "untested"]:
                        violations.append(CheckpointViolation(
                            violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_VERDICT,
                            checkpoint="postflight",
                            message=f"Invalid verdict in adjudication {i}: '{verdict}'",
                            details=[f"Verdict must be: held|refuted|untested, got '{verdict}'"],
                            field=f"claims_adjudication[{i}].verdict",
                            action=CheckpointAction.REJECT
                        ))

                # Check evidence for temporal language
                if "evidence" in adj:
                    evidence_text = adj["evidence"]
                    matches = TemporalDetector.find_all_matches(evidence_text)
                    if matches:
                        details = [f"  - {m.pattern_name}: '{m.matched_text}'" for m in matches[:3]]
                        violations.append(CheckpointViolation(
                            violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_VERDICT,
                            checkpoint="postflight",
                            message=f"Temporal language in evidence for adjudication {i}",
                            details=details,
                            field=f"claims_adjudication[{i}].evidence",
                            action=CheckpointAction.REJECT
                        ))

        # 4. Scan reasoning for temporal language
        if "reasoning" in payload:
            matches = TemporalDetector.find_all_matches(payload["reasoning"])
            if matches:
                details = [f"  - {m.pattern_name}: '{m.matched_text}'" for m in matches[:3]]
                violations.append(CheckpointViolation(
                    violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_OUTPUT,
                    checkpoint="postflight",
                    message="Temporal language in reasoning",
                    details=details,
                    field="reasoning",
                    action=CheckpointAction.REJECT
                ))

        return len(violations) == 0, violations


# ============================================================================
# CHECKPOINT D: OUTPUT VALIDATION (Before User Sees)
# ============================================================================

class OutputCheckpoint:
    """Validate generated output before it reaches the user."""

    @staticmethod
    def validate(text: str) -> Tuple[bool, List[CheckpointViolation]]:
        """
        Scan generated output for temporal language.

        Returns: (is_clean, violations)
        """
        violations = []

        matches = TemporalDetector.find_all_matches(text)

        for match in matches:
            violations.append(CheckpointViolation(
                violation_type=ViolationType.TEMPORAL_LANGUAGE_IN_OUTPUT,
                checkpoint="output",
                message=f"Temporal language detected in output: {match.pattern_name}",
                details=[
                    f"Pattern: {match.pattern_name}",
                    f"Text: '{match.matched_text}'",
                    f"Context: ...{match.context}..."
                ],
                action=CheckpointAction.LOG
            ))

        return len(violations) == 0, violations


# ============================================================================
# UNIFIED CHECKPOINT VALIDATOR
# ============================================================================

class CheckpointValidator:
    """Unified interface for all 4 checkpoints."""

    @staticmethod
    def validate_preflight(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """Validate PREFLIGHT at submission."""
        return PreflightCheckpoint.validate(payload)

    @staticmethod
    def validate_check(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """Validate CHECK at submission."""
        return CheckCheckpoint.validate(payload)

    @staticmethod
    def validate_postflight(payload: Dict[str, Any]) -> Tuple[bool, List[CheckpointViolation]]:
        """Validate POSTFLIGHT at submission."""
        return PostflightCheckpoint.validate(payload)

    @staticmethod
    def validate_output(text: str) -> Tuple[bool, List[CheckpointViolation]]:
        """Validate output before rendering to user."""
        return OutputCheckpoint.validate(text)

    @staticmethod
    def format_violations(violations: List[CheckpointViolation]) -> str:
        """Format violations for error message."""
        if not violations:
            return ""

        lines = [f"\n❌ Validation Errors ({len(violations)} found):\n"]
        for i, v in enumerate(violations, 1):
            lines.append(f"{i}. [{v.violation_type.value}] {v.message}")
            for detail in v.details[:3]:  # Max 3 details per violation
                lines.append(f"   {detail}")
            if len(v.details) > 3:
                lines.append(f"   ... and {len(v.details)-3} more details")

        return "\n".join(lines)
