import logging
import typing

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import html_decoration as hd
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.core.identity import IdentityProvider
from app.dao import ChatDAO
from app.tgbot.services.chat import update_chat_id

logger = logging.getLogger(__name__)


async def start_cmd(message: Message) -> None:
    await message.reply("Hi!")


async def chat_id(message: Message) -> None:
    text = f"chat_id: {hd.pre(str(message.chat.id))}\n"
    if message.from_user:
        text += f"your user_id: {hd.pre(str(message.from_user.id))}"
    if message.reply_to_message and message.reply_to_message.from_user:
        text += (
            f"\nid {hd.bold(message.reply_to_message.from_user.full_name)}: "
            f"{hd.pre(str(message.reply_to_message.from_user.id))}"
        )
    await message.reply(text, disable_notification=True)


async def cancel_state(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info("Cancelling state %s", current_state)
    # Cancel state and inform user about it
    await state.clear()
    # And remove keyboard (just in case)
    await message.reply("Dialog stopped, data removed", reply_markup=ReplyKeyboardRemove())


@inject
async def chat_migrate(
    message: Message, identity: IdentityProvider, dao: FromDishka[ChatDAO]
) -> None:
    new_id = typing.cast(int, message.migrate_to_chat_id)
    await update_chat_id(await identity.get_required_chat(), new_id, dao)
    logger.info("Migrate chat from %s to %s", message.chat.id, new_id)


def setup_base() -> Router:
    router = Router(name=__name__)
    router.message.register(start_cmd, Command("start"))
    router.message.register(
        chat_id,
        Command(commands=["idchat", "chat_id", "id"], prefix="/!"),
    )
    router.message.register(cancel_state, Command(commands="cancel"))
    router.message.register(
        chat_migrate,
        F.content_types == ContentType.MIGRATE_TO_CHAT_ID,
    )
    return router
