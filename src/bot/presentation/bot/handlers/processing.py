import structlog
from aiogram import Router, types

from src.bot.infra.llm.setup import OpenRouterService

ROUTER = Router()

logger = structlog.get_logger()


@ROUTER.message()
async def processing(message: types.Message, service: OpenRouterService):
    if message.text and message.text.startswith("/"):
        return
    if message.text is None:
        await message.answer(
            "Не удалось получить сообщение", parse_mode="HTML"
        )
        logger.error("Error", error="Failed to receive message")
        return

    answer = await message.answer("Начинаю обработку...")
    response = await service.llm_answer(message.text)
    await answer.edit_text(response)
