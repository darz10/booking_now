from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import CountryRepository
from database.models import (
    Country as CountryModel,
)

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_countries() -> List[Record]:
    repository = CountryRepository(database, CountryModel)
    countries = await repository.all()
    return countries


async def getting_country(country_id: int) -> Record:
    repository = CountryRepository(database, CountryModel)
    country = await repository.get(id=country_id)
    if not country:
        raise NotFoundException(NOT_FOUND)
    return country


async def filtering_countries(*args, **kwargs) -> List[Record]:
    repository = CountryRepository(database, CountryModel)
    countries = await repository.filter(*args, **kwargs)
    return countries
