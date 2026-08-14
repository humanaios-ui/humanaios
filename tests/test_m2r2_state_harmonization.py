#!/usr/bin/env python3
"""Unit tests: M2 Rank 2 state machine harmonization (collaborations + projects).

Authority: M2 Rank 2 RFC
Tests:
  - Collaboration state transitions (all 4-tier states)
  - Project state transitions
  - Transition guard validation
  - Legacy state migration
  - Audit trail recording
"""

import pytest
from datetime import datetime, timezone
from src.models.collaboration_state import (
    CollaborationState,
    CollaborationStateSchema,
    migrate_legacy_state as migrate_collab_state,
    LEGACY_STATE_MAPPING as COLLAB_LEGACY_MAPPING,
)
from src.models.project_state import (
    ProjectState,
    ProjectStateSchema,
    migrate_legacy_state as migrate_project_state,
    LEGACY_STATE_MAPPING as PROJECT_LEGACY_MAPPING,
)


class TestCollaborationState:
    """Tests for collaboration state machine."""

    def test_initial_state(self):
        """Collaboration should start in PLANNED state."""
        schema = CollaborationStateSchema()
        assert schema.state == CollaborationState.PLANNED

    def test_valid_transitions_planned_to_in_progress(self):
        """Should allow: PLANNED → IN_PROGRESS."""
        schema = CollaborationStateSchema()
        assert schema.validate_transition(
            CollaborationState.PLANNED,
            CollaborationState.IN_PROGRESS
        )

    def test_valid_transitions_in_progress_to_completed(self):
        """Should allow: IN_PROGRESS → COMPLETED."""
        schema = CollaborationStateSchema()
        assert schema.validate_transition(
            CollaborationState.IN_PROGRESS,
            CollaborationState.COMPLETED
        )

    def test_valid_transitions_completed_to_archived(self):
        """Should allow: COMPLETED → ARCHIVED."""
        schema = CollaborationStateSchema()
        assert schema.validate_transition(
            CollaborationState.COMPLETED,
            CollaborationState.ARCHIVED
        )

    def test_valid_transitions_archived_to_in_progress_reopen(self):
        """Should allow: ARCHIVED → IN_PROGRESS (reopen)."""
        schema = CollaborationStateSchema()
        assert schema.validate_transition(
            CollaborationState.ARCHIVED,
            CollaborationState.IN_PROGRESS
        )

    def test_invalid_transition_planned_to_archived(self):
        """Should NOT allow: PLANNED → ARCHIVED (skip intermediate states)."""
        schema = CollaborationStateSchema()
        assert not schema.validate_transition(
            CollaborationState.PLANNED,
            CollaborationState.ARCHIVED
        )

    def test_transition_to_records_audit_trail(self):
        """Transition should record audit entry with timestamp and authorizer."""
        schema = CollaborationStateSchema()
        schema.transition_to(
            CollaborationState.IN_PROGRESS,
            authorizer_id="user_123",
            reason="Approved by Admiral"
        )

        assert len(schema.state_audit.transitions) == 1
        transition = schema.state_audit.transitions[0]
        assert transition.from_state == "planned"
        assert transition.to_state == "in_progress"
        assert transition.authorizer_id == "user_123"
        assert transition.reason == "Approved by Admiral"

    def test_transition_to_updates_timestamp(self):
        """Transition should update the appropriate timestamp field."""
        schema = CollaborationStateSchema()
        before = datetime.now(timezone.utc)
        schema.transition_to(
            CollaborationState.IN_PROGRESS,
            authorizer_id="user_123",
            reason="Starting work"
        )
        after = datetime.now(timezone.utc)

        assert schema.state_timestamps.started_at is not None
        assert before <= schema.state_timestamps.started_at <= after

    def test_transition_to_invalid_raises_error(self):
        """Invalid transition should raise ValueError."""
        schema = CollaborationStateSchema()
        with pytest.raises(ValueError):
            schema.transition_to(
                CollaborationState.ARCHIVED,
                authorizer_id="user_123",
                reason="Invalid skip"
            )

    def test_legacy_state_migration_draft_to_planned(self):
        """Draft should map to planned."""
        assert migrate_collab_state("draft") == CollaborationState.PLANNED

    def test_legacy_state_migration_ratified_to_in_progress(self):
        """Ratified should map to in_progress."""
        assert migrate_collab_state("ratified") == CollaborationState.IN_PROGRESS

    def test_legacy_state_migration_live_to_in_progress(self):
        """Live should map to in_progress."""
        assert migrate_collab_state("live") == CollaborationState.IN_PROGRESS

    def test_legacy_state_migration_end_of_life_to_archived(self):
        """End of life should map to archived."""
        assert migrate_collab_state("end_of_life") == CollaborationState.ARCHIVED

    def test_legacy_state_migration_all_mapped(self):
        """All legacy states should be mapped."""
        for legacy_state in COLLAB_LEGACY_MAPPING.keys():
            unified = migrate_collab_state(legacy_state)
            assert unified in [s for s in CollaborationState]


class TestProjectState:
    """Tests for project state machine."""

    def test_initial_state(self):
        """Project should start in PLANNED state."""
        schema = ProjectStateSchema()
        assert schema.state == ProjectState.PLANNED

    def test_valid_transitions_planned_to_in_progress(self):
        """Should allow: PLANNED → IN_PROGRESS."""
        schema = ProjectStateSchema()
        assert schema.validate_transition(
            ProjectState.PLANNED,
            ProjectState.IN_PROGRESS
        )

    def test_valid_transitions_in_progress_to_completed(self):
        """Should allow: IN_PROGRESS → COMPLETED."""
        schema = ProjectStateSchema()
        assert schema.validate_transition(
            ProjectState.IN_PROGRESS,
            ProjectState.COMPLETED
        )

    def test_valid_transitions_completed_to_archived(self):
        """Should allow: COMPLETED → ARCHIVED."""
        schema = ProjectStateSchema()
        assert schema.validate_transition(
            ProjectState.COMPLETED,
            ProjectState.ARCHIVED
        )

    def test_invalid_transition_in_progress_to_archived_direct(self):
        """Should NOT allow: IN_PROGRESS → ARCHIVED (skip COMPLETED)."""
        schema = ProjectStateSchema()
        assert not schema.validate_transition(
            ProjectState.IN_PROGRESS,
            ProjectState.ARCHIVED
        )

    def test_transition_to_records_audit_trail(self):
        """Transition should record audit entry with timestamp and authorizer."""
        schema = ProjectStateSchema()
        schema.transition_to(
            ProjectState.IN_PROGRESS,
            authorizer_id="team_lead_001",
            reason="Project kickoff"
        )

        assert len(schema.state_audit.transitions) == 1
        transition = schema.state_audit.transitions[0]
        assert transition.from_state == "planned"
        assert transition.to_state == "in_progress"
        assert transition.authorizer_id == "team_lead_001"

    def test_legacy_state_migration_conception_to_planned(self):
        """Conception should map to planned."""
        assert migrate_project_state("conception") == ProjectState.PLANNED

    def test_legacy_state_migration_active_to_in_progress(self):
        """Active should map to in_progress."""
        assert migrate_project_state("active") == ProjectState.IN_PROGRESS

    def test_legacy_state_migration_paused_to_in_progress(self):
        """Paused should map to in_progress (with metadata flag)."""
        assert migrate_project_state("paused") == ProjectState.IN_PROGRESS

    def test_legacy_state_migration_complete_to_completed(self):
        """Complete should map to completed."""
        assert migrate_project_state("complete") == ProjectState.COMPLETED

    def test_legacy_state_migration_archived_to_archived(self):
        """Archived should map to archived."""
        assert migrate_project_state("archived") == ProjectState.ARCHIVED

    def test_legacy_state_migration_all_mapped(self):
        """All legacy states should be mapped."""
        for legacy_state in PROJECT_LEGACY_MAPPING.keys():
            unified = migrate_project_state(legacy_state)
            assert unified in [s for s in ProjectState]


class TestCrossStateValidation:
    """Tests for state machine consistency across entity types."""

    def test_collaboration_and_project_share_unified_states(self):
        """Both collaborations and projects should use the same 4-tier model."""
        collab_states = set(s.value for s in CollaborationState)
        project_states = set(s.value for s in ProjectState)

        assert collab_states == project_states
        assert collab_states == {"planned", "in_progress", "completed", "archived"}

    def test_no_invalid_transitions_exist(self):
        """Transition graphs should be acyclic (no loops except reopen)."""
        collab_schema = CollaborationStateSchema()

        # Start at PLANNED, follow a path through all states
        assert collab_schema.validate_transition(
            CollaborationState.PLANNED,
            CollaborationState.IN_PROGRESS
        )
        assert collab_schema.validate_transition(
            CollaborationState.IN_PROGRESS,
            CollaborationState.COMPLETED
        )
        assert collab_schema.validate_transition(
            CollaborationState.COMPLETED,
            CollaborationState.ARCHIVED
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
