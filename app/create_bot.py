import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import get_token,get_admins

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id.strip()) for admin_id in get_admins().split(",") if admin_id.strip().isdigit()]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=get_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dispatcher = Dispatcher(storage=MemoryStorage())