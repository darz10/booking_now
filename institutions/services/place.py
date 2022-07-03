from typing import List
from database.db import async_session
from institutions.queries import PlaceRepository
from database.models import Place as PlaceModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import UpdatePlace


async def getting_places() -> List[PlaceModel]:
    async with async_session() as session:
            async with session.begin():
                model = PlaceRepository(session, PlaceModel)
                places = await model.all()
                return places

            
async def getting_place(place_id: int) -> PlaceModel:
    async with async_session() as session:
            async with session.begin():
                model = PlaceRepository(session, PlaceModel)
                place = await model.get(id=place_id)
    if not place:
        raise NotFoundException(NOT_FOUND)
    return place


async def updating_place(place_id: int, place: UpdatePlace) -> PlaceModel:
    async with async_session() as session:
            async with session.begin():
                model = PlaceRepository(session, PlaceModel)
                place_updated = await model.update(id=place_id, 
                                                   title=place.title,
                                                   description=place.description,
                                                   url=place.url,
                                                   avatar=place.avatar,
                                                   email=place.email,
                                                   phone=place.phone,
                                                   type_place=place.type_place,)
    if not place_updated:
        raise NotFoundException(NOT_FOUND)
    return place_updated


async def deleting_place(place_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = PlaceRepository(session, PlaceModel)
                place = await model.delete(id=place_id)
    if not place:
        raise NotFoundException(NOT_FOUND)


async def filter_places(*args, **kwargs) -> List[PlaceModel]:
    async with async_session() as session:
        async with session.begin():
            model = PlaceRepository(session, PlaceModel)
            places = await model.filter(*args, **kwargs)
            return places