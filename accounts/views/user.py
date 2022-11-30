from fastapi import APIRouter, Request, Depends, HTTPException
import logging

from accounts.schemas import CreateUser, UpdatedUser, User
from accounts.services import (
    creating_user,
    updating_user,
    get_current_user
)

tags = ["accounts"]

router = APIRouter()


@router.post("/v1/create-user", tags=tags)
async def add_new_user(request: Request, user: CreateUser):
    """Создание нового пользователя"""
    try:
        return await creating_user(user)
    except Exception as e:
        logging.exception(f"{e}")
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post(
    "/v1/update-user", tags=tags
)
async def update_user(
    request: Request,
    user: UpdatedUser,
    current_user: User = Depends(get_current_user),
):
    """Изменение информации о пользователе"""
    try:
        return await updating_user(current_user.id, user)
    except Exception as e:
        logging.exception(f"{e}")
        print("Ошибка метода update_user", e)  # TODO логирование
        raise HTTPException(status_code=400, detail=f"{e}")
