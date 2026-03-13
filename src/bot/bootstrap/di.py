from collections.abc import AsyncIterable

import structlog
from dishka import Provider, Scope, from_context, provide, provide_all
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from src.bot.config import Config

from src.bot.infra.database.repositories.user_settings import (
    UserSettingsRepository,
)
from src.bot.infra.database.repositories.users_repository import (
    AddUserRepository,
)
from src.bot.interactors.process_message import ProcessMessageInteractor

from agno.agent import Agent
from src.bot.infra.agno.agent import create_agno_assist


logger = structlog.get_logger()

TELEGRAM_DATA_CONTAINER_KEY = "dishka_container"


class MainProvider(Provider):
    get_config = from_context(Config, scope=Scope.APP)


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        engine: AsyncEngine | None = None
        try:
            if engine is None:
                engine = create_async_engine(
                    config.database.url,
                    poolclass=NullPool
                    if config.database.bouncer
                    else AsyncAdaptedQueuePool,
                    pool_pre_ping=True,
                )

            yield engine
        except ConnectionRefusedError as e:
            logger.error("Error connecting to database", error=e)  # noqa: TRY400
        finally:
            if engine is not None:
                await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_async_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine, expire_on_commit=False, autoflush=True
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, engine: AsyncEngine
    ) -> AsyncIterable[AsyncSession]:
        async with async_sessionmaker(
            engine, expire_on_commit=False
        )() as session:
            yield session

    repositories = provide_all(
        UserSettingsRepository,
        AddUserRepository,
        scope=Scope.REQUEST,
    )


class AgnoProvider(Provider):
    @provide(scope=Scope.APP)
    def get_agno_agent(self, config: Config) -> Agent:
        return create_agno_assist(config)
    

    @provide(scope=Scope.REQUEST)
    async def process_message_interactor(
        self,
        users_repository: AddUserRepository,
        agent: Agent, 
    ) -> ProcessMessageInteractor:
        return ProcessMessageInteractor(
            users_repository=users_repository,
            agent=agent, 
        )