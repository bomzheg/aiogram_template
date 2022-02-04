from aiogram import Dispatcher
from aiogram.types import Message


async def exception(message: Message):
    raise RuntimeError(message.text)


def setup_superuser(dp: Dispatcher):
    dp.message.register(exception, commands="exception")
