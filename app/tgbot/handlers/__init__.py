import logging

from aiogram import Dispatcher

from app.models.config.main import BotConfig
from app.tgbot.handlers.base import setup_base
from app.tgbot.handlers.errors import setup_errors
from app.tgbot.handlers.superuser import setup_superuser

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig) -> None:
    setup_errors(dp, bot_config.log_chat)
    dp.include_router(setup_base())
    dp.include_router(setup_superuser(bot_config))
    logger.debug("handlers configured successfully")
