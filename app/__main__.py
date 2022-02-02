import logging
from pathlib import Path

from aiogram import Dispatcher, Bot

from app.config import load_config
from app.handlers import setup_handlers

logger = logging.getLogger(__name__)


def main():
    app_dir = Path(__file__).parent.parent
    config = load_config(app_dir)

    dp = Dispatcher()
    setup_handlers(dp)

    bot = Bot(config.bot.token, parse_mode="HTML")

    logger.info("started")
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
