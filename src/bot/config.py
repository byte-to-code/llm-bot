from datetime import datetime
import os
from pathlib import Path

from dynaconf import Dynaconf
from jinja2 import Environment
from pydantic import AliasGenerator, BaseModel, ConfigDict


class AppConfig(BaseModel):
    title: str
    description: str
    version: str


class TelegramConfig(BaseModel):
    token: str
    bot_name: str
    max_history: int


class OpenRouterConfig(BaseModel):
    api_key: str
    base_url: str
    model: str
    temperature: float
    max_tokens: int
    system_prompt_path: Path | None = None
    _system_prompt: str | None = None

    def _get_prompt(self, name: str) -> str:
        prompt_path = getattr(self, f"{name}_path", None)
        if prompt_path is None:
            raise ValueError(f"Prompt {name} not found")

        return (
            Environment(autoescape=True)
            .from_string(prompt_path.read_text())
            .render(now=datetime.now())
        )

    @property
    def system_prompt(self) -> str:
        if self._system_prompt is None:
            self._system_prompt = (
                self._get_prompt(
                    "system_prompt",
                )
                if self.system_prompt_path is not None
                else "You are a helpful assistant."
            )

        return self._system_prompt


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str
    bouncer: bool = False

    provider: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    json_logs: bool = False


class Config(BaseModel):
    app: AppConfig
    telegram: TelegramConfig
    database: DatabaseConfig
    logging: LoggingConfig
    openrouter: OpenRouterConfig

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=lambda x: x.upper())
    )


def get_config() -> Config:
    """Парсинг dotenv и получение конфига."""
    config = Dynaconf(
        settings_files=[os.getenv("CONFIG_PATH", "./config.toml")],
        envvar_prefix="BOT",
        load_dotenv=True,
        merge_enabled=True,
    )
    return Config.model_validate(config.as_dict())
