
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from app.states.UserRegistration import UserRegistration

reg_router = Router()


@reg_router.message(Command('registration'))
async def registration_handler(message: Message, state: FSMContext):
    await message.answer("Введите username")
    await state.set_state(UserRegistration.username)


@reg_router.message(F.text, UserRegistration.username)
async def capture_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(f"Ваш username {message.text}.\nВведите имя")
    await state.set_state(UserRegistration.first_name)


@reg_router.message(F.text, UserRegistration.first_name)
async def capture_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(f"Ваше имя {message.text}.\nВведите фамилию")
    await state.set_state(UserRegistration.last_name)


#TODO обработка если отчества нет
@reg_router.message(F.text, UserRegistration.last_name)
async def capture_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer(f"Ваша фамилия {message.text}.\nВведите отчество")
    await state.set_state(UserRegistration.patronymic)


@reg_router.message(F.text, UserRegistration.patronymic)
async def capture_patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await message.answer(f"Ваша фамилия {message.text}.\nНа этом все!")
    data = await state.get_data()
    print(data)
    await state.clear()
