import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin, db_enum

if TYPE_CHECKING:
    from app.models.proposal import Proposal


class OrderBroker(str, enum.Enum):
    PAPER = "paper"
    ALPACA = "alpaca"
    ROBINHOOD = "robinhood"


class OrderSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    FAILED = "failed"


class Order(UUIDPKMixin, TimestampMixin, Base):
    """Execution record (paper first, plan §5 Phases 1–2).

    proposal_id is NOT NULL — nothing executes without a proposal chain
    (§7: "nothing executes silently"). idempotency_key is UNIQUE so a
    retried submission can never place a duplicate order.
    """

    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_orders_quantity_positive"),
        CheckConstraint(
            "filled_quantity >= 0 AND filled_quantity <= quantity",
            name="ck_orders_filled_quantity_within_bounds",
        ),
        CheckConstraint("limit_price > 0", name="ck_orders_limit_price_positive"),
        CheckConstraint("avg_fill_price > 0", name="ck_orders_avg_fill_price_positive"),
    )

    proposal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("proposals.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    broker: Mapped[OrderBroker] = mapped_column(
        db_enum(OrderBroker, name="order_broker"), nullable=False
    )
    broker_order_id: Mapped[str | None] = mapped_column(String(255))
    side: Mapped[OrderSide] = mapped_column(db_enum(OrderSide, name="order_side"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    filled_quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False, default=0)
    # NULL limit_price = market order.
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    avg_fill_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    status: Mapped[OrderStatus] = mapped_column(
        db_enum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.PENDING,
        index=True,
    )
    idempotency_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    filled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    proposal: Mapped["Proposal"] = relationship(back_populates="orders")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Order {self.side} {self.quantity} {self.ticker} [{self.status}]>"
