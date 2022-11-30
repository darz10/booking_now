import datetime
from typing import Optional

from jose import jwt

from settings import settings


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