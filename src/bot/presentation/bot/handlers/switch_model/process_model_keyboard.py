import structlog
from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
)
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)

ROUTER = Router()
logger = structlog.get_logger()


@ROUTER.callback_query(
    F.data.startswith("qwen/qwen3-max")
    | F.data.startswith("openai/gpt-4.1")
    | F.data.startswith("mistralai/ministral-8b-2512")
)
@inject
async def process_model_selection(
    callback: CallbackQuery,
    session: FromDishka[AsyncSession],
    config: FromDishka[Config],
):
    user_id = callback.from_user.id
    selected_model = callback.data

    users_repo = AddUserRepository(
        config=config, session=session, user_id=user_id
    )

    check_user = await users_repo.get_user()
    if check_user:
        await users_repo.switch_model(selected_model)
    else:
        await users_repo.add_user(role="user", selected_model=selected_model)

    await callback.message.edit_text(f"Выбрана модель: {selected_model}")
    await callback.answer()
