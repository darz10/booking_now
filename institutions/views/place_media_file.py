import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.views import get_current_user
from institutions.exceptions import NotFoundException
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.schemas import CreatePlaceMediaFile
from institutions.services import (
    deleting_place_media_file,
    creating_place_media_file
)


tags = ["place_media_file"]

router = APIRouter()


@router.delete("/v1/place_media_files/{place_media_file_id}", tags=tags, summary="Удалить связь место-файл")
async def delete_place_media_file(
    request: Request, place_media_file_id: int, current_user: User = Depends(get_current_user) # TODO ограничить достпу к изменению состояния
):
    """Удаление связи пользователь-место"""
    try:
        await deleting_place_media_file(place_media_file_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_place_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post("/v1/place_media_files/", tags=tags, summary="Создать связь место-файл")
async def create_place_media_file(
    request: Request, place_media_file: CreatePlaceMediaFile, current_user: User = Depends(get_current_user) # TODO ограничить достпу к изменению состояния
):
    """Создать связь пользователь-место"""
    try:
        return await creating_place_media_file(place_media_file)
    except Exception as exc:
        logging.exception(f"Error in endpoint create_place_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")