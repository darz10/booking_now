from databases.backends.postgres import Record

from database.db import database
from institutions.queries import PlaceMediaFileRepository
from database.models import PlaceMediaFile as PlaceMediaFileModel
from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CreatePlaceMediaFile


async def creating_place_media_file(
    place_media_file: CreatePlaceMediaFile
) -> Record:
    repository = PlaceMediaFileRepository(database, PlaceMediaFileModel)
    new_place_media_file = await repository.create(
        place_id=place_media_file.place_id,
        file_id=place_media_file.file_id
    )
    return new_place_media_file


async def deleting_place_media_file(place_media_file_id: int) -> None:
    repository = PlaceMediaFileRepository(database, PlaceMediaFileModel)
    place_media_file = await repository.delete(id=place_media_file_id)
    if not place_media_file:
        raise NotFoundException(NOT_FOUND)
