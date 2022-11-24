from typing import List, Optional

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import Table
from database.repository import AbstractRepository


class TableRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: Table):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, table_number: int, max_people: int,
                     floor: int, place_branch_id: int,
                     is_favourite: Optional[bool] = None,
                     is_electricity: Optional[bool] = None,
                     is_available: Optional[bool] = None) -> Record:
        new_table = insert(self.db_model).values(
            is_favourite=is_favourite,
            table_number=table_number,
            max_people=max_people,
            is_electricity=is_electricity,
            floor=floor,
            is_available=is_available,
            place_branch_id=place_branch_id
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_table)

    async def all(self) -> List[Record]:
        tables = await self.db_connection.fetch_all(select(self.db_model))
        return tables

    async def get(self, id: int) -> Record:
        table = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return table

    async def update(self, id: int, *args, **kwargs) -> Record:
        table = update(self.db_model).\
                where(self.db_model.id == id).\
                returning(self.db_model)
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
        return await self.db_connection.fetch_one(table)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        table = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        deleted_table = await self.db_connection.execute(table)
        return deleted_table

    async def filter(self, *args, **kwargs) -> List[Record]:
        queries = []
        if kwargs.get("branch_id"):
            queries.append(
                self.db_model.place_branch_id == kwargs["branch_id"]
            )
        tables = await self.db_connection.fetch_all(
            select(self.db_model).where(*queries)
        )
        return tables
