from pydantic import BaseModel, Field

from institutions.schemas.base_filter import BaseFilter


class Country(BaseModel):
    """Схема страны"""
    id: int = Field(..., description="id страны")
    name: str = Field(..., description="Название страны")


class CountryFilter(BaseFilter):
    name__ilike: str = Field(None, description="Поиск страны по названию")
