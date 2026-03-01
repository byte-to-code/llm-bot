from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.bot.infra.database.models.base import Base


# todo https://docs.sqlalchemy.org/en/20/core/type_basics.html
# todo https://habr.com/ru/articles/751140/?ysclid=mm24tx69ni488756698
# todo разобраться с enum
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role: Mapped[str] = mapped_column(default="user")
    selected_model: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    messages = relationship("MessageHistory", back_populates="user")
