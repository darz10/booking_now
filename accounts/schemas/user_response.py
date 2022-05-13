from pydantic import BaseModel, Field


class ResponseUser(BaseModel):
    status_code: int = Field(None, description="Статус ответа пользователю")
    description: str = Field(None, description="Описание ответа пользователю")