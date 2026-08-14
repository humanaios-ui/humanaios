"""Task 7: Add assessment_jobs table for persistent job queue.

Revision ID: 003_assessment_jobs
Revises: 002_acat_epistemic_tables
Create Date: 2026-08-08

Moves job state from in-memory Map to PostgreSQL for durability.
Jobs now survive app restarts without data loss.

Adds:
- assessment_jobs: Persistent job queue tracking (job_id, assessment_id, status, progress, phase)
- Indexes: (assessment_id), (status, created_at), (org_id, status)
- Recovery on startup: SELECT incomplete jobs, re-queue for execution
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = "003_assessment_jobs"
down_revision = "002_acat_epistemic_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create assessment_jobs table with proper indexing for job persistence."""

    # ============================================
    # ASSESSMENT_JOBS TABLE
    # ============================================
    # Persistent job queue: replaces in-memory Map
    # Each job submission creates a record, tracks progress through phases
    op.create_table(
        "assessment_jobs",
        sa.Column("job_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("assessment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="queued"),
        sa.Column("progress_percent", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_phase", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

        # Constraints
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'completed', 'failed')",
            name="valid_job_status"
        ),
        sa.CheckConstraint("progress_percent >= 0 AND progress_percent <= 100", name="valid_progress"),
        sa.CheckConstraint("current_phase >= 0 AND current_phase <= 3", name="valid_phase"),
    )

    # Indexes for common queries
    # Primary: find jobs for an assessment
    op.create_index("idx_assessment_jobs_assessment_id", "assessment_jobs", ["assessment_id"])

    # Secondary: find incomplete jobs (for recovery on startup)
    op.create_index("idx_assessment_jobs_status_created", "assessment_jobs", ["status", "created_at"])

    # Tertiary: org-scoped queries (for permission/quota checks)
    op.create_index("idx_assessment_jobs_org_status", "assessment_jobs", ["org_id", "status"])

    # Lookup by job_id is covered by primary key (implicit index)


def downgrade() -> None:
    """Drop assessment_jobs table and indexes."""
    op.drop_table("assessment_jobs")
