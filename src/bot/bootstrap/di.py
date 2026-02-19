from collections.abc import AsyncIterable

import structlog
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from bot.config import Config

logger = structlog.get_logger()


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
