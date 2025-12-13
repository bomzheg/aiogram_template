from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db.base import Base

Model = TypeVar("Model", bound=Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_all(self) -> Sequence[Model]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id_: int) -> Model:
        result = await self.session.execute(select(self.model).where(self.model.id == id_))
        return result.scalar_one()

    def save(self, obj: Model) -> None:
        self.session.add(obj)

    async def delete_all(self) -> None:
        await self.session.execute(delete(self.model))

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self, *objects: Sequence[Model]) -> None:
        await self.session.flush(objects)
