import datetime
from typing import Optional
from fastapi import HTTPException
from jose import jwt
from accounts.integrations.firebase import FirebaseManager

from database.db import database
from accounts.schemas.registration import CreateUser
from accounts.utils import get_password_hash, generate_random_password
from settings import settings
from accounts.schemas import User, Token
from accounts.messages import USER_NO_EXISTS
from accounts.queries import UserRepository
from database.models import User as UserModel


def create_token(
    data: dict,
    secret_key: str,
    expires_delta: Optional[datetime.timedelta] = None,
):
    """
    Создание jwt токена пользователя
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_user(user) -> User:
    """
    Метод для получения данных пользователя в схеме User
    """
    if user:
        return User(**user)


async def login(user, response) -> Token:
    if not user:
        raise HTTPException(
            status_code=401,
            detail=USER_NO_EXISTS,
        )
    access_token_expires = datetime.timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )
    access_token = create_token(
        data={"phone": user.phone_number, "user_id": user.id},
        expires_delta=access_token_expires,
        secret_key=settings.SECRET_KEY,
    )
    resp = Token(auth_token=access_token, type_token="bearer")
    response.headers["authorization"] = "Bearer " + access_token
    return resp


async def getting_user_by_phone(phone: str) -> UserModel:
    """Получение данных пользователя по номеру телефона"""
    user_model = UserRepository(database, UserModel)
    user = await user_model.get_user_by_phone(phone)
    return user


async def creating_user(user: CreateUser) -> UserModel:
    """Создание нового пользователя"""
    user_model = UserRepository(database, UserModel)
    phone = FirebaseManager.get_phone_by_token(user.firebase_token)
    new_user = await user_model.create(
        first_name=user.first_name,
        last_name=user.last_name,
        password=get_password_hash(generate_random_password()),
        phone_number=phone,
        email=user.email
    )
    return new_user


async def updating_user(id: int, user: CreateUser) -> UserModel:
    """Обновление пользователя"""
    user_model = UserRepository(database, UserModel)
    user_updated = await user_model.update(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        phone_number=user.phone_number,
        email=user.email
    )
    return user_updated
