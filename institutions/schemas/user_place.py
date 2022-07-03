from typing import Optional
from pydantic import BaseModel, Field


class UserPlace(BaseModel):
    """Схема связи пользователя с местом"""
    user_id: int = Field(..., description="ID пользователя")
    place_branch_id: int = Field(..., description="ID точки компании")
    is_favourite: Optional[bool] = Field(False, description="Статус 'избранный'")


class UpdateUserPlace(BaseModel):
    """Схема связи пользователя с местом для обновления"""
    user_id: Optional[int] = Field(None, description="ID пользователя")
    place_branch_id: Optional[int] = Field(None, description="ID точки компании")
    is_favourite: Optional[bool] = Field(None, description="Статус 'избранный'")