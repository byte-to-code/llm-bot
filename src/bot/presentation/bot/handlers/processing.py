import structlog
from aiogram import Router, types
from dishka.integrations.aiogram import AsyncSession, FromDishka, inject

from src.bot.config import Config
from src.bot.infra.database.repositories.message_history_repository import (
    MessageRepository,
)
from src.bot.infra.llm.setup import OpenRouterService

ROUTER = Router()

logger = structlog.get_logger()


# todo https://openrouter.ai/docs/api/api-reference/models/get-models


@ROUTER.message()
@inject
async def processing(
    message: types.Message,
    service: FromDishka[OpenRouterService],
    session: FromDishka[AsyncSession],
):
    if message.text and message.text.startswith("/"):
        return
    if message.text is None:
        await message.answer(
            "Не удалось получить сообщение", parse_mode="HTML"
        )
        logger.error("Error", error="Failed to receive message")
        return
    message_repository = MessageRepository(
        config=Config(), session=session, user_id=message.from_user.id
    )
    await message_repository.add_message(message.text)
    answer = await message.answer("Начинаю обработку...")
    response = await service.llm_answer(message.text)
    await answer.edit_text(response)
