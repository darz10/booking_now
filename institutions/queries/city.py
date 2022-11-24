from typing import List

from sqlalchemy.future import select
from databases.backends.postgres import Record

from databases import Database
from database.models import City
from database.repository import AbstractRepositoryReadOnly


class CityRepository(AbstractRepositoryReadOnly):
    def __init__(self, db_connection: Database, db_model: City):
        self.db_connection = db_connection
        self.db_model = db_model

    async def all(self) -> List[Record]:
        cities = await self.db_connection.fetch_all(select(self.db_model))
        return cities

    async def get(self, id: int) -> Record:
        city = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return city

    async def get_cities_by_country(self, country_id: int) -> List[Record]:
        cities = await self.db_connection.fetch_all(
            select(self.db_model).where(self.db_model.country_id == country_id)
        )
        return cities
