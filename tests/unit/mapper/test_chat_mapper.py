from aiogram import types as tg

from app.enums.chat_type import ChatType
from app.models import dto

CHAT_ID = 42
TITLE = "My awesome chat"
TYPE = ChatType.group
USERNAME = "ultra_chat"


def test_mapper_from_aiogram_to_dto():
    source = tg.Chat(
        id=CHAT_ID,
        title=TITLE,
        type=TYPE.name,
        username=USERNAME,
    )
    expected = dto.Chat(
        tg_id=CHAT_ID,
        type=TYPE,
        username=USERNAME,
        title=TITLE,
    )
    actual = dto.Chat.from_aiogram(source)
    assert expected == actual
