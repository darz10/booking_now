from typing import List

from databases.backends.postgres import Record

from database.db import database
from institutions.queries import PlaceBranchRepository
from database.models import PlaceBranch as PlaceBranchModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceBranch


async def getting_branches() -> List[Record]:
    repository = PlaceBranchRepository(database, PlaceBranchModel)
    branches = await repository.all()
    return branches


async def getting_branch(branch_id: int) -> Record:
    repository = PlaceBranchRepository(database, PlaceBranchModel)
    branch = await repository.get(id=branch_id)
    if not branch:
        raise NotFoundException(NOT_FOUND)
    return branch


async def updating_branch(
    branch_id: int,
    branch: CreatePlaceBranch
) -> Record:
    repository = PlaceBranchRepository(database, PlaceBranchModel)
    updated_data = branch.dict(exclude_unset=True)
    branch_updated = await repository.update(
        id=branch_id,
        **updated_data
    )
    if not branch_updated:
        raise NotFoundException(NOT_FOUND)
    return branch_updated


async def deleting_branch(place_id: int) -> None:
    repository = PlaceBranchRepository(database, PlaceBranchModel)
    branch = await repository.delete(id=place_id)
    if not branch:
        raise NotFoundException(NOT_FOUND)


async def creating_branch(branch: CreatePlaceBranch) -> Record:
    repository = PlaceBranchRepository(database, PlaceBranchModel)
    new_place = await repository.create(
        place_id=branch.place_id,
        place_address_id=branch.place_address_id
    )
    return new_place
