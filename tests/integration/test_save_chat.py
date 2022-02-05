import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.holder import HolderDao
from app.middlewares.db_middleware import save_chat
from app.models import dto
from tests.fixtures.chat_constants import create_tg_chat, create_db_chat
from tests.utils.chat import assert_chat


@pytest.mark.asyncio
async def test_save_chat(session: AsyncSession):
    dao = HolderDao(session)
    await dao.chat.delete_all()

    data = dict(event_chat=create_tg_chat())
    actual = await save_chat(data, dao)
    expected = dto.Chat.from_db(create_db_chat())
    assert_chat(expected, actual)
    assert actual.db_id is not None
    assert await dao.chat.count() == 1
