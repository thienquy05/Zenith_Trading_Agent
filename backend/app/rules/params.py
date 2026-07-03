"""Typed view of a hard_rule_params.params JSONB snapshot.

The DB row (seeded by migration 0003, versioned append-only per §3.3) is
the source of truth; this module only parses and validates it. Parsing is
strict — a missing or out-of-range key raises ValueError instead of
falling back to a default, so a malformed snapshot can never silently
weaken the gate.

JSON numbers arrive as float/int; they are converted via Decimal(str(x))
so 0.2 becomes exactly Decimal("0.2").
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any


def _as_decimal(snapshot: dict[str, Any], key: str) -> Decimal:
    try:
        value = Decimal(str(snapshot[key]))
    except KeyError:
        raise ValueError(f"hard_rule_params snapshot missing key: {key}") from None
    except InvalidOperation:
        raise ValueError(f"hard_rule_params key {key} is not a number: {snapshot[key]!r}") from None
    return value


def _as_unit_fraction(snapshot: dict[str, Any], key: str) -> Decimal:
    value = _as_decimal(snapshot, key)
    if not (0 < value <= 1):
        raise ValueError(f"hard_rule_params key {key} must be in (0, 1], got {value}")
    return value


@dataclass(frozen=True)
class BlacklistParams:
    leveraged_etfs: bool
    inverse_etfs: bool
    derivatives: bool
    min_price_usd: Decimal

    @classmethod
    def from_snapshot(cls, snapshot: dict[str, Any]) -> "BlacklistParams":
        for key in ("leveraged_etfs", "inverse_etfs", "derivatives"):
            if not isinstance(snapshot.get(key), bool):
                raise ValueError(f"blacklist key {key} must be a bool")
        min_price = _as_decimal(snapshot, "min_price_usd")
        if min_price < 0:
            raise ValueError(f"blacklist min_price_usd must be >= 0, got {min_price}")
        return cls(
            leveraged_etfs=snapshot["leveraged_etfs"],
            inverse_etfs=snapshot["inverse_etfs"],
            derivatives=snapshot["derivatives"],
            min_price_usd=min_price,
        )


@dataclass(frozen=True)
class HardRuleParams:
    """The §6.1 parameter set, validated and Decimal-typed."""

    max_position_pct_per_agent: Decimal
    max_position_pct_portfolio: Decimal
    max_sector_exposure_pct: Decimal
    daily_loss_halt_pct: Decimal
    weekly_loss_halt_pct: Decimal
    per_position_stop_loss_pct: Decimal
    max_trades_per_agent_per_day: int
    blacklist: BlacklistParams
    # Index key the ticker must belong to (e.g. "sp500"); None = no
    # whitelist restriction (later phases, per §6.1).
    whitelist: str | None

    @classmethod
    def from_snapshot(cls, snapshot: dict[str, Any]) -> "HardRuleParams":
        try:
            max_trades = snapshot["max_trades_per_agent_per_day"]
        except KeyError:
            raise ValueError(
                "hard_rule_params snapshot missing key: max_trades_per_agent_per_day"
            ) from None
        if not isinstance(max_trades, int) or isinstance(max_trades, bool) or max_trades < 1:
            raise ValueError(
                f"max_trades_per_agent_per_day must be a positive int, got {max_trades!r}"
            )

        try:
            blacklist_raw = snapshot["blacklist"]
        except KeyError:
            raise ValueError("hard_rule_params snapshot missing key: blacklist") from None
        if not isinstance(blacklist_raw, dict):
            raise ValueError("hard_rule_params key blacklist must be an object")

        # Key must be present even to opt out (explicit null) — an absent
        # key silently disabling the whitelist would be a fail-open path.
        if "whitelist" not in snapshot:
            raise ValueError("hard_rule_params snapshot missing key: whitelist")
        whitelist = snapshot["whitelist"]
        if whitelist is not None and (not isinstance(whitelist, str) or not whitelist):
            raise ValueError(f"whitelist must be a non-empty string or null, got {whitelist!r}")

        return cls(
            max_position_pct_per_agent=_as_unit_fraction(snapshot, "max_position_pct_per_agent"),
            max_position_pct_portfolio=_as_unit_fraction(snapshot, "max_position_pct_portfolio"),
            max_sector_exposure_pct=_as_unit_fraction(snapshot, "max_sector_exposure_pct"),
            daily_loss_halt_pct=_as_unit_fraction(snapshot, "daily_loss_halt_pct"),
            weekly_loss_halt_pct=_as_unit_fraction(snapshot, "weekly_loss_halt_pct"),
            per_position_stop_loss_pct=_as_unit_fraction(snapshot, "per_position_stop_loss_pct"),
            max_trades_per_agent_per_day=max_trades,
            blacklist=BlacklistParams.from_snapshot(blacklist_raw),
            whitelist=whitelist,
        )
