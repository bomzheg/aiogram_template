from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker

from app.dao.holder import HolderDao
from app.mapper.user_mapper import from_aiogram_to_dto
from app.services.user import upsert_user


class DBMiddleware(BaseMiddleware):
    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.pool() as session:
            holder_dao = HolderDao.create(session)
            data["dao"] = holder_dao
            user = await upsert_user(
                from_aiogram_to_dto(data["event_from_user"]),
                holder_dao.user
            )
            data["user"] = user
            await handler(event, data)
            del data["dao"]
