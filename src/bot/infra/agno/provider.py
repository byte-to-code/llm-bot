from agno.agent import Agent
from agno.db.async_postgres import AsyncPostgresDb
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from dishka import Provider, Scope, provide

from src.bot.config import Config


class LLMProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_llm_db(self, config: Config) -> AsyncPostgresDb:
        return AsyncPostgresDb(
            db_url=config.database.url,
            db_schema=config.database.db_schema,
            create_schema=True,
        )

    @provide(scope=Scope.APP)
    async def get_openai_model(self, config: Config) -> OpenAIChat:
        return OpenAIChat(
            api_key=config.agno.api_key.get_secret_value(),
            base_url=config.agno.base_agno_url,
            id=config.agno.model_id,
            name=config.agno.model_id,
            provider="VLLM",
            role_map={
                "user": "user",
                "assistant": "assistant",
                "system": "system",
                "model": "assistant",
                "tool": "tool",
            },
        )

    @provide(scope=Scope.APP)
    async def get_agent(
        self, config: Config, db: AsyncPostgresDb, model: OpenAIChat
    ) -> Agent:
        return Agent(
            name=config.agno.name,
            model=model,
            db=db,
            tools=[MCPTools(url=config.agno.mcp_url)],
            add_datetime_to_context=config.agno.add_datetime_to_context,
            add_history_to_context=config.agno.add_history_to_context,
            num_history_runs=config.agno.num_history_runs,
            markdown=config.agno.markdown,
        )
