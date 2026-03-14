import asyncio
from contextlib import asynccontextmanager, suppress

import structlog
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import (
    AiogramProvider,
)
from dishka.integrations.aiogram import (
    setup_dishka as setup_dishka_aiogram,
)
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI

from bot.infra.agno.provider import LLMProvider
from src.bot.bootstrap.di import AgnoProvider, DatabaseProvider, MainProvider
from src.bot.config import Config, get_config
from src.bot.logging import setup_logger
from src.bot.presentation.bot.app import create_app as create_aiogram_app
from src.bot.presentation.web.app import create_app as create_fastapi_app


def setup_di_container(config: Config) -> AsyncContainer:
    return make_async_container(
        MainProvider(),
        DatabaseProvider(),
        AiogramProvider(),
        AgnoProvider(),
        LLMProvider(),
        context={Config: config},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = structlog.get_logger()
    container = app.state.dishka_container

    config = await container.get(Config)

    bot, dp = create_aiogram_app(config)
    setup_dishka_aiogram(container, dp, auto_inject=True)

    polling_task = asyncio.create_task(dp.start_polling(bot))

    logger.info("Бот Запущен")
    yield

    polling_task.cancel()
    with suppress(asyncio.CancelledError):
        await polling_task
    await bot.close()


def create_app():
    config = get_config()
    setup_logger(config.logging)
    logger = structlog.get_logger()

    logger.info("Initializing app")
    container = setup_di_container(config)
    app = create_fastapi_app(config, lifespan=lifespan)
    setup_dishka_fastapi(container, app)
    logger.info("App initialized")

    return app


app = create_app()
