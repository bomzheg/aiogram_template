from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.middlewares.config_middleware import ConfigMiddleware
from app.middlewares.data_load_middleware import LoadDataMiddleware
from app.middlewares.db_middleware import DBMiddleware
from app.models.config.main import BotConfig


def setup_middlewares(dp: Dispatcher, pool: async_sessionmaker[AsyncSession], bot_config: BotConfig):
    dp.message.middleware(ConfigMiddleware(bot_config))
    dp.message.middleware(DBMiddleware(pool))
    dp.message.middleware(LoadDataMiddleware())
