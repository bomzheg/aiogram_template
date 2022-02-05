import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.holder import HolderDao
from app.middlewares.db_middleware import save_user
from app.models import dto
from tests.fixtures.user_constants import create_tg_user, create_db_user
from tests.utils.user import assert_user


@pytest.mark.asyncio
async def test_save_user(session: AsyncSession):
    data = dict(event_from_user=create_tg_user())
    actual = await save_user(data, HolderDao(session))
    expected = dto.User.from_db(create_db_user())
    assert_user(expected, actual)
    assert actual.db_id is not None
