from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class UsersResponse:
    users: list


@dataclass
class UsersUsecase:
    session: AsyncSession

    async def __call__(self) -> None:
        users = await self.get_users.get()
        return UsersResponse(users=users)
