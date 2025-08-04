from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    patronymic: str
