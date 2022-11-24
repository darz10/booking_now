from datetime import datetime
from typing import List, Optional

from sqlalchemy import update, delete, insert, select
from databases import Database
from databases.backends.postgres import Record

from database.models import MediaFile
from database.repository import AbstractRepository


class MediaFileRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: MediaFile):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(self, source_id: str, user_id: int,
                     source_url: str, uploaded: bool, created_at: datetime,
                     filename: str, source_fields: Optional[dict]) -> Record:
        
        new_media_file = insert(self.db_model).values(
            source_id=source_id,
            source_fields=source_fields,
            source_url=source_url,
            uploaded=uploaded,
            created_at=created_at,
            filename=filename,
            user_id=user_id
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_media_file)

    async def all(self) -> List[Record]:
        media_files = await self.db_connection.fetch_all(select(self.db_model))
        return media_files

    async def get(self, id: int) -> Record:
        media_file = await self.db_connection.fetch_one(
            select(self.db_model).where(self.db_model.id == id)
        )
        return media_file

    async def update(self, id: int, *args, **kwargs) -> Record:
        media_file = update(self.db_model).\
                     where(self.db_model.id == id).\
                     returning(self.db_model)
        if kwargs.get("source_id"):
            media_file = media_file.values(source_id=kwargs["source_id"])
        if kwargs.get("source_fields"):
            media_file = media_file.values(source_fields=kwargs["source_fields"])
        if kwargs.get("source_url"):
            media_file = media_file.values(source_url=kwargs["source_url"])
        if kwargs.get("uploaded"):
            media_file = media_file.values(uploaded=kwargs["uploaded"])
        if kwargs.get("created_at"):
            media_file = media_file.values(created_at=kwargs["created_at"])
        if kwargs.get("filename"):
            media_file = media_file.values(filename=kwargs["filename"])
        if kwargs.get("user_id"):
            media_file = media_file.values(user_id=kwargs["user_id"])
        return await self.db_connection.fetch_one(media_file)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        media_file = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        deleted_media_file = await self.db_connection.execute(media_file)
        return deleted_media_file