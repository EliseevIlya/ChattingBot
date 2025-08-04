from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
