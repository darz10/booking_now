
import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.services import get_current_user
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceAddress, UpdatePlaceAddress
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.services import (
    getting_addresses,
    getting_address,
    creating_address,
    updating_address,
    deleting_address
)


tags = ["address"]

router = APIRouter()


@router.get(
    "/v1/addresses/",
    tags=tags,
    summary="Получение списка адресов"
)
async def get_list_addresses(request: Request):
    """Получение списка адресов"""
    try:
        return await getting_addresses()
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_addresses: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/addresses/{address_id}",
    tags=tags,
    summary="Получение адреса"
)
async def get_address(
    request: Request, address_id: int
):
    """Получение адреса"""
    try:
        return await getting_address(address_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_addresses: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/addresses/{address_id}",
    tags=tags,
    summary="Обновить адрес"
)
async def update_address(
    request: Request,
    address_id: int,
    address: UpdatePlaceAddress,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу к
                                                    # изменению состояния
):
    """Обновление адреса"""
    try:
        return await updating_address(address_id, address)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint update_address: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/addresses/{address_id}",
    tags=tags,
    summary="Удалить адрес"
)
async def delete_address(
    request: Request,
    address_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу к
                                                    # изменению состояния
):
    """Удаление точки компании"""
    try:
        await deleting_address(address_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_address: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post(
    "/v1/addresses/",
    tags=tags,
    summary="Создать адрес"
)
async def create_address(
    request: Request,
    address: CreatePlaceAddress,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу к
                                                    # изменению состояния
):
    """Создать адрес"""
    try:
        return await creating_address(address)
    except Exception as exc:
        logging.exception(f"Error in endpoint create_address: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
