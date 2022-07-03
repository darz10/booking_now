from typing import List
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import Table
from database.repository import AbstractRepository


class TableRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: Table):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, *args, **kwargs) -> Table:
        new_table = self.db_model(is_favourite=kwargs.get("is_favourite"),
                                  table_number=kwargs.get("table_number"),
                                  max_people=kwargs.get("max_people"),
                                  is_electricity=kwargs.get("is_electricity"),
                                  floor=kwargs.get("floor"),
                                  is_available=kwargs.get("is_available"),
                                  place_branch_id=kwargs.get("place_branch_id"))
        self.db_session.add(new_table)
        await self.db_session.flush()

    async def all(self) -> List[Table]:
        tables = await self.db_session.execute(select(self.db_model))
        return tables.scalars().all()

    async def get(self, id: int) -> Table:
        table = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return table.scalars().one_or_none()

    async def update(self, id: int, *args, **kwargs) -> Table:
        table = update(self.db_model).where(self.db_model.id == id)
        if kwargs.get("is_favourite"):
            table = table.values(is_favourite=kwargs["is_favourite"])
        if kwargs.get("table_number"):
            table = table.values(table_number=kwargs["table_number"])
        if kwargs.get("max_people"):
            table = table.values(max_people=kwargs["max_people"])
        if kwargs.get("is_electricity"):
            table = table.values(is_electricity=kwargs["is_electricity"])
        if kwargs.get("floor"):
            table = table.values(floor=kwargs["floor"])
        if kwargs.get("is_available"):
            table = table.values(is_available=kwargs["is_available"])
        if kwargs.get("place_branch_id"):
            table = table.values(place_branch_id=kwargs["place_branch_id"])
        table.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(table)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        table = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        table.execution_options(synchronize_session="delete")
        deleted_table = await self.db_session.execute(table)
        return deleted_table.all()

    async def filter(self, *args, **kwargs) -> List[Table]:
        queries = []
        if kwargs.get("branch_id"):
            queries.append(self.db_model.place_branch_id == kwargs["branch_id"])
        tables = await self.db_session.execute(select(self.db_model).where(*queries))
        return tables.scalars().all()