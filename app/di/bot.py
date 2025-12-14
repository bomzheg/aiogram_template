from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession
from aiogram.client.telegram import PRODUCTION, TelegramAPIServer
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from app.models.config.main import BotApiType, BotConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, config: BotConfig, session: BaseSession) -> AsyncIterable[Bot]:
        async with Bot(
            token=config.token,
            session=session,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                allow_sending_without_reply=True,
            ),
        ) as bot:
            yield bot

    @provide
    def create_session(self, server: TelegramAPIServer) -> BaseSession:
        return AiohttpSession(api=server)

    @provide
    def create_server(self, config: BotConfig) -> TelegramAPIServer:
        if config.bot_api.type != BotApiType.local:
            return PRODUCTION
        return TelegramAPIServer(
            base=f"{config.bot_api.botapi_url}/bot{{token}}/{{method}}",
            file=f"{config.bot_api.botapi_file_url}{{path}}",
        )
