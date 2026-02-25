from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.bot.infra.database.models.base import Base


class MessageHistory(Base):
    __tablename__ = "message_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    message_text_user: Mapped[str] = mapped_column(String(4096))
    message_answer_system: Mapped[str] = mapped_column(String(4096))
    selected_model: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
