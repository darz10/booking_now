from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from institutions.schemas import PlaceAddress, PlaceDB


class CreatePlaceBranch(BaseModel):
    place_id: int = Field(..., description="id места")
    place_address_id: int = Field(..., description="id адреса места")
    created_at: datetime = Field(datetime.now(), description="Время создания")


class PlaceBranch(BaseModel):
    id: int = Field(..., description="id точки места")
    place: PlaceDB = Field(..., description="Место к которой привязана точка")
    place_address: PlaceAddress = Field(..., description="Адрес места точки")


class UpdatePlaceBranch(BaseModel):
    place_id: Optional[int] = Field(
        None,
        description="id места"
    )
    place_address_id: Optional[int] = Field(
        None,
        description="id адреса места"
    )
