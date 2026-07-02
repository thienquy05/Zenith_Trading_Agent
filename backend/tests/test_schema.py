"""Standalone schema-level guards — no live database needed. These check
invariants of the declared metadata itself, catching drift between the
ORM models and what migration 0001 created in Postgres.
"""
import sqlalchemy as sa

import app.models  # noqa: F401 (registers all tables on Base.metadata)
from app.database import Base


def test_all_enum_columns_persist_values_not_names():
    # Migration 0001 created the Postgres enum types from the members'
    # lowercase *values* ('user', 'admin', ...). A model declaring a plain
    # sa.Enum would silently persist the uppercase *names* instead and
    # break on the first insert — every enum column must go through
    # mixins.db_enum (values_callable), which this asserts indirectly.
    checked = 0
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if not isinstance(column.type, sa.Enum):
                continue
            enum_cls = column.type.enum_class
            assert enum_cls is not None, f"{table.name}.{column.name} has no Python enum class"
            assert list(column.type.enums) == [m.value for m in enum_cls], (
                f"{table.name}.{column.name} would persist enum names, not values — "
                "declare it with mixins.db_enum()"
            )
            checked += 1
    assert checked >= 5  # user_role, agent_type, llm_provider (x2), account_status, credential_provider


def test_every_foreign_key_declares_ondelete():
    # Delete semantics must be an explicit decision per FK (CASCADE /
    # RESTRICT / SET NULL), never Postgres's implicit NO ACTION default —
    # dangling rows in a capital/credential schema are a real hazard.
    for table in Base.metadata.tables.values():
        for fk in table.foreign_keys:
            assert fk.ondelete is not None, (
                f"{table.name}.{fk.parent.name} FK has no explicit ondelete"
            )
