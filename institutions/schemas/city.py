from pydantic import BaseModel, Field

from institutions.schemas.base_filter import BaseFilter


class City(BaseModel):
    """Схема города"""
    id: int = Field(..., description="id города")
    name: str = Field(..., description="Название города")
    country_id: int = Field(..., description="id страны города")


class CityFilter(BaseFilter):
    country_id: int = Field(None, description="Выборка городов по стране")
    name__ilike: str = Field(None, description="Поиск города по названию")
