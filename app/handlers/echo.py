from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.utils.markdown import html_decoration as hd


async def chat_id(message: Message):
    text = (
        f"id этого чата: {hd.pre(message.chat.id)}\n"
        f"Ваш id: {hd.pre(message.from_user.id)}"
    )
    if message.reply_to_message:
        text += (
            f"\nid {hd.bold(message.reply_to_message.from_user.full_name)}: "
            f"{hd.pre(message.reply_to_message.from_user.id)}"
        )
    await message.reply(text, disable_notification=True)


async def exception(message: Message):
    raise RuntimeError(message.text)


def setup_echo(dp: Dispatcher):
    dp.message.register(exception, commands="exception")
    dp.message.register(chat_id, commands=["idchat", "chat_id", "id"], commands_prefix=r"\!")
