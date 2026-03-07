from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, select

from src.bot.infra.database.models.message_history import MessageHistory
from src.bot.infra.database.repositories.base import PostgresRepository


class MessageRepository(PostgresRepository):
    async def add_message(
        self,
        user_id: UUID,
        message_text_user: str,
        message_answer_system: str,
        selected_model: str,
    ) -> None:
        message = MessageHistory(
            user_id=user_id,
            message_text_user=message_text_user,
            message_answer_system=message_answer_system,
            selected_model=selected_model,
        )
        self.session.add(message)

    async def clean_context(self, user_id: UUID) -> None:
        await self.session.execute(
            delete(MessageHistory).where(MessageHistory.user_id == user_id)
        )

    async def get_history(
        self, user_id: UUID, limit: int
    ) -> Sequence[MessageHistory]:
        statement = (
            select(MessageHistory)
            .where(MessageHistory.user_id == user_id)
            .order_by(MessageHistory.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
