"""One pure function per §6.1 rule, plus the evaluate-everything entry point.

Semantics, agreed once here so every rule reads the same way:

- Caps (position/sector) are inclusive limits: exactly at the limit
  passes, one cent over fails.
- Circuit breakers and the stop-loss are triggers: exactly at the stated
  loss level fires — a breaker that only trips strictly beyond its stated
  level would be surprising in the direction that loses money.
- Rules gate what they exist to gate: exposure/blacklist/whitelist/
  stop-loss rules apply to buys only (a sell reduces risk and must never
  be blocked by the rule that exists to cap it — exiting a blacklisted or
  de-whitelisted name is the remedy, not a violation). Circuit breakers
  and trade frequency apply to buys and sells. A hold moves no money and
  passes everything.
- The engine returns *every* violation, not just the first (§3.2) — the
  audit ledger and the resubmitting agent learn everything wrong in one
  pass.
"""

from collections.abc import Callable
from decimal import Decimal

from app.models.proposal import ProposalAction
from app.rules.params import HardRuleParams
from app.rules.types import (
    HardRuleResult,
    InstrumentSnapshot,
    PortfolioState,
    ProposalRequest,
    Violation,
)

RuleFn = Callable[
    [ProposalRequest, InstrumentSnapshot, PortfolioState, HardRuleParams],
    Violation | None,
]


def _notional(proposal: ProposalRequest, instrument: InstrumentSnapshot) -> Decimal:
    return proposal.quantity * instrument.price


def check_max_position_per_agent(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Max position size per agent: one ticker may not exceed
    max_position_pct_per_agent of the agent's own allocated capital."""
    if proposal.action is not ProposalAction.BUY:
        return None
    resulting = portfolio.agent_position_value + _notional(proposal, instrument)
    limit = params.max_position_pct_per_agent * portfolio.agent_allocated_capital
    if resulting <= limit:
        return None
    return Violation(
        rule="max_position_pct_per_agent",
        limit=limit,
        observed=resulting,
        message=(
            f"position in {proposal.ticker} would be {resulting} of "
            f"{portfolio.agent_allocated_capital} agent capital, over the "
            f"{params.max_position_pct_per_agent} cap ({limit})"
        ),
    )


def check_max_position_portfolio(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Max position size portfolio-wide: one ticker across all agents may
    not exceed max_position_pct_portfolio of total portfolio value."""
    if proposal.action is not ProposalAction.BUY:
        return None
    resulting = portfolio.portfolio_position_value + _notional(proposal, instrument)
    limit = params.max_position_pct_portfolio * portfolio.portfolio_total_value
    if resulting <= limit:
        return None
    return Violation(
        rule="max_position_pct_portfolio",
        limit=limit,
        observed=resulting,
        message=(
            f"portfolio-wide position in {proposal.ticker} would be {resulting} of "
            f"{portfolio.portfolio_total_value} total, over the "
            f"{params.max_position_pct_portfolio} cap ({limit})"
        ),
    )


def check_max_sector_exposure(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Max sector exposure portfolio-wide. Unknown sector fails closed for
    buys: exposure that can't be verified can't be allowed to grow."""
    if proposal.action is not ProposalAction.BUY:
        return None
    if instrument.sector is None:
        return Violation(
            rule="max_sector_exposure_pct",
            limit=params.max_sector_exposure_pct,
            observed=None,
            message=(
                f"{proposal.ticker} has no sector classification — sector exposure "
                "cannot be verified, failing closed"
            ),
        )
    resulting = portfolio.sector_exposure_value + _notional(proposal, instrument)
    limit = params.max_sector_exposure_pct * portfolio.portfolio_total_value
    if resulting <= limit:
        return None
    return Violation(
        rule="max_sector_exposure_pct",
        limit=limit,
        observed=resulting,
        message=(
            f"{instrument.sector} exposure would be {resulting} of "
            f"{portfolio.portfolio_total_value} total, over the "
            f"{params.max_sector_exposure_pct} cap ({limit})"
        ),
    )


def _loss_breaker(
    proposal: ProposalRequest,
    portfolio: PortfolioState,
    pnl: Decimal,
    halt_pct: Decimal,
    rule: str,
    window: str,
) -> Violation | None:
    if proposal.action is ProposalAction.HOLD:
        return None
    loss = -pnl
    threshold = halt_pct * portfolio.portfolio_total_value
    if loss < threshold:
        return None
    return Violation(
        rule=rule,
        limit=threshold,
        observed=loss,
        message=(
            f"{window} loss {loss} has reached the {halt_pct} circuit breaker "
            f"({threshold} of {portfolio.portfolio_total_value}) — all trading paused"
        ),
    )


def check_daily_loss_breaker(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Daily loss circuit breaker (§3.3/§7 kill-switch tie-in): at or past
    the daily loss threshold, buys and sells are both rejected."""
    return _loss_breaker(
        proposal,
        portfolio,
        portfolio.portfolio_daily_pnl,
        params.daily_loss_halt_pct,
        "daily_loss_halt_pct",
        "daily",
    )


def check_weekly_loss_breaker(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Weekly loss circuit breaker — catches slow bleeds the daily breaker
    misses; resuming requires human review (§6.1)."""
    return _loss_breaker(
        proposal,
        portfolio,
        portfolio.portfolio_weekly_pnl,
        params.weekly_loss_halt_pct,
        "weekly_loss_halt_pct",
        "weekly",
    )


def check_per_position_stop_loss(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Per-position stop-loss at proposal time: buying more of a position
    already at or past its stop level (averaging down into a stopped-out
    name) is rejected. Selling it is the remedy and always passes."""
    if proposal.action is not ProposalAction.BUY:
        return None
    if portfolio.agent_position_avg_cost is None:
        return None
    avg_cost = portfolio.agent_position_avg_cost
    loss_fraction = (avg_cost - instrument.price) / avg_cost
    if loss_fraction < params.per_position_stop_loss_pct:
        return None
    return Violation(
        rule="per_position_stop_loss_pct",
        limit=params.per_position_stop_loss_pct,
        observed=loss_fraction,
        message=(
            f"existing {proposal.ticker} position is down {loss_fraction} from avg cost "
            f"{avg_cost}, at/past the {params.per_position_stop_loss_pct} stop-loss — "
            "cannot add to a stopped-out position"
        ),
    )


def check_trade_frequency(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Anti-overtrading: at most max_trades_per_agent_per_day executed
    trades per agent per day; this proposal would be trade N+1."""
    if proposal.action is ProposalAction.HOLD:
        return None
    would_be = portfolio.agent_trades_today + 1
    if would_be <= params.max_trades_per_agent_per_day:
        return None
    return Violation(
        rule="max_trades_per_agent_per_day",
        limit=params.max_trades_per_agent_per_day,
        observed=would_be,
        message=(
            f"agent already executed {portfolio.agent_trades_today} trades today; "
            f"this would be trade {would_be}, over the "
            f"{params.max_trades_per_agent_per_day}/day limit"
        ),
    )


def check_blacklist(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Instrument-class blacklist (§6.1): leveraged/inverse ETFs,
    derivatives, and sub-min-price names cannot be bought."""
    if proposal.action is not ProposalAction.BUY:
        return None
    reasons: list[str] = []
    if params.blacklist.leveraged_etfs and instrument.is_leveraged_etf:
        reasons.append("leveraged ETF")
    if params.blacklist.inverse_etfs and instrument.is_inverse_etf:
        reasons.append("inverse ETF")
    if params.blacklist.derivatives and instrument.is_derivative:
        reasons.append("derivative")
    if instrument.price < params.blacklist.min_price_usd:
        reasons.append(f"price {instrument.price} below minimum {params.blacklist.min_price_usd}")
    if not reasons:
        return None
    return Violation(
        rule="blacklist",
        limit=None,
        observed=reasons,
        message=f"{proposal.ticker} is blacklisted: {'; '.join(reasons)}",
    )


def check_whitelist(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> Violation | None:
    """Early-phase whitelist (§6.1): buys restricted to members of the
    configured index (e.g. S&P 500). whitelist=null disables the rule."""
    if proposal.action is not ProposalAction.BUY:
        return None
    if params.whitelist is None:
        return None
    if params.whitelist in instrument.index_memberships:
        return None
    return Violation(
        rule="whitelist",
        limit=params.whitelist,
        observed=sorted(instrument.index_memberships),
        message=f"{proposal.ticker} is not in the {params.whitelist} whitelist",
    )


# Evaluation order mirrors the §6.1 table. The engine always runs all of
# them — no short-circuit — so the decisions ledger records every problem.
ALL_RULES: tuple[RuleFn, ...] = (
    check_max_position_per_agent,
    check_max_position_portfolio,
    check_max_sector_exposure,
    check_daily_loss_breaker,
    check_weekly_loss_breaker,
    check_per_position_stop_loss,
    check_trade_frequency,
    check_blacklist,
    check_whitelist,
)


def evaluate_proposal(
    proposal: ProposalRequest,
    instrument: InstrumentSnapshot,
    portfolio: PortfolioState,
    params: HardRuleParams,
) -> HardRuleResult:
    """Run every hard rule; any violation ⇒ auto-reject upstream (§3.2, §7)."""
    if proposal.ticker != instrument.ticker:
        raise ValueError(
            f"instrument snapshot is for {instrument.ticker!r}, proposal is for "
            f"{proposal.ticker!r} — refusing to evaluate mismatched state"
        )
    violations = tuple(
        violation
        for rule in ALL_RULES
        if (violation := rule(proposal, instrument, portfolio, params)) is not None
    )
    return HardRuleResult(violations=violations)
