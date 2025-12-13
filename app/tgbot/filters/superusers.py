from aiogram.types import Message


async def is_superuser(message: Message, superusers: list[int]) -> bool:
    assert message.from_user  # noqa: S101
    return message.from_user.id in superusers
