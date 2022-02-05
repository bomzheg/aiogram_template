from app.models import dto


def assert_chat(expected: dto.Chat, actual: dto.Chat):
    assert expected.tg_id == actual.tg_id
    assert expected.username == actual.username
    assert expected.title == expected.title
    assert expected.type == expected.type
