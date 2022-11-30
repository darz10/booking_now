import logging
from fastapi import APIRouter, Request, HTTPException, Depends

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas import CityFilter
from institutions.services import (
    getting_cities,
    getting_city,
    filter_cities
)


tags = ["cities"]

router = APIRouter()


@router.get("/v1/cities", tags=tags, summary="Получение списка городов")
async def get_list_cities(
    request: Request,
    filters: CityFilter = Depends()
):
    """Получение списка городов"""
    try:
        if filters.has_objects:
            return await filter_cities(
                    filters
                )
        return await getting_cities()
    except Exception as exc:
        logging.exception(f"Error in endpoint get_list_cities: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get("/v1/cities/{city_id}", tags=tags, summary="Получение города")
async def get_city(
    request: Request,
    city_id: int
):
    """Получение города"""
    try:
        return await getting_city(city_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in endpoint get_city: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
