from typing import List
from database.db import async_session
from institutions.queries import TableRepository
from database.models import Table as TableModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    BaseTable,
    UpdateTable
)


async def getting_tables() -> List[TableModel]:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                table = await model.all()
    return table


async def getting_table(table_id: int) -> TableModel:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                table = await model.get(table_id)
    if not table:
        raise NotFoundException(NOT_FOUND)
    return table


async def updating_table(table_id: int, table: UpdateTable) -> TableModel:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                table_updated = await model.update(id=table_id, 
                                                   table_number=table.table_number,
                                                   max_people=table.max_people,
                                                   is_electricity=table.is_electricity,
                                                   floor=table.floor,
                                                   is_available=table.is_available,
                                                   place_branch_id=table.place_branch_id)                           
    if not table_updated:
        raise NotFoundException(NOT_FOUND)
    return table_updated


async def deleting_table(table_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                table = await model.delete(id=table_id)
    if not table:
        raise NotFoundException(NOT_FOUND)


async def creating_table(table: BaseTable) -> TableModel:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                new_table = await model.create(table_number=table.table_number,
                                               max_people=table.max_people,
                                               is_electricity=table.is_electricity,
                                               floor=table.floor,
                                               is_available=table.is_available,
                                               place_branch_id=table.place_branch_id,)
    return new_table


async def filter_tables(*args, **kwargs) -> List[TableModel]:
    async with async_session() as session:
            async with session.begin():
                model = TableRepository(session, TableModel)
                tables = await model.filter(*args, **kwargs)
                return tables
    