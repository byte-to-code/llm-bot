from aiogram import Bot, Dispatcher

from src.bot.config import Config
from src.bot.presentation.bot.handlers.processing import (
    ROUTER as PROCESSING_ROUTER,
)
from src.bot.presentation.bot.handlers.start import ROUTER as START_ROUTER


def create_app(config: Config) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    dp.include_routers(START_ROUTER)
    dp.include_routers(PROCESSING_ROUTER)
    return bot, dp
