from adaptix import P
from adaptix.conversion import get_converter, link_function
from adaptix.type_tools import exec_type_checking
from aiogram import types
from aiogram.client import context_controller
from aiogram.types import chat, user

from app import enums
from app.models import dto

exec_type_checking(user)
exec_type_checking(chat)
exec_type_checking(context_controller)

user_tg_to_dto = get_converter(
    src=types.User,
    dst=dto.User,
    recipe=[
        link_function(lambda _: None, P[dto.User].db_id),
        link_function(lambda user_: user_.id, P[dto.User].tg_id),
    ],
)
chat_tg_to_dto = get_converter(
    src=types.Chat,
    dst=dto.Chat,
    recipe=[
        link_function(lambda _: None, P[dto.Chat].db_id),
        link_function(lambda chat_: chat_.id, P[dto.Chat].tg_id),
        link_function(lambda chat_: enums.ChatType[chat_.type], P[dto.Chat].type),
    ],
)
