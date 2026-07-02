import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import UUIDPKMixin

if TYPE_CHECKING:
    from app.models.user import User


class HardRuleParams(UUIDPKMixin, Base):
    """Versioned hard-rule parameter-set snapshots (§3.3: adjust limits
    without redeploying code; §6.1 for the numbers themselves).

    A change = a new row; nothing is updated in place (no updated_at).
    decisions.hard_rule_params_id FKs the exact version used, so the audit
    trail can always reconstruct the limits in force. Migration 0003 seeds
    the §6.1 starting defaults as version 1 (created_by NULL = system seed).
    """

    __tablename__ = "hard_rule_params"

    params: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    activated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    created_by_user: Mapped["User | None"] = relationship()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<HardRuleParams {self.id} activated={self.activated_at}>"
