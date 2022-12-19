from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import PlaceRepository
from database.models import Place as PlaceModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import UpdatePlace, Place
from accounts.schemas import User


async def getting_places() -> List[Record]:
    repository = PlaceRepository(database, PlaceModel)
    places = await repository.all()
    return places


async def creating_place(
    reservation: Place,
    user: User
) -> Record:
    repository = PlaceRepository(database, PlaceModel)
    created_data = reservation.dict()
    new_place = await repository.create(
        **created_data
    )
    return new_place


async def getting_place(place_id: int) -> Record:
    repository = PlaceRepository(database, PlaceModel)
    place = await repository.get(id=place_id)
    if not place:
        raise NotFoundException(NOT_FOUND)
    return place


async def updating_place(place_id: int, place: UpdatePlace) -> Record:
    repository = PlaceRepository(database, PlaceModel)
    updated_data = place.dict(exclude_unset=True)
    place_updated = await repository.update(
        id=place_id,
        **updated_data
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
