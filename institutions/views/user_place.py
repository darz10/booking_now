import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.services import get_current_user
from institutions.exceptions import NotFoundException
from institutions.schemas import UpdateUserPlace, UserPlace
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.services import (
    getting_user_places,
    getting_user_place,
    updating_user_place,
    deleting_user_place,
    creating_user_place
)


tags = ["user_places"]

router = APIRouter()


@router.get(
    "/v1/user_places/",
    tags=tags,
    summary="Получение списка связей пользователь-место"
)
async def get_list_user_places(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Получение список связей пользователь-место"""
    try:
        return await getting_user_places()
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_user_places: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/user_places/{user_place_id}",
    tags=tags,
    summary="Получение связь пользователь-место"
)
async def get_user_place(
    request: Request,
    user_place_id: int,
    current_user: User = Depends(get_current_user)
):
    """Получение связи пользователь-место"""
    try:
        return await getting_user_place(user_place_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_user_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/user_places/{user_place_id}",
    tags=tags,
    summary="Обновить связь пользователь-место"
)
async def update_user_place(
    request: Request,
    user_place_id: int,
    user_place: UpdateUserPlace,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Обновление связи пользователь-место"""
    try:
        return await updating_user_place(user_place_id, user_place)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint update_user_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/user_places/{user_place_id}",
    tags=tags,
    summary="Удалить связь пользователь-место"
)
async def delete_user_place(
    request: Request,
    user_place_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Удаление связи пользователь-место"""
    try:
        await deleting_user_place(user_place_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_user_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post(
    "/v1/user_places/",
    tags=tags,
    summary="Создать связь пользователь-место"
)
async def create_user_place(
    request: Request,
    user_place: UserPlace,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Создать связь пользователь-место"""
    try:
        return await creating_user_place(user_place)
    except Exception as exc:
        logging.exception(f"Error in endpoint create_user_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
