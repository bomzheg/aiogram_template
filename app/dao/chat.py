from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import BaseDAO
from app.models.db import Chat


class ChatDao(BaseDAO[Chat]):
    def __init__(self, session: AsyncSession):
        super().__init__(Chat, session)
