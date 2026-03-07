from unittest.mock import MagicMock, patch

import pytest

from src.bot.bootstrap.di import OpenRouterProvider
from src.bot.config import Config
from src.bot.infra.llm.setup import OpenRouterService


@pytest.fixture
def mock_async_openai():
    with patch("src.bot.bootstrap.di.AsyncOpenAI") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield mock


@pytest.mark.asyncio
class TestOpenRouterProvider:
    async def test_get_openai_client(self, mock_async_openai):
        """
        Проверяет, что get_openai_client создает клиент AsyncOpenAI.

        с правильными параметрами из конфига.
        """
        provider = OpenRouterProvider()

        mock_config = MagicMock(spec=Config)

        mock_config.openrouter = MagicMock()

        mock_config.openrouter.base_url = "https://test.openrouter.ai/v1"
        mock_config.openrouter.api_key = "k-or-v1-1234567890abcdef"

        client_gen = provider.get_openai_client(mock_config)
        client = await anext(client_gen)

        mock_async_openai.assert_called_once()

        call_kwargs = mock_async_openai.call_args.kwargs
        assert call_kwargs["base_url"] == "https://test.openrouter.ai/v1"
        assert call_kwargs["api_key"] == "k-or-v1-1234567890abcdef"

        assert client is mock_async_openai.return_value

    async def test_get_openrouter_service_returns_service(self):
        """
        Проверяет, что get_openrouter_service создает экземпляр.

        OpenRouterService с переданными зависимостями.
        """
        provider = OpenRouterProvider()

        mock_client = MagicMock(name="AsyncOpenAI_Client")
        mock_config = MagicMock(name="Config")

        service = await provider.get_openrouter_service(
            mock_client, mock_config
        )

        assert isinstance(service, OpenRouterService)
        assert service.client is mock_client
        assert service.config is mock_config
