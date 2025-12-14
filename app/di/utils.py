from typing import Any

from dishka import AsyncContainer

from app.dao.holder import HolderDao


async def warm_up(dishka: AsyncContainer) -> None:
    async with dishka() as request_dishka:
        deps: list[Any] = [
            HolderDao,
        ]
        for dep in deps:
            await request_dishka.get(dep)
