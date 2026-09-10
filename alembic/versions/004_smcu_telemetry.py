"""Add smcu_telemetry table for SMCU autonomous learning engine.

Revision ID: 004_smcu_telemetry
Revises: 003_assessment_jobs_persistence
Create Date: 2026-08-19

Adds:
- smcu_telemetry: Stores per-SMCU execution telemetry records used by the
  contextual bandit router and performance anomaly detector.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = "004_smcu_telemetry"
down_revision = "003_assessment_jobs_persistence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create smcu_telemetry table with indexes for bandit lookups."""

    op.create_table(
        "smcu_telemetry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("smcu_id", sa.Text, nullable=False),
        sa.Column("org_id", sa.Text, nullable=False),
        sa.Column("features", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("action_taken", sa.Text, nullable=False),
        sa.Column("reward", sa.Float, nullable=False),
        sa.Column("outcome", sa.Text, nullable=False, server_default=""),
        sa.Column("system_state", sa.Text, nullable=False, server_default="normal_load"),
        sa.Column("bugs_caught", sa.Integer, nullable=False, server_default="0"),
        sa.Column("duration_s", sa.Float, nullable=False, server_default="0"),
        sa.Column("cloud_cost", sa.Float, nullable=False, server_default="0"),
        sa.Column("is_exploration", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    # Fast lookup by SMCU ID for history queries
    op.create_index("ix_smcu_telemetry_smcu_id", "smcu_telemetry", ["smcu_id"])
    # Fast org-level scans
    op.create_index("ix_smcu_telemetry_org_id", "smcu_telemetry", ["org_id"])
    # Time-series queries (predictive scaling, 30-day look-backs)
    op.create_index("ix_smcu_telemetry_recorded_at", "smcu_telemetry", ["recorded_at"])


def downgrade() -> None:
    op.drop_index("ix_smcu_telemetry_recorded_at", table_name="smcu_telemetry")
    op.drop_index("ix_smcu_telemetry_org_id", table_name="smcu_telemetry")
    op.drop_index("ix_smcu_telemetry_smcu_id", table_name="smcu_telemetry")
    op.drop_table("smcu_telemetry")
