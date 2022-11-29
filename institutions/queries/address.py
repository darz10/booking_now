from typing import List
from decimal import Decimal
from databases.backends.postgres import Record

from sqlalchemy import update, delete, insert, select
from databases import Database

from database.repository import AbstractRepository
from database.models import Address
from database.services import formation_fitlers_database


class AddressRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: Address):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, country_id: int, city_id: int,
                     street: str, building: str, latitude: Decimal,
                     longitude: Decimal) -> Record:
        """Создание адреса"""
        new_address = insert(self.db_model).values(
            country_id=country_id,
            city_id=city_id,
            street=street,
            building=building,
            latitude=latitude,
            longitude=longitude).returning(self.db_model)

        new_address = await self.db_connection.fetch_one(new_address)
        return new_address

    async def all(self) -> List[Record]:
        """Получение всех адресов"""
        branches = await self.db_connection.fetch_all(select(self.db_model))
        return branches

    async def get(self, id: int) -> Record:
        """Получение адреса по id"""
        branch = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return branch

    async def update(self, id: int, *args, **kwargs) -> Record:
        address = update(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model)
        address = address.values(**kwargs)
        result = await self.db_connection.fetch_one(address)
        return result

    async def delete(self, id: int) -> None:
        """Удаление адреса с возвратом статуса, True(объект удалён)"""
        address = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        address.execution_options(synchronize_session="delete")
        deleted_address = await self.db_connection.execute(address)
        return deleted_address.all()

    async def filter(self, *args, **kwargs) -> List[Record]:
        formated_filters = formation_fitlers_database(self.db_model, *args)
        addresses = await self.db_connection.fetch_all(
            select(self.db_model).where(*formated_filters))
        return addresses
