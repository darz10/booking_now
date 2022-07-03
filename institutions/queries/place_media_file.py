from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import PlaceMediaFile
from database.repository import AbstractRepository


class PlaceMediaFileRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: PlaceMediaFile):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, *args, **kwargs) -> PlaceMediaFile:
        new_place_media_file = self.db_model(place_id=kwargs.get("place_id"), 
                                             file_id=kwargs.get("file_id"))
        self.db_session.add(new_place_media_file)
        await self.db_session.flush()

    async def all(self) -> List[PlaceMediaFile]:
        place_media_files = await self.db_session.execute(select(self.db_model))
        return place_media_files.scalars().all()

    async def get(self, id: int) -> PlaceMediaFile:
        place_media_file = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return place_media_file.scalars().one_or_none()

    async def update(self, id: int, *args, **kwargs) -> PlaceMediaFile:
        place_media_file = update(self.db_model).where(self.db_model.id == id)
        if kwargs.get("place_id"):
            place_media_file = place_media_file.values(place_id=kwargs["place_id"])
        if kwargs.get("file_id"):
            place_media_file = place_media_file.values(file_id=kwargs["file_id"])
        place_media_file.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(place_media_file)

    async def delete(self, id: int) -> None:
        """Удаление связи места-файл с возвратом статуса, True(объект удалён)"""
        place = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        place.execution_options(synchronize_session="delete")
        deleted_place = await self.db_session.execute(place)
        return deleted_place.all()