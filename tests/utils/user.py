from app.models import db


def assert_user(expected: db.User, actual: db.User):
    assert expected.tg_id == actual.tg_id
    assert expected.username == actual.username
    assert expected.first_name == actual.first_name
    assert expected.last_name == actual.last_name
    return True
