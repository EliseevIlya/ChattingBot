from typing import Optional

from app.create_bot import bot
from app.models.messages_db_model import MessagesDBModel
from app.models.user import User
from app.reposetory.message_repository import MessageRepository
from app.reposetory.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, message_repository: MessageRepository):
        self.repository = user_repository
        self.message_repository = message_repository

    async def register_user(self, data: dict, tg_id: int, is_admin: bool = False):
        user_data = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            patronymic=data['patronymic'],
            tg_id=tg_id,
            is_admin=is_admin
        )
        await self.repository.add_user(user_create=user_data)

    async def user_exists(self, username: str) -> bool:
        return await self.repository.user_exists(username=username)

    async def update_user(self, tg_id: int, data: dict):
        user = await self.repository.get_user_by_tg_id(tg_id)
        if not user:
            raise ValueError(f"User not found")

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await self.repository.update_user(user)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.repository.get_user_by_tg_id(user_id)

    async def get_all_users(self, offset: int = 0, limit: int = 5) -> list:
        return await self.repository.get_all_users(offset=offset, limit=limit)

    async def send_message_via_bot(self, sender_id: int, receiver_id: int, content: str):
        sender = await self.repository.get_user_by_tg_id(sender_id)

        message = MessagesDBModel(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        print(receiver_id, sender_id, content)
        await self.message_repository.add_message(message)
        receiver = await self.repository.get_user_by_tg_id(receiver_id)
        if receiver:
            print(receiver.tg_id)
            print(content)
            await bot.send_message(receiver.tg_id, f"Вам сообщение от пользователя {sender.username}:\n{content}")