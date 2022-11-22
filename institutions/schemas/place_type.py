from pydantic import BaseModel, Field


class PlaceType(BaseModel):
    id: int = Field(..., description="id типа места")
    title: str = Field(..., description="Название типа места")
