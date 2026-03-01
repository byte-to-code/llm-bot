from __future__ import annotations

from sqlalchemy import select, update

from src.bot.config import Config
from src.bot.infra.database.models.users import Users


class AddUserRepository:
    def __init__(self, config: Config, session, user_id) -> None:
        self.user_id = user_id
        self.session = session
        self.config = config

    async def add_user(
        self,
        role: str,
        selected_model: str,
    ) -> None:
        user = Users(
            user_id=self.user_id,
            role=role,
            selected_model=selected_model,
        )
        self.session.add(user)
        await self.session.commit()

    async def get_user(self) -> Users | None:
        statement = select(Users).where(Users.user_id == self.user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_model(self) -> str | None:
        user = await self.get_user()
        if user:
            return user.selected_model
        return None

    async def switch_model(self, selected_model: str) -> None:
        statement = (
            update(Users)
            .where(Users.user_id == self.user_id)
            .values(selected_model=selected_model)
        )
        await self.session.execute(statement)
        await self.session.commit()
