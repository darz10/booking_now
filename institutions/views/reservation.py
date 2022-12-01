
import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.services import get_current_user
from institutions.exceptions import NotFoundException
from institutions.messages import SUCCESSFULLY, NOT_FOUND
from institutions.schemas import (
    CreateReservation,
    UpdateReservation,
    ReservationFilter
)
from institutions.services import (
    filter_reservations,
    getting_reservation,
    updating_reservation,
    deleting_reservation,
    creating_reservation
)


tags = ["reservations"]

router = APIRouter()


@router.get(
    "/v1/reservations/",
    tags=tags,
    summary="Получение списка броней текущего пользователя"
)
async def get_list_reservations(
    request: Request,
    current_user: User = Depends(get_current_user),
    filters: ReservationFilter = Depends()
):
    """Получение списка броней"""
    try:
        if filters.has_objects:
            return await filter_reservations(
                filters,
                user_id=current_user.id,
            )
        return await filter_reservations(user_id=current_user.id)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_reservations: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/reservations/{reservation_id}",
    tags=tags,
    summary="Получение бронь"
)
async def get_reservation(
    request: Request,
    reservation_id: int,
    current_user: User = Depends(get_current_user)
):
    """Получение бронь"""
    try:
        return await getting_reservation(reservation_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise NotFoundException(detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_reservation: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/reservations/{reservation_id}",
    tags=tags,
    summary="Обновить бронь"
)
async def update_reservation(
    request: Request,
    reservation_id: int,
    reservation: UpdateReservation,
    current_user: User = Depends(get_current_user)
):  # TODO ограничить достпу к изменению состояния
    """Обновление брони"""
    try:
        return await updating_reservation(reservation_id, reservation)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint update_reservation: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/reservations/{reservation_id}",
    tags=tags,
    summary="Удалить бронь"
)
async def delete_reservation(
    request: Request,
    reservation_id: int,
    current_user: User = Depends(get_current_user)
):  # TODO ограничить достпу к изменению состояния
    """Удаление брони"""
    try:
        await deleting_reservation(reservation_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_reservation: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.post("/v1/reservations/", tags=tags, summary="Создать бронь")
async def create_reservation(
    request: Request,
    reservation: CreateReservation,
    current_user: User = Depends(get_current_user)
):  # TODO ограничить достпу к изменению состояния
    """Создать бронь"""
    try:
        return await creating_reservation(reservation)
    except Exception as exc:
        logging.exception(f"Error in endpoint create_reservation: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
