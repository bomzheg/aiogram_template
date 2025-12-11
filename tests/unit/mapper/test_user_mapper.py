from app.models import dto
from tests.fixtures.user_constants import create_dto_user, create_tg_user


def test_from_aiogram_to_dto() -> None:
    source = create_tg_user()
    expected = create_dto_user()
    actual = dto.User.from_aiogram(source)
    assert expected == actual
