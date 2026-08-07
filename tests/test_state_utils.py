"""Tests for M2R2 state machine utilities — serialization, querying, and validation."""

import pytest
from datetime import datetime, timezone, timedelta
from src.models.collaboration_state import CollaborationState, CollaborationStateSchema
from src.models.project_state import ProjectState, ProjectStateSchema
from src.models.state_utils import StateSerializer, StateQuery, StateComparison


class TestStateSerializer:
    """Tests for state serialization to/from JSON."""

    def test_serialize_collaboration_initial_state(self):
        """Serialize collaboration in initial (PLANNED) state."""
        schema = CollaborationStateSchema()
        data = StateSerializer.serialize_collaboration(schema)

        assert data["state"] == "planned"
        assert data["audit"]["transitions"] == []
        assert data["timestamps"]["planned_at"] is None

    def test_serialize_collaboration_with_transitions(self):
        """Serialize collaboration with multiple transitions."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Starting work")
        schema.transition_to(CollaborationState.COMPLETED, "user_1", "Done")

        data = StateSerializer.serialize_collaboration(schema)

        assert data["state"] == "completed"
        assert len(data["audit"]["transitions"]) == 2
        assert data["audit"]["transitions"][0]["from_state"] == "planned"
        assert data["audit"]["transitions"][1]["to_state"] == "completed"

    def test_deserialize_collaboration(self):
        """Deserialize collaboration back from JSON."""
        schema_orig = CollaborationStateSchema()
        schema_orig.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Starting work")

        data = StateSerializer.serialize_collaboration(schema_orig)
        schema_restored = StateSerializer.deserialize_collaboration(data)

        assert schema_restored.state == CollaborationState.IN_PROGRESS
        assert len(schema_restored.state_audit.transitions) == 1
        assert schema_restored.state_audit.transitions[0].authorizer_id == "user_1"

    def test_serialize_deserialize_roundtrip(self):
        """Serialize and deserialize multiple transitions without loss."""
        schema_orig = CollaborationStateSchema()
        schema_orig.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        schema_orig.transition_to(CollaborationState.COMPLETED, "user_2", "Finish")
        schema_orig.transition_to(CollaborationState.ARCHIVED, "user_3", "Archive")

        data = StateSerializer.serialize_collaboration(schema_orig)
        schema_restored = StateSerializer.deserialize_collaboration(data)

        assert StateComparison.are_compatible(schema_orig, schema_restored)
        assert len(schema_orig.state_audit.transitions) == len(schema_restored.state_audit.transitions)

    def test_serialize_project(self):
        """Serialize project state machine."""
        schema = ProjectStateSchema()
        schema.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Kickoff")

        data = StateSerializer.serialize_project(schema)

        assert data["state"] == "in_progress"
        assert len(data["audit"]["transitions"]) == 1
        assert data["audit"]["transitions"][0]["reason"] == "Kickoff"

    def test_deserialize_project(self):
        """Deserialize project from JSON."""
        schema_orig = ProjectStateSchema()
        schema_orig.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Kickoff")

        data = StateSerializer.serialize_project(schema_orig)
        schema_restored = StateSerializer.deserialize_project(data)

        assert schema_restored.state == ProjectState.IN_PROGRESS
        assert schema_restored.state_audit.transitions[0].reason == "Kickoff"


class TestStateQuery:
    """Tests for querying state machine history."""

    def test_transition_count(self):
        """Count total transitions in audit trail."""
        schema = CollaborationStateSchema()
        assert StateQuery.transition_count(schema) == 0

        schema.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        assert StateQuery.transition_count(schema) == 1

        schema.transition_to(CollaborationState.COMPLETED, "user_1", "Done")
        assert StateQuery.transition_count(schema) == 2

    def test_time_in_state_current(self):
        """Calculate time spent in current state."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")

        # Should be very small but positive (started recently)
        time_in_progress = StateQuery.time_in_state(schema, "in_progress")
        assert time_in_progress is not None
        assert time_in_progress >= 0

    def test_time_in_state_completed(self):
        """Calculate time spent in a completed state."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")

        # Sleep logic not used for testing; use timestamps directly
        # In real scenario, this would measure time between transition timestamps

        schema.transition_to(CollaborationState.COMPLETED, "user_1", "Done")
        time_in_progress = StateQuery.time_in_state(schema, "in_progress")

        assert time_in_progress is not None
        assert time_in_progress >= 0

    def test_time_in_state_nonexistent(self):
        """Time in a state that was never entered."""
        schema = CollaborationStateSchema()
        time_in_completed = StateQuery.time_in_state(schema, "completed")
        assert time_in_completed is None

    def test_who_authorized_transition(self):
        """Find who authorized a specific transition."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start work")

        authorizer = StateQuery.who_authorized(schema, "planned", "in_progress")
        assert authorizer == "alice"

        # Non-existent transition
        authorizer = StateQuery.who_authorized(schema, "completed", "archived")
        assert authorizer is None

    def test_why_transitioned(self):
        """Find the reason for a transition."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Ready to start")

        reason = StateQuery.why_transitioned(schema, "planned", "in_progress")
        assert reason == "Ready to start"

        # Non-existent transition
        reason = StateQuery.why_transitioned(schema, "completed", "archived")
        assert reason is None

    def test_transition_timeline(self):
        """Get timeline of all transitions."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        schema.transition_to(CollaborationState.COMPLETED, "bob", "Done")
        schema.transition_to(CollaborationState.ARCHIVED, "charlie", "Archive")

        timeline = StateQuery.transition_timeline(schema)

        assert len(timeline) == 3
        assert timeline[0]["from"] == "planned"
        assert timeline[0]["to"] == "in_progress"
        assert timeline[1]["authorizer"] == "bob"
        assert timeline[2]["reason"] == "Archive"

    def test_is_recent_transition(self):
        """Check if state changed recently."""
        schema = CollaborationStateSchema()
        assert not StateQuery.is_recent_transition(schema, 3600)

        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        assert StateQuery.is_recent_transition(schema, 3600)

        # Check with very short window (should still be true for just-created)
        assert StateQuery.is_recent_transition(schema, 1)


class TestStateComparison:
    """Tests for comparing and validating state machines."""

    def test_are_compatible_identical(self):
        """Compare two identical state machines."""
        schema1 = CollaborationStateSchema()
        schema2 = CollaborationStateSchema()

        assert StateComparison.are_compatible(schema1, schema2)

    def test_are_compatible_divergent(self):
        """Compare two divergent state machines."""
        schema1 = CollaborationStateSchema()
        schema1.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")

        schema2 = CollaborationStateSchema()
        schema2.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        schema2.transition_to(CollaborationState.COMPLETED, "bob", "Done")

        assert not StateComparison.are_compatible(schema1, schema2)

    def test_divergence_point_none(self):
        """Divergence point when schemas match."""
        schema1 = CollaborationStateSchema()
        schema1.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")

        schema2 = CollaborationStateSchema()
        schema2.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")

        assert StateComparison.divergence_point(schema1, schema2) is None

    def test_divergence_point_different_authorizer(self):
        """Divergence point when authorizers differ."""
        schema1 = CollaborationStateSchema()
        schema1.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")

        schema2 = CollaborationStateSchema()
        schema2.transition_to(CollaborationState.IN_PROGRESS, "bob", "Start")

        assert StateComparison.divergence_point(schema1, schema2) == 0

    def test_divergence_point_different_length(self):
        """Divergence point when audit trails have different lengths."""
        schema1 = CollaborationStateSchema()
        schema1.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")

        schema2 = CollaborationStateSchema()
        schema2.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        schema2.transition_to(CollaborationState.COMPLETED, "bob", "Done")

        divergence = StateComparison.divergence_point(schema1, schema2)
        assert divergence == 1

    def test_validate_state_consistency_valid(self):
        """Validate a consistent state machine."""
        schema = CollaborationStateSchema()
        assert StateComparison.validate_state_consistency(schema)

        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        assert StateComparison.validate_state_consistency(schema)

        schema.transition_to(CollaborationState.COMPLETED, "bob", "Done")
        assert StateComparison.validate_state_consistency(schema)

    def test_validate_state_consistency_matches_current(self):
        """Validate that audit trail matches current state."""
        schema = CollaborationStateSchema()
        schema.transition_to(CollaborationState.IN_PROGRESS, "alice", "Start")
        schema.transition_to(CollaborationState.COMPLETED, "bob", "Done")

        assert schema.state == CollaborationState.COMPLETED
        assert StateComparison.validate_state_consistency(schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
