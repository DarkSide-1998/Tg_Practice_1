from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Decorators import AutoDeleteMessage

from Keyboards import key_board_user, inline_keyboard_cancel

from Statements import UserStatements

from Filters import IsValidField, IsValidNumber

user_router = Router()


@user_router.callback_query(F.data == "back_to_menu")
@user_router.message(CommandStart())
@AutoDeleteMessage(num_id_prew=0)
async def greeting(update: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(update, Message):
        await update.answer("""
Добро пожаловать!
Выберите действие ниже:
                            """, reply_markup=key_board_user())
    else:
        await update.message.answer("""
Добро пожаловать!
Выберите действие ниже:                                    
                                    """, reply_markup=key_board_user())
    await state.clear()
    
    
@user_router.message(StateFilter(None), F.text.lower() == "создать карточку")
@AutoDeleteMessage(num_id_prew=1)
async def name_user(message: Message, state: FSMContext):
    await message.answer("""
Введите имя:
Условие: от 3 до 16 символов с использованием только латинских больший, маленьких букв, цифр и знаков подчеркивания, вместо пробелов
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(UserStatements.name)
    
    
@user_router.message(UserStatements.name, IsValidField("_", 3, 16))
@AutoDeleteMessage(num_id_prew=1)
async def age_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("""
Введите возраст:
Условие: целочисленное значение от 1 до 149
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(UserStatements.age)
    
    
@user_router.message(UserStatements.name)
@AutoDeleteMessage(num_id_prew=1)
async def age_user(message: Message, state: FSMContext):
    await message.answer("""
Введите корректное имя!
Условие: от 3 до 16 символов с использованием только латинских больший, маленьких букв, цифр и знаков подчеркивания, вместо пробелов
                   """, reply_markup=inline_keyboard_cancel())
    
    
@user_router.message(UserStatements.age, IsValidNumber(1, 149))
@AutoDeleteMessage(num_id_prew=1)
async def city_user(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("""
Введите место рождения:
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(UserStatements.city)
    
    
@user_router.message(UserStatements.age)
@AutoDeleteMessage(num_id_prew=1)
async def age_user(message: Message, state: FSMContext):
    await message.answer("""
Введите корректный возраст:
Условие: целочисленное значение от 1 до 149
                   """, reply_markup=inline_keyboard_cancel())
    
    
@user_router.message(UserStatements.city)
@AutoDeleteMessage(num_id_prew=1)
async def city_user(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("""
Введите свое семейное полжение:
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(UserStatements.social_status)
    
    
@user_router.message(UserStatements.social_status)
@AutoDeleteMessage(num_id_prew=1)
async def city_user(message: Message, state: FSMContext):
    await state.update_data(social_status=message.text)
    await message.answer("""
Введите дополнительную информацию:
                   """, reply_markup=inline_keyboard_cancel())
    await state.set_state(UserStatements.description)
    
    
@user_router.message(UserStatements.description)
@AutoDeleteMessage(num_id_prew=1)
async def city_user(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"""
Поздравляем - у вас новая карточка: Проверьте данные
Имя: {data["name"]}
Возраст: {data["age"]}
Город: {data["city"]}
Семейное положение: {data["social_status"]}
Дополнительная информация: {message.text}
                   """, reply_markup=inline_keyboard_cancel())