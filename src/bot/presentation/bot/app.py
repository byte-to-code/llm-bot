import structlog
from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from src.bot.config import Config
from src.bot.core.errors import BotError
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

logger = structlog.get_logger()


def create_app(config: Config) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    @dp.error(BotError)
    async def error_handler(event: ErrorEvent):
        logger.error("Critical error caused %r", event.exception)
        if event.update.message:
            await event.update.message.answer(f"Ошибка: {event.exception}")

    dp.include_router(START_ROUTER)
    dp.include_router(SWITCH_MODEL)
    dp.include_router(MODEL_KEYBOARD_ROUTER)
    dp.include_router(PROCESSING_ROUTER)

    return bot, dp
