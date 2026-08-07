"""M2R2 Phase 4: Create collaboration and project state tables for Supabase.

Revision ID: 001_m2r2_create_tables
Revises: None
Create Date: 2026-08-07

This is the initial migration creating tables for M2R2 state machine storage.
Uses JSONB columns for state serialization, with proper indexes for queries.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_m2r2_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create collaborations and projects tables with state machine support."""

    # Enable UUID extension (required for gen_random_uuid())
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create collaborations table
    op.create_table(
        "collaborations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("state_data", postgresql.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Index("idx_collaborations_created", "created_at"),
        sa.Index("idx_collaborations_updated", "updated_at"),
        sa.Index("idx_collaborations_archived", "archived_at"),
    )

    # Create projects table
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("state_data", postgresql.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Index("idx_projects_created", "created_at"),
        sa.Index("idx_projects_updated", "updated_at"),
        sa.Index("idx_projects_archived", "archived_at"),
    )

    # Create audit_log table for tracking state transitions
    op.create_table(
        "state_audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("entity_type", sa.Enum("collaboration", "project", name="entity_type_enum"), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("from_state", sa.String(50), nullable=False),
        sa.Column("to_state", sa.String(50), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("authorizer_id", sa.String(255), nullable=False),
        sa.Column("reason", sa.String(1000), nullable=True),
        sa.Index("idx_audit_entity", ["entity_type", "entity_id"]),
        sa.Index("idx_audit_timestamp", "timestamp"),
        sa.Index("idx_audit_state_change", ["from_state", "to_state"]),
    )


def downgrade() -> None:
    """Drop audit log, projects, and collaborations tables."""

    op.drop_table("state_audit_log")
    op.drop_table("projects")
    op.drop_table("collaborations")
    op.execute("DROP TYPE IF EXISTS entity_type_enum")
