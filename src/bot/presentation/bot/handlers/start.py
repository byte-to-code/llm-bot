from aiogram import Router, types
from aiogram.filters import CommandStart
from dishka import FromDishka

from bot.config import Config

ROUTER = Router()


@ROUTER.message(CommandStart())
async def start(message: types.Message, config: FromDishka[Config]):
    await message.reply(f"Hello, world! My name is {config.telegram.bot_name}")
