from typing import List, Optional
from decimal import Decimal

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.repository import AbstractRepository
from database.models import Address


class AddressRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: Address):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, country_id: int, city_id: int,
                            street: str, building: str, latitude: Decimal,
                            longitude: Decimal) -> Address:
        """Создание адреса"""
        new_place_branch = self.db_model(country_id=country_id, 
                                         city_id=city_id,
                                         street=street,
                                         building=building,
                                         latitude=latitude,
                                         longitude=longitude)
        self.db_session.add(new_place_branch)
        new_address = await self.db_session.flush()
        return new_address

    async def all(self) -> List[Address]:
        branches = await self.db_session.execute(select(self.db_model))
        return branches.scalars().all()

    async def get(self, id: int) -> Address:
        branch = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return branch.scalars().one_or_none()

    async def update(self, id: int, 
                            place_id: Optional[int]=None, 
                            place_address_id: Optional[int]=None) -> Address:
        address = update(self.db_model).where(self.db_model.id == id)
        if place_id:
            address = address.values(place_id=place_id)
        if place_address_id:
            address = address.values(place_address_id=place_address_id)
        address.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(address)

    async def delete(self, id: int) -> None:
        """Удаление адреса с возвратом статуса, True(объект удалён)"""
        address = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        address.execution_options(synchronize_session="delete")
        deleted_address = await self.db_session.execute(address)
        return deleted_address.all()