import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from accounts.schemas import User, CustomResponse
from accounts.views import get_current_user
from institutions.schemas import UpdatePlace
from institutions.messages import NOT_FOUND, SUCCESSFULLY
from institutions.exceptions import NotFoundException
from institutions.schemas.place import PlaceFilter
from institutions.services import (
    filter_places,
    getting_places,
    deleting_place,
    getting_place,
    updating_place
)


tags = ["places"]

router = APIRouter()


@router.get(
    "/v1/places",
    tags=tags,
    summary="Получение списка мест"
)
async def get_list_places(
    request: Request,
    filters: PlaceFilter = Depends()
):
    """Получение список мест"""
    try:
        # if filters.has_objects:
        #     return await filter_places(
        #             filters.to_list()
        #         )
        return await getting_places()
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_places: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get(
    "/v1/places/{place_id}",
    tags=tags,
    summary="Получение места"
)
async def get_place(
    request: Request, place_id: int
):
    """Получение места"""
    try:
        return await getting_place(place_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.patch(
    "/v1/places/{place_id}",
    tags=tags,
    summary="Обновить место"
)
async def update_place(
    request: Request,
    place_id: int,
    place: UpdatePlace,
    current_user: User = Depends(get_current_user),  # TODO ограничить достпу
                                                     # к изменению состояния
):
    """Обновление места"""
    try:
        return await updating_place(place_id, place)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint update_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.delete(
    "/v1/places/{place_id}",
    tags=tags,
    summary="Удалить место"
)
async def delete_place(
    request: Request,
    place_id: int,
    current_user: User = Depends(get_current_user)  # TODO ограничить достпу
                                                    # к изменению состояния
):
    """Удаление места"""
    try:
        await deleting_place(place_id)
        return CustomResponse(status_code=204, description=SUCCESSFULLY)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint delete_place: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


# @router.get(
#     "/v1/places/{place_id}/place_branches",
#     tags=tags,
#     operation_id="Получение точек конретного заведения"
# )
# async def get_place_branches_of_place(
#     request: Request, place_id: int
# ):
#     """Получение точек конретного заведения"""
#     try:
#         place_branches = await get_info_place_branches_by_place_id(place_id)
#         return get_place_schema(place)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"{e}")
