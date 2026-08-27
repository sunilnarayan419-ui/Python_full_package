"""add nullable priority column, backfill, then enforce not null

Revision ID: 0002
Revises: 0001
Create Date: 2025-02-10 09:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Backward-compatible three-step pattern: add nullable, backfill, enforce.
    op.add_column("analysis_jobs", sa.Column("priority", sa.SmallInteger(), nullable=True))
    op.execute("UPDATE analysis_jobs SET priority = 5 WHERE priority IS NULL")
    op.alter_column("analysis_jobs", "priority", nullable=False, server_default="5")


def downgrade() -> None:
    op.drop_column("analysis_jobs", "priority")
