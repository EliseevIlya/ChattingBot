from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_null_false


class MessagesDBModel(Base):
    __tablename__ = 'messages'

    id: Mapped[int_pk]
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    content: Mapped[str_null_false]
