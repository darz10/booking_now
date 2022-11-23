from pydantic import BaseModel, Field


class City(BaseModel):
    """Схема города"""
    id: int = Field(..., description="id города")
    name: str = Field(..., description="Название города")
    country_id: int = Field(..., description="id страны города")
