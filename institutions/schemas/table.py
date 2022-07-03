from typing import Optional
from pydantic import BaseModel, Field


class BaseTable(BaseModel):
    table_number: int = Field(..., description="Номер стола")
    max_people: int = Field(..., description="id страны города")
    is_electricity: int = Field(..., description="id страны города")
    floor: int = Field(..., description="id страны города")
    is_available: int = Field(..., description="id страны города")
    place_branch_id: int = Field(..., description="Точка заведения")


class UpdateTable(BaseModel):
    table_number: Optional[int] = Field(None, description="Номер стола")
    max_people: Optional[int] = Field(None, description="id страны города")
    is_electricity: Optional[int] = Field(None, description="id страны города")
    floor: Optional[int] = Field(None, description="id страны города")
    is_available: Optional[int] = Field(None, description="id страны города")
    place_branch_id: Optional[int] = Field(None, description="Точка заведения")


class Table(BaseTable):
    id: int = Field(..., description="id стола")