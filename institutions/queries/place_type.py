from typing import List

from sqlalchemy.future import select
from databases.backends.postgres import Record

from databases import Database
from database.models import PlaceType
from database.repository import AbstractRepositoryReadOnly


class PlaceTypeRepository(AbstractRepositoryReadOnly):
    def __init__(self, db_connection: Database, db_model: PlaceType):
        self.db_connection = db_connection
        self.db_model = db_model

    async def all(self) -> List[Record]:
        place_types = await self.db_connection.fetch_all(select(self.db_model))
        return place_types

    async def get(self, id: int) -> Record:
        place_type = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return place_type
