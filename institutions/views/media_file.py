from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.views import get_current_user
from institutions.exceptions import NotFoundException
from institutions.schemas import CreateMediaFile, UpdateMediaFile
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.services import (
    getting_media_file, 
    getting_media_files, 
    updating_media_file, 
    deleting_media_file,
    creating_media_file
)


tags = ["media_files"]

router = APIRouter()


@router.get("/v1/media_files/", tags=tags, summary="Получение списка файлов")
async def get_list_media_files(request: Request):
    """Получение списока файлов"""
    try:
        return await getting_media_files()
    except Exception as exc:
        print("Error in endpoint get_list_media_files", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")
        

@router.get("/v1/media_files/{media_file_id}", tags=tags, summary="Получение файла")
async def get_media_file(request: Request, media_file_id: int):
    """Получение файла"""
    try:
        return await getting_media_file(media_file_id)
    except NotFoundException:
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint get_media_file", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.put("/v1/media_files/{media_file_id}", tags=tags, summary="Обновить файл")
async def update_media_file(request: Request, media_file_id: int, 
                            media_file: UpdateMediaFile, current_user: User = Depends(get_current_user)): # TODO ограничить достпу к изменению состояния
    """Обновление файла"""
    try:
        return await updating_media_file(media_file_id, media_file)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint update_media_file", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete("/v1/media_files/{media_file_id}", tags=tags, summary="Удалить файл")
async def delete_media_file(request: Request, media_file_id: int, 
                            current_user: User = Depends(get_current_user)): # TODO ограничить достпу к изменению состояния
    """Удаление файла"""
    try:
        await deleting_media_file(media_file_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint delete_media_file", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post("/v1/media_files/", tags=tags, summary="Создать файл")
async def create_media_file(request: Request, media_file: CreateMediaFile, 
                            current_user: User = Depends(get_current_user)): # TODO ограничить достпу к изменению состояния
    """Создать файл"""
    try:
        return await creating_media_file(media_file)
    except Exception as exc:
        print("Error in endpoint create_media_file", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")
