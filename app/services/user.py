from sqlalchemy.exc import NoResultFound

from app.dao import UserDao
from app.models import dto, db


async def upsert_user(user: dto.User, user_dao: UserDao) -> db.User:
    try:
        saved_user = await user_dao.get_by_tg_id(user.id)
    except NoResultFound:
        saved_user = db.User(tg_id=user.id)
    update_fields(user, saved_user)
    user_dao.save(saved_user)
    await user_dao.commit()
    return saved_user


def update_fields(source: dto.User, target: db.User):
    target.first_name = source.first_name
    target.last_name = source.last_name
    target.username = source.username
