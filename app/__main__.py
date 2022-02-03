import logging
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import ContentTypesFilter

from app.config import load_config
from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from app.models.db import create_pool

logger = logging.getLogger(__name__)


def main():
    app_dir = Path(__file__).parent.parent
    config = load_config(app_dir)

    dp = Dispatcher()
    dp.message.bind_filter(ContentTypesFilter)
    setup_middlewares(dp, create_pool(config.db))
    setup_handlers(dp, config.bot)

    bot = Bot(config.bot.token, parse_mode="HTML")

    logger.info("started")
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
