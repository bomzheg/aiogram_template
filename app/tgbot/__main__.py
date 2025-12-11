import logging
import os
from pathlib import Path
from typing import NoReturn

from aiogram import Bot, Dispatcher
from sqlalchemy.orm import close_all_sessions

from app.config import load_config
from app.config.logging_config import setup_logging
from app.models.config.main import Paths
from app.tgbot.handlers import setup_handlers
from app.tgbot.middlewares import setup_middlewares

logger = logging.getLogger(__name__)


def main() -> NoReturn:
    paths = get_paths()

    setup_logging(paths)
    config = load_config(paths)

    dp = Dispatcher()
    setup_middlewares(dp)
    setup_handlers(dp, config.bot)
    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML",
        session=config.bot.create_session(),
    )

    logger.info("started")
    try:
        dp.run_polling(bot)
    finally:
        close_all_sessions()
        logger.info("stopped")


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parents[2])


if __name__ == "__main__":
    main()
