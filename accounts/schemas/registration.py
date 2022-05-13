from typing import Optional
from pydantic import BaseModel, Field

from accounts.schemas import FirebaseToken


class CreateUser(FirebaseToken):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    phone_number: int = Field(..., description="Телефон пользователя")
    email: Optional[str] = Field(..., description="Email пользователя")


class UpdatedUser(BaseModel):
    user_id: int = Field(None, description="Id пользователя")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    second_name: Optional[str] = Field(
        None, description="Фамилия пользователя"
    )
    email: Optional[str] = Field(None, description="Email")
    password: Optional[str] = Field(None, description="Пароль пользователя")
