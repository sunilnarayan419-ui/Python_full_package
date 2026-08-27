"""convert status to enum type and add a partial index for active jobs

Revision ID: 0003
Revises: 0002
Create Date: 2025-03-05 09:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

job_status_enum = sa.Enum("queued", "running", "completed", "failed", name="job_status")


def upgrade() -> None:
    job_status_enum.create(op.get_bind(), checkfirst=True)
    op.execute(
        "ALTER TABLE analysis_jobs "
        "ALTER COLUMN status TYPE job_status USING status::job_status"
    )
    op.create_index(
        "ix_analysis_jobs_active",
        "analysis_jobs",
        ["experiment_id"],
        postgresql_where=sa.text("status IN ('queued', 'running')"),
    )


def downgrade() -> None:
    op.drop_index("ix_analysis_jobs_active", table_name="analysis_jobs")
    op.execute("ALTER TABLE analysis_jobs ALTER COLUMN status TYPE VARCHAR(16) USING status::text")
    job_status_enum.drop(op.get_bind(), checkfirst=True)
