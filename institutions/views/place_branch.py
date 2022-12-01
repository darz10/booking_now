import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.services import get_current_user
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceBranch, UpdatePlaceBranch
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.services import (
    getting_branches,
    getting_branch,
    updating_branch,
    deleting_branch,
    creating_branch,
    get_tables_by_branch_id
)


tags = ["place_branches"]

router = APIRouter()


@router.get(
    "/v1/place_branches/",
    tags=tags,
    summary="Получение списка точек компаний"
)
async def get_list_branches(
    request: Request
):
    """Получение список точкек компаний"""
    try:
        return await getting_branches()
    except Exception as exc:
        logging.exception(f"Error in method get_list_branches: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/place_branches/{branch_id}",
    tags=tags,
    summary="Получение точки компании"
)
async def get_branch(
    request: Request, branch_id: int
):
    """Получение точки компании"""
    try:
        return await getting_branch(branch_id)
    except NotFoundException as exc:
        logging.exception(f"Error in method get_list_media_files: {exc}")
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method get_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/place_branches/{branch_id}",
    tags=tags,
    summary="Обновить точку компании"
)
async def update_branch(
    request: Request,
    branch_id: int,
    branch: UpdatePlaceBranch,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Обновление точки компании"""
    try:
        return await updating_branch(branch_id, branch)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method update_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/place_branches/{branch_id}",
    tags=tags,
    summary="Удалить точку компании"
)
async def delete_branch(
    request: Request,
    branch_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Удаление точки компании"""
    try:
        await deleting_branch(branch_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method delete_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post(
    "/v1/place_branches/",
    tags=tags,
    summary="Создать точку компании"
)
async def create_branch(
    request: Request,
    branch: CreatePlaceBranch,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Создать точку компании"""
    try:
        return await creating_branch(branch)
    except Exception as exc:
        logging.exception(f"Error in method create_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
        "/v1/place_branches/{branch_id}/tables",
        tags=tags,
        summary="Получение списка столов точки компании"
)
async def get_list_tables_branch(request: Request, branch_id: int):
    """Получение списка столов точки компании"""
    try:
        if await getting_branch(branch_id):
            return await get_tables_by_branch_id(branch_id)
        else:
            raise NotFoundException(NOT_FOUND)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method get_list_tables_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


# @router.get(
#     "/v1/place_branches/{place_branch_id}/favorite/{favorite_status}",
#     tags=tags,
#     responses={200: {"model": PlaceBranch}}
# )
# async def set_user_to_place_branch(
#     request: Request,
#     place_branch_id: int,
#     favorite_status: bool = False,
#     current_user: User = Depends(get_current_user),
# ):
#     """Создание связи пользователь-место"""
#     pass
