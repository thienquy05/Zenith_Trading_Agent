"""ORM/constraint-level tests against a real Postgres (see conftest.py's
`engine`/`db_session` fixtures) — CI runs these against a service
container. Not runnable without a live Postgres reachable at the
settings' DATABASE_URL.
"""
from cryptography.fernet import Fernet
from sqlalchemy.exc import IntegrityError

import pytest

from app import security
from app.models import (
    Account,
    AccountStatus,
    Agent,
    AgentType,
    ApiCredential,
    ApiUsageLog,
    CredentialProvider,
    Decision,
    DecisionOutcome,
    DecisionStage,
    HardRuleParams,
    LlmProvider,
    Order,
    OrderBroker,
    OrderSide,
    Position,
    Proposal,
    ProposalAction,
    ProposalStatus,
    SystemControl,
    User,
)


def make_user(db_session, username="trader"):
    user = User(username=username, password_hash=security.hash_password("s3cret!"))
    db_session.add(user)
    db_session.flush()
    return user


def make_agent(db_session, name="Momentum-Claude"):
    agent = Agent(
        name=name,
        agent_type=AgentType.MEMBER,
        llm_provider=LlmProvider.ANTHROPIC,
        llm_model="claude-sonnet-5",
    )
    db_session.add(agent)
    db_session.flush()
    return agent


def make_account(db_session, allocated_capital=1000):
    user = make_user(db_session)
    agent = make_agent(db_session)
    account = Account(
        user_id=user.id,
        agent_id=agent.id,
        account_name="main",
        allocated_capital=allocated_capital,
    )
    db_session.add(account)
    db_session.flush()
    return account


def make_proposal(db_session, account, **overrides):
    fields = dict(
        account_id=account.id,
        action=ProposalAction.BUY,
        ticker="AAPL",
        quantity=10,
        reasoning="momentum breakout above 50-day MA",
        confidence="0.8",
        capital_snapshot={"allocated": "1000", "cash": "1000", "positions": {}},
    )
    fields.update(overrides)
    proposal = Proposal(**fields)
    db_session.add(proposal)
    db_session.flush()
    return proposal


def test_user_defaults(db_session):
    user = make_user(db_session)

    assert user.id is not None
    assert user.is_active is True


def test_user_username_must_be_unique(db_session):
    make_user(db_session, username="dup")
    db_session.flush()

    with pytest.raises(IntegrityError):
        make_user(db_session, username="dup")


def test_account_links_user_and_agent_with_defaults(db_session):
    account = make_account(db_session)

    assert account.status == AccountStatus.ACTIVE
    assert account.current_balance == 0
    assert account.currency == "USD"


def test_account_rejects_negative_allocated_capital(db_session):
    with pytest.raises(IntegrityError):
        make_account(db_session, allocated_capital=-1)


def test_deleting_user_cascades_to_their_accounts(db_session):
    account = make_account(db_session)
    account_id = account.id

    db_session.delete(account.user)
    db_session.flush()
    # The DB's ON DELETE CASCADE removed the row behind the ORM's back
    # (passive_deletes) — expire the identity map so get() re-queries.
    db_session.expire_all()

    assert db_session.get(Account, account_id) is None


def test_deleting_user_cascades_to_their_api_credentials(db_session, clear_settings_cache, monkeypatch):
    # Security-relevant cleanup: a deleted user must not leave encrypted
    # credential rows behind (ON DELETE CASCADE on api_credentials.user_id).
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode())
    user = make_user(db_session, username="cascade-creds")
    credential = ApiCredential(
        user_id=user.id,
        provider=CredentialProvider.OPENAI,
        credential_name="default",
        encrypted_value=security.encrypt_secret("sk-live-1234567890"),
    )
    db_session.add(credential)
    db_session.flush()
    credential_id = credential.id

    db_session.delete(user)
    db_session.flush()
    db_session.expire_all()

    assert db_session.get(ApiCredential, credential_id) is None


def test_deleting_agent_with_open_accounts_is_restricted(db_session):
    account = make_account(db_session)

    db_session.delete(account.agent)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_api_credential_never_stores_plaintext(db_session, clear_settings_cache, monkeypatch):
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode())
    user = make_user(db_session, username="creds")
    plaintext = "sk-live-1234567890"

    credential = ApiCredential(
        user_id=user.id,
        provider=CredentialProvider.OPENAI,
        credential_name="default",
        encrypted_value=security.encrypt_secret(plaintext),
    )
    db_session.add(credential)
    db_session.flush()

    assert plaintext.encode() not in credential.encrypted_value
    assert security.decrypt_secret(credential.encrypted_value) == plaintext


def test_api_usage_log_rejects_negative_token_counts(db_session):
    agent = make_agent(db_session, name="Sentiment-Gemini")

    log = ApiUsageLog(
        agent_id=agent.id, provider=LlmProvider.GOOGLE, model="gemini-2.5", tokens_in=-5
    )
    db_session.add(log)

    with pytest.raises(IntegrityError):
        db_session.flush()


# --- trading core (migration 0003) -----------------------------------------


def test_proposal_defaults_and_revision_chain(db_session):
    account = make_account(db_session)
    rejected = make_proposal(db_session, account, status=ProposalStatus.REJECTED_HARD_RULES)

    # Revise-and-resubmit (§6 Q4): a new row pointing at the rejected one.
    revised = make_proposal(db_session, account, quantity=5, parent_proposal_id=rejected.id)

    assert revised.status == ProposalStatus.SUBMITTED
    assert revised.parent_proposal is rejected


def test_proposal_rejects_zero_quantity(db_session):
    account = make_account(db_session)

    with pytest.raises(IntegrityError):
        make_proposal(db_session, account, quantity=0)


def test_proposal_rejects_confidence_above_one(db_session):
    account = make_account(db_session)

    with pytest.raises(IntegrityError):
        make_proposal(db_session, account, confidence="1.5")


def test_deleting_account_with_proposal_history_is_restricted(db_session):
    # Audit integrity: proposal history pins its account (and transitively
    # the user and agent) in place — the DB refuses the delete.
    account = make_account(db_session)
    make_proposal(db_session, account)

    db_session.delete(account)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_decision_records_params_version_used(db_session):
    account = make_account(db_session)
    proposal = make_proposal(db_session, account)
    params = HardRuleParams(
        params={"max_trades_per_agent_per_day": 5}, reason="test version"
    )
    db_session.add(params)
    db_session.flush()

    decision = Decision(
        proposal_id=proposal.id,
        stage=DecisionStage.HARD_RULES,
        outcome=DecisionOutcome.PASSED,
        details={"violations": []},
        hard_rule_params_id=params.id,
    )
    db_session.add(decision)
    db_session.flush()

    assert decision.hard_rule_params is params
    assert decision.decided_by_user_id is None  # automated stage, no human


def test_deleting_proposal_with_decisions_is_restricted(db_session):
    # The §7 audit ledger must never lose its subject rows.
    account = make_account(db_session)
    proposal = make_proposal(db_session, account)
    db_session.add(
        Decision(
            proposal_id=proposal.id,
            stage=DecisionStage.HARD_RULES,
            outcome=DecisionOutcome.REJECTED,
        )
    )
    db_session.flush()

    db_session.delete(proposal)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_order_idempotency_key_must_be_unique(db_session):
    account = make_account(db_session)
    proposal = make_proposal(db_session, account)

    def order():
        return Order(
            proposal_id=proposal.id,
            broker=OrderBroker.PAPER,
            side=OrderSide.BUY,
            ticker="AAPL",
            quantity=10,
            idempotency_key="retry-safe-key-1",
        )

    db_session.add(order())
    db_session.flush()
    db_session.add(order())

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_order_fill_cannot_exceed_quantity(db_session):
    account = make_account(db_session)
    proposal = make_proposal(db_session, account)
    db_session.add(
        Order(
            proposal_id=proposal.id,
            broker=OrderBroker.PAPER,
            side=OrderSide.BUY,
            ticker="AAPL",
            quantity=10,
            filled_quantity=11,
            idempotency_key="overfill",
        )
    )

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_position_unique_per_account_and_ticker(db_session):
    account = make_account(db_session)
    db_session.add(Position(account_id=account.id, ticker="AAPL", quantity=10, avg_cost=190))
    db_session.flush()
    db_session.add(Position(account_id=account.id, ticker="AAPL", quantity=5, avg_cost=200))

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_system_controls_is_single_row(db_session):
    # The CHECK pins id=1 — a second kill-switch row can never exist.
    db_session.add(SystemControl(id=2, trading_halted=True))

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_usage_log_survives_proposal_delete_with_link_nulled(db_session):
    account = make_account(db_session)
    proposal = make_proposal(db_session, account)
    log = ApiUsageLog(
        agent_id=account.agent_id,
        provider=LlmProvider.ANTHROPIC,
        model="claude-sonnet-5",
        linked_proposal_id=proposal.id,
    )
    db_session.add(log)
    db_session.flush()

    db_session.delete(proposal)
    db_session.flush()
    db_session.expire_all()

    refreshed = db_session.get(ApiUsageLog, log.id)
    assert refreshed is not None
    assert refreshed.linked_proposal_id is None
