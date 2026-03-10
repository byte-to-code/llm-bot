import structlog
from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka import AsyncContainer

from src.bot.bootstrap.di import TELEGRAM_DATA_CONTAINER_KEY
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)

logger = structlog.get_logger()


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
            raise ValueError("Container not found")
        async with container() as c:
            users_repository = await c.get(AddUserRepository)
            user, created = await users_repository.get_or_create(
                telegram_id=event.from_user.id
            )

            if created:
                logger.info(
                    "New user:",
                    telegram_id=event.from_user.id,
                    user_id=str(user.user_id),
                )
            if user.role == "blocked":
                logger.info(
                    "Request from a blocked user",
                    telegram_id=event.from_user.id,
                    user_id=str(user.user_id),
                )
                return None

            data["user"] = user
            data["created"] = created
        return await handler(event, data)
