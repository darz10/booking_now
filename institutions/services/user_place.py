from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import UserPlaceRepository
from database.models import UserPlace as UserPlaceModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    UserPlace,
    UpdateUserPlace,
)


async def getting_user_places() -> List[Record]:
    repository = UserPlaceRepository(database, UserPlaceModel)
    user_places = await repository.all()
    return user_places


async def getting_user_place(user_place_id: int) -> Record:
    repository = UserPlaceRepository(database, UserPlaceModel)
    user_place = await repository.get(user_place_id)
    if not user_place:
        raise NotFoundException(NOT_FOUND)
    return user_place


async def updating_user_place(
    user_place_id: int,
    user_place: UpdateUserPlace
) -> Record:
    repository = UserPlaceRepository(database, UserPlaceModel)
    user_place_updated = await repository.update(
        id=user_place_id,
        user_id=user_place.user_id,
        place_branch_id=user_place.place_branch_id,
        is_favourite=user_place.is_favourite
    )
    if not user_place_updated:
        raise NotFoundException(NOT_FOUND)
    return user_place_updated


async def deleting_user_place(user_place_id: int) -> None:
    repository = UserPlaceRepository(database, UserPlaceModel)
    user_place = await repository.delete(id=user_place_id)
    if not user_place:
        raise NotFoundException(NOT_FOUND)


async def creating_user_place(user_place: UserPlace) -> Record:
    repository = UserPlaceRepository(database, UserPlaceModel)
    new_user_place = await repository.create(
        user_id=user_place.user_id,
        place_branch_id=user_place.place_branch_id,
        is_favourite=user_place.is_favourite
    )
    return new_user_place
