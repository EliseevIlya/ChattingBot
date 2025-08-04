from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='help', description='Что я умею'),
                BotCommand(command='registration', description='Регистрация'),
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
