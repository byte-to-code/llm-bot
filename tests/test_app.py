from unittest.mock import Mock, patch

from src.bot.presentation.bot.app import create_app
from src.bot.presentation.bot.handlers.processing import (
    ROUTER as PROCESSING_ROUTER,
)

TEST_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456789"


def test_processing_router_included():
    """Тест что PROCESSING_ROUTER подключен к диспетчеру."""
    with patch("src.bot.presentation.bot.app.Bot"):
        config = Mock()
        config.telegram.token = TEST_TOKEN

        bot, dp = create_app(config)

        assert PROCESSING_ROUTER in dp.sub_routers, (
            "Роутер обработки не подключен к диспетчеру"
        )

        count = dp.sub_routers.count(PROCESSING_ROUTER)
        assert count == 1, f"Роутер подключен {count} раз, а должен быть 1"
