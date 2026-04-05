from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import (
    RowMapping,
    select,
)
from structlog import get_logger

from src.bot.infra.database.gates.base import PostgresGateway
from src.bot.infra.database.models import user

# todo создать infra/database/tables/users.py
# todo добавить обработку ошибок
logger = get_logger(__name__)


@dataclass
class UsersGateway(PostgresGateway):
    async def get_users(self) -> Sequence[RowMapping]:
        stmt = select(user)

        return (await self.session.execute(stmt)).mappings().all()
