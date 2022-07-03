from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import Country
from database.repository import AbstractRepository


class CountryRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: Country):
        self.db_session = db_session
        self.db_model = db_model

    async def all(self) -> List[Country]:
        countries = await self.db_session.execute(select(self.db_model))
        return countries.scalars().all()

    async def get(self, id: int) -> Country:
        country = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return country.scalars().one_or_none()