from aiogram import Dispatcher
from aiogram.types import Message, ContentType


async def echo(message: Message):
    await message.answer(message.text)


def setup_echo(dp: Dispatcher):
    dp.message.register(echo, content_types=ContentType.TEXT)
