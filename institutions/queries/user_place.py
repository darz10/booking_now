from typing import List

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import UserPlace
from database.repository import AbstractRepository


class UserPlaceRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: UserPlace):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, *args, **kwargs) -> UserPlace:
        """Создание связи пользователя с местом"""
        user_place = self.db_model(user_id=kwargs.get("user_id"),
                                   place_branch_id=kwargs.get("place_branch_id"),
                                   is_favourite=kwargs.get("is_favourite"))
        self.db_session.add(user_place)
        new_user_place = await self.db_session.flush()
        return new_user_place

    async def all(self) -> List[UserPlace]:
        user_places = await self.db_session.execute(select(self.db_model))
        return user_places.scalars().all()

    async def get(self, id: int) -> UserPlace:
        user_place = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return user_place.scalars().one_or_none()

    async def update(self, id: int, *args, **kwargs) -> UserPlace:
        user_place = update(self.db_model).where(self.db_model.id == id)
        if kwargs.get("place_id"):
            user_place = user_place.values(place_id=kwargs["place_id"])
        if kwargs.get("place_address_id"):
            user_place = user_place.values(place_address_id=kwargs["place_address_id"])
        if kwargs.get("is_favourite"):
            user_place = user_place.values(place_address_id=kwargs["place_address_id"])
        user_place.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(user_place)

    async def delete(self, id: int) -> None:
        """Удаление адреса с возвратом статуса, True(объект удалён)"""
        user_place = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        user_place.execution_options(synchronize_session="delete")
        deleted_user_place = await self.db_session.execute(user_place)
        return deleted_user_place.all()