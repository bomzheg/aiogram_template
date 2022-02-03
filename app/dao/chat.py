from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models.db import Chat


class ChatDao(BaseDAO[Chat]):
    def __init__(self, session: AsyncSession):
        super().__init__(Chat, session)

    async def get_by_tg_id(self, tg_id: int) -> Chat:
        result = await self.session.execute(
            select(Chat).where(Chat.tg_id == tg_id)
        )
        return result.scalar_one()
