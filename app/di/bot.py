from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from app.models.config.main import BotConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(
        self,
        config: BotConfig,
        session: None
    ) -> AsyncIterable[Bot]:
        async with Bot(
            token=config.token,
            session=session,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                allow_sending_without_reply=True,
            ),
        ) as bot:
            yield bot
