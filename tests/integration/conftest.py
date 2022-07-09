import logging

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer


logger = logging.getLogger(__name__)


@pytest.fixture()
async def session(postgres_url: str) -> AsyncSession:
    engine = create_async_engine(url=postgres_url)
    pool = sessionmaker(bind=engine, class_=AsyncSession,
                        expire_on_commit=False, autoflush=False)
    async with pool() as session:
        yield session


@pytest.fixture()
async def postgres_url() -> str:
    with PostgresContainer("postgres:13") as postgres:
        postgres_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url)
        return postgres_url

