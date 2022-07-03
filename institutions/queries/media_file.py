from datetime import datetime
from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.models import MediaFile
from database.repository import AbstractRepository


class MediaFileRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: MediaFile):
        self.db_session = db_session
        self.db_model = db_model

    async def create(self, source_id: str, user_id: int,
                     source_url: str, uploaded: bool, created_at: datetime,
                     filename: str, source_fields: Optional[dict]):
        new_media_file = self.db_model(source_id=source_id,
                                       source_fields=source_fields,
                                       source_url=source_url,
                                       uploaded=uploaded,
                                       created_at=created_at,
                                       filename=filename,
                                       user_id=user_id)
        self.db_session.add(new_media_file)
        await self.db_session.flush()

    async def all(self) -> List[MediaFile]:
        media_files = await self.db_session.execute(select(self.db_model))
        return media_files.scalars().all()

    async def get(self, id: int) -> MediaFile:
        media_file = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return media_file.scalars().one_or_none()

    async def update(self, id: int, source_id: Optional[str]=None,
                     source_fields: Optional[dict]=None, source_url: Optional[str]=None,
                     uploaded: Optional[bool]=None, created_at: Optional[datetime]=None,
                     filename: Optional[str]=None, user_id: Optional[int]=None,) -> MediaFile:
        media_file = update(self.db_model).where(self.db_model.id == id)
        if source_id:
            media_file = media_file.values(source_id=source_id)
        if source_fields:
            media_file = media_file.values(source_fields=source_fields)
        if source_url:
            media_file = media_file.values(source_url=source_url)
        if uploaded:
            media_file = media_file.values(uploaded=uploaded)
        if created_at:
            media_file = media_file.values(created_at=created_at)
        if filename:
            media_file = media_file.values(filename=filename)
        if user_id:
            media_file = media_file.values(user_id=user_id)
        media_file.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(media_file)

    async def delete(self, id: int) -> None:
        """Удаление стола возвратом статуса, True(объект удалён)"""
        media_file = delete(self.db_model).where(self.db_model.id == id).returning(self.db_model.id)
        media_file.execution_options(synchronize_session="delete")
        deleted_media_file = await self.db_session.execute(media_file)
        return deleted_media_file.all()