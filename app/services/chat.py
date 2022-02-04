from sqlalchemy.exc import NoResultFound

from app.dao import ChatDao
from app.models import dto, db


async def upsert_chat(chat: dto.Chat, dao: ChatDao) -> db.Chat:
    try:
        saved_chat = await dao.get_by_tg_id(chat.id)
    except NoResultFound:
        saved_chat = db.Chat(tg_id=chat.id)
    update_fields(chat, saved_chat)
    dao.save(saved_chat)
    await dao.commit()
    return saved_chat


async def update_chat_id(chat: db.Chat, new_tg_id: int, chat_dao: ChatDao):
    chat.tg_id = new_tg_id
    chat_dao.save(chat)
    await chat_dao.commit()


def update_fields(source: dto.Chat, target: db.Chat):
    target.title = source.name
    target.username = source.username
