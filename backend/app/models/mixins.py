import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def db_enum(enum_cls: type[enum.Enum], name: str) -> Enum:
    """Build a sa.Enum that persists the members' *values* ('user'), not
    their names ('USER'). Plain sa.Enum stores names, which silently
    mismatches the lowercase-value Postgres types created by migration
    0001 — every model must use this helper for enum columns.
    """
    return Enum(enum_cls, name=name, values_callable=lambda e: [m.value for m in e])


class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # onupdate fires only on ORM UPDATEs — raw SQL or non-Python writers
    # won't refresh this column. Acceptable while the app is the sole
    # writer; revisit (DB trigger) if that ever changes.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
