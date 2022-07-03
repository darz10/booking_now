from typing import List
from database.db import async_session
from institutions.queries import MediaFileRepository
from database.models import MediaFile as MediaFileModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import (
    CreateMediaFile,
    UpdateMediaFile,
)


async def getting_media_files() -> List[MediaFileModel]:
    async with async_session() as session:
            async with session.begin():
                model = MediaFileRepository(session, MediaFileModel)
                media_files = await model.all()
    return media_files


async def getting_media_file(media_file_id: int) -> MediaFileModel:
    async with async_session() as session:
            async with session.begin():
                model = MediaFileRepository(session, MediaFileModel)
                media_file = await model.get(media_file_id)
    if not media_file:
        raise NotFoundException(NOT_FOUND)
    return media_file


async def updating_media_file(media_file_id: int, media_file: UpdateMediaFile) -> MediaFileModel:
    async with async_session() as session:
            async with session.begin():
                model = MediaFileRepository(session, MediaFileModel)
                media_file_updated = await model.update(id=media_file_id,
                                                        source_id=media_file.source_id,
                                                        source_fields=media_file.source_fields,
                                                        source_url=media_file.source_url,
                                                        uploaded=media_file.uploaded,
                                                        filename=media_file.filename,
                                                        user_id=media_file.user_id,)                           
    if not media_file_updated:
        raise NotFoundException(NOT_FOUND)
    return media_file_updated


async def deleting_media_file(media_file_id: int) -> None:
    async with async_session() as session:
            async with session.begin():
                model = MediaFileRepository(session, MediaFileModel)
                media_file = await model.delete(id=media_file_id)
    if not media_file:
        raise NotFoundException(NOT_FOUND)


async def creating_media_file(media_file: CreateMediaFile) -> MediaFileModel:
    async with async_session() as session:
            async with session.begin():
                model = MediaFileRepository(session, MediaFileModel)
                new_media_file = await model.create(source_id=media_file.source_id,
                                                    source_fields=media_file.source_fields,
                                                    source_url=media_file.source_url,
                                                    uploaded=media_file.uploaded,
                                                    filename=media_file.filename,
                                                    user_id=media_file.user_id,)
    return new_media_file