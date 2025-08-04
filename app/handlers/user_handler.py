from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter

from app.database import async_session_maker
from app.reposetory.user_repository import UserRepository
from app.services.user_service import UserService
from app.states.update_user import UpdateUser
from app.states.user_registration import UserRegistration
from keyboards.user_update_inline import user_update_inline_kb, actions_inline_kb

user_router = Router()


@asynccontextmanager
async def get_service() -> AsyncGenerator[UserService, Any]:
    async with async_session_maker() as session:
        repo = UserRepository(session)
        service = UserService(repo)
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
