from aiogram.fsm.state import StatesGroup, State


class MessageSend(StatesGroup):
    message_to_send = State()