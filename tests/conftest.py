import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from testcontainers.postgres import PostgresContainer

from app.db.database import Base
from app.repositories.link import LinkRepository
from tests.utils import make_link


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:15-alpine", driver="asyncpg") as pg:
        yield pg


@pytest_asyncio.fixture
async def engine(pg_container):
    engine = create_async_engine(
        pg_container.get_connection_url(),
        connect_args={"ssl": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield async_session
    finally:
        await async_session.close()
        async with engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())


@pytest_asyncio.fixture
async def repo(session):
    return LinkRepository(session)


@pytest_asyncio.fixture
async def created_link(repo):
    return await repo.create(make_link())
