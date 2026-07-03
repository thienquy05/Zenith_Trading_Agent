"""Hard-rules engine test matrix (roadmap branch 3).

Pure-function tests — no database, no network. Every rule is exercised at
its boundary: exactly at a cap passes and one cent over fails; exactly at
a breaker/stop trigger fires. Plus action applicability (buy/sell/hold),
whole-engine aggregation (every violation reported, not just the first),
and fail-closed params parsing.
"""

import json
from decimal import Decimal

import pytest

from app.models.proposal import ProposalAction
from app.rules import (
    ALL_RULES,
    HardRuleParams,
    InstrumentSnapshot,
    PortfolioState,
    ProposalRequest,
    evaluate_proposal,
)

# Mirror of migration 0003's seeded §6.1 version-1 row — the engine must
# accept the exact snapshot shape that lives in the database.
SEEDED_DEFAULTS = {
    "max_position_pct_per_agent": 0.20,
    "max_position_pct_portfolio": 0.10,
    "max_sector_exposure_pct": 0.30,
    "daily_loss_halt_pct": 0.03,
    "weekly_loss_halt_pct": 0.05,
    "per_position_stop_loss_pct": 0.08,
    "max_trades_per_agent_per_day": 5,
    "blacklist": {
        "leveraged_etfs": True,
        "inverse_etfs": True,
        "derivatives": True,
        "min_price_usd": 5,
    },
    "whitelist": "sp500",
}

PARAMS = HardRuleParams.from_snapshot(SEEDED_DEFAULTS)


def make_proposal(
    action: ProposalAction = ProposalAction.BUY,
    ticker: str = "AAPL",
    quantity: str = "10",
) -> ProposalRequest:
    return ProposalRequest(action=action, ticker=ticker, quantity=Decimal(quantity))


def make_instrument(
    ticker: str = "AAPL",
    price: str = "100",
    sector: str | None = "Information Technology",
    **flags,
) -> InstrumentSnapshot:
    return InstrumentSnapshot(
        ticker=ticker,
        price=Decimal(price),
        sector=sector,
        index_memberships=flags.pop("index_memberships", frozenset({"sp500"})),
        **flags,
    )


def make_portfolio(**overrides) -> PortfolioState:
    defaults = dict(
        agent_allocated_capital=Decimal("10000"),
        portfolio_total_value=Decimal("100000"),
    )
    defaults.update(overrides)
    return PortfolioState(**defaults)


def violated_rules(proposal, instrument, portfolio, params=PARAMS) -> set[str]:
    return {v.rule for v in evaluate_proposal(proposal, instrument, portfolio, params).violations}


# --- max position per agent (20% of agent capital = 2000) ---------------


def test_agent_cap_exactly_at_limit_passes():
    # existing 1000 + 10 shares * 100 = 2000, exactly 20% of 10000
    portfolio = make_portfolio(agent_position_value=Decimal("1000"))
    assert "max_position_pct_per_agent" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_agent_cap_one_cent_over_fails():
    portfolio = make_portfolio(agent_position_value=Decimal("1000.01"))
    assert "max_position_pct_per_agent" in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_agent_cap_ignores_sell_and_hold():
    portfolio = make_portfolio(agent_position_value=Decimal("9000"))
    for action in (ProposalAction.SELL, ProposalAction.HOLD):
        assert "max_position_pct_per_agent" not in violated_rules(
            make_proposal(action=action), make_instrument(), portfolio
        )


# --- max position portfolio-wide (10% of 100000 = 10000) ----------------


def test_portfolio_cap_exactly_at_limit_passes():
    portfolio = make_portfolio(portfolio_position_value=Decimal("9000"))
    assert "max_position_pct_portfolio" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_portfolio_cap_one_cent_over_fails():
    portfolio = make_portfolio(portfolio_position_value=Decimal("9000.01"))
    assert "max_position_pct_portfolio" in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_portfolio_cap_catches_pileup_even_when_agent_is_clean():
    """The §6.1 rationale: every agent piling into one name must trip the
    portfolio-wide cap even though each agent is inside its own cap."""
    portfolio = make_portfolio(
        agent_position_value=Decimal("0"),
        portfolio_position_value=Decimal("9500"),
    )
    rules = violated_rules(make_proposal(quantity="6"), make_instrument(), portfolio)
    assert "max_position_pct_portfolio" in rules
    assert "max_position_pct_per_agent" not in rules


# --- max sector exposure (30% of 100000 = 30000) -------------------------


def test_sector_cap_exactly_at_limit_passes():
    portfolio = make_portfolio(sector_exposure_value=Decimal("29000"))
    assert "max_sector_exposure_pct" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_sector_cap_one_cent_over_fails():
    portfolio = make_portfolio(sector_exposure_value=Decimal("29000.01"))
    assert "max_sector_exposure_pct" in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_unknown_sector_fails_closed_for_buys():
    assert "max_sector_exposure_pct" in violated_rules(
        make_proposal(), make_instrument(sector=None), make_portfolio()
    )


def test_unknown_sector_does_not_block_sells():
    assert "max_sector_exposure_pct" not in violated_rules(
        make_proposal(action=ProposalAction.SELL), make_instrument(sector=None), make_portfolio()
    )


# --- daily / weekly loss circuit breakers --------------------------------


def test_daily_breaker_just_under_threshold_passes():
    portfolio = make_portfolio(portfolio_daily_pnl=Decimal("-2999.99"))
    assert "daily_loss_halt_pct" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_daily_breaker_fires_exactly_at_threshold():
    # -3% of 100000 = -3000: the breaker is a trigger, inclusive
    portfolio = make_portfolio(portfolio_daily_pnl=Decimal("-3000"))
    assert "daily_loss_halt_pct" in violated_rules(make_proposal(), make_instrument(), portfolio)


def test_daily_breaker_blocks_sells_too():
    portfolio = make_portfolio(portfolio_daily_pnl=Decimal("-3000"))
    assert "daily_loss_halt_pct" in violated_rules(
        make_proposal(action=ProposalAction.SELL), make_instrument(), portfolio
    )


def test_daily_breaker_ignores_holds():
    portfolio = make_portfolio(portfolio_daily_pnl=Decimal("-3000"))
    assert "daily_loss_halt_pct" not in violated_rules(
        make_proposal(action=ProposalAction.HOLD), make_instrument(), portfolio
    )


def test_daily_gain_never_trips_breaker():
    portfolio = make_portfolio(portfolio_daily_pnl=Decimal("5000"))
    assert "daily_loss_halt_pct" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_weekly_breaker_boundary():
    # -5% of 100000 = -5000
    under = make_portfolio(portfolio_weekly_pnl=Decimal("-4999.99"))
    at = make_portfolio(portfolio_weekly_pnl=Decimal("-5000"))
    assert "weekly_loss_halt_pct" not in violated_rules(make_proposal(), make_instrument(), under)
    assert "weekly_loss_halt_pct" in violated_rules(make_proposal(), make_instrument(), at)


def test_weekly_breaker_catches_slow_bleed_daily_misses():
    portfolio = make_portfolio(
        portfolio_daily_pnl=Decimal("-1000"),  # only -1% today
        portfolio_weekly_pnl=Decimal("-6000"),  # but -6% on the week
    )
    rules = violated_rules(make_proposal(), make_instrument(), portfolio)
    assert "weekly_loss_halt_pct" in rules
    assert "daily_loss_halt_pct" not in rules


# --- per-position stop-loss (8%) ------------------------------------------


def test_stop_loss_just_inside_allows_averaging():
    # avg cost 100, price 92.01 → down 7.99%
    portfolio = make_portfolio(
        agent_position_value=Decimal("100"), agent_position_avg_cost=Decimal("100")
    )
    assert "per_position_stop_loss_pct" not in violated_rules(
        make_proposal(quantity="1"), make_instrument(price="92.01"), portfolio
    )


def test_stop_loss_fires_exactly_at_threshold():
    # avg cost 100, price 92 → down exactly 8%
    portfolio = make_portfolio(
        agent_position_value=Decimal("100"), agent_position_avg_cost=Decimal("100")
    )
    assert "per_position_stop_loss_pct" in violated_rules(
        make_proposal(quantity="1"), make_instrument(price="92"), portfolio
    )


def test_stop_loss_never_blocks_the_sell_that_remedies_it():
    portfolio = make_portfolio(
        agent_position_value=Decimal("100"), agent_position_avg_cost=Decimal("100")
    )
    assert "per_position_stop_loss_pct" not in violated_rules(
        make_proposal(action=ProposalAction.SELL, quantity="1"),
        make_instrument(price="80"),
        portfolio,
    )


def test_stop_loss_not_applicable_without_existing_position():
    portfolio = make_portfolio(agent_position_avg_cost=None)
    assert "per_position_stop_loss_pct" not in violated_rules(
        make_proposal(quantity="1"), make_instrument(price="1000"), portfolio
    )


# --- trade frequency (≤5/agent/day) ---------------------------------------


def test_fifth_trade_of_the_day_allowed():
    portfolio = make_portfolio(agent_trades_today=4)
    assert "max_trades_per_agent_per_day" not in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_sixth_trade_of_the_day_rejected():
    portfolio = make_portfolio(agent_trades_today=5)
    assert "max_trades_per_agent_per_day" in violated_rules(
        make_proposal(), make_instrument(), portfolio
    )


def test_frequency_counts_sells_but_not_holds():
    portfolio = make_portfolio(agent_trades_today=5)
    assert "max_trades_per_agent_per_day" in violated_rules(
        make_proposal(action=ProposalAction.SELL), make_instrument(), portfolio
    )
    assert "max_trades_per_agent_per_day" not in violated_rules(
        make_proposal(action=ProposalAction.HOLD), make_instrument(), portfolio
    )


# --- blacklist -------------------------------------------------------------


@pytest.mark.parametrize("flag", ["is_leveraged_etf", "is_inverse_etf", "is_derivative"])
def test_blacklisted_instrument_classes_rejected_on_buy(flag):
    instrument = make_instrument(**{flag: True})
    assert "blacklist" in violated_rules(make_proposal(), instrument, make_portfolio())


def test_blacklist_class_can_be_disabled_by_params():
    snapshot = json.loads(json.dumps(SEEDED_DEFAULTS))
    snapshot["blacklist"]["leveraged_etfs"] = False
    params = HardRuleParams.from_snapshot(snapshot)
    instrument = make_instrument(is_leveraged_etf=True)
    assert "blacklist" not in violated_rules(make_proposal(), instrument, make_portfolio(), params)


def test_sub_five_dollar_stock_rejected_and_five_dollar_passes():
    assert "blacklist" in violated_rules(
        make_proposal(), make_instrument(price="4.99"), make_portfolio()
    )
    assert "blacklist" not in violated_rules(
        make_proposal(), make_instrument(price="5"), make_portfolio()
    )


def test_selling_a_blacklisted_name_is_allowed():
    instrument = make_instrument(is_leveraged_etf=True, price="3")
    assert "blacklist" not in violated_rules(
        make_proposal(action=ProposalAction.SELL), instrument, make_portfolio()
    )


def test_blacklist_reports_every_reason_at_once():
    instrument = make_instrument(is_leveraged_etf=True, is_inverse_etf=True, price="2")
    result = evaluate_proposal(make_proposal(), instrument, make_portfolio(), PARAMS)
    blacklist = next(v for v in result.violations if v.rule == "blacklist")
    assert len(blacklist.observed) == 3


# --- whitelist --------------------------------------------------------------


def test_non_sp500_buy_rejected():
    instrument = make_instrument(index_memberships=frozenset())
    assert "whitelist" in violated_rules(make_proposal(), instrument, make_portfolio())


def test_sp500_member_buy_passes():
    assert "whitelist" not in violated_rules(make_proposal(), make_instrument(), make_portfolio())


def test_selling_out_of_a_delisted_name_is_allowed():
    instrument = make_instrument(index_memberships=frozenset())
    assert "whitelist" not in violated_rules(
        make_proposal(action=ProposalAction.SELL), instrument, make_portfolio()
    )


def test_null_whitelist_disables_the_rule():
    snapshot = dict(SEEDED_DEFAULTS, whitelist=None)
    params = HardRuleParams.from_snapshot(snapshot)
    instrument = make_instrument(index_memberships=frozenset())
    assert "whitelist" not in violated_rules(make_proposal(), instrument, make_portfolio(), params)


# --- whole-engine behavior ---------------------------------------------------


def test_clean_buy_passes_every_rule():
    result = evaluate_proposal(make_proposal(), make_instrument(), make_portfolio(), PARAMS)
    assert result.passed
    assert result.violations == ()


def test_hold_moves_no_money_and_always_passes():
    portfolio = make_portfolio(
        agent_position_value=Decimal("9999"),
        portfolio_daily_pnl=Decimal("-50000"),
        agent_trades_today=99,
    )
    instrument = make_instrument(sector=None, is_derivative=True, price="1")
    result = evaluate_proposal(
        make_proposal(action=ProposalAction.HOLD), instrument, portfolio, PARAMS
    )
    assert result.passed


def test_every_violation_reported_in_one_pass_not_just_the_first():
    """§3.2: the audit trail and the agent learn everything wrong at once."""
    portfolio = make_portfolio(
        agent_position_value=Decimal("2000"),  # agent cap already full
        portfolio_position_value=Decimal("10000"),  # portfolio cap already full
        sector_exposure_value=Decimal("30000"),  # sector cap already full
        portfolio_daily_pnl=Decimal("-3000"),  # daily breaker tripped
        portfolio_weekly_pnl=Decimal("-5000"),  # weekly breaker tripped
        agent_position_avg_cost=Decimal("100"),  # position down 96% → stop
        agent_trades_today=5,  # frequency exhausted
    )
    instrument = make_instrument(
        price="4",  # sub-$5 → blacklist (and deepens the stop-loss)
        is_leveraged_etf=True,
        index_memberships=frozenset(),  # not in sp500 → whitelist
    )
    result = evaluate_proposal(make_proposal(), instrument, portfolio, PARAMS)
    assert not result.passed
    assert {v.rule for v in result.violations} == {
        "max_position_pct_per_agent",
        "max_position_pct_portfolio",
        "max_sector_exposure_pct",
        "daily_loss_halt_pct",
        "weekly_loss_halt_pct",
        "per_position_stop_loss_pct",
        "max_trades_per_agent_per_day",
        "blacklist",
        "whitelist",
    }
    assert len(result.violations) == len(ALL_RULES)


def test_result_details_are_json_serializable_for_the_decisions_ledger():
    portfolio = make_portfolio(agent_position_value=Decimal("2000.01"))
    result = evaluate_proposal(make_proposal(), make_instrument(), portfolio, PARAMS)
    details = result.to_details()
    round_tripped = json.loads(json.dumps(details))
    assert round_tripped["passed"] is False
    violation = round_tripped["violations"][0]
    assert violation["rule"] == "max_position_pct_per_agent"
    # Decimals serialized as exact strings, not floats
    assert violation["limit"] == "2000.0"
    assert violation["observed"] == "3000.01"


def test_mismatched_instrument_snapshot_is_refused():
    with pytest.raises(ValueError, match="mismatched"):
        evaluate_proposal(
            make_proposal(ticker="AAPL"),
            make_instrument(ticker="MSFT"),
            make_portfolio(),
            PARAMS,
        )


# --- params parsing (fail closed) ---------------------------------------------


def test_seeded_defaults_parse_with_exact_decimals():
    assert PARAMS.max_position_pct_per_agent == Decimal("0.2")
    assert PARAMS.daily_loss_halt_pct == Decimal("0.03")
    assert PARAMS.blacklist.min_price_usd == Decimal("5")
    assert PARAMS.max_trades_per_agent_per_day == 5
    assert PARAMS.whitelist == "sp500"


@pytest.mark.parametrize(
    "missing",
    [
        "max_position_pct_per_agent",
        "max_position_pct_portfolio",
        "max_sector_exposure_pct",
        "daily_loss_halt_pct",
        "weekly_loss_halt_pct",
        "per_position_stop_loss_pct",
        "max_trades_per_agent_per_day",
        "blacklist",
        "whitelist",
    ],
)
def test_missing_param_key_raises_instead_of_defaulting(missing):
    snapshot = {k: v for k, v in SEEDED_DEFAULTS.items() if k != missing}
    with pytest.raises(ValueError, match=missing):
        HardRuleParams.from_snapshot(snapshot)


@pytest.mark.parametrize(
    ("key", "bad"),
    [
        ("max_position_pct_per_agent", 0),
        ("max_position_pct_per_agent", 1.5),
        ("daily_loss_halt_pct", -0.03),
        ("max_trades_per_agent_per_day", 0),
        ("max_trades_per_agent_per_day", "5"),
        ("whitelist", ""),
    ],
)
def test_out_of_range_param_raises(key, bad):
    with pytest.raises(ValueError):
        HardRuleParams.from_snapshot(dict(SEEDED_DEFAULTS, **{key: bad}))


def test_bad_blacklist_shapes_raise():
    with pytest.raises(ValueError):
        HardRuleParams.from_snapshot(dict(SEEDED_DEFAULTS, blacklist="everything"))
    broken = json.loads(json.dumps(SEEDED_DEFAULTS))
    broken["blacklist"]["min_price_usd"] = -1
    with pytest.raises(ValueError):
        HardRuleParams.from_snapshot(broken)
    del broken["blacklist"]["min_price_usd"]
    with pytest.raises(ValueError, match="min_price_usd"):
        HardRuleParams.from_snapshot(broken)


# --- input validation (fail closed) --------------------------------------------


def test_nonsensical_inputs_raise():
    with pytest.raises(ValueError):
        make_proposal(quantity="0")
    with pytest.raises(ValueError):
        make_instrument(price="0")
    with pytest.raises(ValueError):
        make_portfolio(agent_allocated_capital=Decimal("0"))
    with pytest.raises(ValueError):
        make_portfolio(portfolio_total_value=Decimal("0"))
    with pytest.raises(ValueError):
        make_portfolio(agent_trades_today=-1)
    with pytest.raises(ValueError):
        make_portfolio(agent_position_value=Decimal("-1"))
