from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import PlaceBranch
from database.repository import AbstractRepository


class PlaceBranchRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: PlaceBranch):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, place_id: int, place_address_id: int) -> PlaceBranch:
        """Создание точки заведения"""
        new_place_branch = self.db_model(place_id=place_id, 
                                         place_address_id=place_address_id)
        self.db_session.add(new_place_branch)
        await self.db_session.flush()

    async def all(self) -> List[PlaceBranch]:
        branches = await self.db_session.execute(select(self.db_model))
        return branches.scalars().all()

    async def get(self, id: int) -> PlaceBranch:
        branch = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return branch.scalars().one_or_none()

    async def update(self, id: int, 
                            place_id: Optional[int]=None, 
                            place_address_id: Optional[int]=None) -> PlaceBranch:
        branch = update(self.db_model).where(self.db_model.id == id)
        if place_id:
            branch = branch.values(place_id=place_id)
        if place_address_id:
            branch = branch.values(place_address_id=place_address_id)
        branch.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(branch)

    async def delete(self, id: int) -> None:
        """Удаление точки места с возвратом статуса, True(объект удалён)"""
        branch = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        branch.execution_options(synchronize_session="delete")
        deleted_branch = await self.db_session.execute(branch)
        return deleted_branch.all()

    async def filter(self, *args, **kwargs) -> List[PlaceBranch]:
        queries = []
        if kwargs.get("place_id"):
            queries.append(self.db_model.type_place == kwargs["place_type"])
        places = await self.db_session.execute(select(self.db_model).where(*queries))
        return places.scalars().all()