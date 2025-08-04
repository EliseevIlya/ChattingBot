from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from app.database import async_session_maker
from app.reposetory.user_repository import UserRepository
from app.services.user_service import UserService
from app.states.user_registration import UserRegistration

update_user_router = Router()

@update_user_router.message(Command("update"))
async def user_update(message: Message):
    pass