from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.tgbot.services.identity import TgBotIdentityProvider


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:  # noqa: ANN401
        dishka = data["dishka_container"]
        identity_provider = await dishka.get(TgBotIdentityProvider)

        data["user"] = await identity_provider.get_user()
        data["chat"] = await identity_provider.get_chat()
        return await handler(event, data)
