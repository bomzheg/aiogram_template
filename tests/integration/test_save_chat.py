import pytest

from app.dao.holder import HolderDao
from app.middlewares.db_middleware import save_chat
from app.models import dto
from app.models.db import create_pool
from tests.common import create_app_config
from tests.fixtures.chat_constants import create_tg_chat, create_db_chat
from tests.utils.chat import assert_chat


@pytest.mark.asyncio
async def test_save_chat():
    data = dict(event_chat=create_tg_chat())
    config = create_app_config()
    pool = create_pool(config.db)
    async with pool() as session:
        actual = await save_chat(data, HolderDao(session))
    expected = dto.Chat.from_db(create_db_chat())
    assert_chat(expected, actual)
    assert actual.db_id is not None
