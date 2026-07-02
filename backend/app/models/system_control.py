import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    SmallInteger,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import db_enum

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.proposal import Proposal
    from app.models.user import User


class ControlAction(str, enum.Enum):
    HALT = "halt"
    RESUME = "resume"
    PAUSE_AGENT = "pause_agent"
    RESUME_AGENT = "resume_agent"
    FORCE_REJECT = "force_reject"


class SystemControl(Base):
    """Single-row table holding the current global halt state (§3.3 kill
    switch) — a fast synchronous read in the order path. The CHECK pins
    id to 1 so a second row can never exist; migration 0003 seeds the row.
    History of every flip lives in control_events, not here.
    """

    __tablename__ = "system_controls"
    __table_args__ = (CheckConstraint("id = 1", name="ck_system_controls_single_row"),)

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=False)
    trading_halted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<SystemControl halted={self.trading_halted}>"


class ControlEvent(Base):
    """Append-only record of every control-plane flip (§3.3/§7): who, what
    (halt / resume / pause-agent / force-reject), when, why.

    Same append-only pattern as decisions/api_usage_log — bigint identity
    PK, created_at only, no UPDATE/DELETE grant for the app DB role.
    """

    __tablename__ = "control_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    action: Mapped[ControlAction] = mapped_column(
        db_enum(ControlAction, name="control_action"), nullable=False
    )
    # NULL = system-initiated (e.g. a loss circuit breaker), not a human.
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    # pause_agent / resume_agent events point at the affected account.
    target_account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="RESTRICT")
    )
    # force_reject events point at the affected proposal.
    target_proposal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="RESTRICT")
    )
    # The "why" is mandatory — a control flip without a reason is invalid.
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    actor: Mapped["User | None"] = relationship()
    target_account: Mapped["Account | None"] = relationship()
    target_proposal: Mapped["Proposal | None"] = relationship()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ControlEvent {self.action} at {self.created_at}>"
