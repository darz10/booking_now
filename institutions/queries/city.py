from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import City
from database.repository import AbstractRepository


class CityRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: City):
        self.db_session = db_session
        self.db_model = db_model

    async def all(self) -> List[City]:
        cities = await self.db_session.execute(select(self.db_model))
        return cities.scalars().all()

    async def get(self, id: int) -> City:
        city = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return city.scalars().one_or_none()

    async def get_cities_by_country(self, country_id: int):
        cities = await self.db_session.execute(select(self.db_model).where(self.db_model.country_id == country_id))
        return cities.scalars().all()