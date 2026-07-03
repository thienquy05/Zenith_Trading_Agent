"""Input/output types for the hard-rules engine.

Deliberately not ORM models: the engine takes plain frozen dataclasses so
rule functions stay pure and testable without a database. The caller (the
proposal pipeline, roadmap branch 4) maps ORM rows and market data into
these. The one shared import is ProposalAction — the enum on the
proposals table is the single source of truth for what an action is.

All money math is Decimal, never float. Every dataclass validates itself
on construction and raises ValueError on nonsensical state — a gate that
guards capital fails closed on bad input rather than guessing.
"""

import dataclasses
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from app.models.proposal import ProposalAction


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class ProposalRequest:
    """The slice of a §3.1 proposal the rules need to judge it."""

    action: ProposalAction
    ticker: str
    quantity: Decimal

    def __post_init__(self) -> None:
        _require(bool(self.ticker), "ticker must be non-empty")
        _require(isinstance(self.quantity, Decimal), "quantity must be a Decimal")
        _require(self.quantity > 0, "quantity must be > 0")


@dataclass(frozen=True)
class InstrumentSnapshot:
    """Market/reference data for the proposal's ticker at check time."""

    ticker: str
    price: Decimal
    # None = provider gave no GICS sector; the sector-exposure rule treats
    # that as unverifiable and fails closed for buys.
    sector: str | None = None
    is_leveraged_etf: bool = False
    is_inverse_etf: bool = False
    is_derivative: bool = False
    # Index memberships this ticker belongs to, e.g. {"sp500"}. The
    # whitelist rule checks the params' whitelist key against this set.
    index_memberships: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require(bool(self.ticker), "ticker must be non-empty")
        _require(isinstance(self.price, Decimal), "price must be a Decimal")
        _require(self.price > 0, "price must be > 0")


@dataclass(frozen=True)
class PortfolioState:
    """Capital/position/P&L state the caller fetched, frozen for the check.

    Values scoped to the proposal's ticker or sector are relative to the
    InstrumentSnapshot passed alongside. P&L signs: negative = loss.
    """

    # The proposing agent's own sub-budget and its exposure to this ticker.
    agent_allocated_capital: Decimal
    # Whole-portfolio total, across all agents.
    portfolio_total_value: Decimal
    agent_position_value: Decimal = Decimal(0)
    # Per-share average cost of the agent's existing position in this
    # ticker; None = no existing position (stop-loss rule not applicable).
    agent_position_avg_cost: Decimal | None = None
    # Trades this agent has already executed today (this proposal would be
    # trade N+1).
    agent_trades_today: int = 0

    # Whole-portfolio view, across all agents.
    portfolio_position_value: Decimal = Decimal(0)
    # Current portfolio exposure to the instrument's GICS sector.
    sector_exposure_value: Decimal = Decimal(0)
    portfolio_daily_pnl: Decimal = Decimal(0)
    portfolio_weekly_pnl: Decimal = Decimal(0)

    def __post_init__(self) -> None:
        _require(self.agent_allocated_capital > 0, "agent_allocated_capital must be > 0")
        _require(self.agent_position_value >= 0, "agent_position_value must be >= 0")
        if self.agent_position_avg_cost is not None:
            _require(self.agent_position_avg_cost > 0, "agent_position_avg_cost must be > 0")
        _require(self.agent_trades_today >= 0, "agent_trades_today must be >= 0")
        _require(self.portfolio_total_value > 0, "portfolio_total_value must be > 0")
        _require(self.portfolio_position_value >= 0, "portfolio_position_value must be >= 0")
        _require(self.sector_exposure_value >= 0, "sector_exposure_value must be >= 0")


def _json_safe(value: Any) -> Any:
    """Decimals go into JSONB as strings — exact, never float-rounded."""
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class Violation:
    """One broken rule: key, the limit in force, and the observed value.

    Shaped for the decisions.details JSONB ledger — machine-queryable, so
    the audit trail and the resubmitting agent both see exactly what was
    wrong and by how much.
    """

    rule: str
    limit: Any
    observed: Any
    message: str

    def to_details(self) -> dict[str, Any]:
        return _json_safe(dataclasses.asdict(self))


@dataclass(frozen=True)
class HardRuleResult:
    """Outcome of one full engine pass: every violation, not just the first."""

    violations: tuple[Violation, ...]

    @property
    def passed(self) -> bool:
        return not self.violations

    def to_details(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "violations": [v.to_details() for v in self.violations],
        }
