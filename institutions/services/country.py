from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import CountryRepository, CityRepository
from database.models import (
    Country as CountryModel,
    City as CityModel
)

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_countries(self) -> List[Record]:
    repository = CountryRepository(database, CountryModel)
    countries = await repository.all()
    return countries


async def getting_country(country_id: int) -> Record:
    repository = CountryRepository(database, CountryModel)
    country = await repository.get(id=country_id)
    if not country:
        raise NotFoundException(NOT_FOUND)
    return country


async def getting_cities_country(country_id: int) -> List[Record]:
    repository = CityRepository(database, CityModel)
    cities = await repository.get_cities_by_country(country_id)
    if not cities:
        raise NotFoundException(NOT_FOUND)
    return cities


async def filtering_countries(*args, **kwargs) -> List[Record]:
    # repository = CountryRepository(database, CountryModel)
    # country = await repository.filter(**kwargs)
    pass
