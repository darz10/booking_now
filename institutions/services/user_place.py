from typing import List
from database.db import async_session
from institutions.queries import UserPlaceRepository
from database.models import UserPlace as UserPlaceModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    UserPlace,
    UpdateUserPlace,
)


async def getting_user_places() -> List[UserPlaceModel]:
    async with async_session() as session:
            async with session.begin():
                model = UserPlaceRepository(session, UserPlaceModel)
                user_places = await model.all()
    return user_places


async def getting_user_place(user_place_id: int) -> UserPlaceModel:
    async with async_session() as session:
            async with session.begin():
                model = UserPlaceRepository(session, UserPlaceModel)
                user_place = await model.get(user_place_id)
    if not user_place:
        raise NotFoundException(NOT_FOUND)
    return user_place


async def updating_user_place(user_place_id: int, user_place: UpdateUserPlace) -> UserPlaceModel:
    async with async_session() as session:
            async with session.begin():
                model = UserPlaceRepository(session, UserPlaceModel)
                user_place_updated = await model.update(id=user_place_id, 
                                                        user_id=user_place.user_id, 
                                                        place_branch_id=user_place.place_branch_id,
                                                        is_favourite=user_place.is_favourite)
    if not user_place_updated:
        raise NotFoundException(NOT_FOUND)
    return user_place_updated


async def deleting_user_place(user_place_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = UserPlaceRepository(session, UserPlaceModel)
                user_place = await model.delete(id=user_place_id)
    if not user_place:
        raise NotFoundException(NOT_FOUND)


async def creating_user_place(user_place: UserPlace) -> UserPlaceModel:
    async with async_session() as session:
            async with session.begin():
                model = UserPlaceRepository(session, UserPlaceModel)
                new_user_place = await model.create(user_id=user_place.user_id,
                                                    place_branch_id=user_place.place_branch_id,
                                                    is_favourite=user_place.is_favourite)
    return new_user_place
