import logging

import json
from aiogram import Dispatcher, Bot
from functools import partial

from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd

logger = logging.getLogger(__name__)


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot):
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error.exception.__class__.__name__, error.update.dict(exclude_none=True), exc_info=error.exception,
    )
    if not log_chat_id:
        return
    await bot.send_message(
        log_chat_id,
        f"Received exception {hd.quote(str(error.exception))}\n"
        f"by processing update "
        f"{hd.quote(json.dumps(error.update.dict(exclude_none=True), default=str)[:3500])}\n"
    )


def setup_errors(dp: Dispatcher, log_chat_id: int):
    dp.errors.register(partial(handle, log_chat_id=log_chat_id))
