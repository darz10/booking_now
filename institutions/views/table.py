
import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.views import get_current_user
from institutions.exceptions import NotFoundException
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.schemas import BaseTable, UpdateTable
from institutions.services import (
    getting_tables,
    getting_table,
    updating_table,
    deleting_table,
    creating_table,
    getting_active_reservations_by_table
)


tags = ["tables"]

router = APIRouter()


@router.get(
    "/v1/tables/",
    tags=tags,
    summary="Получение списка столов"
)
async def get_list_tables(request: Request):
    """Получение списка столов"""
    try:
        return await getting_tables()
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_tables: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/tables/{table_id}",
    tags=tags,
    summary="Получение стола"
)
async def get_table(request: Request, table_id: int):
    """Получение стола"""
    try:
        return await getting_table(table_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_table: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/tables/{table_id}",
    tags=tags,
    summary="Обновить стол"
)
async def update_table(
    request: Request,
    table_id: int,
    table: UpdateTable,
    current_user: User = Depends(get_current_user)  # TODO ограничить доступ
                                                    # к изменению состояния
):
    """Обновление стола"""
    try:
        return await updating_table(table_id, table)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint update_table: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete("/v1/tables/{table_id}", tags=tags, summary="Удалить стол")
async def delete_table(
    request: Request,
    table_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Удаление стола"""
    try:
        await deleting_table(table_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_table: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post("/v1/tables/", tags=tags, summary="Создать стол")
async def create_table(
    request: Request,
    table: BaseTable,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Создать стол"""
    try:
        return await creating_table(table)
    except Exception as exc:
        logging.exception(f"Error in endpoint create_table: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/tables/{table_id}/reservations",
    tags=tags,
    summary="Получение списка резерваций стола"
            " активных на текущий момент"
)
async def get_list_reservations_by_table(request: Request, table_id: int):
    """Получение список точкек компаний"""
    try:
        if await getting_table(table_id):
            return await getting_active_reservations_by_table(table_id)
        else:
            raise NotFoundException(NOT_FOUND)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_tables_branch: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")