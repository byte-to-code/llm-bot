import pytest
from unittest.mock import MagicMock, patch
from collections.abc import AsyncIterable

from src.bot.config import Config
from src.bot.infra.llm.setup import OpenRouterService
from src.bot.bootstrap.di import OpenRouterProvider


# Мок для класса AsyncOpenAI, чтобы не делать реальных запросов
@pytest.fixture
def mock_async_openai():
    # Патчим класс AsyncOpenAI в том модуле, где он ИСПОЛЬЗУЕТСЯ (в di.py)
    with patch("src.bot.bootstrap.di.AsyncOpenAI") as mock:
        # Настраиваем мок, чтобы он возвращал объект при вызове конструктора
        instance = MagicMock()
        mock.return_value = instance
        yield mock


@pytest.mark.asyncio
class TestOpenRouterProvider:

    async def test_get_openai_client(self, mock_async_openai):
        """
        Проверяет, что get_openai_client создает клиент AsyncOpenAI 
        с правильными параметрами из конфига.
        """
        provider = OpenRouterProvider()

        # --- НАЧАЛО ИСПРАВЛЕНИЯ ---
        # Создаем мок конфига с использованием spec (хорошая практика)
        mock_config = MagicMock(spec=Config)
        
        # Явно создаем вложенный мок для openrouter, так как spec не создает вложенные объекты автоматически
        mock_config.openrouter = MagicMock()
        
        # Теперь безопасно устанавливаем значения
        mock_config.openrouter.base_url = "https://test.openrouter.ai/v1"
        mock_config.openrouter.api_key = "k-or-v1-1234567890abcdef"
        # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

        client_gen = provider.get_openai_client(mock_config)
        client = await anext(client_gen)

        mock_async_openai.assert_called_once()
        
        call_kwargs = mock_async_openai.call_args.kwargs
        assert call_kwargs['base_url'] == "https://test.openrouter.ai/v1"
        assert call_kwargs['api_key'] == "k-or-v1-1234567890abcdef"

        assert client is mock_async_openai.return_value

    async def test_get_openrouter_service_returns_service(self):
        """
        Проверяет, что get_openrouter_service создает экземпляр OpenRouterService
        с переданными зависимостями.
        """
        provider = OpenRouterProvider()
        
        mock_client = MagicMock(name="AsyncOpenAI_Client")
        mock_config = MagicMock(name="Config")

        service = await provider.get_openrouter_service(mock_client, mock_config)

        assert isinstance(service, OpenRouterService)
        assert service.client is mock_client
        assert service.config is mock_config