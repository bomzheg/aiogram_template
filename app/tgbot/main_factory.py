import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject
from dishka import (
    STRICT_VALIDATION,
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.aiogram import AiogramMiddlewareData, setup_dishka

from app.core.identity import IdentityProvider
from app.di import get_providers
from app.di.db import create_redis
from app.models.config import Config
from app.models.config.main import BotConfig
from app.models.config.storage import StorageConfig, StorageType
from app.tgbot.handlers import setup_handlers
from app.tgbot.middlewares import setup_middlewares
from app.tgbot.services.identity import TgBotIdentityProvider
from app.tgbot.utils.router import print_router_tree

logger = logging.getLogger(__name__)


def create_dishka(config: Config) -> AsyncContainer:
    return make_async_container(
        *get_bot_providers(),
        context={Config: config},
        validation_settings=STRICT_VALIDATION,
    )


def get_bot_providers() -> list[Provider]:
    return [
        *get_providers(),
        *get_bot_specific_providers(),
        *get_bot_only_providers(),
    ]


def get_bot_specific_providers() -> list[Provider]:
    return [
        DpProvider(),
        BotIdpProvider(),
    ]


def get_bot_only_providers() -> list[Provider]:
    return [
        BotOnlyIdpProvider(),
    ]


class DpProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
        self,
        dishka: AsyncContainer,
        event_isolation: BaseEventIsolation,
        bot_config: BotConfig,
        storage: BaseStorage,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=storage,
            events_isolation=event_isolation,
        )
        setup_dishka(container=dishka, router=dp)
        setup_handlers(dp, bot_config)
        setup_middlewares(
            dp=dp,
        )
        logger.info("Configured bot routers \n%s", print_router_tree(dp))
        return dp

    @provide
    def create_storage(self, config: StorageConfig) -> BaseStorage:
        logger.info("creating storage for type %s", config.type_)
        match config.type_:
            case StorageType.memory:
                return MemoryStorage()
            case StorageType.redis:
                return RedisStorage(
                    create_redis(config.get_redis()),
                    key_builder=DefaultKeyBuilder(with_destiny=True),
                )
            case _:
                raise NotImplementedError

    @provide
    def get_event_isolation(self) -> BaseEventIsolation:
        return SimpleEventIsolation()


class BotIdpProvider(Provider):
    scope = Scope.REQUEST
    event = from_context(TelegramObject)
    aiogram_data = from_context(AiogramMiddlewareData)
    bot_idp = provide(TgBotIdentityProvider)


class BotOnlyIdpProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_idp(self, idp: TgBotIdentityProvider) -> IdentityProvider:
        return idp
