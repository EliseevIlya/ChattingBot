import asyncio

from app.handlers.registration_handler import reg_router
from app.handlers.user_handler import user_router
from create_bot import bot, dispatcher
from utils.commands import set_commands


async def main():
    dispatcher.include_router(reg_router)
    dispatcher.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
