from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models import dto
from app.models.db import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_tg_id(self, tg_id: int) -> dto.User:
        tg_user = await self._get_by_tg_id(tg_id)
        return tg_user.to_dto()

    async def _get_by_tg_id(self, tg_id: int) -> User:
        result = await self.session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one()

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = {
            "tg_id": user.tg_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_bot": user.is_bot,
        }
        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.tg_id,), set_=kwargs, where=User.tg_id == user.tg_id
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()
