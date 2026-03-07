from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.bot.infra.database.models.base import Base


class MessageHistory(Base):  # TODO: Убрать и переехать на agno
    __tablename__ = "message_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )
    message_text_user: Mapped[str] = mapped_column(String(4096))
    message_answer_system: Mapped[str] = mapped_column(String(4096))
    selected_model: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user = relationship("UserModel", back_populates="messages")
