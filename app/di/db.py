import logging
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import dao
from app.dao.holder import HolderDao
from app.models.config.db import DBConfig, RedisConfig

logger = logging.getLogger(__name__)


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: DBConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(url=make_url(db_config.uri), echo=db_config.echo)
        yield engine
        await engine.dispose(close=True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session


class DAOProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_dao(self, session: AsyncSession) -> HolderDao:
        return HolderDao(session=session)

    @provide
    async def get_user_dao(self, holder: HolderDao) -> dao.UserDAO:
        return holder.user

    @provide
    def get_chat_dao(self, holder: HolderDao) -> dao.ChatDAO:
        return holder.chat


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, config: RedisConfig) -> AsyncIterable[Redis]:
        logger.info("created redis for %s", config)
        async with create_redis(config) as redis:
            yield redis


def create_redis(config: RedisConfig) -> Redis:
    return Redis(host=config.url, port=config.port, db=config.db)
