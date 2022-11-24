from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import ReservationRepository
from database.models import Reservation as ReservationModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    UpdateReservation,
    CreateReservation,
)


async def getting_reservations() -> List[Record]:
    repository = ReservationRepository(database, ReservationModel)
    reservations = await repository.all()
    return reservations


async def getting_reservation(reservation_id: int) -> Record:
    repository = ReservationRepository(database, ReservationModel)
    reservation = await repository.get(reservation_id)
    if not reservation:
        raise NotFoundException(NOT_FOUND)
    return reservation


async def updating_reservation(
    reservation_id: int,
    reservation: UpdateReservation
) -> Record:
    repository = ReservationRepository(database, ReservationModel)
    reservation_updated = await repository.update(
        id=reservation_id,
        amount_guests=reservation.amount_guests,
        date_reservation=reservation.date_reservation,
        time_start=reservation.time_start,
        time_end=reservation.time_end,
        celebration=reservation.celebration,
        note=reservation.note,
        user_id=reservation.user_id,
        table_id=reservation.table_id
    )
    if not reservation_updated:
        raise NotFoundException(NOT_FOUND)
    return reservation_updated


async def deleting_reservation(reservation_id: int) -> None:
    repository = ReservationRepository(database, ReservationModel)
    reservation = await repository.delete(id=reservation_id)
    if not reservation:
        raise NotFoundException(NOT_FOUND)


async def creating_reservation(
    reservation: CreateReservation
) -> Record:
    repository = ReservationRepository(database, ReservationModel)
    new_reservation = await repository.create(
        amount_guests=reservation.amount_guests,
        date_reservation=reservation.date_reservation,
        time_start=reservation.time_start,
        time_end=reservation.time_end,
        celebration=reservation.celebration,
        note=reservation.note,
        user_id=reservation.user_id,
        table_id=reservation.table_id
    )
    return new_reservation


async def filter_reservations(*args, **kwargs) -> List[Record]:
    repository = ReservationRepository(database, ReservationModel)
    reservations = await repository.filter(*args, **kwargs)
    return reservations


async def getting_active_reservations_by_table(table_id: int) -> List[Record]:
    repository = ReservationRepository(database, ReservationModel)
    reservations = await repository.filter(is_active=True, table_id=table_id)
    return reservations
