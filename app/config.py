import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    TOKEN: str
    ADMINS: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return f"sqlite+aiosqlite:///../{settings.DB_NAME}"


def get_token():
    return settings.TOKEN


def get_admins():
    return settings.ADMINS
