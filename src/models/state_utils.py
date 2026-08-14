"""M2R2 State Machine Utilities — Serialization, querying, and integration helpers.

Provides:
  - JSON serialization/deserialization for state machines
  - State query and history utilities
  - State comparison and consistency checks
  - Integration helpers for domain logic
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import asdict

from .collaboration_state import CollaborationState, CollaborationStateSchema
from .project_state import ProjectState, ProjectStateSchema


class StateSerializer:
    """Serialize and deserialize state machines to/from JSON."""

    @staticmethod
    def serialize_collaboration(schema: CollaborationStateSchema) -> Dict[str, Any]:
        """Convert CollaborationStateSchema to JSON-serializable dict."""
        return {
            "state": schema.state.value,
            "timestamps": {
                "planned_at": schema.state_timestamps.planned_at.isoformat() if schema.state_timestamps.planned_at else None,
                "started_at": schema.state_timestamps.started_at.isoformat() if schema.state_timestamps.started_at else None,
                "completed_at": schema.state_timestamps.completed_at.isoformat() if schema.state_timestamps.completed_at else None,
                "archived_at": schema.state_timestamps.archived_at.isoformat() if schema.state_timestamps.archived_at else None,
            },
            "audit": {
                "transitions": [
                    {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "timestamp": t.timestamp.isoformat(),
                        "authorizer_id": t.authorizer_id,
                        "reason": t.reason,
                    }
                    for t in schema.state_audit.transitions
                ],
                "metadata": schema.state_audit.metadata,
            },
        }

    @staticmethod
    def serialize_project(schema: ProjectStateSchema) -> Dict[str, Any]:
        """Convert ProjectStateSchema to JSON-serializable dict."""
        return {
            "state": schema.state.value,
            "timestamps": {
                "planned_at": schema.state_timestamps.planned_at.isoformat() if schema.state_timestamps.planned_at else None,
                "started_at": schema.state_timestamps.started_at.isoformat() if schema.state_timestamps.started_at else None,
                "completed_at": schema.state_timestamps.completed_at.isoformat() if schema.state_timestamps.completed_at else None,
                "archived_at": schema.state_timestamps.archived_at.isoformat() if schema.state_timestamps.archived_at else None,
            },
            "audit": {
                "transitions": [
                    {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "timestamp": t.timestamp.isoformat(),
                        "authorizer_id": t.authorizer_id,
                        "reason": t.reason,
                    }
                    for t in schema.state_audit.transitions
                ],
                "metadata": schema.state_audit.metadata,
            },
        }

    @staticmethod
    def deserialize_collaboration(data: Dict[str, Any]) -> CollaborationStateSchema:
        """Reconstruct CollaborationStateSchema from JSON dict."""
        schema = CollaborationStateSchema()
        schema.state = CollaborationState(data["state"])

        # Restore timestamps
        ts = data.get("timestamps", {})
        schema.state_timestamps.planned_at = datetime.fromisoformat(ts["planned_at"]) if ts.get("planned_at") else None
        schema.state_timestamps.started_at = datetime.fromisoformat(ts["started_at"]) if ts.get("started_at") else None
        schema.state_timestamps.completed_at = datetime.fromisoformat(ts["completed_at"]) if ts.get("completed_at") else None
        schema.state_timestamps.archived_at = datetime.fromisoformat(ts["archived_at"]) if ts.get("archived_at") else None

        # Restore audit trail
        audit = data.get("audit", {})
        from .collaboration_state import StateTransition
        for t_data in audit.get("transitions", []):
            t = StateTransition(
                from_state=t_data["from_state"],
                to_state=t_data["to_state"],
                timestamp=datetime.fromisoformat(t_data["timestamp"]),
                authorizer_id=t_data["authorizer_id"],
                reason=t_data["reason"],
            )
            schema.state_audit.transitions.append(t)

        schema.state_audit.metadata = audit.get("metadata", {})

        return schema

    @staticmethod
    def deserialize_project(data: Dict[str, Any]) -> ProjectStateSchema:
        """Reconstruct ProjectStateSchema from JSON dict."""
        schema = ProjectStateSchema()
        schema.state = ProjectState(data["state"])

        # Restore timestamps
        ts = data.get("timestamps", {})
        schema.state_timestamps.planned_at = datetime.fromisoformat(ts["planned_at"]) if ts.get("planned_at") else None
        schema.state_timestamps.started_at = datetime.fromisoformat(ts["started_at"]) if ts.get("started_at") else None
        schema.state_timestamps.completed_at = datetime.fromisoformat(ts["completed_at"]) if ts.get("completed_at") else None
        schema.state_timestamps.archived_at = datetime.fromisoformat(ts["archived_at"]) if ts.get("archived_at") else None

        # Restore audit trail
        audit = data.get("audit", {})
        from .project_state import StateTransition
        for t_data in audit.get("transitions", []):
            t = StateTransition(
                from_state=t_data["from_state"],
                to_state=t_data["to_state"],
                timestamp=datetime.fromisoformat(t_data["timestamp"]),
                authorizer_id=t_data["authorizer_id"],
                reason=t_data["reason"],
            )
            schema.state_audit.transitions.append(t)

        schema.state_audit.metadata = audit.get("metadata", {})

        return schema


class StateQuery:
    """Query and analyze state machine history."""

    @staticmethod
    def transition_count(schema) -> int:
        """Count total state transitions."""
        return len(schema.state_audit.transitions)

    @staticmethod
    def time_in_state(schema, state_name: str) -> Optional[float]:
        """Calculate seconds spent in a given state.

        Returns None if state was never entered or not yet exited.
        """
        transitions = schema.state_audit.transitions
        if not transitions:
            return None

        entered_at = None
        exited_at = None

        for t in transitions:
            if t.to_state == state_name:
                entered_at = t.timestamp
            elif t.from_state == state_name and entered_at is not None:
                exited_at = t.timestamp
                break

        if entered_at is None:
            return None

        if exited_at is None and schema.state.value == state_name:
            exited_at = datetime.now(timezone.utc)

        if exited_at is None:
            return None

        return (exited_at - entered_at).total_seconds()

    @staticmethod
    def who_authorized(schema, state_from: str, state_to: str) -> Optional[str]:
        """Find who authorized a specific transition."""
        for t in schema.state_audit.transitions:
            if t.from_state == state_from and t.to_state == state_to:
                return t.authorizer_id
        return None

    @staticmethod
    def why_transitioned(schema, state_from: str, state_to: str) -> Optional[str]:
        """Find the reason for a specific transition."""
        for t in schema.state_audit.transitions:
            if t.from_state == state_from and t.to_state == state_to:
                return t.reason
        return None

    @staticmethod
    def transition_timeline(schema) -> List[Dict[str, Any]]:
        """Get ordered timeline of all state transitions."""
        return [
            {
                "from": t.from_state,
                "to": t.to_state,
                "timestamp": t.timestamp.isoformat(),
                "authorizer": t.authorizer_id,
                "reason": t.reason,
            }
            for t in schema.state_audit.transitions
        ]

    @staticmethod
    def is_recent_transition(schema, seconds: int = 3600) -> bool:
        """Check if state changed in the last N seconds."""
        if not schema.state_audit.transitions:
            return False

        last_transition = schema.state_audit.transitions[-1]
        elapsed = (datetime.now(timezone.utc) - last_transition.timestamp).total_seconds()

        return elapsed < seconds


class StateComparison:
    """Compare and validate state machine consistency."""

    @staticmethod
    def are_compatible(schema1, schema2) -> bool:
        """Check if two state schemas can be considered consistent.

        For testing/validation purposes.
        """
        return (
            schema1.state == schema2.state
            and len(schema1.state_audit.transitions) == len(schema2.state_audit.transitions)
        )

    @staticmethod
    def divergence_point(schema1, schema2) -> Optional[int]:
        """Find where two schemas' audit trails diverge.

        Returns index of first diverging transition, or None if identical.
        """
        min_len = min(
            len(schema1.state_audit.transitions),
            len(schema2.state_audit.transitions),
        )

        for i in range(min_len):
            t1 = schema1.state_audit.transitions[i]
            t2 = schema2.state_audit.transitions[i]

            if (
                t1.from_state != t2.from_state
                or t1.to_state != t2.to_state
                or t1.authorizer_id != t2.authorizer_id
            ):
                return i

        # Check if one has extra transitions
        if len(schema1.state_audit.transitions) != len(schema2.state_audit.transitions):
            return min_len

        return None

    @staticmethod
    def validate_state_consistency(schema) -> bool:
        """Validate that audit trail is consistent (no broken transitions).

        Returns True if all transitions form a valid path.
        """
        if not schema.state_audit.transitions:
            return schema.state.value == "planned"

        # First transition should start from planned
        first = schema.state_audit.transitions[0]
        if first.from_state != "planned":
            return False

        # Check that each transition connects to the previous
        prev_state = first.from_state
        for t in schema.state_audit.transitions:
            if t.from_state != prev_state:
                return False
            prev_state = t.to_state

        # Final transition should match current state
        return prev_state == schema.state.value
