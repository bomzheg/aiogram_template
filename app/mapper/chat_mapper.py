import aiogram.types

from app.enums.chat_type import ChatType
from app.models import dto


def from_aiogram_to_dto(chat: aiogram.types.Chat) -> dto.Chat:
    return dto.Chat(
        id=chat.id,
        title=chat.title,
        type=ChatType[chat.type],
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
    )
