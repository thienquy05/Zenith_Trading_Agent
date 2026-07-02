import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.agent import LlmProvider
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.agent import Agent


class ApiUsageLog(TimestampMixin, Base):
    """Per-call token/cost ledger for every LLM request an agent makes.

    High-volume, append-only — uses a bigint identity PK instead of the
    UUID PK mixin the other tables use.

    linked_proposal_id has no FK yet: the proposals table doesn't exist
    until Phase 1 (plan §5). Column is kept nullable and unconstrained so
    it can be backfilled/constrained once that table lands.
    """

    __tablename__ = "api_usage_log"
    __table_args__ = (
        CheckConstraint("tokens_in >= 0", name="ck_api_usage_log_tokens_in_non_negative"),
        CheckConstraint("tokens_out >= 0", name="ck_api_usage_log_tokens_out_non_negative"),
        CheckConstraint("cost_usd >= 0", name="ck_api_usage_log_cost_usd_non_negative"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="SET NULL"), index=True
    )
    provider: Mapped[LlmProvider] = mapped_column(
        Enum(LlmProvider, name="llm_provider"), nullable=False
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_usd: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False, default=0)
    linked_proposal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    request_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    agent: Mapped["Agent"] = relationship(back_populates="usage_logs")
    account: Mapped["Account | None"] = relationship(back_populates="usage_logs")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ApiUsageLog agent={self.agent_id} tokens={self.tokens_in}/{self.tokens_out}>"
