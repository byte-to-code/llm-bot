from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.presentation.bot.keyboards.models_list import models_list

ROUTER = Router()


@ROUTER.message(CommandStart())
async def start(message: types.Message, **kwargs):
    created = kwargs.get("created", False)
    if not created:
        await message.reply("Привет! Вы уже зарегистрированный пользователь")
        return

    await message.reply(
        "Добро пожаловать! Я с Вами не знаком, но сейчас это исправим!"
    )
    await message.answer(
        "Выберите доступную модель:", reply_markup=models_list()
    )
