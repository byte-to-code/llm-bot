from aiogram import Bot, Dispatcher

from src.bot.config import Config
from src.bot.presentation.bot.handlers.processing import (
    ROUTER as PROCESSING_ROUTER,
)
from src.bot.presentation.bot.handlers.start import ROUTER as START_ROUTER
from src.bot.presentation.bot.handlers.switch_model.process_model_keyboard import (  # noqa: E501
    ROUTER as MODEL_KEYBOARD_ROUTER,
)
from src.bot.presentation.bot.handlers.switch_model.switch_model import (
    ROUTER as SWITCH_MODEL,
)


def create_app(config: Config) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    dp.include_router(START_ROUTER)
    dp.include_router(SWITCH_MODEL)
    dp.include_router(MODEL_KEYBOARD_ROUTER)
    dp.include_router(PROCESSING_ROUTER)

    return bot, dp
