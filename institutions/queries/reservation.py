from typing import List

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import Reservation
from database.repository import AbstractRepository


class ReservationRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: Reservation):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, *args, **kwargs):
        new_reservation = self.db_model(amount_guests=kwargs.get("amount_guests"),
                                        date_reservation=kwargs.get("date_reservation"),
                                        time_start=kwargs.get("time_start"), 
                                        time_end=kwargs.get("time_end"),
                                        celebration=kwargs.get("celebration"), 
                                        note=kwargs.get("note"),
                                        user_id=kwargs.get("user_id"), 
                                        table_id=kwargs.get("table_id"))
        self.db_session.add(new_reservation)
        await self.db_session.flush()

    async def all(self) -> List[Reservation]:
        reservations = await self.db_session.execute(select(self.db_model))
        return reservations.scalars().all()

    async def get(self, id: int) -> Reservation:
        reservation = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return reservation.scalars().one_or_none()

    async def update(self, id: int, *args, **kwargs) -> Reservation:
        reservation = update(self.db_model).where(self.db_model.id == id)
        if kwargs.get("amount_guests"):
            reservation = reservation.values(amount_guests=kwargs["amount_guests"])
        if kwargs.get("date_reservation"):
            reservation = reservation.values(date_reservation=kwargs["date_reservation"])
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
        reservation.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(reservation)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        reservation = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        reservation.execution_options(synchronize_session="delete")
        deleted_reservation = await self.db_session.execute(reservation)
        return deleted_reservation.all()

    async def filter(self, *args, **kwargs) -> List[Reservation]:
        queries = []
        if kwargs.get("user_id"):
            queries.append(self.db_model.user_id == kwargs["user_id"]) # TODO возможно стоит делть проверку на тип данных которые я кладу в список
        reservations = await self.db_session.execute(select(self.db_model).where(*queries))
        return reservations.scalars().all()
