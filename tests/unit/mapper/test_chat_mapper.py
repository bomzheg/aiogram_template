from aiogram.types import Chat

from app.enums.chat_type import ChatType
from app.mapper.chat_mapper import from_aiogram_to_dto
from app.models import dto

CHAT_ID = 42
TITLE = "My awesome chat"
TYPE = ChatType.group
USERNAME = "ultra_chat"


def test_mapper_from_aiogram_to_dto():
    source = Chat(
        id=CHAT_ID,
        title=TITLE,
        type=TYPE.name,
        username=USERNAME,
    )
    expected = dto.Chat(
        id=CHAT_ID,
        type=TYPE,
        username=USERNAME,
        title=TITLE,
    )
    actual = from_aiogram_to_dto(source)
    assert expected == actual
