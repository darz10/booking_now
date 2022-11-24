from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import AddressRepository
from database.models import Address as AddressModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceAddress


async def getting_addresses() -> List[Record]:
    repository = AddressRepository(database, AddressModel)
    addresses = await repository.all()
    return addresses


async def getting_address(address_id: int) -> Record:
    repository = AddressRepository(database, AddressModel)
    address = await repository.get(address_id)
    if not address:
        raise NotFoundException(NOT_FOUND)
    return address


async def updating_address(
    address_id: int,
    address: CreatePlaceAddress
) -> Record:
    repository = AddressRepository(database, AddressModel)
    address_updated = await repository.update(
        id=address_id,
        country_id=address.country_id,
        city_id=address.city_id,
        street=address.street,
        building=address.building,
        latitude=address.latitude,
        longitude=address.longitude
    )
    if not address_updated:
        raise NotFoundException(NOT_FOUND)
    return address_updated


async def deleting_address(address_id: int) -> None:
    repository = AddressRepository(database, AddressModel)
    address = await repository.delete(id=address_id)
    if not address:
        raise NotFoundException(NOT_FOUND)


async def creating_address(address: CreatePlaceAddress) -> Record:
    repository = AddressRepository(database, AddressModel)
    new_address = await repository.create(
        country_id=address.country_id,
        city_id=address.city_id,
        street=address.street,
        building=address.building,
        latitude=address.latitude,
        longitude=address.longitude
    )
    return new_address
