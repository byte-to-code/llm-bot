import structlog
from openai import APITimeoutError, AsyncOpenAI

from src.bot.config import Config

logger = structlog.get_logger()


class OpenRouterService:
    def __init__(self, client: AsyncOpenAI, config: Config):
        self.client = client
        self.config = config

    async def llm_answer(self, user_message: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                model=self.config.openrouter.model,
                messages=[{"role": "user", "content": user_message}],
                timeout=15.0,
            )
            return completion.choices[0].message.content

        except APITimeoutError:
            logger.exception("Timeout error", timeout=15.0)
            return "Превышено время ожидания ответа от llm"

        except Exception:
            logger.exception("OpenRouter error")
            return "Ошибка при обращении к LLM"
