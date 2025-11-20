import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_url():
    """Spin up a disposable Postgres for integration tests."""
    image = os.getenv("POSTGRES_IMAGE", "postgres:15")
    with PostgresContainer(image) as pg:
        url = pg.get_connection_url().replace("postgresql://", "postgresql+psycopg2://")
        yield url


@pytest.fixture(scope="function")
def engine(postgres_url):
    engine = create_engine(postgres_url, future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture
def db_session(session_factory):
    session = session_factory()
    yield session
    session.close()


@pytest.fixture
def client(session_factory):
    """FastAPI client wired to the disposable database."""
    def _get_test_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.state.skip_db_init = True
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
