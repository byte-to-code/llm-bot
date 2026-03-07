from dataclasses import dataclass

from src.bot.core.errors import ModelNotFoundError
from src.bot.infra.database.repositories.message_history_repository import (
    MessageRepository,
)
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.infra.llm.setup import OpenRouterService


@dataclass
class ProcessMessageInteractor:
    message_repository: MessageRepository
    users_repository: AddUserRepository
    service: OpenRouterService

    async def process_message(self, message: str, telegram_id: int):
        user = await self.users_repository.get_user(telegram_id=telegram_id)
        if user is None:
            raise ValueError("User not found")  # TODO: Отловить и обработать
        history_message = await self.message_repository.get_history(
            user_id=user.user_id, limit=10
        )  # TODO: Переделать на айдишник пользователя

        model = await self.users_repository.get_user_model(
            user_id=user.user_id
        )
        if model is None:
            raise ModelNotFoundError  # TODO: Отловить и обработать

        response = await self.service.llm_answer(
            history_message, message, model
        )
        await self.message_repository.add_message(
            message_text_user=message,
            message_answer_system=response,
            selected_model=model,
            user_id=user.user_id,
        )
        return response
