from aiogram.types import User

from app.mapper.user_mapper import from_aiogram_to_dto
from app.models import dto

ID = 666
FIRST_NAME = "Harry"
LAST_NAME = "Potter"
USERNAME = "voldemort_killer"


def test_from_aiogram_to_dto():
    source = User(
        id=ID,
        username=USERNAME,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        is_bot=False,
    )
    expected = dto.User(
        id=ID,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        username=USERNAME,
    )
    actual = from_aiogram_to_dto(source)
    assert expected == actual
