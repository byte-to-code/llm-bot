import structlog
from aiogram import Router, types
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.config import Config
from src.bot.infra.database.repositories.message_history_repository import (
    MessageRepository,
)
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.infra.llm.setup import OpenRouterService

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.message()
@inject
async def processing(
    message: types.Message,
    service: FromDishka[OpenRouterService],
    session: FromDishka[AsyncSession],
    config: FromDishka[Config],
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
        config=config, session=session, user_id=message.from_user.id
    )
    history_message = await message_repository.get_history()
    answer = await message.answer("Начинаю обработку...")

    users = AddUserRepository(
        config=config, session=session, user_id=message.from_user.id
    )

    model = await users.get_user_model()

    response = await service.llm_answer(history_message, message.text, model)
    await message_repository.add_message(
        message_text_user=message.text,
        message_answer_system=response,
        selected_model=model,
    )
    await answer.edit_text(response)
