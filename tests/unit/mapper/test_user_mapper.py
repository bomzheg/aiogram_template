from app.mapper.user_mapper import from_aiogram_to_dto
from tests.fixtures.user_constants import create_user, create_dto_user


def test_from_aiogram_to_dto():
    source = create_user()
    expected = create_dto_user()
    actual = from_aiogram_to_dto(source)
    assert expected == actual


