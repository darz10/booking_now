from pydantic import BaseModel, Field


class CustomResponse(BaseModel):
    status_code: int = Field(None, description="Статус ответа пользователю")
    description: str = Field(None, description="Описание ответа пользователю")
