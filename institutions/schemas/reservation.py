from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field

from institutions.enums import CelebrationType
from institutions.schemas import Table
from institutions.schemas.base_filter import BaseFilter


class BaseReservation(BaseModel):
    amount_guests: int = Field(..., description="Кол-во гостей")
    date_reservation: datetime = Field(..., description="Дата бронирования")
    time_start: time = Field(..., description="Время начала брони")
    time_end: time = Field(..., description="Время конца брони")
    note: int = Field(..., description="Заметка")
    celebration: Optional[CelebrationType] = Field(
        None,
        description="Праздник"
    )


class CreateReservation(BaseReservation):
    table_id: int = Field(..., description="id стола")


class UpdateReservation(BaseModel):
    amount_guests: Optional[int] = Field(None, description="Кол-во гостей")
    date_reservation: Optional[int] = Field(
        None,
        description="Дата бронирования"
    )
    time_start: Optional[int] = Field(None, description="Время начала брони")
    time_end: Optional[int] = Field(None, description="Время конца брони")
    note: Optional[int] = Field(None, description="Заметка")
    celebration: Optional[CelebrationType] = Field(
        None,
        description="Праздник"
    )
    table_id: Optional[int] = Field(None, description="id стола")


class Reservation(BaseReservation):
    id: int = Field(..., description="id бронирования")
    table: Table = Field(..., description="Информация о столе")


class ReservationFilter(BaseFilter):
    table_id__eq: Optional[int] = Field(
        None,
        description="Фильтр по номеру стола"
    )
    celebration__eq: Optional[CelebrationType] = Field(
        None,
        description="Фильтр по мероприятию"
    )
