from aiogram import Router, types
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka

from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.presentation.bot.keyboards.models_list import models_list

ROUTER = Router()


@ROUTER.message(CommandStart())
async def start(
    message: types.Message,
    users_repository: FromDishka[AddUserRepository],
):
    user, created = await users_repository.get_or_create(
        telegram_id=message.from_user.id
    )

    if not created:
        await message.reply("Привет! Вы уже зарегистрированный пользователь")
        return

    await message.reply(
        "Добро пожаловать! Я с Вами не знаком, но сейчас это исправим!"
    )
    await message.answer(
        "Выберите доступную модель:", reply_markup=models_list()
    )
