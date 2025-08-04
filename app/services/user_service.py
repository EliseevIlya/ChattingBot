from app.models.user import User
from app.reposetory.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

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

