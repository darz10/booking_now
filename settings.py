from typing import List
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    """Валидация данных конфигруации"""

    DB_CONNECT: PostgresDsn = Field(
        ..., description="Подключение к PostgreSQL"
    )
    REDIS_HOST: str = Field(..., description="Хост для подключения redis")
    REDIS_PORT: int = Field(..., description="Порт для подключения redis")
    REDIS_DB: int = Field(..., description="Адрес для подключения redis")
    SECRET_KEY: str = Field(..., description="Секретный ключ проекта")
    ACCESS_TOKEN_EXPIRE_DAYS: int = Field(
        ..., description="Время действия токена"
    )
    ALGORITHM: str = Field(..., description="Алгоритм создания токена")
    ORIGINS: List[str] = Field(
        ..., description="Список доступных адресов(CORS)"
    )
    USER_DEFAULT_ROLE: int = Field(
        ..., description="Стандартное значение роли пользователя"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "BN_"


settings = Settings()


def get_settings():
    global settings
    settings = Settings() if not settings else settings
    return settings
