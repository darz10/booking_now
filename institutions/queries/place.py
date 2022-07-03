from typing import List

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import Place
from database.repository import AbstractRepository


class PlaceRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: Place):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, *args, **kwargs) -> Place:
        new_place = self.db_model(title=kwargs.get("title"),
                                  place_description=kwargs.get("place_description"),
                                  url=kwargs.get("url"),
                                  avatar=kwargs.get("avatar"),
                                  email=kwargs.get("email"),
                                  phone=kwargs.get("phone"),
                                  type_place=kwargs.get("type_place"),
                                  user_id=kwargs.get("user_id"),)
        self.db_session.add(new_place)
        await self.db_session.flush()

    async def all(self) -> List[Place]:
        places = await self.db_session.execute(select(self.db_model))
        return places.scalars().all()

    async def get(self, id: int) -> Place:
        place = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return place.scalars().one_or_none()

    async def update(self, id: int, *args, **kwargs) -> Place:
        place = update(self.db_model).where(self.db_model.id == id)
        if kwargs.get("title"):
            place = place.values(title=kwargs["title"])
        if kwargs.get("type_place"):
            place = place.values(type_place=kwargs["type_place"])
        if kwargs.get("avatar"):
            place = place.values(avatar=kwargs["avatar"]) 
        if kwargs.get("description"):
            place = place.values(description=kwargs["description"]) 
        if kwargs.get("url"):
            place = place.values(url=kwargs["url"])
        if kwargs.get("email"):
            place = place.values(email=kwargs["email"]) 
        if kwargs.get("phone"):
            place = place.values(phone=kwargs["phone"])
        place.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(place)

    async def delete(self, id: int) -> None:
        """Удаление места с возвратом статуса, True(объект удалён)"""
        place = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        place.execution_options(synchronize_session="delete")
        deleted_place = await self.db_session.execute(place)
        return deleted_place.all()

    async def filter(self, *args, **kwargs) -> List[Place]:
        queries = []
        if kwargs.get("search"):
            format_string = f"%{kwargs['search']}%"
            queries.append(self.db_model.title.ilike(format_string))
        if kwargs.get("place_type"):
            queries.append(self.db_model.type_place == kwargs["place_type"])
        places = await self.db_session.execute(select(self.db_model).where(*queries))
        return places.scalars().all()