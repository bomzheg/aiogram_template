from aiogram import Dispatcher

from .data_load_middleware import LoadDataMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(LoadDataMiddleware())
