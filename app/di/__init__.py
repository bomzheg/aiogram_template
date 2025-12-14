from dishka import Provider

from app.di.bot import BotProvider
from app.di.config import ConfigProvider, DbConfigProvider
from app.di.db import DAOProvider, DbProvider, RedisProvider
from app.models.config.main import Paths


def get_providers() -> list[Provider]:
    return [
        ConfigProvider(),
        DbConfigProvider(),
        DbProvider(),
        DAOProvider(),
        RedisProvider(),
        BotProvider(),
    ]
