import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401 (registers all tables on Base.metadata)
from app.config import get_settings
from app.database import Base


@pytest.fixture(scope="session")
def engine():
    """Requires a live Postgres reachable via the settings' DATABASE_URL
    (see app/config.py) — these fixtures are only pulled in by tests that
    need real ORM/constraint behavior (test_models.py), not by tests that
    can run standalone (test_security.py, test_main.py).
    """
    eng = create_engine(get_settings().database_url)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
