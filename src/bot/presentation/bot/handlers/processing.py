import structlog
from aiogram import Router, types
from dishka.integrations.aiogram import FromDishka

from src.bot.interactors.process_message import ProcessMessageInteractor

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.message()
async def processing(
    message: types.Message,
    interactor: FromDishka[ProcessMessageInteractor],
):
    if message.from_user is None:
        logger.info("No message from user")
        return
    if message.text and message.text.startswith("/"):
        return
    if message.text is None:
        await message.answer(
            "Не удалось получить сообщение", parse_mode="HTML"
        )
        logger.error("Error", error="Failed to receive message")
        return

    answer_message = await message.answer("Начинаю обработку...")
    response = await interactor.process_message(
        message=message.text, telegram_id=message.from_user.id
    )
    await answer_message.edit_text(response)
