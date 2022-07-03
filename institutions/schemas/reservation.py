from typing import Optional
from pydantic import BaseModel, Field

from institutions.enums import CelebrationType
from institutions.schemas import Table


class BaseReservation(BaseModel):
    amount_guests: int = Field(..., description="Номер стола")
    date_reservation: int = Field(..., description="id страны города")
    time_start: int = Field(..., description="id страны города")
    time_end: int = Field(..., description="id страны города")
    note: int = Field(..., description="id страны города")
    celebration: Optional[CelebrationType] = Field(None, description="Точка заведения")


class CreateReservation(BaseReservation):
    table_id: int = Field(..., description="id стола")


class UpdateReservation(BaseModel):
    amount_guests: Optional[int] = Field(None, description="Номер стола")
    date_reservation: Optional[int] = Field(None, description="id страны города")
    time_start: Optional[int] = Field(None, description="id страны города")
    time_end: Optional[int] = Field(None, description="id страны города")
    note: Optional[int] = Field(None, description="id страны города")
    celebration: Optional[CelebrationType] = Field(None, description="Точка заведения")
    table_id: Optional[int] = Field(None, description="id стола")


class Reservation(BaseReservation):
    id: int = Field(..., description="id бронирования")
    table: Table = Field(..., description="Информация о столе")