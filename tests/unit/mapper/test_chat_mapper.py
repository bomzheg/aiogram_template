from app.tgbot.utils.mappers import chat_tg_to_dto
from tests.fixtures.chat_constants import create_dto_chat, create_tg_chat


def test_mapper_from_aiogram_to_dto() -> None:
    source = create_tg_chat()
    expected = create_dto_chat()
    actual = chat_tg_to_dto(source)
    assert expected == actual
