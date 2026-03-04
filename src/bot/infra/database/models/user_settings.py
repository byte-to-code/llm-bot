from datetime import datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from src.bot.infra.database.models.base import Base


class UserSettingsModel(Base):
    __tablename__ = "user_settings"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )

    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[Any] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
