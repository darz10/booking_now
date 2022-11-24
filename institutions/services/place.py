from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import PlaceRepository
from database.models import Place as PlaceModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import UpdatePlace


async def getting_places() -> List[Record]:
    repository = PlaceRepository(database, PlaceModel)
    places = await repository.all()
    return places


async def getting_place(place_id: int) -> Record:
    repository = PlaceRepository(database, PlaceModel)
    place = await repository.get(id=place_id)
    if not place:
        raise NotFoundException(NOT_FOUND)
    return place


async def updating_place(place_id: int, place: UpdatePlace) -> Record:
    repository = PlaceRepository(database, PlaceModel)
    place_updated = await repository.update(
        id=place_id,
        title=place.title,
        description=place.description,
        url=place.url,
        avatar=place.avatar,
        email=place.email,
        phone=place.phone,
        place_type=place.place_type,
    )
    if not place_updated:
        raise NotFoundException(NOT_FOUND)
    return place_updated


async def deleting_place(place_id: int) -> None:
    repository = PlaceRepository(database, PlaceModel)
    place = await repository.delete(id=place_id)
    if not place:
        raise NotFoundException(NOT_FOUND)


async def filter_places(*args, **kwargs) -> List[Record]:
    repository = PlaceRepository(database, PlaceModel)
    places = await repository.filter(*args, **kwargs)
    return places
