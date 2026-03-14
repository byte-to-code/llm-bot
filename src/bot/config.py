import os
from datetime import UTC, datetime
from pathlib import Path

from dynaconf import Dynaconf
from jinja2 import Environment
from pydantic import AliasGenerator, BaseModel, ConfigDict, SecretStr


class AppConfig(BaseModel):
    title: str
    description: str
    version: str


class TelegramConfig(BaseModel):
    token: str
    bot_name: str
    max_history: int


class OpenRouterConfig(BaseModel):
    api_key: SecretStr
    base_url: str
    model: str
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    system_prompt_path: Path | None = None
    _system_prompt: str | None = None

    def _get_prompt(self, name: str) -> str:
        prompt_path = getattr(self, f"{name}_path", None)
        if prompt_path is None:
            raise ValueError(f"Prompt {name} not found")

        return (
            Environment(autoescape=True)
            .from_string(prompt_path.read_text())
            .render(now=datetime.now(UTC))
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
    db_schema: str = "public"

    provider: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    json_logs: bool = False


class AgentConfig(BaseModel):
    name: str
    model_id: str
    db_url: str
    mcp_url: str
    add_datetime_to_context: bool
    add_history_to_context: bool
    num_history_runs: int
    markdown: bool
    api_key: SecretStr
    base_agno_url: str


class Config(BaseModel):
    app: AppConfig
    telegram: TelegramConfig
    database: DatabaseConfig
    logging: LoggingConfig
    openrouter: OpenRouterConfig
    agno: AgentConfig

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=lambda x: x.upper()),
        populate_by_name=True,
    )


def get_config() -> Config:

    config = Dynaconf(
        settings_files=[os.getenv("CONFIG_PATH", "./config.toml")],
        envvar_prefix="BOT",
        load_dotenv=True,
        merge_enabled=True,
    )
    return Config.model_validate(config.as_dict())
