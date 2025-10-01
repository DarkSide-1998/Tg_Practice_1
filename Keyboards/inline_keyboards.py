from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard_cancel() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Вернуться в меню", callback_data="back_to_menu")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)