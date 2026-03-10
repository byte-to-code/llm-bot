from uuid import UUID, uuid4

from sqlalchemy import select, update

from src.bot.config import get_config
from src.bot.infra.database.models.user import UserModel
from src.bot.infra.database.repositories.base import PostgresRepository


class AddUserRepository(PostgresRepository):
    async def add_user(
        self,
        telegram_id: int,
        role: str,
        selected_model: str,
    ) -> None:
        user = UserModel(
            user_id=uuid4(),
            telegram_id=telegram_id,
            role=role,
            selected_model=selected_model,
        )
        self.session.add(user)

    async def get_user(
        self, *, user_id: UUID | None = None, telegram_id: int | None = None
    ) -> UserModel | None:
        if user_id is None and telegram_id is None:
            raise ValueError("user_id or telegram_id must be provided")
        statement = select(UserModel)
        if user_id is not None:
            statement = statement.where(UserModel.user_id == user_id)
        if telegram_id is not None:
            statement = statement.where(UserModel.telegram_id == telegram_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_model(self, user_id: UUID) -> str | None:
        user = await self.get_user(user_id=user_id)
        if user:
            return user.selected_model
        return None

    async def switch_model(
        self, telegram_id: int, selected_model: str
    ) -> None:
        statement = (
            update(UserModel)
            .where(UserModel.telegram_id == telegram_id)
            .values(selected_model=selected_model)
        )
        await self.session.execute(statement)
        await self.session.commit()

    async def get_or_create(self, telegram_id: int) -> tuple[UserModel, bool]:
        config = get_config()
        selected_model = config.openrouter.model
        user = await self.get_user(telegram_id=telegram_id)
        if user:
            return user, False

        await self.add_user(
            telegram_id=telegram_id,
            role="user",
            selected_model=selected_model,
        )
        await self.session.commit()
        user = await self.get_user(telegram_id=telegram_id)
        return user, True
