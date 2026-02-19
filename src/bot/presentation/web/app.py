from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from fastapi import FastAPI

from bot.config import Config
from bot.presentation.web.routers.internal import ROUTER as INTERNAL_ROUTER

Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_app(config: Config, lifespan: Lifespan) -> FastAPI:
    app = FastAPI(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        lifespan=lifespan,
    )

    app.include_router(INTERNAL_ROUTER, prefix="/internal")

    return app
