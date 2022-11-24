from typing import List, Optional
from datetime import time, date

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import Reservation
from database.repository import AbstractRepository
from institutions.enums import CelebrationType


class ReservationRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: Reservation):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(
        self,
        amount_guests: int,
        user_id: int,
        table_id: int,
        date_reservation: date,
        time_start: time,
        time_end: time,
        celebration: Optional[CelebrationType] = None,
        note: Optional[str] = None
    ) -> Record:
        new_reservation = insert(self.db_model).values(
            amount_guests=amount_guests,
            date_reservation=date_reservation,
            time_start=time_start,
            time_end=time_end,
            celebration=celebration,
            note=note,
            user_id=user_id,
            table_id=table_id
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_reservation)

    async def all(self) -> List[Record]:
        reservations = await self.db_connection.fetch_all(
                select(self.db_model)
        )
        return reservations

    async def get(self, id: int) -> Record:
        reservation = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return reservation

    async def update(self, id: int, *args, **kwargs) -> Record:
        reservation = update(self.db_model).\
                      where(self.db_model.id == id).\
                      returning(self.db_model)
        if kwargs.get("amount_guests"):
            reservation = reservation.values(
                amount_guests=kwargs["amount_guests"]
            )
        if kwargs.get("date_reservation"):
            reservation = reservation.values(
                date_reservation=kwargs["date_reservation"]
            )
        if kwargs.get("time_start"):
            reservation = reservation.values(time_start=kwargs["time_start"])
        if kwargs.get("time_end"):
            reservation = reservation.values(time_end=kwargs["time_end"])
        if kwargs.get("celebration"):
            reservation = reservation.values(celebration=kwargs["celebration"])
        if kwargs.get("note"):
            reservation = reservation.values(note=kwargs["note"])
        if kwargs.get("user_id"):
            reservation = reservation.values(user_id=kwargs["user_id"])
        if kwargs.get("table_id"):
            reservation = reservation.values(table_id=kwargs["table_id"])
        return await self.db_connection.fetch_one(reservation)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        reservation = delete(self.db_model).where(
            self.db_model.id == id).returning(self.db_model.id)
        deleted_reservation = await self.db_connection.execute(reservation)
        return deleted_reservation

    async def filter(self, *args, **kwargs) -> List[Record]:
        queries = []
        if kwargs.get("user_id"):
            queries.append(self.db_model.user_id == kwargs["user_id"])  # TODO возможно стоит делть проверку на тип данных которые я кладу в список
        if kwargs.get("is_active"):
            queries.append(self.db_model.is_active == kwargs["is_active"])
        if kwargs.get("table_id"):
            queries.append(self.db_model.table_id == kwargs["table_id"])
        reservations = await self.db_connection.fetch_all(
                select(self.db_model).where(*queries)
            )
        return reservations
