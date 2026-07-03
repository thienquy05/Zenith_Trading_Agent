"""Hard-rules engine — §3.2 layer 1, the deterministic money gate.

Pure functions only: input = proposal + market/portfolio state + a
hard_rule_params snapshot; output = a structured violations list. No DB,
no network, no LLM inside — the caller fetches state and persists the
result. Any violation ⇒ auto-reject, no LLM involved (§3.2, §7).
"""

from app.rules.engine import ALL_RULES, evaluate_proposal
from app.rules.params import BlacklistParams, HardRuleParams
from app.rules.types import (
    HardRuleResult,
    InstrumentSnapshot,
    PortfolioState,
    ProposalRequest,
    Violation,
)

__all__ = [
    "ALL_RULES",
    "BlacklistParams",
    "HardRuleParams",
    "HardRuleResult",
    "InstrumentSnapshot",
    "PortfolioState",
    "ProposalRequest",
    "Violation",
    "evaluate_proposal",
]
