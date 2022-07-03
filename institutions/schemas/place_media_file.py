from typing import Optional
from pydantic import BaseModel, Field


class CreatePlaceMediaFile(BaseModel):
    """Схема связи места с файлом"""
    file_id: int = Field(..., description="ID пользователя")
    place_id: int = Field(..., description="ID точки компании")