from sqlalchemy import delete, select

from src.bot.config import Config
from src.bot.infra.database.models.base import MessageHistory


class MessageRepository:
    def __init__(self, config: Config, session, user_id) -> None:
        self.user_id = user_id
        self.session = session
        self.config = config

    async def add_message(
        self, message_text: str, selected_model: str
    ) -> None:
        await self._clean_old_messages()
        message = MessageHistory(
            user_id=self.user_id,
            message_text=message_text,
            selected_model=selected_model,
        )
        await self.session.add(message)
        await self.session.commit()

    async def _clean_old_messages(self) -> None:
        max_history = self.config.telegram.max_history
        messages = await self.get_history()

        if len(messages) >= max_history:
            delete_size = len(messages) - max_history + 1
            old_messages = messages[-delete_size:]
            for msg in old_messages:
                await self.session.delete(msg)

    async def clean_context(self) -> None:
        await self.session.execute(
            delete(MessageHistory).where(user_id=self.user_id)
        )
        await self.session.commit()

    async def get_history(self) -> list[MessageHistory]:
        statement = (
            select(MessageHistory)
            .where(MessageHistory.user_id == self.user_id)
            .order_by(MessageHistory.created_at.desc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
