import logging
import os
import typing
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from dishka import AsyncContainer, Provider, Scope, make_async_container
from testcontainers.postgres import PostgresContainer

from app.dao.holder import HolderDao
from app.models.config import Config
from app.models.config.db import DBConfig
from app.tgbot.main_factory import get_bot_providers
from tests.mocks.config import DBConfigMock

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def dao(request_dishka: AsyncContainer) -> HolderDao:
    dao_ = await request_dishka.get(HolderDao)
    await clear_data(dao_)
    return dao_


@pytest.fixture(scope="session")
def postgres_url(app_config: Config) -> Generator[DBConfigMock, None, None]:
    postgres = PostgresContainer("postgres:11")
    if os.name == "nt":  # TODO workaround from testcontainers-python#108  # noqa: FIX002
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        db_config = DBConfigMock(_uri=postgres_url_)
        app_config.db = db_config
        yield db_config
    finally:
        postgres.stop()


@pytest_asyncio.fixture(scope="session")
async def dishka(
    postgres_url: DBConfigMock, app_config: Config
) -> AsyncGenerator[AsyncContainer, None]:
    mock_provider = Provider(scope=Scope.APP)
    mock_provider.provide(lambda: postgres_url, provides=DBConfig, scope=Scope.APP, override=True)
    mock_provider.provide(
        lambda: AsyncMock(BaseSession), provides=BaseSession, scope=Scope.APP, override=True
    )
    container = make_async_container(
        *get_bot_providers(),
        mock_provider,
        context={Config: app_config},
    )
    yield container
    await container.close()


@pytest.fixture()
async def request_dishka(dishka: AsyncContainer) -> AsyncGenerator[AsyncContainer, None]:
    async with dishka() as scoped:
        yield scoped


@pytest_asyncio.fixture
async def bot_session(dishka: AsyncContainer) -> BaseSession:
    return await dishka.get(BaseSession)


@pytest_asyncio.fixture
async def bot(dishka: AsyncContainer) -> Bot:
    return await dishka.get(Bot)


@pytest_asyncio.fixture
async def dp(dishka: AsyncContainer) -> Dispatcher:
    return await dishka.get(Dispatcher)


@pytest.fixture(autouse=True)
def clean_up_bot_session(bot_session: BaseSession) -> None:  # noqa: PT004
    session = typing.cast(MagicMock, bot_session)
    session.reset_mock(return_value=True, side_effect=True)


async def clear_data(dao: HolderDao) -> None:
    await dao.chat.delete_all()
    await dao.user.delete_all()
    await dao.commit()
