from pydantic import BaseModel, Field


class Country(BaseModel):
    id: int = Field(..., description="id страны")
    name: str = Field(..., description="Название страны")