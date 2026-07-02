import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, LargeBinary, String, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from app.models.user import User


class CredentialProvider(str, enum.Enum):
    ROBINHOOD = "robinhood"
    ALPACA = "alpaca"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    FINNHUB = "finnhub"
    ALPHA_VANTAGE = "alpha_vantage"
    OTHER = "other"


class ApiCredential(UUIDPKMixin, TimestampMixin, Base):
    """Secret owned by a user (broker/LLM/data-provider keys). Value is
    encrypted at rest with app-level Fernet (see app.security), never
    stored in plaintext — required by Security-Agent charter.
    """

    __tablename__ = "api_credentials"
    __table_args__ = (UniqueConstraint("user_id", "provider", "credential_name"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[CredentialProvider] = mapped_column(
        SqlEnum(CredentialProvider, name="credential_provider"), nullable=False
    )
    credential_name: Mapped[str] = mapped_column(String(255), nullable=False)
    encrypted_value: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="api_credentials")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ApiCredential {self.provider}:{self.credential_name}>"
