from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    patronymic = State()