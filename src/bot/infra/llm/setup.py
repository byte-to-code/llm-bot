from collections.abc import Sequence

import structlog
from openai import APITimeoutError, AsyncOpenAI

from src.bot.config import Config

logger = structlog.get_logger()

# TODO: Переехать на Agno
class OpenRouterService:
    def __init__(self, client: AsyncOpenAI, config: Config):
        self.client = client
        self.config = config
        self.system_prompt = config.openrouter.system_prompt

    async def llm_answer(
        self, history_message: Sequence, user_message: str, model: str
    ) -> str:
        history_obj = await self._get_history_obj(history_message)
        history_obj.insert(
            0,
            {
                "role": "system",
                "content": self.config.openrouter.system_prompt,
            },
        )
        history_obj.append({"role": "user", "content": user_message})
        try:
            completion = await self.client.chat.completions.create(
                model=model,
                messages=history_obj,
                timeout=15.0,
            )
            return completion.choices[0].message.content

        except APITimeoutError:
            logger.exception("Timeout error", timeout=15.0)
            return "Превышено время ожидания ответа от llm"

        except Exception:
            logger.exception("OpenRouter error")
            return "Ошибка при обращении к LLM"

    async def _get_history_obj(self, history_message: list):
        history_obj = []
        for message in history_message:
            history_obj.append(
                {"role": "user", "content": message.message_text_user}
            )
            history_obj.append(
                {"role": "assistant", "content": message.message_answer_system}
            )

        return history_obj
