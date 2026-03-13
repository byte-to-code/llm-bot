from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIResponses

from agno.tools.mcp import MCPTools

from src.bot.config import Config


def create_agno_assist(config: Config) -> Agent:

    return Agent(
        name=config.agno.name,
        model=OpenAIResponses(
            id=config.agno.model_id,
            api_key=config.agno.api_key,
            base_url=config.agno.base_agno_url,
        ),
        db=PostgresDb(db_url=config.agno.db_url),
        tools=[MCPTools(url=config.agno.mcp_url)],
        add_datetime_to_context=config.agno.add_datetime_to_context,
        add_history_to_context=config.agno.add_history_to_context,
        num_history_runs=config.agno.num_history_runs,
        markdown=config.agno.markdown,
    )
