from dataclasses import dataclass
from agno.agent import Agent
from src.bot.core.errors import ModelNotFoundError
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)


@dataclass
class ProcessMessageInteractor:
    users_repository: AddUserRepository

    agent: Agent
    async def process_message(self, message: str, telegram_id: int):
        user = await self.users_repository.get_user(telegram_id=telegram_id)
        if user is None:
            raise ValueError("User not found")  # TODO: Отловить и обработать
  

        model = await self.users_repository.get_user_model(
            user_id=user.user_id
        )
        if model is None:
            raise ModelNotFoundError  # TODO: Отловить и обработать

        
        response = await self.agent.arun(
            message,
            session_id=str(telegram_id),  
        )

        return response.content 
