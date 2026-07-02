import enum
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin, db_enum

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.decision import Decision
    from app.models.order import Order


class ProposalAction(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class ProposalStatus(str, enum.Enum):
    """Single source of truth for where a proposal is in the §3.2 pipeline.

    submitted → rejected_hard_rules | pending_manager
    pending_manager → approved | rejected_manager | modification_requested
    approved → executing → executed | failed | cancelled
    any non-terminal → expired
    """

    SUBMITTED = "submitted"
    REJECTED_HARD_RULES = "rejected_hard_rules"
    PENDING_MANAGER = "pending_manager"
    APPROVED = "approved"
    REJECTED_MANAGER = "rejected_manager"
    MODIFICATION_REQUESTED = "modification_requested"
    EXECUTING = "executing"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Proposal(UUIDPKMixin, TimestampMixin, Base):
    """The structured proposal object of plan §3.1.

    Comes from a *funded account* (which already binds agent + user +
    capital) — no denormalized agent_id, so agent/account facts can never
    drift apart. Revise-and-resubmit (§6 Q4) creates a new row pointing at
    the rejected one via parent_proposal_id; past rows are never mutated.
    """

    __tablename__ = "proposals"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_proposals_quantity_positive"),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1", name="ck_proposals_confidence_unit_interval"
        ),
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    action: Mapped[ProposalAction] = mapped_column(
        db_enum(ProposalAction, name="proposal_action"), nullable=False
    )
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    timeframe: Mapped[str | None] = mapped_column(String(50))
    # The "why" is mandatory (§3.1) — an unexplained proposal is invalid by schema.
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), nullable=False)
    # Agent capital state at submission (§3.1), frozen for audit.
    capital_snapshot: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    status: Mapped[ProposalStatus] = mapped_column(
        db_enum(ProposalStatus, name="proposal_status"),
        nullable=False,
        default=ProposalStatus.SUBMITTED,
        index=True,
    )
    parent_proposal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="RESTRICT"), index=True
    )

    account: Mapped["Account"] = relationship(back_populates="proposals")
    parent_proposal: Mapped["Proposal | None"] = relationship(remote_side="Proposal.id")
    # "all": never touch child rows on proposal delete — both FKs are
    # ON DELETE RESTRICT, the DB itself must reject deleting a proposal
    # that has decisions or orders (§7 audit integrity).
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="proposal", passive_deletes="all"
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="proposal", passive_deletes="all")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Proposal {self.action} {self.quantity} {self.ticker} [{self.status}]>"
