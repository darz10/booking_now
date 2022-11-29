from typing import List, Optional
from datetime import time, date

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import Reservation
from database.repository import AbstractRepository
from database.services import formation_fitlers_database
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
        reservation = reservation.values(**kwargs)
        return await self.db_connection.fetch_one(reservation)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        reservation = delete(self.db_model).where(
            self.db_model.id == id).returning(self.db_model.id)
        deleted_reservation = await self.db_connection.execute(reservation)
        return deleted_reservation

    async def filter(self, *args, **kwargs) -> List[Record]:
        formated_filters = formation_fitlers_database(self.db_model, *args)
        reservations = await self.db_connection.fetch_all(
            select(self.db_model).where(*formated_filters))
        return reservations
