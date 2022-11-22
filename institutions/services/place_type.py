from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import PlaceTypeRepository
from database.models import PlaceType as PlaceTypeModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException


async def getting_place_types() -> List[Record]:
    repository = PlaceTypeRepository(database, PlaceTypeModel)
    place_types = await repository.all()
    return place_types


async def getting_place_type(place_type_id: int) -> Record:
    repository = PlaceTypeRepository(database, PlaceTypeModel)
    place_type = await repository.get(id=place_type_id)
    if not place_type:
        raise NotFoundException(NOT_FOUND)
    return place_type
