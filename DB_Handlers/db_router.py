from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from Middlewares import DataBaseSession

from DataBase import session_maker, orm_add, orm_get_card, orm_delete_card, orm_update_card, orm_get_all_cards
from Models import Attributes

from Filters import IsAdmin, IsValidNumber

from Statements import AdminStatements

from Decorators import AutoDeleteMessage

from Keyboards import key_board_user, key_board_admin, inline_deleter_card


db_router = Router()
db_router.message.filter(AutoDeleteMessage(num_id_prew=1))


@AutoDeleteMessage(num_id_prew=1)
@db_router.callback_query(F.data == "sender")
async def load_to_db_usercard(update: CallbackQuery, state: FSMContext, session: AsyncSession):
    # Здесь если карточки уникальной нет - записать новую, иначе - перезаписать старую
    data = await state.get_data()
    table = Attributes(
        name=data["name"],
        age=int(data["age"]),
        city=data["city"],
        social_status=data["social_status"],
        description=data["description"],
        id_telegram_user=update.from_user.id,
        rating=0,
        messages=0,
        strikes=0,
    )
    card = await orm_get_card(session, update.from_user.id)
    print(card)
    if card:
        await orm_update_card(session, card.id_telegram_user, table)
        await update.message.answer("Карточка обновлена!", reply_markup=key_board_user())
    else:
        await orm_add(session, table)
        await update.message.answer("""
Карточка добавлена, поздравляем!
Теперь вы можете ее просмотреть, нажав на кнопку "Просмотреть карточку"                  
                   """, reply_markup=key_board_user())
    await state.clear()
    

@AutoDeleteMessage(num_id_prew=1)    
@db_router.message(StateFilter(None), F.text.lower() == "посмотреть карточку")
async def load_from_db_card(message: Message, session: AsyncSession):
    card = await orm_get_card(session, message.from_user.id)
    if card:
            await message.answer(f"""
Вот ваша карточка:
Имя: {card.name},
Возраст: {card.age},
Город: {card.city},
Семейное положение: {card.social_status},
Дополнительная информация: {card.description},
Рейтинг: {card.rating},
Сообщений: {card.messages},
Предупреждений: {card.strikes}                                 
                                """, reply_markup=key_board_user())
    else:
        await message.answer("Похоже, у Вас нет карточки в нашей базе. Предлагаем создать новую!", reply_markup=key_board_user())
        

@AutoDeleteMessage(num_id_prew=1)
@db_router.message(IsAdmin(), StateFilter(None), F.text.lower() == "выгрузить все карточки")
async def admin_load_all_cards(message: Message, session: AsyncSession):
    string_text: str = ""
    for card in await orm_get_all_cards(session):
        string_text += f"Айди юзера: {card.id_telegram_user}, Имя: {card.name}\n"
    if string_text:
        await message.answer(string_text, reply_markup=key_board_admin())
    else:
        await message.answer("Карточек в базе нет.", reply_markup=key_board_admin())
    

@AutoDeleteMessage(num_id_prew=1) 
@db_router.message(IsAdmin(), IsValidNumber(1,9_999_999_999), AdminStatements.id_user)
async def admin_load_one_card(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(id_user=int(message.text))
    card = await orm_get_card(session, int(message.text))
    if card:
            await message.answer(f"""
Вот карточка id {int(message.text)}:
Имя: {card.name},
Возраст: {card.age},
Город: {card.city},
Семейное положение: {card.social_status},
Дополнительная информация: {card.description},
Рейтинг: {card.rating},
Сообщений: {card.messages},
Предупреждений: {card.strikes}                                 
                                """, reply_markup=(inline_deleter_card(int(message.text))))
    else:
        await message.answer("Такой карточки в базе нет!", reply_markup=key_board_admin())
        await state.clear()
        

@AutoDeleteMessage(num_id_prew=1)        
@db_router.callback_query(F.data.contains("delete_card"))
async def admin_delete_card_from_db(update: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await orm_delete_card(session, data["id_user"])
    await update.message.answer(f"Карточка {data['id_user']} удалена!", reply_markup=key_board_admin())
    await state.clear()