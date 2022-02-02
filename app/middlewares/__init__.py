from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from app.middlewares.db_middleware import DBMiddleware


def setup_middlewares(dp: Dispatcher, pool: sessionmaker):
    dp.message.middleware(DBMiddleware(pool))
