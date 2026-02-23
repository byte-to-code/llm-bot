import os
import pytest
from dynaconf import Dynaconf
from bot.config import Config, get_config, AppConfig, TelegramConfig, DatabaseConfig, LoggingConfig


class TestConfigModels:
    def test_app_config_creation(self):
        data = {"title": "Test Bot", "description": "Test Desc", "version": "1.0.0"}
        config = AppConfig(**data)
        
        assert config.title == "Test Bot"
        assert config.description == "Test Desc"
        assert config.version == "1.0.0"

