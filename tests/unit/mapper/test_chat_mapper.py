from app.models import dto
from tests.fixtures.chat_constants import create_dto_chat, create_tg_chat


def test_mapper_from_aiogram_to_dto() -> None:
    source = create_tg_chat()
    expected = create_dto_chat()
    actual = dto.Chat.from_aiogram(source)
    assert expected == actual
