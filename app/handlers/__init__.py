import logging

from aiogram import Dispatcher

from app.handlers.echo import setup_echo
from app.handlers.errors import setup_errors
from app.models.config.main import BotConfig

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    setup_errors(dp, bot_config.log_chat)
    setup_echo(dp)
    logger.debug("handlers configured successfully")
