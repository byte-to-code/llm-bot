import structlog
from aiogram import Router, types
from aiogram.filters import Command
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.presentation.bot.keyboards.models_list import models_list

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.message(Command("switch_model"))
@inject
async def show_models(
    message: types.Message,
    config: FromDishka[Config],
    session: FromDishka[AsyncSession],
):
    users = AddUserRepository(
        config=config, session=session, user_id=message.from_user.id
    )
    check_user = await users.get_user()

    if not check_user:  # todo добавить миддлварь!! а то че за прикол
        await users.add_user(
            role="user", selected_model=config.openrouter.model
        )

    kb = models_list()
    await message.answer("Выберите доступную модель:", reply_markup=kb)
