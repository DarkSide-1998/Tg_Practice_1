from aiogram.fsm.state import StatesGroup, State


class UserStatements(StatesGroup):
    name = State()
    age = State()
    city = State()
    social_status = State()
    description = State()