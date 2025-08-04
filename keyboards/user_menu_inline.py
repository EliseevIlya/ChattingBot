from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_menu_inline_kb() -> InlineKeyboardMarkup:
    inline_kb_list = [
        [InlineKeyboardButton(text="Отобразить всех пользователей", callback_data="show_users")],
        [InlineKeyboardButton(text="Изменить профиль", callback_data="edit_profile")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def show_users_inline_kb(users: list, offset: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for user in users:
        builder.button(text=user.username, callback_data=f"user_{user.tg_id}")
    if len(users) == 5:
        builder.button(text="Дальше", callback_data=f"next_users_{offset + 5}")
    builder.adjust(1)
    return builder.as_markup()
