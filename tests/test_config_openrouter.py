import pytest
from pydantic import ValidationError
from src.bot.config import OpenRouterConfig

def test_valid_config():
    """Тест конфигурации"""
    config = OpenRouterConfig(
        api_key="sk-or-v1-1234567890abcdef",
        base_url="https://openrouter.ai/api/v1",
        model="qwen/qwen3-next-80b-instruct",
        temperature=0.1,
        max_tokens=512,
        system_prompt="You are a helpful assistant"    
    )
    assert config.api_key == "sk-or-v1-1234567890abcdef"
    assert config.base_url == "https://openrouter.ai/api/v1"
    assert config.model == "qwen/qwen3-next-80b-instruct"
    assert config.temperature == 0.1
    assert config.max_tokens == 512
    assert config.system_prompt == "You are a helpful assistant"