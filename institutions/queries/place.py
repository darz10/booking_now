from typing import List, Optional

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import Place
from database.repository import AbstractRepository
from database.services import formation_fitlers_database


class PlaceRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: Place):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(
        self,
        title: str,
        user_id: int,
        place_type: int,
        description: Optional[str] = None,
        url: Optional[str] = None,
        avatar: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Record:
        new_place = insert(self.db_model).values(
            title=title,
            place_description=description,
            url=url,
            avatar=avatar,
            email=email,
            phone=phone,
            place_type=place_type,
            user_id=user_id,
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_place)

    async def all(self) -> List[Record]:
        places = await self.db_connection.fetch_all(
            query=select(self.db_model)
        )
        return places

    async def get(self, id: int) -> Record:
        place = await self.db_connection.fetch_one(
            query=select(self.db_model).where(self.db_model.id == id)
        )
        return place

    async def update(self, id: int, *args, **kwargs) -> Record:
        place = update(self.db_model).where(self.db_model.id == id)
        place = place.values(**kwargs)
        return await self.db_connection.execute(place)

    async def delete(self, id: int) -> None:
        """Удаление места с возвратом статуса, True(объект удалён)"""
        place = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        deleted_place = await self.db_connection.execute(place)
        return deleted_place.all()

    async def filter(self, *args, **kwargs) -> List[Record]:
        formated_filters = formation_fitlers_database(self.db_model, *args)
        places = await self.db_connection.fetch_all(
            select(self.db_model).where(*formated_filters))
        return places
