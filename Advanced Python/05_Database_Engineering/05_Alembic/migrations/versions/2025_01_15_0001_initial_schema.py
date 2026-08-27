"""initial schema: experiments and analysis_jobs

Revision ID: 0001
Revises:
Create Date: 2025-01-15 09:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "experiments",
        sa.Column("experiment_id", sa.BigInteger(), primary_key=True),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("started_at", sa.Date(), nullable=False),
    )
    op.create_table(
        "analysis_jobs",
        sa.Column("analysis_job_id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "experiment_id",
            sa.BigInteger(),
            sa.ForeignKey("experiments.experiment_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(16), nullable=False, server_default="queued"),
    )
    op.create_index("ix_analysis_jobs_experiment_id", "analysis_jobs", ["experiment_id"])


def downgrade() -> None:
    op.drop_index("ix_analysis_jobs_experiment_id", table_name="analysis_jobs")
    op.drop_table("analysis_jobs")
    op.drop_table("experiments")
