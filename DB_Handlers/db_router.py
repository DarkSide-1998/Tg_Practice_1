from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from Middlewares import DataBaseSession

from DataBase import session_maker, orm_add, orm_get_card
from Models import Attributes

from Decorators import AutoDeleteMessage

from Keyboards import key_board_user


db_router = Router()
db_router.message.middleware(DataBaseSession(session_pool=session_maker))


@db_router.callback_query(F.data == "sender")
@AutoDeleteMessage(num_id_prew=1)
async def load_to_db_usercard(update: CallbackQuery, state: FSMContext, session: AsyncSession):
    # Здесь если карточки уникальной нет - записать новую, иначе - перезаписать старую
    data = await state.get_data()
    table = Attributes(
        name=data["name"],
        age=data["age"],
        city=data["city"],
        social_status=data["social_status"],
        description=data["description"],
        id_telegram_user=update.from_user.id,
        rating=0,
        messages=0,
        strikes=0,
    )
    for card in await orm_get_card(session, update.from_user.id):
        if card.id_telegram_user == update.from_user.id:
            update.message.answer("Карточка обновлена!", reply_markup=key_board_user())
        else:
            orm_add(session, table)
            update.message.answer("""
Карточка добавлена, поздравляем!
Теперь вы можете ее просмотреть, нажав на кнопку "Просмотреть карточку"                  
                   """, reply_markup=key_board_user())
    
    
@db_router.message(StateFilter(None), F.data.lower() == "посмотреть карточку")
@AutoDeleteMessage(num_id_prew=1)
async def load_from_db_card(message: Message, session: AsyncSession):
    for card in await orm_get_card(session, message.from_user.id):
        if card.id_telegram_user == message.from_user.id:
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
            