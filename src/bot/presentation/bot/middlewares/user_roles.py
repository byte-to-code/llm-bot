from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)


class UserAccessMiddleware(BaseMiddleware):
    @inject
    async def __call__(
        self,
        handler,
        event: Message,
        data: dict,
        config: FromDishka[Config],
        session: FromDishka[AsyncSession],
    ):
        users = AddUserRepository(
            config=config, session=session, user_id=event.from_user.id
        )
        user = await users.get_user()
        if not user:
            await users.add_user(
                role="user", selected_model=config.openrouter.model
            )
            role = "user"
        else:
            role = user.role
        if role == "blocked":
            return None
        return await handler(event, data)
