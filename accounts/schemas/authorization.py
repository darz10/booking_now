from typing import Optional
from pydantic import BaseModel, Field


class FirebaseToken(BaseModel):
    firebase_token: str = Field(..., description="Firebase токен")


class Token(BaseModel):
    auth_token: str = Field(..., description="Токен")
    type_token: str = Field(..., description="Тип токена")


class User(BaseModel):
    id: int = Field(..., description="id пользователя")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    phone_number: int = Field(..., description="Телефон пользователя")
    role_id: int = Field(..., description="Роль пользователя")
    email: Optional[str] = Field(..., description="Email пользователя")
    is_active: Optional[bool] = Field(..., description="Активность аккаунта")
