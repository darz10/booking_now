from typing import List

from sqlalchemy import update, delete, select, insert
from databases import Database
from databases.backends.postgres import Record

from database.models import PlaceMediaFile
from database.repository import AbstractRepository


class PlaceMediaFileRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: PlaceMediaFile):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, place_id: int, file_id: int) -> Record:
        new_place_media_file = insert(self.db_model).values(
            place_id=place_id,
            file_id=file_id
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_place_media_file)

    async def all(self) -> List[Record]:
        place_media_files = await self.db_connection.fetch_all(
            select(self.db_model)
        )
        return place_media_files

    async def get(self, id: int) -> Record:
        place_media_file = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return place_media_file

    async def update(self, id: int, *args, **kwargs) -> Record:
        place_media_file = update(self.db_model).\
                           where(self.db_model.id == id).\
                           returning(self.db_model)
        if kwargs.get("place_id"):
            place_media_file = place_media_file.values(
                place_id=kwargs["place_id"]
            )
        if kwargs.get("file_id"):
            place_media_file = place_media_file.values(
                file_id=kwargs["file_id"]
            )
        return await self.db_connection.fetch_one(place_media_file)

    async def delete(self, id: int) -> None:
        """
        Удаление связи места-файл с
        возвратом статуса, True(объект удалён)
        """
        place = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        deleted_place = await self.db_connection.execute(place)
        return deleted_place
