import structlog
from aiogram import Bot, Dispatcher, types

from bot.core.errors import BotError
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

logger = structlog.get_logger()


def create_app(config: Config) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    @dp.error(BotError)
    async def error_handler(
        event: BotError, message: types.Message
    ):  # TODO: ВЫНЕСТИ КУДА НИБУДЬ
        logger.error("Critical error caused", message=event.message)
        # do something with error
        await message.answer(event.message)

    dp.include_router(START_ROUTER)
    dp.include_router(SWITCH_MODEL)
    dp.include_router(MODEL_KEYBOARD_ROUTER)
    dp.include_router(PROCESSING_ROUTER)

    return bot, dp
