from aiogram import Bot, Dispatcher

from bot.config import Config
from bot.presentation.bot.handlers.start import ROUTER as START_ROUTER


def create_app(config: Config) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    dp.include_routers(START_ROUTER)
    return bot, dp
