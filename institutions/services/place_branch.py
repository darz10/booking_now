from typing import List
from database.db import async_session
from institutions.queries import PlaceBranchRepository 
from database.models import PlaceBranch as PlaceBranchModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceBranch 


async def getting_branches() -> List[PlaceBranchModel]:
    async with async_session() as session:
            async with session.begin():
                model = PlaceBranchRepository(session, PlaceBranchModel)
                branches = await model.all()
    return branches


async def getting_branch(branch_id: int) -> PlaceBranchModel:
    async with async_session() as session:
            async with session.begin():
                model = PlaceBranchRepository(session, PlaceBranchModel)
                branch = await model.get(id=branch_id)
    if not branch:
        raise NotFoundException(NOT_FOUND)
    return branch


async def updating_branch(branch_id: int, branch: CreatePlaceBranch) -> PlaceBranchModel:
    async with async_session() as session:
            async with session.begin():
                model = PlaceBranchRepository(session, PlaceBranchModel)
                branch_updated = await model.update(id=branch_id, 
                                                    place_id=branch.place_id,
                                                    place_address_id=branch.place_address_id)
    if not branch_updated:
        raise NotFoundException(NOT_FOUND)
    return branch_updated


async def deleting_branch(place_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = PlaceBranchRepository(session, PlaceBranchModel)
                branch = await model.delete(id=place_id)
    if not branch:
        raise NotFoundException(NOT_FOUND)


async def creating_branch(branch: CreatePlaceBranch) -> PlaceBranchModel:
    async with async_session() as session:
            async with session.begin():
                model = PlaceBranchRepository(session, PlaceBranchModel)
                new_place = await model.create(place_id=branch.place_id,
                                               place_address_id=branch.place_address_id)
    return new_place
