from typing import List
from database.db import async_session
from institutions.queries import ReservationRepository
from database.models import Reservation as ReservationModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    UpdateReservation,
    CreateReservation,
)


async def getting_reservations() -> List[ReservationModel]:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                reservations = await model.all()
    return reservations


async def getting_reservation(reservation_id: int) -> ReservationModel:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                reservation = await model.get(reservation_id)
    if not reservation:
        raise NotFoundException(NOT_FOUND)
    return reservation


async def updating_reservation(reservation_id: int, reservation: UpdateReservation) -> ReservationModel:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                reservation_updated = await model.update(id=reservation_id,
                                                         amount_guests=reservation.amount_guests,
                                                         date_reservation=reservation.date_reservation,
                                                         time_start=reservation.time_start,
                                                         time_end=reservation.time_end,
                                                         celebration=reservation.celebration,
                                                         note=reservation.note,
                                                         user_id=reservation.user_id,
                                                         table_id=reservation.table_id)                           
    if not reservation_updated:
        raise NotFoundException(NOT_FOUND)
    return reservation_updated


async def deleting_reservation(reservation_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                reservation = await model.delete(id=reservation_id)
    if not reservation:
        raise NotFoundException(NOT_FOUND)


async def creating_reservation(reservation: CreateReservation) -> ReservationModel:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                new_reservation = await model.create(amount_guests=reservation.amount_guests,
                                                     date_reservation=reservation.date_reservation,
                                                     time_start=reservation.time_start,
                                                     time_end=reservation.time_end,
                                                     celebration=reservation.celebration,
                                                     note=reservation.note,
                                                     user_id=reservation.user_id,
                                                     table_id=reservation.table_id)
    return new_reservation


async def filter_reservations(*args, **kwargs) -> List[ReservationModel]:
    async with async_session() as session:
            async with session.begin():
                model = ReservationRepository(session, ReservationModel)
                reservations = await model.filter(*args, **kwargs)
    return reservations