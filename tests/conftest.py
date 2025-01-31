import pytest
import asyncio
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.config import Config
from alembic import command
from task_management import config


@pytest.fixture(scope="session")
def event_loop():
    """Allow pytest-asyncio to use a session-scoped event loop."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_postgres():
    """Start a test PostgreSQL container."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_db_uri(test_postgres):
    """Return the test database URI and replace get_db_uri in config."""
    db_uri = test_postgres.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    config.get_db_uri = lambda: db_uri
    return db_uri


@pytest.fixture(scope="session", autouse=True)
async def apply_migrations(test_db_uri):
    """Run Alembic migrations on the test database."""
    alembic_cfg = Config("alembic.ini")
    test_db_uri = test_db_uri.replace('+asyncpg', '')
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_uri)

    command.upgrade(alembic_cfg, "head")
    yield

