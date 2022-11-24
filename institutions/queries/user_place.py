from typing import List, Optional

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import UserPlace
from database.repository import AbstractRepository


class UserPlaceRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: UserPlace):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, user_id: int, place_branch_id: int, 
                     is_favourite: Optional[bool]=None) -> Record:
        """Создание связи пользователя с местом"""
        user_place = insert(self.db_model).values(
            user_id=user_id,
            place_branch_id=place_branch_id,
            is_favourite=is_favourite
        ).returning(self.db_model)        
        return await self.db_connection.fetch_one(user_place)

    async def all(self) -> List[Record]:
        user_places = await self.db_connection.fetch_all(select(self.db_model))
        return user_places

    async def get(self, id: int) -> Record:
        user_place = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return user_place

    async def update(self, id: int, *args, **kwargs) -> Record:
        user_place = update(self.db_model).\
                     where(self.db_model.id == id).\
                     returning(self.db_model)
        if kwargs.get("place_id"):
            user_place = user_place.values(place_id=kwargs["place_id"])
        if kwargs.get("place_address_id"):
            user_place = user_place.values(place_address_id=kwargs["place_address_id"])
        if kwargs.get("is_favourite"):
            user_place = user_place.values(place_address_id=kwargs["place_address_id"])
        return await self.db_connection.fetch_one(user_place)

    async def delete(self, id: int) -> None:
        """Удаление адреса с возвратом статуса, True(объект удалён)"""
        user_place = delete(self.db_model).\
                     where(self.db_model.id == id).\
                     returning(self.db_model.id)
        deleted_user_place = await self.db_connection.execute(user_place)
        return deleted_user_place