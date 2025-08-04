from aiogram.fsm.state import StatesGroup, State


class UpdateUser(StatesGroup):
    field_to_update = State()
    new_value = State()
    changes = State()
