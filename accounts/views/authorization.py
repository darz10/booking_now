from fastapi import APIRouter, Request, HTTPException, Response

from accounts.integrations.firebase import FirebaseManager
from accounts.schemas import FirebaseToken, Token
from accounts.services import login, getting_user_by_phone

tags = ["accounts"]

router = APIRouter()


@router.post("/v1/authorization", tags=tags, responses={200: {"model": Token}})
async def authorization_user(
    request: Request, response: Response, firebase_token: FirebaseToken
):
    """Авторизация пользователя с помощью firebase_token"""
    try:
        token = firebase_token.firebase_token
        phone = FirebaseManager.get_phone_by_token(token)
        user = await getting_user_by_phone(phone)
        return await login(user, response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

