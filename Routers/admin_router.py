from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Decorators import AutoDeleteMessage

from Keyboards import inline_keyboard_cancel, key_board_admin

from Statements import AdminStatements

from Filters import IsAdmin, IsValidNumber

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.callback_query(F.data == "back_to_menu") 
@admin_router.message(CommandStart())
@AutoDeleteMessage(num_id_prew=0)
async def greeting_admin(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await update.answer("""
Добро пожаловать, Администратор!
Выберите действие ниже:
                            """, reply_markup=key_board_admin())
    else:
        await update.message.answer("""
Добро пожаловать, Администратор!
Выберите действие ниже:                                    
                                    """, reply_markup=key_board_admin())
    await state.clear() 
    
    
@admin_router.message(StateFilter(None), F.text.lower() == "найти карточку по id")
async def search_id(message: Message, state: FSMContext):
    await message.answer("""
Введите ID:
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(AdminStatements.id)
    
    
@admin_router.message(IsAdmin(), AdminStatements.id_user)
async def invalid_number(message: Message):
    await message.answer("Введите корректный айди юзернейма Телеграм для поиска - пример: 123456789")