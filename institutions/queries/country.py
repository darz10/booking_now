from typing import List

from sqlalchemy.future import select
from databases import Database
from databases.backends.postgres import Record

from database.models import Country
from database.repository import AbstractRepositoryReadOnly


class CountryRepository(AbstractRepositoryReadOnly):
    def __init__(self, db_connection: Database, db_model: Country):
        self.db_connection = db_connection
        self.db_model = db_model

    async def all(self) -> List[Record]:
        countries = await self.db_connection.fetch_all(
            query=select(self.db_model)
        )
        return countries

    async def get(self, id: int) -> Record:
        country = await self.db_connection.fetch_one(
            query=select(self.db_model).where(self.db_model.id == id)
        )
        return country

    async def filter(self, *args, **kwargs):
        pass
