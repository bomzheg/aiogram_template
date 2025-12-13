import pytest

from app.dao.holder import HolderDao
from app.tgbot.services.identity import save_user
from tests.fixtures.user_constants import create_dto_user, create_tg_user
from tests.utils.user import assert_user


@pytest.mark.asyncio()
async def test_save_user(dao: HolderDao) -> None:
    await dao.user.delete_all()

    data = {"event_from_user": create_tg_user()}
    actual = await save_user(data, dao)
    assert actual is not None
    expected = create_dto_user()
    assert_user(expected, actual)
    assert actual.db_id is not None
    assert await dao.user.count() == 1


@pytest.mark.asyncio()
async def test_upsert_user(dao: HolderDao) -> None:
    await dao.user.delete_all()

    old_tg_user = create_tg_user(username="tom_riddle_friend")
    data = {"event_from_user": old_tg_user}
    old = await save_user(data, dao)
    expected_old = create_dto_user()
    expected_old.username = "tom_riddle_friend"
    assert old is not None
    assert_user(expected_old, old)

    data = {"event_from_user": create_tg_user()}
    actual = await save_user(data, dao)

    assert actual is not None
    expected = create_dto_user()
    assert_user(expected, actual)
    assert old.db_id == actual.db_id
    assert await dao.user.count() == 1
