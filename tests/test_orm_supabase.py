"""Tests for M2R2 Supabase ORM models — SQLAlchemy integration with state machines.

Note: This test suite uses in-memory dataclass simulation (not requiring SQLAlchemy
in dev environment). Real Supabase deployment uses SQLAlchemy + PostgreSQL.
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4
from dataclasses import dataclass, field

from src.models.collaboration_state import CollaborationState
from src.models.project_state import ProjectState
from src.models.state_utils import StateSerializer


@dataclass
class MockCollaboration:
    """In-memory mock of Collaboration ORM model for testing."""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    state_data: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    archived_at: datetime = None

    def __post_init__(self):
        if not self.state_data:
            from src.models.collaboration_state import CollaborationStateSchema

            schema = CollaborationStateSchema()
            self.state_data = StateSerializer.serialize_collaboration(schema)

    @property
    def current_state(self) -> CollaborationState:
        """Get current state."""
        from src.models.collaboration_state import CollaborationStateSchema

        schema = StateSerializer.deserialize_collaboration(self.state_data)
        return schema.state

    def transition_to(
        self,
        new_state: CollaborationState,
        authorizer_id: str,
        reason: str,
    ) -> None:
        """Execute state transition."""
        from src.models.collaboration_state import CollaborationStateSchema

        schema = StateSerializer.deserialize_collaboration(self.state_data)
        schema.transition_to(new_state, authorizer_id, reason)
        self.state_data = StateSerializer.serialize_collaboration(schema)
        self.updated_at = datetime.now(timezone.utc)

        if new_state == CollaborationState.ARCHIVED:
            self.archived_at = datetime.now(timezone.utc)

    def get_audit_trail(self):
        """Get audit trail."""
        from src.models.collaboration_state import CollaborationStateSchema

        schema = StateSerializer.deserialize_collaboration(self.state_data)
        return schema.state_audit.transitions


@dataclass
class MockProject:
    """In-memory mock of Project ORM model for testing."""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    state_data: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    archived_at: datetime = None

    def __post_init__(self):
        if not self.state_data:
            from src.models.project_state import ProjectStateSchema

            schema = ProjectStateSchema()
            self.state_data = StateSerializer.serialize_project(schema)

    @property
    def current_state(self) -> ProjectState:
        """Get current state."""
        from src.models.project_state import ProjectStateSchema

        schema = StateSerializer.deserialize_project(self.state_data)
        return schema.state

    def transition_to(
        self,
        new_state: ProjectState,
        authorizer_id: str,
        reason: str,
    ) -> None:
        """Execute state transition."""
        from src.models.project_state import ProjectStateSchema

        schema = StateSerializer.deserialize_project(self.state_data)
        schema.transition_to(new_state, authorizer_id, reason)
        self.state_data = StateSerializer.serialize_project(schema)
        self.updated_at = datetime.now(timezone.utc)

        if new_state == ProjectState.ARCHIVED:
            self.archived_at = datetime.now(timezone.utc)

    def get_audit_trail(self):
        """Get audit trail."""
        from src.models.project_state import ProjectStateSchema

        schema = StateSerializer.deserialize_project(self.state_data)
        return schema.state_audit.transitions


class TestCollaborationModel:
    """Tests for Collaboration ORM model (using in-memory mock)."""

    def test_create_collaboration_initial_state(self):
        """Create collaboration starts in PLANNED state."""
        collab = MockCollaboration(
            name="Test Collab",
            description="A test collaboration",
        )

        assert collab.name == "Test Collab"
        assert collab.description == "A test collaboration"
        assert collab.current_state == CollaborationState.PLANNED
        assert collab.id is not None

    def test_collaboration_state_persistence(self):
        """State can be serialized and deserialized."""
        collab = MockCollaboration(name="Test Collab")
        collab_id = collab.id
        state_data = collab.state_data

        # Simulate database roundtrip: create new object with same state data
        restored = MockCollaboration(id=collab_id, state_data=state_data.copy())

        assert restored.id == collab_id
        assert restored.current_state == CollaborationState.PLANNED

    def test_collaboration_transition(self):
        """Transition updates state."""
        collab = MockCollaboration(name="Test Collab")

        collab.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Starting work")

        assert collab.current_state == CollaborationState.IN_PROGRESS

    def test_collaboration_multiple_transitions(self):
        """Multiple transitions recorded in audit trail."""
        collab = MockCollaboration(name="Test Collab")

        collab.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        collab.transition_to(CollaborationState.COMPLETED, "user_2", "Done")

        audit = collab.get_audit_trail()

        assert len(audit) == 2
        assert audit[0].from_state == "planned"
        assert audit[1].to_state == "completed"

    def test_collaboration_archived_timestamp(self):
        """Archived state sets archived_at timestamp."""
        collab = MockCollaboration(name="Test Collab")

        assert collab.archived_at is None

        collab.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        collab.transition_to(CollaborationState.COMPLETED, "user_2", "Done")
        collab.transition_to(CollaborationState.ARCHIVED, "user_3", "Archive")

        assert collab.archived_at is not None

    def test_collaboration_invalid_transition_raises(self):
        """Invalid transition raises ValueError."""
        collab = MockCollaboration(name="Test Collab")

        # Try invalid transition: PLANNED → ARCHIVED
        with pytest.raises(ValueError):
            collab.transition_to(CollaborationState.ARCHIVED, "user_1", "Invalid")

    def test_collaboration_reopen(self):
        """Archived collaboration can be reopened."""
        collab = MockCollaboration(name="Test Collab")

        # Go through full lifecycle
        collab.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        collab.transition_to(CollaborationState.COMPLETED, "user_2", "Done")
        collab.transition_to(CollaborationState.ARCHIVED, "user_3", "Archive")

        # Reopen
        collab.transition_to(CollaborationState.IN_PROGRESS, "user_4", "Reopen")

        assert collab.current_state == CollaborationState.IN_PROGRESS


class TestProjectModel:
    """Tests for Project ORM model (using in-memory mock)."""

    def test_create_project_initial_state(self):
        """Create project starts in PLANNED state."""
        project = MockProject(
            name="Test Project",
            description="A test project",
        )

        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert project.current_state == ProjectState.PLANNED
        assert project.id is not None

    def test_project_state_persistence(self):
        """Project state can be serialized and deserialized."""
        project = MockProject(name="Test Project")
        project_id = project.id
        state_data = project.state_data

        # Simulate database roundtrip
        restored = MockProject(id=project_id, state_data=state_data.copy())

        assert restored.id == project_id
        assert restored.current_state == ProjectState.PLANNED

    def test_project_transition(self):
        """Project transition updates state."""
        project = MockProject(name="Test Project")

        project.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Kickoff")

        assert project.current_state == ProjectState.IN_PROGRESS

    def test_project_multiple_transitions(self):
        """Project records multiple transitions."""
        project = MockProject(name="Test Project")

        project.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Kickoff")
        project.transition_to(ProjectState.COMPLETED, "pm_2", "Closure")

        audit = project.get_audit_trail()

        assert len(audit) == 2
        assert audit[0].from_state == "planned"
        assert audit[1].to_state == "completed"

    def test_project_archived_timestamp(self):
        """Project archived state sets timestamp."""
        project = MockProject(name="Test Project")

        assert project.archived_at is None

        project.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Start")
        project.transition_to(ProjectState.COMPLETED, "pm_2", "Done")
        project.transition_to(ProjectState.ARCHIVED, "pm_3", "Archive")

        assert project.archived_at is not None

    def test_project_invalid_transition_raises(self):
        """Project invalid transition raises ValueError."""
        project = MockProject(name="Test Project")

        # Try invalid: IN_PROGRESS → ARCHIVED (skip COMPLETED)
        project.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Start")

        with pytest.raises(ValueError):
            project.transition_to(ProjectState.ARCHIVED, "pm_2", "Invalid")


class TestModelInteroperability:
    """Tests for collaboration and project working together."""

    def test_mixed_entities_in_memory(self):
        """Collaborations and projects can coexist in memory."""
        collab = MockCollaboration(name="Collab 1")
        project = MockProject(name="Project 1")

        # Transition both
        collab.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")
        project.transition_to(ProjectState.IN_PROGRESS, "pm_1", "Start")

        assert collab.current_state == CollaborationState.IN_PROGRESS
        assert project.current_state == ProjectState.IN_PROGRESS

    def test_multiple_entities_store_independently(self):
        """Multiple collaborations and projects track state independently."""
        collab1 = MockCollaboration(name="Collab 1")
        collab2 = MockCollaboration(name="Collab 2")
        project1 = MockProject(name="Project 1")

        # Transition only collab1
        collab1.transition_to(CollaborationState.IN_PROGRESS, "user_1", "Start")

        assert collab1.current_state == CollaborationState.IN_PROGRESS
        assert collab2.current_state == CollaborationState.PLANNED
        assert project1.current_state == ProjectState.PLANNED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
