from sqlalchemy.ext.asyncio import AsyncSession

from app.models.messages_db_model import MessagesDBModel


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, message: MessagesDBModel):
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)