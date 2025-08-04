from typing import List, Optional

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from dto.UserCreate import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_tg_id(self, user_tg_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.tg_id == user_tg_id))
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def add_user(self, user_create: User):
        if await self.get_user_by_tg_id(user_create.tg_id):
            raise ValidationError('User with this username already exists')
        self.session.add(user_create)
        await self.session.commit()
        await self.session.refresh(user_create)

    async def user_exists(self, username: str) -> bool:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none() is not None

    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def update_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)