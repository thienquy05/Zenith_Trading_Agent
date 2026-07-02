import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import db_enum

if TYPE_CHECKING:
    from app.models.hard_rule_params import HardRuleParams
    from app.models.proposal import Proposal
    from app.models.user import User


class DecisionStage(str, enum.Enum):
    HARD_RULES = "hard_rules"
    MANAGER_LLM = "manager_llm"
    HUMAN_OVERRIDE = "human_override"
    EXECUTION = "execution"


class DecisionOutcome(str, enum.Enum):
    PASSED = "passed"  # hard-rules gate cleared
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFICATION_REQUESTED = "modification_requested"
    EXECUTED = "executed"
    FAILED = "failed"


class Decision(Base):
    """Append-only audit ledger required by §7: every proposal, reasoning,
    decision, and override gets a row — nothing executes silently.

    High-volume, append-only — bigint identity PK and created_at only
    (no updated_at), the same pattern as api_usage_log. Rows are never
    edited; the app DB role has no UPDATE/DELETE grant on this table.
    """

    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    proposal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("proposals.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    stage: Mapped[DecisionStage] = mapped_column(
        db_enum(DecisionStage, name="decision_stage"), nullable=False
    )
    outcome: Mapped[DecisionOutcome] = mapped_column(
        db_enum(DecisionOutcome, name="decision_outcome"), nullable=False
    )
    # Structured rule violations (rule key, limit, observed value) or LLM
    # reasoning text — machine-queryable either way.
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    # Human overrides only; NULL for automated stages.
    decided_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    # The exact limits in force at decision time — the audit trail can
    # always answer "what limits were live when this was approved?".
    hard_rule_params_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("hard_rule_params.id", ondelete="RESTRICT")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    proposal: Mapped["Proposal"] = relationship(back_populates="decisions")
    decided_by: Mapped["User | None"] = relationship()
    hard_rule_params: Mapped["HardRuleParams | None"] = relationship()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Decision {self.stage}:{self.outcome} proposal={self.proposal_id}>"
