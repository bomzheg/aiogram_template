import typing
from datetime import datetime, timezone
from unittest.mock import MagicMock

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.types import Message, Update

from app.dao.holder import HolderDao
from tests.fixtures.chat_constants import create_tg_chat
from tests.fixtures.user_constants import create_tg_user


async def test_start(dp: Dispatcher, bot: Bot, dao: HolderDao, bot_session: BaseSession) -> None:
    user = create_tg_user()
    chat = create_tg_chat()
    session = typing.cast(MagicMock, bot_session)
    session.side_effect = [
        {},
    ]
    update = Update(
        update_id=1,
        message=Message(
            message_id=2,
            from_user=user,
            chat=chat,
            text="/start",
            date=datetime.now(tz=timezone.utc),
        ),
    )
    await dp.feed_update(bot, update)
    assert await dao.user.count() == 1
    assert await dao.chat.count() == 1
    session.assert_called_once()
    call = session.mock_calls.pop()
    request = call.args[1]
    assert request.__api_method__ == "sendMessage"
    assert request.text == "Hi!"


async def test_chat_id(dp: Dispatcher, bot: Bot, dao: HolderDao, bot_session: BaseSession) -> None:
    user = create_tg_user()
    chat = create_tg_chat()
    session = typing.cast(MagicMock, bot_session)
    session.side_effect = [
        {},
    ]
    update = Update(
        update_id=1,
        message=Message(
            message_id=2,
            from_user=user,
            chat=chat,
            text="/id",
            date=datetime.now(tz=timezone.utc),
        ),
    )
    await dp.feed_update(bot, update)
    assert await dao.user.count() == 1
    assert await dao.chat.count() == 1
    session.assert_called_once()
    call = session.mock_calls.pop()
    request = call.args[1]
    assert request.__api_method__ == "sendMessage"
    assert str(user.id) in request.text
    assert str(chat.id) in request.text
