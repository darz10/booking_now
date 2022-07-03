from typing import Optional
from pydantic import BaseModel, Field

from institutions.enums import PlaceType
from accounts.schemas import User


class BasePlace(BaseModel):
    """Базовая схема места (для наследования)"""
    title: str = Field(None, description="Название места")
    description: Optional[str] = Field(None, description="Описание места")
    url: Optional[str] = Field(
        None, description="Адрес сайта места"
    )
    avatar: Optional[str] = Field(None, description="Изображение места")
    email: Optional[str] = Field(None, description="Email места")
    phone: Optional[str] = Field(None, description="Email места")


class Place(BasePlace):
    """Основная схема места с определением типа места"""
    type_place: PlaceType = Field(None, description="Тип места")


class UpdatePlace(Place):
    id: int = Field(..., description="id места")


class PlaceDB(UpdatePlace):
    owner: User = Field(None, description="Создатель места")
