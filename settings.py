from typing import List
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    """Валидация данных конфигруации"""

    DB_CONNECT: PostgresDsn = Field(
        ..., description="Подключение к postgresql"
    )
    REDIS_HOST: str = Field(..., description="Хост для подключения redis")
    REDIS_PORT: int = Field(..., description="Порт для подключения redis")
    REDIS_DB: int = Field(..., description="Бд для подключения redis")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "BN_"