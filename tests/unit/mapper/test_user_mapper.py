from app.tgbot.utils.mappers import user_tg_to_dto
from tests.fixtures.user_constants import create_dto_user, create_tg_user


def test_from_aiogram_to_dto() -> None:
    source = create_tg_user()
    expected = create_dto_user()
    actual = user_tg_to_dto(source)
    assert expected == actual
