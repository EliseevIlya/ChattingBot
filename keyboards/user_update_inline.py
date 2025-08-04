from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_update_inline_kb() -> InlineKeyboardMarkup:
    inline_kb_list = [
        [InlineKeyboardButton(text="Username", callback_data="update_username")],
        [InlineKeyboardButton(text="Имя", callback_data="update_first_name")],
        [InlineKeyboardButton(text="Фамилия", callback_data="update_last_name")],
        [InlineKeyboardButton(text="Отчество", callback_data="update_patronymic")],

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def actions_inline_kb() -> InlineKeyboardMarkup:
    inline_kb_list = [
        [InlineKeyboardButton(text="Сохранить", callback_data="save_changes")],
        [InlineKeyboardButton(text="Изменить другое", callback_data="change_another")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)