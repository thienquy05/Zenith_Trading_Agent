"""drop api_usage_log.updated_at — append-only ledger, rows are never updated

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-01

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("api_usage_log", "updated_at")


def downgrade() -> None:
    op.add_column(
        "api_usage_log",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
