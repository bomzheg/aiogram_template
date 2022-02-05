import pytest

from app.dao.holder import HolderDao
from app.middlewares.db_middleware import save_user
from app.models import dto
from app.models.db import create_pool
from tests.common import create_app_config
from tests.fixtures.user_constants import create_tg_user, create_db_user
from tests.utils.user import assert_user


@pytest.mark.asyncio
async def test_save_user():
    data = dict(event_from_user=create_tg_user())
    config = create_app_config()
    pool = create_pool(config.db)
    async with pool() as session:
        actual = await save_user(data, HolderDao(session))
    expected = dto.User.from_db(create_db_user())
    assert_user(expected, actual)
    assert actual.db_id is not None
