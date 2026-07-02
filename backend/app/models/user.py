from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.api_credential import ApiCredential


class User(UUIDPKMixin, TimestampMixin, Base):
    """The operator. Local single-operator project (decision 2026-07-02):
    no email/full_name/role — username is the login identifier, and one
    auth dependency ("logged-in operator") guards every mutating endpoint.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # passive_deletes: the DB's ON DELETE CASCADE (migration 0001) removes
    # children; without it the ORM nulls child FKs first, which violates
    # their NOT NULL constraints.
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    api_credentials: Mapped[list["ApiCredential"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User {self.username}>"
