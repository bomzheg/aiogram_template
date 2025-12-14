import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher

from app.config import load_config
from app.config.logging_config import setup_logging
from app.di.utils import warm_up
from app.models.config.main import Paths
from app.tgbot.main_factory import create_dishka

logger = logging.getLogger(__name__)


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(app_dir=Path(path))
    return Paths(app_dir=Path(__file__).parents[2])


async def main() -> None:
    paths = get_paths()
    setup_logging(paths)
    config = load_config(paths)
    dishka = create_dishka(config=config)
    dp = await dishka.get(Dispatcher)
    bot = await dishka.get(Bot)

    try:
        await bot.delete_webhook()
        await warm_up(dishka)
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types(skip_events={"aiogd_update"})
        )
    finally:
        logger.info("stopped")
        await dishka.close()


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
