from typing import Optional, Tuple, List
from pydantic import BaseModel, Field

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
    place_type: int = Field(..., description="Тип места")


class PlaceFilter(BaseModel):
    title__ilike: Optional[str] = Field(
        None,
        description="Поиск мест по названию"
    )
    place_type_id__eq: Optional[int] = Field(
        None,
        description="Поиск мест по id типа места"
    )

    @property
    def has_objects(self):
        values = self.dict().values()
        return any(values)


class UpdatePlace(Place):
    id: int = Field(..., description="id места")


class PlaceDB(UpdatePlace):
    owner: User = Field(None, description="Создатель места")
