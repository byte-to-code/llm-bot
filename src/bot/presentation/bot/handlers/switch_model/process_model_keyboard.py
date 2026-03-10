import structlog
from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
)
from dishka.integrations.aiogram import FromDishka, inject

from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.callback_query(
    F.data.startswith("qwen/qwen3-max")
    | F.data.startswith("openai/gpt-4.1")
    | F.data.startswith("mistralai/ministral-8b-2512")
)
@inject
async def process_model_selection(
    callback: CallbackQuery,
    config: FromDishka[Config],
    users_repository: AddUserRepository,
):
    telegram_id = callback.from_user.id
    selected_model = callback.data

    try:
        await users_repository.switch_model(telegram_id, selected_model)
        await callback.message.edit_text(f"Выбрана модель: {selected_model}")
        await callback.answer()
    except Exception as e:
        await users_repository.switch_model(
            telegram_id, config.openrouter.model
        )

        await callback.message.edit_text(
            "Не удалось выбрать данную модель. Установлена модель по умолчанию."  # noqa: E501
        )
        logger.exception(
            "Error when switch the model",
            telegram_id=telegram_id,
            error=str(e),
        )
