from typing import List
from database.db import async_session
from institutions.queries import AddressRepository
from database.models import Address as AddressModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceAddress


async def getting_addresses() -> List[AddressModel]:
    async with async_session() as session:
            async with session.begin():
                model = AddressRepository(session, AddressModel)
                addresses = await model.all()
    return addresses


async def getting_address(address_id: int) -> AddressModel:
    async with async_session() as session:
            async with session.begin():
                model = AddressRepository(session, AddressModel)
                address = await model.get(address_id)
    if not address:
        raise NotFoundException(NOT_FOUND)
    return address


async def updating_address(address_id: int, address: CreatePlaceAddress) -> AddressModel:
    async with async_session() as session:
            async with session.begin():
                model = AddressRepository(session, AddressModel)
                address_updated = await model.update(id=address_id, 
                                                     country_id=address.country_id, 
                                                     city_id=address.city_id,
                                                     street=address.street,
                                                     building=address.building,
                                                     latitude=address.latitude,
                                                     longitude=address.longitude)
    if not address_updated:
        raise NotFoundException(NOT_FOUND)
    return address_updated


async def deleting_address(address_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = AddressRepository(session, AddressModel)
                address = await model.delete(id=address_id)
    if not address:
        raise NotFoundException(NOT_FOUND)


async def creating_address(address: CreatePlaceAddress) -> AddressModel:
    async with async_session() as session:
            async with session.begin():
                model = AddressRepository(session, AddressModel)
                new_address = await model.create(country_id=address.country_id,
                                                 city_id=address.city_id,
                                                 street=address.street,
                                                 building=address.building,
                                                 latitude=address.latitude,
                                                 longitude=address.longitude)
    return new_address
