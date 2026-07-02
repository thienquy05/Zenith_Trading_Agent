"""trading-domain core: proposals, decisions, hard_rule_params,
system_controls, control_events, orders, positions; users simplified to
username-only (single-operator decision 2026-07-02); api_usage_log finally
gets its linked_proposal_id FK. Seeds §6.1 defaults + the kill-switch row.

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-02

"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# §6.1 starting defaults, conservative end of each stated range. Seeded as
# hard_rule_params version 1; every later change is a new row via the API.
HARD_RULE_DEFAULTS = {
    "max_position_pct_per_agent": 0.20,
    "max_position_pct_portfolio": 0.10,
    "max_sector_exposure_pct": 0.30,
    "daily_loss_halt_pct": 0.03,
    "weekly_loss_halt_pct": 0.05,
    "per_position_stop_loss_pct": 0.08,
    "max_trades_per_agent_per_day": 5,
    "blacklist": {
        "leveraged_etfs": True,
        "inverse_etfs": True,
        "derivatives": True,
        "min_price_usd": 5,
    },
    "whitelist": "sp500",
}

NEW_ENUMS: dict[str, list[str]] = {
    "proposal_action": ["buy", "sell", "hold"],
    "proposal_status": [
        "submitted",
        "rejected_hard_rules",
        "pending_manager",
        "approved",
        "rejected_manager",
        "modification_requested",
        "executing",
        "executed",
        "failed",
        "cancelled",
        "expired",
    ],
    "decision_stage": ["hard_rules", "manager_llm", "human_override", "execution"],
    "decision_outcome": [
        "passed",
        "approved",
        "rejected",
        "modification_requested",
        "executed",
        "failed",
    ],
    "control_action": ["halt", "resume", "pause_agent", "resume_agent", "force_reject"],
    "order_broker": ["paper", "alpaca", "robinhood"],
    "order_side": ["buy", "sell"],
    "order_status": [
        "pending",
        "submitted",
        "partially_filled",
        "filled",
        "cancelled",
        "rejected",
        "failed",
    ],
}


def upgrade() -> None:
    bind = op.get_bind()

    # --- users simplified: username replaces email/full_name/role -------
    # Backfill username from email so existing dev rows survive; left(50)
    # matches the new column width (collision risk accepted — Phase 0 dev
    # data only, and the UNIQUE constraint below would fail loudly).
    op.add_column("users", sa.Column("username", sa.String(50), nullable=True))
    op.execute("UPDATE users SET username = left(email, 50)")
    op.alter_column("users", "username", nullable=False)
    op.create_unique_constraint("users_username_key", "users", ["username"])
    op.create_index("ix_users_username", "users", ["username"])
    op.drop_index("ix_users_email", table_name="users")
    op.drop_column("users", "email")
    op.drop_column("users", "full_name")
    op.drop_column("users", "role")
    postgresql.ENUM(name="user_role").drop(bind, checkfirst=True)

    # --- new enum types (same explicit-create pattern as migration 0001:
    # created once here, inline references use create_type=False) --------
    for name, values in NEW_ENUMS.items():
        postgresql.ENUM(*values, name=name).create(bind, checkfirst=True)
    enums = {
        name: postgresql.ENUM(*values, name=name, create_type=False)
        for name, values in NEW_ENUMS.items()
    }

    # --- hard_rule_params (versioned snapshots, append-only by API) -----
    op.create_table(
        "hard_rule_params",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("params", postgresql.JSONB, nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("activated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_hard_rule_params_activated_at", "hard_rule_params", ["activated_at"])

    # --- proposals (the §3.1 structured proposal object) ----------------
    op.create_table(
        "proposals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", enums["proposal_action"], nullable=False),
        sa.Column("ticker", sa.String(20), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 8), nullable=False),
        sa.Column("timeframe", sa.String(50), nullable=True),
        sa.Column("reasoning", sa.Text, nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("capital_snapshot", postgresql.JSONB, nullable=False),
        sa.Column("status", enums["proposal_status"], nullable=False, server_default="submitted"),
        sa.Column("parent_proposal_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["parent_proposal_id"], ["proposals.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("quantity > 0", name="ck_proposals_quantity_positive"),
        sa.CheckConstraint(
            "confidence >= 0 AND confidence <= 1", name="ck_proposals_confidence_unit_interval"
        ),
    )
    op.create_index("ix_proposals_account_id", "proposals", ["account_id"])
    op.create_index("ix_proposals_status", "proposals", ["status"])
    op.create_index("ix_proposals_parent_proposal_id", "proposals", ["parent_proposal_id"])

    # --- decisions (append-only audit ledger, §7) ------------------------
    op.create_table(
        "decisions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("proposal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stage", enums["decision_stage"], nullable=False),
        sa.Column("outcome", enums["decision_outcome"], nullable=False),
        sa.Column("details", postgresql.JSONB, nullable=True),
        sa.Column("decided_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("hard_rule_params_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["decided_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["hard_rule_params_id"], ["hard_rule_params.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_decisions_proposal_id", "decisions", ["proposal_id"])
    op.create_index("ix_decisions_created_at", "decisions", ["created_at"])

    # --- system_controls (single-row kill-switch state, §3.3) ------------
    op.create_table(
        "system_controls",
        sa.Column("id", sa.SmallInteger, primary_key=True, autoincrement=False),
        sa.Column("trading_halted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_system_controls_single_row"),
    )

    # --- control_events (append-only control-plane audit) ----------------
    op.create_table(
        "control_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("action", enums["control_action"], nullable=False),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("target_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("target_proposal_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["target_account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["target_proposal_id"], ["proposals.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_control_events_created_at", "control_events", ["created_at"])

    # --- orders (execution records, paper first) --------------------------
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("proposal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("broker", enums["order_broker"], nullable=False),
        sa.Column("broker_order_id", sa.String(255), nullable=True),
        sa.Column("side", enums["order_side"], nullable=False),
        sa.Column("ticker", sa.String(20), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 8), nullable=False),
        sa.Column("filled_quantity", sa.Numeric(18, 8), nullable=False, server_default="0"),
        sa.Column("limit_price", sa.Numeric(18, 4), nullable=True),
        sa.Column("avg_fill_price", sa.Numeric(18, 4), nullable=True),
        sa.Column("status", enums["order_status"], nullable=False, server_default="pending"),
        sa.Column("idempotency_key", sa.String(64), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("filled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("idempotency_key"),
        sa.CheckConstraint("quantity > 0", name="ck_orders_quantity_positive"),
        sa.CheckConstraint(
            "filled_quantity >= 0 AND filled_quantity <= quantity",
            name="ck_orders_filled_quantity_within_bounds",
        ),
        sa.CheckConstraint("limit_price > 0", name="ck_orders_limit_price_positive"),
        sa.CheckConstraint("avg_fill_price > 0", name="ck_orders_avg_fill_price_positive"),
    )
    op.create_index("ix_orders_proposal_id", "orders", ["proposal_id"])
    op.create_index("ix_orders_status", "orders", ["status"])

    # --- positions (current holdings; fast lookups for hard rules) --------
    op.create_table(
        "positions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ticker", sa.String(20), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 8), nullable=False),
        sa.Column("avg_cost", sa.Numeric(18, 4), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("account_id", "ticker"),
        sa.CheckConstraint("quantity >= 0", name="ck_positions_quantity_non_negative"),
        sa.CheckConstraint("avg_cost >= 0", name="ck_positions_avg_cost_non_negative"),
    )
    op.create_index("ix_positions_account_id", "positions", ["account_id"])

    # --- api_usage_log.linked_proposal_id: the deferred Phase 0 FK -------
    op.create_foreign_key(
        "fk_api_usage_log_linked_proposal_id",
        "api_usage_log",
        "proposals",
        ["linked_proposal_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_api_usage_log_linked_proposal_id", "api_usage_log", ["linked_proposal_id"])

    # --- seeds ------------------------------------------------------------
    op.execute(
        sa.text(
            "INSERT INTO hard_rule_params (id, params, created_by, reason) "
            "VALUES (gen_random_uuid(), CAST(:params AS jsonb), NULL, :reason)"
        ).bindparams(
            params=json.dumps(HARD_RULE_DEFAULTS),
            reason="§6.1 starting defaults (conservative end of each stated range) — "
            "seeded by migration 0003 as version 1",
        )
    )
    op.execute("INSERT INTO system_controls (id, trading_halted) VALUES (1, false)")


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index("ix_api_usage_log_linked_proposal_id", table_name="api_usage_log")
    op.drop_constraint("fk_api_usage_log_linked_proposal_id", "api_usage_log")

    op.drop_table("positions")
    op.drop_table("orders")
    op.drop_table("control_events")
    op.drop_table("system_controls")
    op.drop_table("decisions")
    op.drop_table("proposals")
    op.drop_table("hard_rule_params")

    for name in NEW_ENUMS:
        postgresql.ENUM(name=name).drop(bind, checkfirst=True)

    # --- restore the pre-simplification users shape -----------------------
    postgresql.ENUM("user", "admin", name="user_role").create(bind, checkfirst=True)
    user_role = postgresql.ENUM("user", "admin", name="user_role", create_type=False)
    op.add_column("users", sa.Column("email", sa.String(255), nullable=True))
    # username || '@restored.local' keeps email unique because username is.
    op.execute("UPDATE users SET email = username || '@restored.local'")
    op.alter_column("users", "email", nullable=False)
    op.create_unique_constraint("users_email_key", "users", ["email"])
    op.create_index("ix_users_email", "users", ["email"])
    op.add_column("users", sa.Column("full_name", sa.String(255), nullable=True))
    op.add_column("users", sa.Column("role", user_role, nullable=False, server_default="user"))
    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "username")
