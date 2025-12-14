from dishka import Provider, Scope, from_context, provide

from app.models.config import Config
from app.models.config.db import DBConfig, RedisConfig
from app.models.config.main import BotConfig, Paths
from app.models.config.storage import StorageConfig


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(Config)

    @provide
    def get_paths(self, config: Config) -> Paths:
        return config.paths

    @provide
    def get_tgbot_config(self, config: Config) -> BotConfig:
        return config.bot

    @provide
    def get_bot_storage_config(self, config: BotConfig) -> StorageConfig:
        return config.storage


class DbConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def get_db_config(self, config: Config) -> DBConfig:
        return config.db
