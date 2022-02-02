import logging

from aiogram import Dispatcher

from app.handlers.echo import setup_echo

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    setup_echo(dp)
    logger.debug("handlers configured successfully")
