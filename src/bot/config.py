import os

from dynaconf import Dynaconf
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
    system_prompt: str


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
