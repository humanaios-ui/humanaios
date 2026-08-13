"""M2R2 Phase 5: Add ACAT assessment and epistemic artifact tables.

Revision ID: 002_acat_epistemic_tables
Revises: 001_m2r2_create_tables
Create Date: 2026-08-08

Adds foundation tables for Goal 2 (ACAT Protocol Service):
- assessments: Store AI system assessment submissions
- acat_protocol_runs: Track ACAT protocol step execution
- epistemic_artifacts: Store findings, decisions, assumptions, etc.
- epistemic_edges: Link artifacts together (grounded_by, evidence, resolves, etc.)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = "002_acat_epistemic_tables"
down_revision = "001_m2r2_create_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create ACAT and epistemic tables with proper indexing."""

    # ============================================
    # ASSESSMENTS TABLE
    # ============================================
    # Stores AI system assessment submissions
    op.create_table(
        "assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("system_id", sa.String(255), nullable=False),
        sa.Column("system_name", sa.String(255), nullable=False),
        sa.Column("system_info", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("result_summary", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),

        # Constraints
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.CheckConstraint("status IN ('pending', 'running', 'completed', 'failed')", name="valid_assessment_status"),
    )

    # Indexes for common queries
    op.create_index("idx_assessments_org_status", "assessments", ["org_id", "status"])
    op.create_index("idx_assessments_created", "assessments", ["created_at"])
    op.create_index("idx_assessments_status", "assessments", ["status"])
    op.create_index("idx_assessments_system", "assessments", ["system_id"])

    # ============================================
    # ACAT_PROTOCOL_RUNS TABLE
    # ============================================
    # Tracks ACAT protocol step execution with full audit trail
    op.create_table(
        "acat_protocol_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("assessment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("step_number", sa.Integer, nullable=False),
        sa.Column("step_name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("step_data", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("result_data", postgresql.JSONB, nullable=True),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),

        # Constraints
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.CheckConstraint("status IN ('pending', 'running', 'completed', 'failed')", name="valid_protocol_step_status"),
        sa.CheckConstraint("step_number >= 1 AND step_number <= 50", name="valid_step_number"),
    )

    # Indexes for protocol step queries
    op.create_index("idx_acat_runs_assessment", "acat_protocol_runs", ["assessment_id"])
    op.create_index("idx_acat_runs_step", "acat_protocol_runs", ["assessment_id", "step_number"])
    op.create_index("idx_acat_runs_created", "acat_protocol_runs", ["created_at"])
    op.create_index("idx_acat_runs_status", "acat_protocol_runs", ["status"])

    # ============================================
    # EPISTEMIC_ARTIFACTS TABLE
    # ============================================
    # Stores findings, decisions, assumptions, unknowns, dead-ends, mistakes
    # Full traceability of reasoning
    op.create_table(
        "epistemic_artifacts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("assessment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_id", sa.String(255), nullable=True),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("data", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("confidence", sa.Numeric(3, 2), nullable=True),
        sa.Column("impact", sa.Numeric(3, 2), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),

        # Constraints
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.CheckConstraint(
            "type IN ('finding', 'decision', 'assumption', 'unknown', 'dead_end', 'mistake')",
            name="valid_artifact_type"
        ),
        sa.CheckConstraint("status IN ('open', 'resolved', 'archived', 'superseded')", name="valid_artifact_status"),
    )

    # Indexes for artifact queries
    op.create_index("idx_artifacts_assessment", "epistemic_artifacts", ["assessment_id"])
    op.create_index("idx_artifacts_type", "epistemic_artifacts", ["type"])
    op.create_index("idx_artifacts_status", "epistemic_artifacts", ["status"])
    op.create_index("idx_artifacts_created", "epistemic_artifacts", ["created_at"])
    op.create_index("idx_artifacts_assessment_type", "epistemic_artifacts", ["assessment_id", "type"])

    # ============================================
    # EPISTEMIC_EDGES TABLE
    # ============================================
    # Links artifacts together (evidence, grounded_by, resolves, invalidates, etc.)
    op.create_table(
        "epistemic_edges",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relation", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

        # Constraints
        sa.ForeignKeyConstraint(["source_id"], ["epistemic_artifacts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_id"], ["epistemic_artifacts.id"], ondelete="CASCADE"),
        sa.CheckConstraint(
            "relation IN ('attached_to', 'caused_by', 'evidence', 'grounded_by', 'invalidates', 'prevents', 'raised_by', 'related', 'resolves', 'sourced_from')",
            name="valid_edge_relation"
        ),
        sa.UniqueConstraint("source_id", "target_id", "relation", name="unique_edge"),
    )

    # Indexes for graph traversal
    op.create_index("idx_edges_source", "epistemic_edges", ["source_id", "relation"])
    op.create_index("idx_edges_target", "epistemic_edges", ["target_id"])
    op.create_index("idx_edges_relation", "epistemic_edges", ["relation"])

    # ============================================
    # ORGANIZATION SCHEMA UPDATES
    # ============================================
    # Add columns to organizations if not exists (for future subscription tier)
    try:
        with op.batch_alter_table("organizations") as batch_op:
            batch_op.add_column(sa.Column("assessment_quota", sa.Integer, nullable=True))
    except Exception:
        # Column may already exist
        pass


def downgrade() -> None:
    """Drop ACAT and epistemic tables."""

    # Drop in reverse order of creation (edges before artifacts, artifacts before assessments)
    op.drop_table("epistemic_edges")
    op.drop_table("epistemic_artifacts")
    op.drop_table("acat_protocol_runs")
    op.drop_table("assessments")
