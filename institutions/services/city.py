from typing import List
from database.db import async_session
from institutions.queries import CityRepository
from database.models import City as CityModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_cities() -> List[CityModel]:
    async with async_session() as session:
            async with session.begin():
                model = CityRepository(session, CityModel)
                cities = await model.all()
    return cities


async def getting_city(city_id: int) -> CityModel:
    async with async_session() as session:
            async with session.begin():
                model = CityRepository(session, CityModel)
                city = await model.get(id=city_id)
    if not city:
        raise NotFoundException(NOT_FOUND)
    return city


async def getting_cities_by_country(country_id: int) -> CityModel:
    async with async_session() as session:
            async with session.begin():
                model = CityRepository(session, CityModel)
                cities = await model.get_cities_by_country(country_id)
    return cities
