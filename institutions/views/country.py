from fastapi import APIRouter, Request, HTTPException

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.services import getting_countries, getting_country, getting_cities_by_country

tags = ["countries"]

router = APIRouter()


@router.get("/v1/countries", tags=tags, summary="Получение списка стран")
async def get_list_countries(
    request: Request
):
    """Получение список стран"""
    try:
        return await getting_countries()
    except Exception as exc:
        print("Error in endpoint get_list_places", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")
        

@router.get("/v1/country/{country_id}", tags=tags, summary="Получение страны")
async def get_country(
    request: Request, country_id: int
):
    """Получение страны"""
    try:
        return await getting_country(country_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint get_place", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get("/v1/country/{country_id}/cities", tags=tags, summary="Получение городов страны")
async def get_cities_by_country(
    request: Request, country_id: int
):
    """Получение городов страны"""
    try:
        return await getting_cities_by_country(country_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        print("Error in endpoint get_place", exc)
        raise HTTPException(status_code=400, detail=f"{exc}")