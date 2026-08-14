"""M2R2 ORM Models for Supabase — SQLAlchemy integration with state machines.

Models for Collaboration and Project entities with embedded state machine support.
Uses JSONB columns to store serialized state schemas.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import Column, String, JSON, DateTime, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import declarative_base, Session

from .collaboration_state import CollaborationStateSchema, CollaborationState
from .project_state import ProjectStateSchema, ProjectState
from .state_utils import StateSerializer

Base = declarative_base()


class Collaboration(Base):
    """Collaboration entity with embedded state machine (Supabase backend)."""

    __tablename__ = "collaborations"
    __table_args__ = {"schema": "public"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)

    # State machine stored as JSONB
    state_data = Column(JSON, nullable=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    archived_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
    ):
        """Initialize collaboration in PLANNED state."""
        self.id = id or uuid4()
        self.name = name
        self.description = description

        # Initialize state machine in PLANNED state
        schema = CollaborationStateSchema()
        self.state_data = StateSerializer.serialize_collaboration(schema)

    @property
    def state_schema(self) -> CollaborationStateSchema:
        """Deserialize state machine from JSONB column."""
        return StateSerializer.deserialize_collaboration(self.state_data)

    @property
    def current_state(self) -> CollaborationState:
        """Get current state."""
        return self.state_schema.state

    def transition_to(
        self,
        new_state: CollaborationState,
        authorizer_id: str,
        reason: str,
    ) -> None:
        """Execute state transition and persist to database.

        Args:
            new_state: Target state
            authorizer_id: Who authorized the transition
            reason: Why the transition occurred

        Raises:
            ValueError: If transition is invalid
        """
        schema = self.state_schema
        schema.transition_to(new_state, authorizer_id, reason)
        self.state_data = StateSerializer.serialize_collaboration(schema)
        self.updated_at = datetime.now(timezone.utc)

        # Track archived timestamp
        if new_state == CollaborationState.ARCHIVED:
            self.archived_at = datetime.now(timezone.utc)

    def get_audit_trail(self) -> list[Dict[str, Any]]:
        """Get full audit trail of state transitions."""
        return self.state_schema.state_audit.transitions

    def time_in_current_state(self) -> Optional[float]:
        """Get seconds spent in current state."""
        from .state_utils import StateQuery

        return StateQuery.time_in_state(self.state_schema, self.current_state.value)

    def __repr__(self) -> str:
        return f"<Collaboration(id={self.id}, name={self.name}, state={self.current_state.value})>"


class Project(Base):
    """Project entity with embedded state machine (Supabase backend)."""

    __tablename__ = "projects"
    __table_args__ = {"schema": "public"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)

    # State machine stored as JSONB
    state_data = Column(JSON, nullable=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    archived_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
    ):
        """Initialize project in PLANNED state."""
        self.id = id or uuid4()
        self.name = name
        self.description = description

        # Initialize state machine in PLANNED state
        schema = ProjectStateSchema()
        self.state_data = StateSerializer.serialize_project(schema)

    @property
    def state_schema(self) -> ProjectStateSchema:
        """Deserialize state machine from JSONB column."""
        return StateSerializer.deserialize_project(self.state_data)

    @property
    def current_state(self) -> ProjectState:
        """Get current state."""
        return self.state_schema.state

    def transition_to(
        self,
        new_state: ProjectState,
        authorizer_id: str,
        reason: str,
    ) -> None:
        """Execute state transition and persist to database.

        Args:
            new_state: Target state
            authorizer_id: Who authorized the transition
            reason: Why the transition occurred

        Raises:
            ValueError: If transition is invalid
        """
        schema = self.state_schema
        schema.transition_to(new_state, authorizer_id, reason)
        self.state_data = StateSerializer.serialize_project(schema)
        self.updated_at = datetime.now(timezone.utc)

        # Track archived timestamp
        if new_state == ProjectState.ARCHIVED:
            self.archived_at = datetime.now(timezone.utc)

    def get_audit_trail(self) -> list[Dict[str, Any]]:
        """Get full audit trail of state transitions."""
        return self.state_schema.state_audit.transitions

    def time_in_current_state(self) -> Optional[float]:
        """Get seconds spent in current state."""
        from .state_utils import StateQuery

        return StateQuery.time_in_state(self.state_schema, self.current_state.value)

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, state={self.current_state.value})>"


# Helper functions for common queries

def create_collaboration(
    session: Session,
    name: str,
    description: Optional[str] = None,
) -> Collaboration:
    """Create a new collaboration in PLANNED state."""
    collab = Collaboration(name=name, description=description)
    session.add(collab)
    session.flush()
    return collab


def create_project(
    session: Session,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """Create a new project in PLANNED state."""
    project = Project(name=name, description=description)
    session.add(project)
    session.flush()
    return project


def get_collaboration_by_state(
    session: Session,
    state: CollaborationState,
) -> list[Collaboration]:
    """Query collaborations by current state."""
    # Note: In production, would use a computed column or denormalized field
    # For now, retrieve all and filter
    collabs = session.query(Collaboration).all()
    return [c for c in collabs if c.current_state == state]


def get_project_by_state(
    session: Session,
    state: ProjectState,
) -> list[Project]:
    """Query projects by current state."""
    # Note: In production, would use a computed column or denormalized field
    projects = session.query(Project).all()
    return [p for p in projects if p.current_state == state]


def get_recent_transitions(
    session: Session,
    entity_type: str = "collaboration",
    minutes: int = 60,
) -> list[Dict[str, Any]]:
    """Get recent state transitions (last N minutes)."""
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)

    if entity_type == "collaboration":
        collabs = session.query(Collaboration).filter(
            Collaboration.updated_at >= cutoff
        ).all()
        transitions = []
        for c in collabs:
            transitions.extend(c.get_audit_trail())
        return transitions
    elif entity_type == "project":
        projects = session.query(Project).filter(
            Project.updated_at >= cutoff
        ).all()
        transitions = []
        for p in projects:
            transitions.extend(p.get_audit_trail())
        return transitions
    else:
        return []
