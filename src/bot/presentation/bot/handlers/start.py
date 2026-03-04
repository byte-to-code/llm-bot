from aiogram import Router, types
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka

from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.presentation.bot.keyboards.models_list import models_list

ROUTER = Router()


@ROUTER.message(CommandStart())
async def start(
    message: types.Message,
    config: FromDishka[Config],
    users_repository: FromDishka[AddUserRepository],
):
    if message.from_user is None:
        return
    check_user = await users_repository.get_or_create(
        telegram_id=message.from_user.id
    )

    if check_user.selected_model is not None:
        await message.reply("Привет! Вы уже зарегистрированный пользователь")
        return

    await message.reply(
        "Добро пожаловать! Я с Вами не знаком, но сейчас это исправим!"
    )
    await users_repository.add_user(
        role="user",
        selected_model=config.openrouter.model,
        user_id=message.from_user.id,
    )

    await message.answer(
        "Выберите доступную модель:", reply_markup=models_list()
    )
