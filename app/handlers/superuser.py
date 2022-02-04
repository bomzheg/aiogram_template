from aiogram import Dispatcher
from aiogram.types import Message

from app.filters.superusers import is_superuser


async def exception(message: Message):
    raise RuntimeError(message.text)


def setup_superuser(dp: Dispatcher):
    dp.message.register(exception, is_superuser, commands="exception")
