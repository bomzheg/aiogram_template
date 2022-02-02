from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import UserDao, ChatDao


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDao
    chat: ChatDao

    async def commit(self):
        await self.session.commit()

    @classmethod
    def create(cls, session: AsyncSession):
        return HolderDao(
            session=session,
            user=UserDao(session),
            chat=ChatDao(session),
        )
