from fastapi import APIRouter, Request, HTTPException

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.services import getting_countries, getting_country

tags = ["cities"]

router = APIRouter()


@router.get("/v1/cities", tags=tags, summary="Получение списка городов")
async def get_list_cities(
    request: Request
):
    """Получение список городов"""
    try:
        return await getting_countries()
    except Exception as exc:
        print("Error in endpoint get_list_places", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")
        

@router.get("/v1/cities/{city_id}", tags=tags, summary="Получение города")
async def get_city(
    request: Request, city_id: int
):
    """Получение места"""
    try:
        return await getting_country(city_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint get_place", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")