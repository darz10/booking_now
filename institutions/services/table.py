from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import TableRepository
from database.models import Table as TableModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    BaseTable,
    UpdateTable
)


async def getting_tables() -> List[Record]:
    repository = TableRepository(database, TableModel)
    table = await repository.all()
    return table


async def getting_table(table_id: int) -> Record:
    repository = TableRepository(database, TableModel)
    table = await repository.get(table_id)
    if not table:
        raise NotFoundException(NOT_FOUND)
    return table


async def updating_table(table_id: int, table: UpdateTable) -> Record:
    repository = TableRepository(database, TableModel)
    table_updated = await repository.update(
        id=table_id,
        table_number=table.table_number,
        max_people=table.max_people,
        is_electricity=table.is_electricity,
        floor=table.floor,
        is_available=table.is_available,
        place_branch_id=table.place_branch_id
    )
    if not table_updated:
        raise NotFoundException(NOT_FOUND)
    return table_updated


async def deleting_table(table_id: int) -> None:
    repository = TableRepository(database, TableModel)
    table = await repository.delete(id=table_id)
    if not table:
        raise NotFoundException(NOT_FOUND)


async def creating_table(table: BaseTable) -> Record:
    repository = TableRepository(database, TableModel)
    new_table = await repository.create(
        table_number=table.table_number,
        max_people=table.max_people,
        is_electricity=table.is_electricity,
        floor=table.floor,
        is_available=table.is_available,
        place_branch_id=table.place_branch_id,
    )
    return new_table


async def get_tables_by_branch_id(branch_id: int) -> List[Record]:
    repository = TableRepository(database, TableModel)
    tables = await repository.filter(branch_id=branch_id)
    return tables


async def filter_tables(*args, **kwargs) -> List[Record]:
    repository = TableRepository(database, TableModel)
    tables = await repository.filter(*args, **kwargs)
    return tables
