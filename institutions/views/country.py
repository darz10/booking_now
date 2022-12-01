import logging

from fastapi import APIRouter, Request, HTTPException, Depends

from institutions.messages import NOT_FOUND
from institutions.exceptions import NotFoundException
from institutions.schemas.country import CountryFilter
from institutions.services import (
    getting_countries,
    getting_country,
    filtering_countries
)


tags = ["countries"]

router = APIRouter()


@router.get("/v1/countries", tags=tags, summary="Получение списка стран")
async def get_list_countries(
    request: Request,
    filters: CountryFilter = Depends()
):
    """Получение список стран"""
    try:
        if filters.has_objects:
            return await filtering_countries(filters)
        return await getting_countries()
    except Exception as exc:
        logging.exception(f"Error in method get_list_countries: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")


@router.get("/v1/country/{country_id}", tags=tags, summary="Получение страны")
async def get_country(
    request: Request, country_id: int
):
    """Получение страны"""
    try:
        return await getting_country(country_id)
    except NotFoundException:
        logging.exception(NOT_FOUND)
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    except Exception as exc:
        logging.exception(f"Error in method get_country: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
