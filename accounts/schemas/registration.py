from typing import Optional
from pydantic import BaseModel, Field

from accounts.schemas import FirebaseToken


class CreateUser(FirebaseToken):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    email: Optional[str] = Field(None, description="Email пользователя")


class UpdatedUser(BaseModel):
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    email: Optional[str] = Field(None, description="Email")
    password: Optional[str] = Field(None, description="Пароль пользователя")
    phone_number: Optional[int] = Field(
        None,
        description="Телефон пользователя"
    )
