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
