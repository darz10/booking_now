
import logging
from fastapi import APIRouter, Request, HTTPException

from institutions.services import getting_place_types

tags = ["place_type"]

router = APIRouter()


@router.get(
    "/v1/place_types/",
    tags=tags,
    summary="Получение списка типов мест"
)
async def get_list_addresses(request: Request):
    """Получение списка категорий мест"""
    try:
        return await getting_place_types()
    except Exception as exc:
        logging.exception(f"Error in method get_list_addresses: {exc}")
        raise HTTPException(status_code=400, detail=f"{exc}")
