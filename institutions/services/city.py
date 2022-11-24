from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import CityRepository
from database.models import City as CityModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_cities() -> List[Record]:
    repository = CityRepository(database, CityModel)
    cities = await repository.all()
    return cities


async def getting_city(city_id: int) -> Record:
    repository = CityRepository(database, CityModel)
    city = await repository.get(id=city_id)
    if not city:
        raise NotFoundException(NOT_FOUND)
    return city


async def getting_cities_by_country(country_id: int) -> Record:
    repository = CityRepository(database, CityModel)
    cities = await repository.get_cities_by_country(country_id)
    return cities
