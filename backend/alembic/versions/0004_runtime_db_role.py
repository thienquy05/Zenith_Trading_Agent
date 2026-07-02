"""least-privilege runtime DB role (closes the standing pre-Phase-1
security finding): migrations keep running as the schema-owning
POSTGRES_USER; the backend runtime connects as POSTGRES_APP_USER, which
gets DML only — and *no* UPDATE/DELETE on the append-only ledgers
(decisions, control_events, api_usage_log), so append-only is enforced
by the database itself, not by convention.

Roles are cluster-level: upgrade creates the role only if missing, and
downgrade revokes this database's grants but leaves the role in place
(dropping it could break another database sharing the cluster).

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-02

"""
import re
from typing import Sequence, Union

from alembic import op

from app.config import get_settings

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

APPEND_ONLY_TABLES = ("decisions", "control_events", "api_usage_log")


def _app_role() -> str:
    role = get_settings().postgres_app_user
    # Interpolated into DDL (CREATE ROLE/GRANT take no bind params) — allow
    # only plain identifier characters.
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", role):
        raise ValueError(f"unsafe POSTGRES_APP_USER: {role!r}")
    return role


def upgrade() -> None:
    role = _app_role()
    # Single-quote escaping is the only quoting a Postgres string literal
    # needs here; the password itself lives in env, never in this file.
    password = get_settings().postgres_app_password.replace("'", "''")
    conn = op.get_bind()

    conn.exec_driver_sql(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '{role}') THEN
                CREATE ROLE {role} LOGIN PASSWORD '{password}';
            END IF;
        END
        $$;
        """
    )

    conn.exec_driver_sql(f"GRANT USAGE ON SCHEMA public TO {role}")
    conn.exec_driver_sql(
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {role}"
    )
    conn.exec_driver_sql(f"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {role}")
    # Future tables created by the migration role default to full DML;
    # future append-only tables must REVOKE in their own migration.
    conn.exec_driver_sql(
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public "
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {role}"
    )
    conn.exec_driver_sql(
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO {role}"
    )

    for table in APPEND_ONLY_TABLES:
        conn.exec_driver_sql(f"REVOKE UPDATE, DELETE ON {table} FROM {role}")
    # Migration bookkeeping is the migration role's alone.
    conn.exec_driver_sql(f"REVOKE ALL ON alembic_version FROM {role}")


def downgrade() -> None:
    role = _app_role()
    conn = op.get_bind()
    # No % characters allowed in exec_driver_sql (psycopg reads them as
    # placeholders) — the role name is regex-validated, inline it directly.
    conn.exec_driver_sql(
        f"""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = '{role}') THEN
                ALTER DEFAULT PRIVILEGES IN SCHEMA public
                    REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES FROM {role};
                ALTER DEFAULT PRIVILEGES IN SCHEMA public
                    REVOKE USAGE, SELECT ON SEQUENCES FROM {role};
                REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {role};
                REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM {role};
                REVOKE USAGE ON SCHEMA public FROM {role};
            END IF;
        END
        $$;
        """
    )
