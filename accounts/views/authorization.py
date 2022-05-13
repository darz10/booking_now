from fastapi import APIRouter, Request, HTTPException, Response
import datetime

from accounts.integrations.firebase import FirebaseManager
from accounts.schemas import FirebaseToken, Token, User
from accounts.services import create_token
from settings import settings
from accounts.messages import USER_NO_EXISTS


router = APIRouter()

tags = ["accounts"]


@router.post("/v1/authorization", tags=tags, responses={200: {"model": Token}})
async def authorization_user(
    request: Request, response: Response, firebase_token: FirebaseToken
):
    """Авторизация пользователя с помощью firebase_token"""
    try:
        # token = firebase_token.firebase_token
        # phone = FirebaseManager.get_phone_by_token(token)
        phone = "79025854917"
        user = await request.app.db.get_user(phone)
        schema_user = get_user(user)
        return await login(schema_user, response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


def get_user(user) -> User:
    """
    Метод для получения данных пользователя в схеме User
    """
    if user:
        return User(**user)


async def login(user, response):
    if not user:
        raise HTTPException(
            status_code=401,
            detail=USER_NO_EXISTS,
        )
    access_token_expires = datetime.timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )
    access_token = create_token(
        data={"sub": user.phone_number, "user_id": user.id},
        expires_delta=access_token_expires,
        secret_key=settings.SECRET_KEY,
    )
    resp = Token(auth_token=access_token, type_token="bearer")
    response.headers["authorization"] = "Bearer " + access_token
    return resp
