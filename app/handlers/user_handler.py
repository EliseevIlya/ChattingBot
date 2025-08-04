from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter

from app.database import async_session_maker
from app.reposetory.message_repository import MessageRepository
from app.reposetory.user_repository import UserRepository
from app.services.user_service import UserService
from app.states.message_send import MessageSend
from app.states.update_user import UpdateUser
from app.states.user_registration import UserRegistration
from keyboards.user_menu_inline import user_menu_inline_kb, show_users_inline_kb
from keyboards.user_update_inline import user_update_inline_kb, actions_inline_kb

user_router = Router()


@asynccontextmanager
async def get_service() -> AsyncGenerator[UserService, Any]:
    async with async_session_maker() as session:
        user_repo = UserRepository(session)
        message_repo = MessageRepository(session)
        service = UserService(user_repository=user_repo, message_repository=message_repo)
        yield service


@user_router.message(Command("update"))
async def user_update(message: Message):
    await message.answer(f"Выберите что хотите обновить", reply_markup=user_update_inline_kb())


@user_router.callback_query(F.data.startswith('update_'))
async def user_update_callback(query: CallbackQuery, state: FSMContext):
    field = query.data.replace('update_', '')
    await state.update_data(field_to_update=field)
    await state.set_state(UpdateUser.new_value)
    await query.message.edit_text(f"Введите новое значение для {field}:")
    await query.answer()


#TODO обработка что username уже есть
@user_router.message(F.text, UpdateUser.new_value)
async def process_new_value(message: Message, state: FSMContext):
    new_value = message.text.strip()
    if not new_value:
        await message.reply("Пожалуйста, введите новое значение.")
        return

    data = await state.get_data()
    field = data.get('field_to_update')
    changes = data.get('changes', {})
    changes[field] = new_value
    await state.update_data(changes=changes)

    await state.set_state(UpdateUser.changes)
    await message.reply(f"Новое значение для {field}: {new_value}", reply_markup=actions_inline_kb())


@user_router.callback_query(F.data == 'save_changes')
async def save_changes_callback(query: CallbackQuery, state: FSMContext):
    async with get_service() as service:
        data = await state.get_data()
        changes = data.get('changes', {})
        await service.update_user(data=changes, tg_id=query.from_user.id)
    await query.answer()
    await query.message.delete()


@user_router.callback_query(F.data == 'change_another')
async def change_another_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateUser.field_to_update)
    await query.message.edit_text("Выберите, что хотите обновить", reply_markup=user_update_inline_kb())
    await query.answer()


@user_router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Выберите действие:", reply_markup=user_menu_inline_kb())


@user_router.callback_query(F.data == "show_users")
async def show_users_callback(query: CallbackQuery, state: FSMContext):
    async with get_service() as service:
        users = await service.get_all_users(offset=0, limit=5)
        await query.message.edit_text("Выберите пользователя:",
                                      reply_markup=show_users_inline_kb(users=users, offset=0))


@user_router.callback_query(F.data.startswith("next_users_"))
async def next_users_callback(query: CallbackQuery, state: FSMContext):
    offset = int(query.data.split("_")[2])
    async with get_service() as service:
        users = await service.get_all_users(offset=offset, limit=5)
        await query.message.edit_text("Выберите пользователя:",
                                      reply_markup=show_users_inline_kb(users=users, offset=offset))


@user_router.callback_query(F.data.startswith("user_"))
async def user_selected_callback(query: CallbackQuery, state: FSMContext):
    user_id = int(query.data.split("_")[1])
    await state.set_state(MessageSend.message_to_send)
    await state.update_data(user_id=user_id)
    await query.message.edit_text("Введите текст сообщения или отправьте медиа:")


#TODO отправка медиа
@user_router.message(MessageSend.message_to_send)
async def send_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        await message.answer("Не удалось определить получателя.")
        await state.clear()
        return

    async with get_service() as service:
        user = await service.get_user_by_id(user_id)
        if not user:
            await message.answer("Пользователь не найден.")
            await state.clear()
            return
        print(message.from_user.id)
        if message.text:
            await service.send_message_via_bot(sender_id=message.from_user.id, receiver_id=user.tg_id,content=message.text)
            await message.answer(f"Сообщение отправлено пользователю {user.username} \n")
        else:
            await message.answer("Поддерживается только текст.")


    await state.clear()
