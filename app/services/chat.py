from app.dao import ChatDAO
from app.models import dto


async def upsert_chat(chat: dto.Chat, dao: ChatDAO) -> dto.Chat:
    saved_chat = await dao.upsert_chat(chat)
    await dao.commit()
    return saved_chat


async def update_chat_id(chat: dto.Chat, new_tg_id: int, dao: ChatDAO):
    await dao.update_chat_id(chat, new_tg_id)
    await dao.commit()
