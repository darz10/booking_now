from typing import List

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import PlaceBranch
from database.repository import AbstractRepository


class PlaceBranchRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: PlaceBranch):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, place_id: int, place_address_id: int) -> Record:
        """Создание точки заведения"""
        new_place_branch = insert(self.db_model).values(
            place_id=place_id,
            place_address_id=place_address_id
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_place_branch)

    async def all(self) -> List[Record]:
        branches = await self.db_connection.fetch_all(select(self.db_model))
        return branches

    async def get(self, id: int) -> Record:
        branch = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return branch

    async def update(self, id: int, *args, **kwargs) -> Record:
        branch = update(self.db_model).\
                 where(self.db_model.id == id).\
                 returning(self.db_model)
        if kwargs.get("place_id"):
            branch = branch.values(place_id=kwargs["place_id"])
        if kwargs.get("place_address_id"):
            branch = branch.values(place_address_id=kwargs["place_address_id"])
        return await self.db_connection.fetch_one(branch)

    async def delete(self, id: int) -> None:
        """Удаление точки места с возвратом статуса, True(объект удалён)"""
        branch = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        deleted_branch = await self.db_connection.execute(branch)
        return deleted_branch

    async def filter(self, *args, **kwargs) -> List[Record]:
        queries = []
        if kwargs.get("place_id"):
            queries.append(self.db_model.place_type == kwargs["place_type"])
        places = await self.db_connection.fetch_all(
            select(self.db_model).where(*queries)
        )
        return places
