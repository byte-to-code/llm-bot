import structlog
from aiogram import Router, types
from aiogram.filters import Command
from dishka.integrations.aiogram import inject

from src.bot.presentation.bot.keyboards.models_list import models_list

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.message(Command("switch_model"))
@inject
async def show_models(
    message: types.Message,
):
    await message.answer(
        "Выберите доступную модель:", reply_markup=models_list()
    )
