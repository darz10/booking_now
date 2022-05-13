import datetime
from typing import Optional
from passlib.context import CryptContext
import random
import string

from jose import jwt, JWTError
from settings import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    """
    Создание хэша пароля
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Проверка пароля
    """
    return password_context.verify(plain_password, hashed_password)


def generate_random_password():
    """
    Создание случайного пароля
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


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
