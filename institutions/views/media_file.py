import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.services import get_current_user
from institutions.exceptions import NotFoundException
from institutions.schemas import CreateMediaFile, UpdateMediaFile
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.services import (
    getting_media_files,
    getting_media_file,
    updating_media_file,
    deleting_media_file,
    creating_media_file
)


tags = ["media_files"]

router = APIRouter()


@router.get(
    "/v1/media_files/",
    tags=tags,
    summary="Получение списка файлов"
)
async def get_list_media_files(request: Request):
    """Получение списока файлов"""
    try:
        return await getting_media_files()
    except Exception as exc:
        logging.exception(f"Error in method get_list_media_files: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/media_files/{media_file_id}",
    tags=tags,
    summary="Получение файла"
)
async def get_media_file(request: Request, media_file_id: int):
    """Получение файла"""
    try:
        return await getting_media_file(media_file_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method get_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/media_files/{media_file_id}",
    tags=tags,
    summary="Обновить файл"
)
async def update_media_file(
    request: Request,
    media_file_id: int,
    media_file: UpdateMediaFile,
    current_user: User = Depends(get_current_user)  # TODO огр достпу
                                                    # к изменению состояния
):
    """Обновление файла"""
    try:
        return await updating_media_file(media_file_id, media_file)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method update_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/media_files/{media_file_id}",
    tags=tags,
    summary="Удалить файл"
)
async def delete_media_file(
    request: Request,
    media_file_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Удаление файла"""
    try:
        await deleting_media_file(media_file_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method delete_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post("/v1/media_files/", tags=tags, summary="Создать файл")
async def create_media_file(
    request: Request,
    media_file: CreateMediaFile,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Создать файл"""
    try:
        return await creating_media_file(media_file)
    except Exception as exc:
        logging.exception(f"Error in method create_media_file: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
