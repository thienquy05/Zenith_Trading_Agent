import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from app.models.account import Account


class Position(UUIDPKMixin, TimestampMixin, Base):
    """Current holdings per account + ticker (qty, avg cost), maintained
    transactionally with fills — hard rules need fast position lookups
    without replaying the order history.

    quantity >= 0: early phases are long-only stocks (§6.1 blacklists
    derivatives); revisit the CHECK if shorting is ever gated in.
    """

    __tablename__ = "positions"
    __table_args__ = (
        UniqueConstraint("account_id", "ticker"),
        CheckConstraint("quantity >= 0", name="ck_positions_quantity_non_negative"),
        CheckConstraint("avg_cost >= 0", name="ck_positions_avg_cost_non_negative"),
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    avg_cost: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    account: Mapped["Account"] = relationship(back_populates="positions")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Position {self.ticker} x{self.quantity} account={self.account_id}>"
