from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
