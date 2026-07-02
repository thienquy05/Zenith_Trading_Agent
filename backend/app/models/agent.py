import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin, db_enum

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.api_usage_log import ApiUsageLog


class AgentType(str, enum.Enum):
    MANAGER = "manager"
    MEMBER = "member"


class LlmProvider(str, enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OTHER = "other"


class Agent(UUIDPKMixin, TimestampMixin, Base):
    """A reusable agent definition (plan §3.1/§3.2) — not a running instance.

    Capital/holdings live on Account, not here, so the same agent
    definition can be reused across multiple funded accounts.
    """

    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    agent_type: Mapped[AgentType] = mapped_column(
        db_enum(AgentType, name="agent_type"), nullable=False
    )
    strategy: Mapped[str | None] = mapped_column(String(100))
    llm_provider: Mapped[LlmProvider] = mapped_column(
        db_enum(LlmProvider, name="llm_provider"), nullable=False
    )
    llm_model: Mapped[str] = mapped_column(String(100), nullable=False)
    task_description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # "all": never touch child rows on agent delete — accounts.agent_id is
    # ON DELETE RESTRICT, the DB itself must reject deleting a funded agent.
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="agent", passive_deletes="all"
    )
    usage_logs: Mapped[list["ApiUsageLog"]] = relationship(
        back_populates="agent", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Agent {self.name}>"
