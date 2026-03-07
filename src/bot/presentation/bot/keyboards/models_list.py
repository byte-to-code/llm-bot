from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.config import Config


def switch_model_webapp(config: Config) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        type="web_app",
        text="Switch model",
        web_app=WebAppInfo(
            url=f"https://{config.app.web_app_url}/switch-model",
        ),
    )
    return builder.as_markup()


def models_list() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="qwen/qwen3-max", callback_data="qwen/qwen3-max"
                )
            ],
            [
                InlineKeyboardButton(
                    text="openai/gpt-4.1", callback_data="openai/gpt-4.1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="mistralai/ministral-8b-2512",
                    callback_data="mistralai/ministral-8b-2512",
                )
            ],
        ]
    )
