"""M2 Rank 2: Project state machine harmonization.

Unified 4-tier state model: planned → in_progress → completed → archived

Mapping from legacy states:
  conception → planned
  active → in_progress (use metadata.paused flag if paused)
  paused → in_progress (with metadata.paused=true)
  complete → completed
  archived → archived
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime, timezone


class ProjectState(str, Enum):
    """Unified project state (4-tier model)."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class StateTimestamp:
    """Track when each state was entered."""
    planned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None


@dataclass
class StateTransition:
    """Audit trail entry for a state change."""
    from_state: str
    to_state: str
    timestamp: datetime
    authorizer_id: str
    reason: str


@dataclass
class StateAudit:
    """Complete audit trail and metadata for state lifecycle."""
    transitions: List[StateTransition] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class ProjectStateSchema:
    """Schema for project state machine (for ORM/database)."""

    def __init__(self):
        self.state: ProjectState = ProjectState.PLANNED
        self.state_timestamps: StateTimestamp = StateTimestamp()
        self.state_audit: StateAudit = StateAudit()

    def validate_transition(self, from_state: ProjectState, to_state: ProjectState) -> bool:
        """Validate state transition rules."""
        valid_transitions = {
            ProjectState.PLANNED: [ProjectState.IN_PROGRESS],
            ProjectState.IN_PROGRESS: [ProjectState.COMPLETED, ProjectState.PLANNED],
            ProjectState.COMPLETED: [ProjectState.ARCHIVED, ProjectState.IN_PROGRESS],
            ProjectState.ARCHIVED: [ProjectState.IN_PROGRESS],  # reopen
        }
        return to_state in valid_transitions.get(from_state, [])

    def transition_to(self, new_state: ProjectState, authorizer_id: str, reason: str):
        """Execute a state transition with guards and audit trail."""
        if not self.validate_transition(self.state, new_state):
            raise ValueError(f"Invalid transition: {self.state.value} → {new_state.value}")

        # Record transition
        transition = StateTransition(
            from_state=self.state.value,
            to_state=new_state.value,
            timestamp=datetime.now(timezone.utc),
            authorizer_id=authorizer_id,
            reason=reason
        )
        self.state_audit.transitions.append(transition)

        # Update state and timestamp
        self.state = new_state
        now = datetime.now(timezone.utc)

        if new_state == ProjectState.PLANNED:
            self.state_timestamps.planned_at = now
        elif new_state == ProjectState.IN_PROGRESS:
            self.state_timestamps.started_at = now
        elif new_state == ProjectState.COMPLETED:
            self.state_timestamps.completed_at = now
        elif new_state == ProjectState.ARCHIVED:
            self.state_timestamps.archived_at = now


# Compatibility layer: alias old state names (1 release cycle)
LEGACY_STATE_MAPPING = {
    "conception": ProjectState.PLANNED,
    "active": ProjectState.IN_PROGRESS,
    "paused": ProjectState.IN_PROGRESS,  # paused status via metadata.paused flag
    "complete": ProjectState.COMPLETED,
    "archived": ProjectState.ARCHIVED,
}


def migrate_legacy_state(old_state: str) -> ProjectState:
    """Convert legacy state name to unified 4-tier model."""
    if old_state in LEGACY_STATE_MAPPING:
        return LEGACY_STATE_MAPPING[old_state]
    # If already in unified format, return as-is
    try:
        return ProjectState(old_state)
    except ValueError:
        raise ValueError(f"Unknown state: {old_state}")
