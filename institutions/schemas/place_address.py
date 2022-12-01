from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from institutions.schemas import Country, City


class BasePlaceAddress(BaseModel):
    """Базовая схема адеса места place_branch (для наследования)"""
    street: str = Field(..., description="Улица")
    building: str = Field(..., description="Дом")
    latitude: Decimal = Field(..., description="Широта")
    longitude: Decimal = Field(..., description="Долгота")


class CreatePlaceAddress(BasePlaceAddress):
    country_id: int = Field(..., description="id страны")
    city_id: int = Field(..., description="id города")


class PlaceAddress(BasePlaceAddress):
    id: int = Field(..., description="id адреса")
    country: Country = Field(..., description="Cтрана")
    city: City = Field(..., description="Город")


class UpdatePlaceAddress(BaseModel):
    street: Optional[str] = Field(None, description="Улица")
    building: Optional[str] = Field(None, description="Дом")
    latitude: Optional[Decimal] = Field(None, description="Широта")
    longitude: Optional[Decimal] = Field(None, description="Долгота")
