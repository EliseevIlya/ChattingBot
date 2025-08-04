from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk, str_uniq, str_null_true, str_null_false


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    first_name: Mapped[str_null_false]
    last_name: Mapped[str_null_false]
    patronymic: Mapped[str_null_true]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)