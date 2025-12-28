import logging

from aiogram import Dispatcher

from app.models.config.main import BotConfig

from . import base, errors, superuser

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig) -> None:
    errors.setup(dp, bot_config.log_chat)
    dp.include_router(base.setup())
    dp.include_router(superuser.setup(bot_config))
    logger.debug("handlers configured successfully")
