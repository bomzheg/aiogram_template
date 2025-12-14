from typing import Any, TypedDict

from aiogram import types
from aiogram.types import TelegramObject
from aiogram_dialog.api.entities import DialogUpdate
from dishka.integrations.aiogram import AiogramMiddlewareData

from app.core.identity import IdentityProvider
from app.dao.holder import HolderDao
from app.models import dto
from app.tgbot.services.chat import upsert_chat
from app.tgbot.services.user import upsert_user
from app.tgbot.utils.mappers import chat_tg_to_dto, user_tg_to_dto


class LoadedData(TypedDict, total=False):
    user: dto.User | None
    chat: dto.Chat | None


class TgBotIdentityProvider(IdentityProvider):
    def __init__(
        self,
        *,
        dao: HolderDao,
        event: TelegramObject,
        aiogram_data: AiogramMiddlewareData,
    ) -> None:
        self.dao = dao
        self.event = event
        self.aiogram_data = aiogram_data
        self.cache = LoadedData()

    async def get_user(self) -> dto.User | None:
        if "user" in self.cache:
            return self.cache["user"]
        if isinstance(self.event, DialogUpdate):
            user_tg: types.User | None
            if user_tg := self.aiogram_data.get("event_from_user", None):
                user = await self.dao.user.get_by_tg_id(user_tg.id)
            else:
                user = None
        else:
            user = await save_user(self.aiogram_data, self.dao)
        self.cache["user"] = user
        return user

    async def get_chat(self) -> dto.Chat | None:
        if "chat" in self.cache:
            return self.cache["chat"]
        if isinstance(self.event, DialogUpdate):
            chat_tg: types.Chat | None
            if chat_tg := self.aiogram_data.get("event_chat", None):
                chat = await self.dao.chat.get_by_tg_id(chat_tg.id)
            else:
                chat = None
        else:
            chat = await save_chat(self.aiogram_data, self.dao)
        self.cache["chat"] = chat
        return chat


async def save_user(data: dict[str, Any], holder_dao: HolderDao) -> dto.User | None:
    user = data.get("event_from_user")
    if not user:
        return None
    return await upsert_user(user_tg_to_dto(user), holder_dao.user)


async def save_chat(data: dict[str, Any], holder_dao: HolderDao) -> dto.Chat | None:
    chat = data.get("event_chat")
    if not chat:
        return None
    return await upsert_chat(chat_tg_to_dto(chat), holder_dao.chat)
