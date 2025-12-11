from functools import partial
from typing import NoReturn

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.models.config.main import BotConfig
from app.tgbot.filters.superusers import is_superuser


async def exception(message: Message) -> NoReturn:
    raise RuntimeError(message.text)


async def leave_chat(message: Message, bot: Bot) -> None:
    await bot.leave_chat(message.chat.id)


def setup_superuser(dp: Dispatcher, bot_config: BotConfig) -> None:
    is_superuser_ = partial(is_superuser, superusers=bot_config.superusers)
    router = Router(name=__name__)
    router.message.filter(is_superuser_)
    router.message.register(exception, Command(commands="exception"))
    router.message.register(leave_chat, Command(commands="get_out"))

    dp.include_router(router)
