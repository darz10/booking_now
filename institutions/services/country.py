from typing import List
from database.db import async_session
from institutions.queries import CountryRepository
from database.models import Country as CountryModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_countries() -> List[CountryModel]:
    async with async_session() as session:
            async with session.begin():
                model = CountryRepository(session, CountryModel)
                countries = await model.all()
    return countries


async def getting_country(country_id: int) -> CountryModel:
    async with async_session() as session:
            async with session.begin():
                model = CountryRepository(session, CountryModel)
                country = await model.get(id=country_id)
    if not country:
        raise NotFoundException(NOT_FOUND)
    return country
