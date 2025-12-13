import logging
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.dao.holder import HolderDao
from app.models.config import Config
from tests.mocks.config import DBConfig

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def session(pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session_:
        yield session_


@pytest_asyncio.fixture
async def dao(session: AsyncSession) -> HolderDao:
    return HolderDao(session=session)


@pytest.fixture(scope="session")
def pool(postgres_url: str) -> sessionmaker:
    engine = create_async_engine(url=postgres_url)
    return sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )  # type: ignore[call-overload]


@pytest.fixture(scope="session")
def postgres_url(app_config: Config) -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:11")
    if os.name == "nt":  # TODO workaround from testcontainers-python#108  # noqa: FIX002
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        app_config.db = DBConfig(postgres_url_)  # type: ignore[assignment]
        yield postgres_url_
    finally:
        postgres.stop()
