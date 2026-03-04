from typing import Any
from uuid import UUID

from bot.infra.database.models.user_settings import UserSettingsModel
from bot.infra.database.repositories.base import PostgresRepository


class UserSettingsRepository(
    PostgresRepository
):  # TODO: Доделать и использовать
    async def get_user_settings(self, user_id: UUID) -> Any:
        """
        Gets user settings.

        SELECT * FROM user_settings WHERE user_id = user_id
        """

    async def get_user_settings_by_key(
        self, user_id: UUID, key: str, default: Any
    ) -> UserSettingsModel | None:
        """Get or create user settings by key."""

    async def set_user_settings(
        self, user_id: UUID, key: str, value: Any
    ) -> None:
        """
        Upserts user settings.

        INSERT INTO user_settings (user_id, key, value)
            VALUES (user_id, key, value)
            ON CONFLICT (user_id, key)
            DO UPDATE SET value = excluded.value
        """

    async def switch_model(self, user_id: UUID, selected_model: str) -> None:
        return await self.set_user_settings(
            user_id=user_id,
            key="selected_model",
            value=selected_model,
        )
