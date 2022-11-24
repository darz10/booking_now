from typing import Optional
from pydantic import BaseModel, Field

from accounts.schemas import User


class BaseMediaFile(BaseModel):
    """Базовая схема медиа файла (для наследования)"""
    source_id: str = Field(..., description="id файла для интеграции S3")
    source_fields: Optional[dict] = Field(
        None,
        description="Поля для интеграции S3"
    )
    source_url: Optional[str] = Field(
        None,
        description="Url для интеграции S3"
    )
    uploaded: Optional[bool] = Field(False, description="Статус загрузки в S3")
    filename: str = Field(..., description="Название файла")


class CreateMediaFile(BaseMediaFile):
    user_id: int = Field(..., description="id пользователя кто создаёт файл")


class UpdateMediaFile(BaseModel):
    source_id: Optional[str] = Field(
        None,
        description="id файла для интеграции S3"
    )
    source_fields: Optional[dict] = Field(
        None,
        description="Поля для интеграции S3"
    )
    source_url: Optional[str] = Field(
        None,
        description="Url для интеграции S3"
    )
    uploaded: Optional[bool] = Field(
        False,
        description="Статус загрузки в S3"
    )
    filename: Optional[str] = Field(
        None,
        description="Название файла"
    )
    user_id: Optional[int] = Field(
        None,
        description="id пользователя кто создаёт файл"
    )


class MediaFile(BaseMediaFile):
    id: int = Field(..., description="id файла")
    user: User = Field(..., description="Создатель файла")
