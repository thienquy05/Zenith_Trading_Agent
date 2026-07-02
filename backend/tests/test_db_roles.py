"""Least-privilege runtime role (migration 0004) — proves the append-only
ledgers are enforced by the database itself, not by convention.

These tests connect as the runtime role (settings.app_database_url), which
only exists after `alembic upgrade head` has run against this database —
conftest's create_all shortcut does not provision roles or grants. CI runs
the migration round-trip before pytest, so the role is always there; a
local create_all-only run skips with an explanation instead of failing.
"""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.config import get_settings

APPEND_ONLY_TABLES = ("decisions", "control_events", "api_usage_log")


@pytest.fixture(scope="module")
def app_role_engine(engine):  # depends on `engine` so tables exist first
    eng = create_engine(get_settings().app_database_url)
    try:
        with eng.connect():
            pass
    except OperationalError:
        eng.dispose()
        pytest.skip(
            "runtime role not provisioned — run `alembic upgrade head` "
            "(migration 0004) against this database first"
        )
    yield eng
    eng.dispose()


@pytest.mark.parametrize("table", APPEND_ONLY_TABLES)
def test_app_role_cannot_update_append_only_table(app_role_engine, table):
    # Postgres checks privileges before matching rows, so this fails on
    # permission grounds even with the table empty.
    with app_role_engine.connect() as conn:
        with pytest.raises(ProgrammingError, match="permission denied"):
            conn.execute(text(f"UPDATE {table} SET created_at = now()"))


@pytest.mark.parametrize("table", APPEND_ONLY_TABLES)
def test_app_role_cannot_delete_from_append_only_table(app_role_engine, table):
    with app_role_engine.connect() as conn:
        with pytest.raises(ProgrammingError, match="permission denied"):
            conn.execute(text(f"DELETE FROM {table}"))


def test_app_role_can_append_and_read_ledger_rows(app_role_engine):
    # The denials above must come from the *revoked* verbs, not from the
    # role having no access at all — INSERT + SELECT are granted.
    with app_role_engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO control_events (action, reason) "
                "VALUES ('halt', 'role-separation smoke test')"
            )
        )
        count = conn.execute(
            text("SELECT count(*) FROM control_events WHERE reason = 'role-separation smoke test'")
        ).scalar()
        assert count == 1
        conn.rollback()


def test_app_role_cannot_touch_alembic_version(app_role_engine):
    with app_role_engine.connect() as conn:
        with pytest.raises(ProgrammingError, match="permission denied"):
            conn.execute(text("SELECT * FROM alembic_version"))


def test_migration_seeds_are_present(app_role_engine):
    # Sanity on the 0003 seeds, visible to the runtime role: exactly one
    # kill-switch row (id=1, not halted) and the §6.1 params as version 1.
    with app_role_engine.connect() as conn:
        controls = conn.execute(
            text("SELECT id, trading_halted FROM system_controls")
        ).all()
        assert controls == [(1, False)]

        seeded = conn.execute(
            text(
                "SELECT jsonb_exists(params, 'max_trades_per_agent_per_day') FROM hard_rule_params "
                "ORDER BY activated_at LIMIT 1"
            )
        ).scalar()
        assert seeded is True
