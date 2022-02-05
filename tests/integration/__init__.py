import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import create_pool
from tests.common import create_app_config


@pytest.fixture()
async def session() -> AsyncSession:
    config = create_app_config()
    pool = create_pool(config.db)
    async with pool() as session:
        yield session
