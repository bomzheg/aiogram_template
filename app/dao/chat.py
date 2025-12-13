from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import db, dto


class ChatDAO(BaseDAO[db.Chat]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Chat, session)

    async def get_by_tg_id(self, tg_id: int) -> dto.Chat:
        db_chat = await self._get_by_tg_id(tg_id)
        return db_chat.to_dto()

    async def _get_by_tg_id(self, tg_id: int) -> db.Chat:
        result = await self.session.execute(select(db.Chat).where(db.Chat.tg_id == tg_id))
        return result.scalar_one()

    async def upsert_chat(self, chat: dto.Chat) -> dto.Chat:
        kwargs = {
            "tg_id": chat.tg_id,
            "title": chat.title,
            "username": chat.username,
            "type": chat.type,
        }
        saved_chat = await self.session.scalars(
            insert(db.Chat)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(db.Chat.tg_id,), set_=kwargs, where=db.Chat.tg_id == chat.tg_id
            )
            .returning(db.Chat)
        )
        return saved_chat.one().to_dto()

    async def update_chat_id(self, chat: dto.Chat, new_id: int) -> None:
        chat_db = await self._get_by_tg_id(chat.tg_id)
        chat_db.tg_id = new_id
        self.save(chat_db)
