import aiogram
from app.models import dto


def from_aiogram_to_dto(user: aiogram.types.User) -> dto.User:
    return dto.User(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
