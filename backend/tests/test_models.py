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
    LlmProvider,
    User,
    UserRole,
)


def make_user(db_session, email="trader@example.com"):
    user = User(email=email, password_hash=security.hash_password("s3cret!"))
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


def test_user_defaults(db_session):
    user = make_user(db_session)

    assert user.id is not None
    assert user.role == UserRole.USER
    assert user.is_active is True


def test_user_email_must_be_unique(db_session):
    make_user(db_session, email="dup@example.com")
    db_session.flush()

    with pytest.raises(IntegrityError):
        make_user(db_session, email="dup@example.com")


def test_account_links_user_and_agent_with_defaults(db_session):
    user = make_user(db_session)
    agent = make_agent(db_session)

    account = Account(
        user_id=user.id, agent_id=agent.id, account_name="main", allocated_capital=1000
    )
    db_session.add(account)
    db_session.flush()

    assert account.status == AccountStatus.ACTIVE
    assert account.current_balance == 0
    assert account.currency == "USD"


def test_account_rejects_negative_allocated_capital(db_session):
    user = make_user(db_session)
    agent = make_agent(db_session)

    account = Account(
        user_id=user.id, agent_id=agent.id, account_name="main", allocated_capital=-1
    )
    db_session.add(account)

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_deleting_user_cascades_to_their_accounts(db_session):
    user = make_user(db_session)
    agent = make_agent(db_session)
    account = Account(user_id=user.id, agent_id=agent.id, account_name="main")
    db_session.add(account)
    db_session.flush()
    account_id = account.id

    db_session.delete(user)
    db_session.flush()

    assert db_session.get(Account, account_id) is None


def test_deleting_agent_with_open_accounts_is_restricted(db_session):
    user = make_user(db_session)
    agent = make_agent(db_session)
    account = Account(user_id=user.id, agent_id=agent.id, account_name="main")
    db_session.add(account)
    db_session.flush()

    db_session.delete(agent)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_api_credential_never_stores_plaintext(db_session, clear_settings_cache, monkeypatch):
    monkeypatch.setenv("CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode())
    user = make_user(db_session, email="creds@example.com")
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
