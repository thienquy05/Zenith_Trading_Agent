import enum
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from app.models.agent import Agent
    from app.models.api_usage_log import ApiUsageLog
    from app.models.user import User


class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    KILLED = "killed"  # set by the manual override kill switch (plan §3.3)


class Account(UUIDPKMixin, TimestampMixin, Base):
    """One agent's funded capital allocation, owned by a user (plan §3.1: 'own allocated capital')."""

    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "agent_id", "account_name"),
        CheckConstraint("allocated_capital >= 0", name="ck_accounts_allocated_capital_non_negative"),
        CheckConstraint("current_balance >= 0", name="ck_accounts_current_balance_non_negative"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    allocated_capital: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    current_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[AccountStatus] = mapped_column(
        SqlEnum(AccountStatus, name="account_status"), nullable=False, default=AccountStatus.ACTIVE
    )

    user: Mapped["User"] = relationship(back_populates="accounts")
    agent: Mapped["Agent"] = relationship(back_populates="accounts")
    usage_logs: Mapped[list["ApiUsageLog"]] = relationship(back_populates="account")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Account {self.account_name} agent={self.agent_id}>"
