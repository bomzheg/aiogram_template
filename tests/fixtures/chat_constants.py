from aiogram import types as tg

from app.enums.chat_type import ChatType
from app.models import db, dto

CHAT_ID = 42
NEW_CHAT_ID = -10048
TITLE = "My awesome chat"
TYPE = ChatType.group
USERNAME = "ultra_chat"


def create_dto_chat() -> dto.Chat:
    return dto.Chat(
        tg_id=CHAT_ID,
        type=TYPE,
        username=USERNAME,
        title=TITLE,
    )


def create_tg_chat(
    id_: int = CHAT_ID,
    title: str = TITLE,
    type_: ChatType = TYPE,
    username: str = USERNAME,
) -> tg.Chat:
    return tg.Chat(
        id=id_,
        title=title,
        type=type_.name,
        username=username,
    )


def create_db_chat() -> db.Chat:
    return db.Chat(
        tg_id=CHAT_ID,
        type=TYPE,
        username=USERNAME,
        title=TITLE,
    )
