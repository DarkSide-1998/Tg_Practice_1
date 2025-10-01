from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard_cancel() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Вернуться в меню", callback_data="back_to_menu")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def inline_prewiev_before_db() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Заполнить заново", callback_data="reset")
    kb.button(text="Отправить данные", callback_data="sender")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def inline_deleter_card(id_user_telegram: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Удалить карточку", callback_data=f"delete_card:{id_user_telegram}")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)