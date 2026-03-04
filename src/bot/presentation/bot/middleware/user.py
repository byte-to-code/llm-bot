from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka import AsyncContainer
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from bot.bootstrap.di import TELEGRAM_DATA_CONTAINER_KEY
from src.bot.config import Config
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler,
        event: Message,
        data: dict,
    ):
        if event.from_user is None:
            return await handler(event, data)

        container: AsyncContainer | None = data.get(
            TELEGRAM_DATA_CONTAINER_KEY
        )
        if container is None:
            raise ValueError("Container not found")  # TODO: Обработать

        users_repository: AddUserRepository = container.get(AddUserRepository)
        config = container.get(Config)
        user = await users_repository.get_user()
        if not user:
            await users_repository.add_user(
                role="user",
                selected_model=config.openrouter.model,
                user_id=event.from_user.id,
            )
            role = "user"
        else:
            role = user.role
        if role == "blocked":
            return None
        data["user"] = user
        return await handler(event, data)
