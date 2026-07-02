import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin, db_enum

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.api_credential import ApiCredential


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"  # required for manual override / kill-switch control plane (plan §3.3)


class User(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        db_enum(UserRole, name="user_role"), nullable=False, default=UserRole.USER
    )
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
        return f"<User {self.email}>"
