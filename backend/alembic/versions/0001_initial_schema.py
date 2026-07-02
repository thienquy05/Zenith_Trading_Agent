"""initial schema: users, agents, accounts, api_credentials, api_usage_log

Revision ID: 0001
Revises:
Create Date: 2026-07-01

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # create_type=False on every inline column reference below: these enum
    # types are created explicitly once here (llm_provider in particular is
    # reused across two tables), so table creation must not try to
    # (re)create or drop them itself.
    user_role = postgresql.ENUM("user", "admin", name="user_role", create_type=False)
    agent_type = postgresql.ENUM("manager", "member", name="agent_type", create_type=False)
    llm_provider = postgresql.ENUM(
        "openai", "anthropic", "google", "other", name="llm_provider", create_type=False
    )
    account_status = postgresql.ENUM(
        "active", "paused", "killed", name="account_status", create_type=False
    )
    credential_provider = postgresql.ENUM(
        "robinhood", "alpaca", "openai", "anthropic", "google",
        "finnhub", "alpha_vantage", "other", name="credential_provider", create_type=False,
    )

    bind = op.get_bind()
    postgresql.ENUM("user", "admin", name="user_role").create(bind, checkfirst=True)
    postgresql.ENUM("manager", "member", name="agent_type").create(bind, checkfirst=True)
    postgresql.ENUM("openai", "anthropic", "google", "other", name="llm_provider").create(
        bind, checkfirst=True
    )
    postgresql.ENUM("active", "paused", "killed", name="account_status").create(
        bind, checkfirst=True
    )
    postgresql.ENUM(
        "robinhood", "alpaca", "openai", "anthropic", "google",
        "finnhub", "alpha_vantage", "other", name="credential_provider",
    ).create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("role", user_role, nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "agents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("agent_type", agent_type, nullable=False),
        sa.Column("strategy", sa.String(100), nullable=True),
        sa.Column("llm_provider", llm_provider, nullable=False),
        sa.Column("llm_model", sa.String(100), nullable=False),
        sa.Column("task_description", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_name", sa.String(255), nullable=False),
        sa.Column("allocated_capital", sa.Numeric(18, 2), nullable=False, server_default="0"),
        sa.Column("current_balance", sa.Numeric(18, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("status", account_status, nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("user_id", "agent_id", "account_name"),
        sa.CheckConstraint("allocated_capital >= 0", name="ck_accounts_allocated_capital_non_negative"),
        sa.CheckConstraint("current_balance >= 0", name="ck_accounts_current_balance_non_negative"),
    )
    op.create_index("ix_accounts_user_id", "accounts", ["user_id"])
    op.create_index("ix_accounts_agent_id", "accounts", ["agent_id"])

    op.create_table(
        "api_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider", credential_provider, nullable=False),
        sa.Column("credential_name", sa.String(255), nullable=False),
        sa.Column("encrypted_value", sa.LargeBinary, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "provider", "credential_name"),
    )
    op.create_index("ix_api_credentials_user_id", "api_credentials", ["user_id"])

    op.create_table(
        "api_usage_log",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("provider", llm_provider, nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("tokens_in", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tokens_out", sa.Integer, nullable=False, server_default="0"),
        sa.Column("cost_usd", sa.Numeric(12, 6), nullable=False, server_default="0"),
        sa.Column("linked_proposal_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="SET NULL"),
        sa.CheckConstraint("tokens_in >= 0", name="ck_api_usage_log_tokens_in_non_negative"),
        sa.CheckConstraint("tokens_out >= 0", name="ck_api_usage_log_tokens_out_non_negative"),
        sa.CheckConstraint("cost_usd >= 0", name="ck_api_usage_log_cost_usd_non_negative"),
    )
    op.create_index("ix_api_usage_log_agent_id", "api_usage_log", ["agent_id"])
    op.create_index("ix_api_usage_log_account_id", "api_usage_log", ["account_id"])
    op.create_index("ix_api_usage_log_request_timestamp", "api_usage_log", ["request_timestamp"])


def downgrade() -> None:
    op.drop_table("api_usage_log")
    op.drop_table("api_credentials")
    op.drop_table("accounts")
    op.drop_table("agents")
    op.drop_table("users")

    bind = op.get_bind()
    postgresql.ENUM(name="credential_provider").drop(bind, checkfirst=True)
    postgresql.ENUM(name="account_status").drop(bind, checkfirst=True)
    postgresql.ENUM(name="llm_provider").drop(bind, checkfirst=True)
    postgresql.ENUM(name="agent_type").drop(bind, checkfirst=True)
    postgresql.ENUM(name="user_role").drop(bind, checkfirst=True)
